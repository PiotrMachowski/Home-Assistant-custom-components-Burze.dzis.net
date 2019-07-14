from zeep import Client
from zeep.exceptions import Fault
import voluptuous as vol
import logging

from homeassistant.util.dt import parse_datetime
from homeassistant.components.binary_sensor import PLATFORM_SCHEMA, ENTITY_ID_FORMAT
from homeassistant.const import CONF_NAME, CONF_RADIUS, CONF_API_KEY, ATTR_ATTRIBUTION, CONF_LATITUDE, CONF_LONGITUDE
import homeassistant.helpers.config_validation as cv
from homeassistant.components.binary_sensor import BinarySensorDevice
from homeassistant.helpers.entity import async_generate_entity_id

_LOGGER = logging.getLogger(__name__)

CONF_WARNINGS = 'warnings'
CONF_STORMS_NEARBY = 'storms_nearby'

DEFAULT_NAME = 'Burze.dzis.net'
ATTRIBUTION = 'Information provided by Burze.dzis.net.'

WARNING_TYPES = {
    'frost_warning': ['mroz', 'Ostrzeżenie - Mróz'],
    'heat_warning': ['upal', 'Ostrzeżenie - Upał'],
    'wind_warning': ['wiatr', 'Ostrzeżenie - Wiatr'],
    'precipitation_warning': ['opad', 'Ostrzeżenie - Opad'],
    'storm_warning': ['burza', 'Ostrzeżenie - Burza'],
    'tornado_warning': ['traba', 'Ostrzeżenie - Trąba'],
}
WARNING_DESCRIPTIONS = {
    'frost_warning': {
        1: "od -20 do -25°C",
        2: "od -26 do -30°C",
        3: "poniżej -30°C"
    },
    'heat_warning': {
        1: "od 30 do 34°C",
        2: "od 35 do 38°C",
        3: "powyżej 38°C"
    },
    'wind_warning': {
        1: "w porywach od 70 do 90 km/h",
        2: "w porywach od 91 do 110 km/h",
        3: "w porywach powyżej 110 km/h"
    },
    'precipitation_warning': {
        1: "deszcz od 25 do 40 mm w ciągu 24 godzin/śnieg od 10 do 15 cm w ciągu 24 godzin",
        2: "deszcz od 41 do 70 mm w ciągu 24 godzin/śnieg od 16 do 30 cm w ciągu 24 godzin/śnieg od 10 do 15 cm w ciągu 12 godzin",
        3: "deszcz powyżej 70 mm w ciągu 24 godzin/śnieg powyżej 30 cm w ciągu 24 godzin/śnieg powyżej 15 cm w ciągu 12 godzin"
    },
    'storm_warning': {
        1: "deszcz od 15 do 40 mm/wiatr w porywach od 60 do 90 km/h/grad poniżej 2 cm",
        2: "deszcz od 41 do 70 mm/wiatr w porywach od 91 do 110 km/h/grad od 2 do 5 cm",
        3: "wiatr w porywach od 91 do 110 km/h/grad od 2 do 5 cm/deszcz powyżej 70 mm/wiatr w porywach powyżej 110 km/h/grad powyżej 5 cm"
    },
    'tornado_warning': {
        1: "ryzyko niewielkie",
        2: "ryzyko umiarkowane",
        3: "ryzyko wysokie"
    }
}
STORM_NEARBY = 'Burze w pobliżu'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_LATITUDE): cv.string,
    vol.Optional(CONF_LONGITUDE): cv.string,
    vol.Required(CONF_API_KEY): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_WARNINGS, default=[]):
        vol.All(cv.ensure_list, [vol.In(WARNING_TYPES)]),
    vol.Optional(CONF_STORMS_NEARBY):
        vol.Schema({
            vol.Required(CONF_RADIUS): cv.positive_int
        })
})


def get_service():
    return Client('https://burze.dzis.net/soap.php?WSDL').service


