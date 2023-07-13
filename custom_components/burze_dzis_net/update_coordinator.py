"""Update coordinator for burze.dzis.net integration."""
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .connector import BurzeDzisNetConnector, BurzeDzisNetData
from .const import DOMAIN, DEFAULT_UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class BurzeDzisNetUpdateCoordinator(DataUpdateCoordinator[BurzeDzisNetData]):

    def __init__(self, hass: HomeAssistant, api_key: str, latitude: float, longitude: float, radius: int):
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=DEFAULT_UPDATE_INTERVAL,
                         update_method=self.update_method)
        self.connector = BurzeDzisNetConnector(api_key, latitude, longitude, radius)

    async def update_method(self) -> BurzeDzisNetData:
        return await self.hass.async_add_executor_job(self._update)

    def _update(self) -> BurzeDzisNetData:
        return self.connector.get_data()
