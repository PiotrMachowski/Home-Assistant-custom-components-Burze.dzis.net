[![HACS Default][hacs_shield]][hacs]
[![GitHub Latest Release][releases_shield]][latest_release]
[![GitHub All Releases][downloads_total_shield]][releases]
[![Buy me a coffee][buy_me_a_coffee_shield]][buy_me_a_coffee]
[![PayPal.Me][paypal_me_shield]][paypal_me]


[hacs_shield]: https://img.shields.io/static/v1.svg?label=HACS&message=Default&style=popout&color=green&labelColor=41bdf5&logo=HomeAssistantCommunityStore&logoColor=white
[hacs]: https://hacs.xyz/docs/default_repositories

[latest_release]: https://github.com/PiotrMachowski/Home-Assistant-custom-components-Burze.dzis.net/releases/latest
[releases_shield]: https://img.shields.io/github/release/PiotrMachowski/Home-Assistant-custom-components-Burze.dzis.net.svg?style=popout

[releases]: https://github.com/PiotrMachowski/Home-Assistant-custom-components-Burze.dzis.net/releases
[downloads_total_shield]: https://img.shields.io/github/downloads/PiotrMachowski/Home-Assistant-custom-components-Burze.dzis.net/total

[buy_me_a_coffee_shield]: https://img.shields.io/static/v1.svg?label=%20&message=Buy%20me%20a%20coffee&color=6f4e37&logo=buy%20me%20a%20coffee&logoColor=white
[buy_me_a_coffee]: https://www.buymeacoffee.com/PiotrMachowski

[paypal_me_shield]: https://img.shields.io/static/v1.svg?label=%20&message=PayPal.Me&logo=paypal
[paypal_me]: https://paypal.me/PiMachowski

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

## Installation

### Using [HACS](https://hacs.xyz/) (recommended)

This integration can be installed using HACS.
To do it search for `Burze.dzis.net` in *Integrations* section.

### Manual

To install this integration manually you have to download [*burze_dzis_net.zip*](https://github.com/PiotrMachowski/Home-Assistant-custom-components-Burze.dzis.net/releases/latest/download/burze_dzis_net.zip) and extract its contents to `config/custom_components/burze_dzis_net` directory:
```bash
mkdir -p custom_components/burze_dzis_net
cd custom_components/burze_dzis_net
wget https://github.com/PiotrMachowski/Home-Assistant-custom-components-Burze.dzis.net/releases/latest/download/burze_dzis_net.zip
unzip burze_dzis_net.zip
rm burze_dzis_net.zip
```

## FAQ

* **How to get API key?**
  
  To get API key you have to follow steps available at [*official project page*](https://burze.dzis.net/?page=api_interfejs).

* **What to do if Home Assistant does not find this component?**

  Most likely you have to install additional dependency required for it to run. Activate Python environment Home Assistant is running in and use following command:
  ```bash
  pip install zeep
  ```

<a href="https://www.buymeacoffee.com/PiotrMachowski" target="_blank"><img src="https://bmc-cdn.nyc3.digitaloceanspaces.com/BMC-button-images/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>
<a href="https://paypal.me/PiMachowski" target="_blank"><img src="https://www.paypalobjects.com/webstatic/mktg/logo/pp_cc_mark_37x23.jpg" border="0" alt="PayPal Logo" style="height: auto !important;width: auto !important;"></a>
