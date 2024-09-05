from datetime import timedelta
from decimal import Decimal
import redis
import dramatiq
import requests
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings
from models.parcels import Parcel


URL_DATABASE_SYNC = (
    f"{settings.db.dialect}+"
    f"{settings.db.driver_sync}://"
    f"{settings.db.user}:"
    f"{settings.db.password}@"
    f"{settings.db.host}:"
    f"{settings.db.port}/"
    f"{settings.db.database}"
)
engine = create_engine(
    URL_DATABASE_SYNC,
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)
Session = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

URL_RABBIT = (
    f"amqp://"
    f"{settings.rabbit.user}:"
    f"{settings.rabbit.password}@"
    f"{settings.rabbit.host}:"
    f"{settings.rabbit.port}/"
)
rabbitmq_broker = RabbitmqBroker(url=URL_RABBIT)
dramatiq.set_broker(rabbitmq_broker)

r = redis.Redis(
    host=settings.redis.host,
    port=settings.redis.port,
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
