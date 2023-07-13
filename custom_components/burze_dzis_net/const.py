from typing import Final
from datetime import timedelta

from homeassistant.const import Platform

DOMAIN: Final = "burze_dzis_net"
DEFAULT_NAME: Final = "Burze.dzis.net"
DEFAULT_UPDATE_INTERVAL: Final = timedelta(minutes=2, seconds=30)
WSDL_URL: Final = 'https://burze.dzis.net/soap.php?WSDL'

CONF_USE_HOME_COORDINATES: Final = "use_home_coordinates"
CONF_WARNINGS = 'warnings'
CONF_STORMS_NEARBY = 'storms_nearby'

DEFAULT_RADIUS_IN_KM = 25

PLATFORMS = [
    Platform.BINARY_SENSOR,
    Platform.SENSOR
]

ATTRIBUTION = 'Information provided by Burze.dzis.net.'

WARNING_TYPES = {
    'frost_warning': [
        'mroz',
        'mdi:weather-snowy',
        'Ostrzeżenie - Mróz',
        'Ostrzeżenie Aktywne - Mróz',
        'Stopień zagrożenia - Mróz',
        'Stopień aktywnego zagrożenia - Mróz',
    ],
    'heat_warning': [
        'upal',
        'mdi:weather-sunny',
        'Ostrzeżenie - Upał',
        'Ostrzeżenie Aktywne - Upał',
        'Stopień zagrożenia - Upał',
        'Stopień aktywnego zagrożenia - Upał',
    ],
    'wind_warning': [
        'wiatr',
        'mdi:weather-windy',
        'Ostrzeżenie - Wiatr',
        'Ostrzeżenie Aktywne - Wiatr',
        'Stopień zagrożenia - Wiatr',
        'Stopień aktywnego zagrożenia - Wiatr',
    ],
    'precipitation_warning': [
        'opad',
        'mdi:weather-pouring',
        'Ostrzeżenie - Opad',
        'Ostrzeżenie Aktywne - Opad',
        'Stopień zagrożenia - Opad',
        'Stopień aktywnego zagrożenia - Opad',
    ],
    'storm_warning': [
        'burza',
        'mdi:weather-lightning-rainy',
        'Ostrzeżenie - Burza',
        'Ostrzeżenie Aktywne - Burza',
        'Stopień zagrożenia - Burza',
        'Stopień aktywnego zagrożenia - Burza',
    ],
    'tornado_warning': [
        'traba',
        'mdi:weather-hurricane',
        'Ostrzeżenie - Trąba',
        'Ostrzeżenie Aktywne - Trąba',
        'Stopień zagrożenia - Trąba',
        'Stopień aktywnego zagrożenia - Trąba',
    ],
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

STORM_NEARBY = ['mdi:weather-lightning', 'Wyładowania w pobliżu', 'Wyładowania w pobliżu']
GAMMA_RADIATION = ['Promieniowanie gamma', 'mdi:radioactive']
