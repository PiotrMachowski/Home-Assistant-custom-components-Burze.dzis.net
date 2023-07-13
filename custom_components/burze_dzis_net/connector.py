from __future__ import annotations

from typing import Dict
import logging

from homeassistant.core import HomeAssistant
from suds import WebFault
from suds.client import Client, ServiceSelector

from .const import WSDL_URL

_LOGGER = logging.getLogger(__name__)


class BurzeDzisNetData:

    def __init__(self):
        self.ostrzezenia_pogodowe: Dict[str, str | int] | None = None
        self.szukaj_burzy: Dict[str, str | int | float] | None = None
        self.promieniowanie: float | None = None


class BurzeDzisNetConnector:
    def __init__(self, api_key: str, latitude: float, longitude: float, radius: int):
        self._service: ServiceSelector | None = None
        self._api_key = api_key
        self._latitude = latitude
        self._longitude = longitude
        self._radius = radius

    def get_service(self) -> ServiceSelector:
        if self._service is None:
            self._service = Client(WSDL_URL).service
        return self._service

    def get_data(self):
        service = self.get_service()
        data = BurzeDzisNetData()
        try:
            latitude = self.convert_to_dm(self._latitude)
            longitude = self.convert_to_dm(self._longitude)
            data.ostrzezenia_pogodowe = service.ostrzezenia_pogodowe(latitude, longitude, self._api_key)
            data.promieniowanie = service.promieniowanie(self._api_key)
            data.szukaj_burzy = service.szukaj_burzy(latitude, longitude, self._radius, self._api_key)
        except WebFault as fault:
            _LOGGER.error('Error while downloading data from burze.dzis.net: {}', fault)
        return data

    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        service = Client(WSDL_URL).service
        try:
            return service.KeyAPI(api_key)
        except WebFault as fault:
            _LOGGER.error('Error while downloading data from burze.dzis.net: {}', fault)
        return False

    @staticmethod
    async def async_validate_api_key(hass: HomeAssistant, api_key: str) -> bool:
        return await hass.async_add_executor_job(BurzeDzisNetConnector.validate_api_key, api_key)

    @staticmethod
    def convert_to_dm(dmf: float) -> str:
        degrees = int(dmf)
        minutes = round(dmf % 1 * 60)
        if minutes >= 60:
            minutes -= 60
            degrees += 1
        return f'{degrees}.{minutes:02}'
