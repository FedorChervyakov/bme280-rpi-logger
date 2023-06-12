# BME280 Rasperry Pi logger service

Log temperature, humidity, and pressure sampled with the Bosch BME280 sensor connected via I2C to a file.

## Installation

### From source

Clone this repository and cd into created folder:
```bash
git clone git@github.com:FedorChervyakov/bme280-rpi-logger.git
cd bme280-rpi-logger
```

Initialize virtual environment and install dependencies
```bash
python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
```

#### Systemd unit

Use bme280-rpi-logger.service as a template to create a systemd unit.

Make sure you are using systemd-timesyncd, so that the time-sync.target is available.
See [Howto: delay a systemd service until the clock is synchronized](https://blog.debiania.in.ua/posts/2020-11-27-howto-delay-a-systemd-service-until-the-clock-is-synchronized.html) for more info.
