"""Config flow to configure burze.dzis.net integration."""

import logging
from typing import Any, Mapping

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import (CONF_LOCATION, CONF_API_KEY, CONF_LATITUDE, CONF_LONGITUDE, CONF_RADIUS)
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_validation as cv, selector

from .connector import BurzeDzisNetConnector
from .const import (DEFAULT_RADIUS_IN_KM, DOMAIN, CONF_USE_HOME_COORDINATES, DEFAULT_NAME)

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA_API_KEY = vol.Schema({
    vol.Required(CONF_API_KEY): str
})

DATA_SCHEMA_USE_HOME_LOCATION = vol.Schema({
    vol.Required(CONF_USE_HOME_COORDINATES): bool
})

DATA_SCHEMA_LOCATION = vol.Schema(
    {
        vol.Required(CONF_LOCATION): selector.LocationSelector(
            selector.LocationSelectorConfig(radius=False, icon="mdi:radar")
        ),
    }
)

DATA_SCHEMA_RADIUS = vol.Schema({
    vol.Required(CONF_RADIUS): cv.positive_int
})


class BurzeDzisNetFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self):
        self._api_key = None
        self._latitude = None
        self._longitude = None
        self._use_home_coordinates = None
        self._radius = None

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}
        if user_input is not None:
            api_key = user_input[CONF_API_KEY]
            is_valid = await BurzeDzisNetConnector.async_validate_api_key(self.hass, api_key)
            if is_valid:
                self._api_key = api_key
                return await self.async_step_use_home_location()
            else:
                errors[CONF_API_KEY] = "invalid_api_key"
        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA_API_KEY, errors=errors)

    async def async_step_use_home_location(self, user_input=None) -> FlowResult:
        if user_input is None:
            suggested_values: Mapping[str, Any] = {
                CONF_USE_HOME_COORDINATES: True
            }
            data_schema = self.add_suggested_values_to_schema(
                DATA_SCHEMA_USE_HOME_LOCATION, suggested_values
            )
            return self.async_show_form(step_id="use_home_location", data_schema=data_schema)

        self._use_home_coordinates = user_input[CONF_USE_HOME_COORDINATES]
        if self._use_home_coordinates:
            self._latitude = self.hass.config.latitude
            self._longitude = self.hass.config.longitude
            return await self.async_step_radius()
        else:
            return await self.async_step_location()

    async def async_step_location(self, user_input=None) -> FlowResult:
        if user_input is None:
            suggested_values: Mapping[str, Any] = {
                CONF_LOCATION: {
                    CONF_LATITUDE: self.hass.config.latitude,
                    CONF_LONGITUDE: self.hass.config.longitude,
                }
            }
            data_schema = self.add_suggested_values_to_schema(
                DATA_SCHEMA_LOCATION, suggested_values
            )
            return self.async_show_form(step_id="location", data_schema=data_schema)

        self._longitude = user_input[CONF_LOCATION][CONF_LONGITUDE]
        self._latitude = user_input[CONF_LOCATION][CONF_LATITUDE]
        return await self.async_step_radius()

    async def async_step_radius(self, user_input=None) -> FlowResult:
        if user_input is None:
            suggested_values: Mapping[str, Any] = {
                CONF_RADIUS: DEFAULT_RADIUS_IN_KM
            }
            data_schema = self.add_suggested_values_to_schema(
                DATA_SCHEMA_RADIUS, suggested_values
            )
            return self.async_show_form(step_id="radius", data_schema=data_schema)
        self._radius = user_input[CONF_RADIUS]
        return await self.async_create_entry_from_fields()

    async def async_create_entry_from_fields(self):
        if self._use_home_coordinates:
            title = f"{DEFAULT_NAME}"
        else:
            title = f"{DEFAULT_NAME} ({self._latitude:.2f}, {self._longitude:.2f})"
        return self.async_create_entry(
            title=title,
            data={
                CONF_API_KEY: self._api_key,
                CONF_LATITUDE: self._latitude,
                CONF_LONGITUDE: self._longitude,
                CONF_USE_HOME_COORDINATES: self._use_home_coordinates,
                CONF_RADIUS: self._radius,
            },
        )