def convert_to_dm(dmf):
    return '{}.{:02}'.format(int(dmf), round(dmf % 1 * 60))


def check_connection(api_key):
    try:
        get_service().ostrzezenia_pogodowe('0', '0', api_key)
    except Fault as fault:
        raise 'Error setting up burze_dzis_net: {}'.format(fault.message)


def setup_platform(hass, config, add_entities, discovery_info=None):
    name = config.get(CONF_NAME)
    latitude = float(config.get(CONF_LATITUDE, hass.config.latitude))
    longitude = float(config.get(CONF_LONGITUDE, hass.config.longitude))
    api_key = config.get(CONF_API_KEY)
    warnings = config.get(CONF_WARNINGS)
    storms_nearby = config.get(CONF_STORMS_NEARBY)
    radius = 0
    if storms_nearby is not None:
        radius = storms_nearby.get(CONF_RADIUS)
    check_connection(api_key)
    sensors = []
    sensor_name = '{} - '.format(name)
    x = convert_to_dm(longitude)
    y = convert_to_dm(latitude)
    for warning_type in warnings:
        uid = '{}_{}'.format(name, warning_type)
        entity_id = async_generate_entity_id(ENTITY_ID_FORMAT, uid, hass=hass)
        sensors.append(BurzeDzisNetWarningsSensor(entity_id, sensor_name, x, y, api_key, warning_type))
    if storms_nearby is not None:
        uid = '{}_storms_nearby'.format(name)
        entity_id = async_generate_entity_id(ENTITY_ID_FORMAT, uid, hass=hass)
        sensors.append(BurzeDzisNetStormsNearbySensor(entity_id, sensor_name, x, y, api_key, radius))
    add_entities(sensors, True)


class BurzeDzisNetSensor(BinarySensorDevice):

    def __init__(self, entity_id, name, x, y, api_key):
        self.entity_id = entity_id
        self._name = name
        self._x = x
        self._y = y
        self._api_key = api_key
        self._data = None

    @property
    def device_state_attributes(self):
        output = dict()
        output[ATTR_ATTRIBUTION] = ATTRIBUTION
        return output


class BurzeDzisNetWarningsSensor(BurzeDzisNetSensor):
    def __init__(self, entity_id, name, x, y, api_key, warning_type):
        super().__init__(entity_id, name, x, y, api_key)
        self._warning_type = warning_type
        self._warning_key = WARNING_TYPES[self._warning_type][0]

    @property
    def is_on(self):
        return self._data is not None and self._data[self._warning_key] > 0

    @property
    def device_state_attributes(self):
        output = super().device_state_attributes
        if self.is_on:
            output['level'] = self._data[self._warning_key]
            output['description'] = WARNING_DESCRIPTIONS[self._warning_type][self._data[self._warning_key]]
            output['from'] = str(parse_datetime(self._data[self._warning_key + '_od_dnia'] + 'Z'))
            output['to'] = str(parse_datetime(self._data[self._warning_key + '_do_dnia'] + 'Z'))
        return output

    @property
    def name(self):
        return self._name + WARNING_TYPES[self._warning_type][1]

    def update(self):
        self._data = get_service().ostrzezenia_pogodowe(self._y, self._x, self._api_key)


class BurzeDzisNetStormsNearbySensor(BurzeDzisNetSensor):
    def __init__(self, entity_id, name, x, y, api_key, radius):
        super().__init__(entity_id, name, x, y, api_key)
        self._radius = radius

    @property
    def is_on(self):
        return self._data is not None and self._data['liczba'] > 0

    @property
    def device_state_attributes(self):
        output = super().device_state_attributes
        if self.is_on:
            output['number'] = self._data['liczba']
            output['distance'] = self._data['odleglosc']
            output['direction'] = self._data['kierunek']
            output['period'] = self._data['okres']
        return output

    @property
    def name(self):
        return self._name + STORM_NEARBY

    def update(self):
        self._data = get_service().szukaj_burzy(self._y, self._x, self._radius, self._api_key)
