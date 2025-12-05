"""
Currency conversion service using exchange rate API
"""
import httpx
from typing import Dict, Optional


class CurrencyConverter:
    def __init__(self):
        self.api_url = "https://open.er-api.com/v6/latest/USD"
        self.rates: Optional[Dict[str, float]] = None
        self.initialized = False

    async def initialize(self):
        """Fetch exchange rates from API"""
        if not self.initialized:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.api_url)
                if response.status_code == 200:
                    data = response.json()
                    self.rates = data.get("rates", {})
                    self.initialized = True
                else:
                    raise Exception("Error fetching exchange rates")

    def convert_to_usd(self, currency_code: Optional[str], amount: float) -> float:
        """Convert amount in given currency to USD"""
        if not self.initialized or not self.rates:
            raise Exception("Currency converter not initialized")

        if currency_code and currency_code in self.rates:
            exchange_rate = self.rates[currency_code]
            return round(amount / exchange_rate, 2)
        else:
            return 999.0 if amount != 0 else 0.0
