from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ATTRIBUTION, CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .update_coordinator import BurzeDzisNetUpdateCoordinator
from .connector import BurzeDzisNetData
from .const import ATTRIBUTION, DEFAULT_NAME, CONF_USE_HOME_COORDINATES, DOMAIN


class BurzeDzisNetEntity(CoordinatorEntity):

    def __init__(self, coordinator: BurzeDzisNetUpdateCoordinator, config_entry: ConfigEntry):
        super().__init__(coordinator)
        self.config_entry = config_entry

    @property
    def extra_state_attributes(self) -> dict:
        return {ATTR_ATTRIBUTION: ATTRIBUTION}

    def get_data(self) -> BurzeDzisNetData | None:
        return self.coordinator.data

    @property
    def name(self):
        return self.base_name()

    def base_name(self):
        if self.config_entry.data[CONF_USE_HOME_COORDINATES]:
            return DEFAULT_NAME
        longitude = self.config_entry.data[CONF_LONGITUDE]
        latitude = self.config_entry.data[CONF_LATITUDE]
        return f"{DEFAULT_NAME} ({longitude:.2f}-{latitude:.2f})"

    @property
    def unique_id(self):
        if self.config_entry.data[CONF_USE_HOME_COORDINATES]:
            return f"{DOMAIN}_home"
        longitude = self.config_entry.data[CONF_LONGITUDE]
        latitude = self.config_entry.data[CONF_LATITUDE]
        return f"{DOMAIN}_{longitude}_{latitude}"

    @property
    def device_info(self):
        longitude = self.config_entry.data[CONF_LONGITUDE]
        latitude = self.config_entry.data[CONF_LATITUDE]
        return {
            "identifiers": {(DOMAIN, longitude, latitude)},
            "name": self.base_name(),
        }
