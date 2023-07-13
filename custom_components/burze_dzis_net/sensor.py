import asyncio
import datetime
import logging
from typing import Any, Mapping

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util.dt import parse_datetime
from homeassistant.components.sensor import SensorEntity, SensorStateClass

from .const import (DOMAIN, GAMMA_RADIATION, STORM_NEARBY, WARNING_DESCRIPTIONS, WARNING_TYPES)
from .update_coordinator import BurzeDzisNetUpdateCoordinator
from .entity import BurzeDzisNetEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    coordinator: BurzeDzisNetUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []
    for warning_type in WARNING_TYPES.keys():
        entities.append(BurzeDzisNetPresentWarningLevelSensor(coordinator, entry, warning_type))
        entities.append(BurzeDzisNetActiveWarningLevelSensor(coordinator, entry, warning_type))
    entities.append(BurzeDzisNetStormNearbySensor(coordinator, entry))
    entities.append(BurzeDzisNetGammaRadiationSensor(coordinator, entry))
    async_add_entities(entities)


class BurzeDzisNetSensor(SensorEntity, BurzeDzisNetEntity):
    def __init__(self, coordinator: BurzeDzisNetUpdateCoordinator, config_entry: ConfigEntry):
        super().__init__(coordinator, config_entry)

    @property
    def unique_id(self):
        return f"{super().unique_id}_sensor"


class BurzeDzisNetPresentWarningLevelSensor(BurzeDzisNetSensor):

    def __init__(self, coordinator: BurzeDzisNetUpdateCoordinator, config_entry: ConfigEntry, warning_type: str):
        super().__init__(coordinator, config_entry)
        self._warning_type = warning_type
        self._warning_key = WARNING_TYPES[self._warning_type][0]
        self._attr_entity_registry_enabled_default = False

    @property
    def native_value(self) -> Any:
        data = self.get_data()
        if (data is not None
                and self._warning_key in data.ostrzezenia_pogodowe):
            return data.ostrzezenia_pogodowe[self._warning_key]
        return None

    @property
    def extra_state_attributes(self) -> Mapping[str, str]:
        output = super().extra_state_attributes
        data = self.get_data().ostrzezenia_pogodowe
        if self.state is not None and self.state > 0 and data is not None:
            output['level'] = data[self._warning_key]
            output['description'] = WARNING_DESCRIPTIONS[self._warning_type][data[self._warning_key]]
            output['from'] = str(parse_datetime(data[self._warning_key + '_od_dnia'] + 'Z'))
            output['to'] = str(parse_datetime(data[self._warning_key + '_do_dnia'] + 'Z'))
        return output

    @property
    def available(self) -> bool:
        return super().available and self.get_data() is not None and self.get_data().ostrzezenia_pogodowe is not None

    @property
    def unique_id(self):
        return f"{super().unique_id}_present_warning_level_{self._warning_type}"

    @property
    def icon(self):
        return WARNING_TYPES[self._warning_type][1]

    @property
    def name(self):
        return f"{self.base_name()} {WARNING_TYPES[self._warning_type][4]}"

    @property
    def native_unit_of_measurement(self) -> str:
        return " "


class BurzeDzisNetActiveWarningLevelSensor(BurzeDzisNetPresentWarningLevelSensor):

    def __init__(self, coordinator: BurzeDzisNetUpdateCoordinator, config_entry: ConfigEntry, warning_type: str):
        super().__init__(coordinator, config_entry, warning_type)

    @property
    def native_value(self) -> float:
        super_state = super().native_value
        is_present = super_state is not None and super_state > 0
        if is_present:
            data = self.get_data().ostrzezenia_pogodowe
            start = parse_datetime(data[self._warning_key + '_od_dnia'] + 'Z')
            end = parse_datetime(data[self._warning_key + '_do_dnia'] + 'Z')
            if start <= datetime.datetime.now(tz=start.tzinfo) <= end:
                return super_state
            return 0
        return 0

    def should_poll(self) -> bool:
        return True

    async def async_update(self) -> None:
        await asyncio.sleep(0)

    @property
    def unique_id(self):
        return super().unique_id.replace("present", "active")

    @property
    def name(self):
        return f"{self.base_name()} {WARNING_TYPES[self._warning_type][5]}"


class BurzeDzisNetStormNearbySensor(BurzeDzisNetSensor):

    def __init__(self, coordinator: BurzeDzisNetUpdateCoordinator, config_entry: ConfigEntry):
        super().__init__(coordinator, config_entry)
        self._attr_entity_registry_enabled_default = False

    @property
    def native_value(self):
        data = self.get_data()
        if (data is not None
                and data.szukaj_burzy is not None
                and 'liczba' in data.szukaj_burzy):
            return data.szukaj_burzy['liczba']
        return 0

    @property
    def extra_state_attributes(self) -> dict:
        output = super().extra_state_attributes
        if self.native_value is not None and self.native_value > 0:
            data = self.get_data().szukaj_burzy
            output['number'] = data['liczba']
            output['distance'] = data['odleglosc']
            output['direction'] = data['kierunek']
            output['period'] = data['okres']
        return output

    @property
    def available(self) -> bool:
        return super().available and self.get_data() is not None and self.get_data().szukaj_burzy is not None

    @property
    def name(self):
        return f"{self.base_name()} {STORM_NEARBY[2]}"

    @property
    def icon(self):
        return STORM_NEARBY[0]

    @property
    def unique_id(self):
        return f"{super().unique_id}_storm_nearby"

    @property
    def state_class(self) -> SensorStateClass:
        return SensorStateClass.MEASUREMENT


class BurzeDzisNetGammaRadiationSensor(BurzeDzisNetSensor):
    def __init__(self, coordinator: BurzeDzisNetUpdateCoordinator, config_entry: ConfigEntry):
        super().__init__(coordinator, config_entry)

    @property
    def unique_id(self):
        return f"{super().unique_id}_gamma_radiation"

    @property
    def native_value(self) -> Any:
        data = self.get_data()
        if data is not None:
            return data.promieniowanie
        return None

    @property
    def available(self) -> bool:
        return super().available and self.get_data() is not None and self.get_data().promieniowanie is not None

    @property
    def name(self):
        return f"{self.base_name()} {GAMMA_RADIATION[0]}"

    @property
    def icon(self):
        return GAMMA_RADIATION[1]

    @property
    def native_unit_of_measurement(self) -> str:
        return "µSv/h"

    @property
    def state_class(self) -> SensorStateClass:
        return SensorStateClass.MEASUREMENT
