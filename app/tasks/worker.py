from datetime import timedelta
from decimal import Decimal
import redis
import dramatiq
import requests
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.parcels import Parcel

# TODO: перенести данные в env
engine = create_engine("postgresql+psycopg2://postgres:1234@localhost:5432/app_db")
Session = sessionmaker(bind=engine)

rabbitmq_broker = RabbitmqBroker(url="amqp://guest:guest@localhost:5672/")
dramatiq.set_broker(rabbitmq_broker)

redis_host = "localhost"
redis_port = 6379

r = redis.Redis(
    host=redis_host,
    port=redis_port,
    decode_responses=True,
)


@dramatiq.actor
def process_package(parcel_id: int):
    dollars_rate = Decimal(get_dollar_rate())
    with Session() as session:
        parcel = session.get(Parcel, parcel_id)
        cost_delivery = round(
            (
                (Decimal("0.5") * parcel.weight + parcel.cost_content * Decimal("0.01"))
                * dollars_rate
            ),
            2,
        )
        parcel.cost_delivery = cost_delivery
        session.commit()


def get_dollar_rate():
    cached_rate = r.get("usd_to_rub")
    if cached_rate:
        return cached_rate
    try:
        response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
        response.raise_for_status()
        data = response.json()
        usd_rate = data["Valute"]["USD"]["Value"]
        r.setex("usd_to_rub", timedelta(hours=1), usd_rate)
        return usd_rate
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(
            f"Ошибка при получении данных из API: {e}"
        )
