from decimal import Decimal
import httpx
from fastapi import HTTPException


async def get_dollar_rate() -> Decimal:
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            return Decimal(data["Valute"]["USD"]["Value"])
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail="Error fetching dollar rate") from e
