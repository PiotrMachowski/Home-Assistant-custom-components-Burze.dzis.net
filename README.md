# Burze.dzis.net sensor

This sensor uses official API to get weather warnings from [*Burze.dzis.net*](https://burze.dzis.net/). To get more detailed information about parameters of warnings visit [*official API documentation*](https://burze.dzis.net/soap.php?WSDL).

## Configuration options

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `name` | `string` | `False` | `Burze.dzis.net` | Name of sensor |
| `api_key` | `string` | `True` | - | API key for Burze.dzis.net |
| `latitude` | `float` | `False` | Latitude of home | Latitude of monitored point |
| `longitude` | `float` | `False` | Longitude of home | Longitude of monitored point |
| `warnings` | `list` | `False` | - | List of monitored warnings |
| `storms_nearby` | - | `False` | - | Enables monitoring nearby storms |

### Configuration options of `storms_nearby`

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `radius` | `positive int` | `True` | - | Radius of nearby storms monitoring |

### Possible monitored warnings

| Key | Description |
| --- | --- | 
| `frost_warning` | Enables frost warnings monitoring |
| `heat_warning` | Enables heat warnings monitoring |
| `wind_warning` | Enables wind warnings monitoring |
| `precipitation_warning` | Enables precipitation warnings monitoring |
| `storm_warning` | Enables storm warnings monitoring |
| `tornado_warning` | Enables tornado warnings monitoring |

## Example usage

```
binary_sensor:
  - platform: burze_dzis_net
    api_key: !secret burze_dzis_net.api_key
    warnings:
      - frost_warning
      - heat_warning
      - wind_warning
      - precipitation_warning
      - storm_warning
      - tornado_warning
    storms_nearby:
      radius: 30
```

## Instalation

Download [*binary_sensor.py*](https://github.com/PiotrMachowski/Home-Assistant-custom-components-Burze.dzis.net/raw/master/custom_components/burze_dzis_net/binary_sensor.py) and [*manifest.json*](https://github.com/PiotrMachowski/Home-Assistant-custom-components-Burze.dzis.net/raw/master/custom_components/burze_dzis_net/manifest.json) to `config/custom_components/burze_dzis_net` directory:
```bash
mkdir -p custom_components/burze_dzis_net
cd custom_components/burze_dzis_net
wget https://github.com/PiotrMachowski/Home-Assistant-custom-components-Burze.dzis.net/raw/master/custom_components/burze_dzis_net/binary_sensor.py
wget https://github.com/PiotrMachowski/Home-Assistant-custom-components-Burze.dzis.net/raw/master/custom_components/burze_dzis_net/manifest.json
```

## FAQ

* **How to get API key?**
  
  To get API key you have to follow steps available at [*official project page*](https://burze.dzis.net/?page=api_interfejs).

* **What to do if Home Assistant does not find this component?**

  Most likely you have to install additional dependency required for it to run. Activate Python environment Home Assistant is running in and use following command:
  ```bash
  pip install zeep
  ```