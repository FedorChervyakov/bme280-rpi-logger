import os
import time
import logging
import argparse

import smbus2
import bme280


def _configure_logging():
    logging.basicConfig(level=logging.INFO)


def _parse_args():
    def auto_int(val):
        "Detect base automatically"
        return int(val, 0)

    parser = argparse.ArgumentParser(
        description="""BME280 logger. Log temperature, humidity, and pressure to a file.""")

    parser.add_argument('filename')
    parser.add_argument('-p', '--port', help='I2C port (bus)', default=1, type=int)
    parser.add_argument('-a', '--address', help='I2C address', default=0x76, type=auto_int)

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', '--interval', help='sample interval in seconds', default=15, type=float)
    group.add_argument('-1', '--one-shot', help='sample once, append result to a file, and exit', action='store_true')

    return parser.parse_args()


def main():
    _configure_logging()

    args = _parse_args()

    log_file = args.filename
    sample_interval = args.interval
    address = args.address
    port = args.port

    logging.info('Starting BME280 rpi logger')
    logging.info('Writing measurements to %s', log_file)
    logging.info('I2C port: %s, address: %s', port, address)
    logging.info('Sample interval: %s', 'one-shot mode' if args.one_shot else str(args.interval) + ' s')

    bus = smbus2.SMBus(port)

    logging.info('Loading calibration parameters')

    calibration_params = bme280.load_calibration_params(bus, address)
    logging.debug('Loaded calibration parameters from the device: %s', calibration_params)

    # create log file and write header
    if not os.path.exists(log_file):
        logging.info('Log file does not exist. Creating %s and writing header', log_file)
        with open(log_file, 'w') as f:
            f.write('timestamp,temperature,humidity,pressure\n')

    logging.info('Starting sampling')
    retries = 3
    while retries:
        try:
            data = bme280.sample(bus, address, calibration_params)
            logging.debug('Acquired sample: %s', data)

            with open(log_file, 'a') as f:
                f.writelines(f'{data.timestamp},{data.temperature},{data.humidity},{data.pressure}\n')

            if args.one_shot:
                break

            time.sleep(sample_interval)
        except PermissionError as e:
            logging.exception(e)
            break
        except Exception as e:
            logging.exception("Caught %s, retrying.", e)
            retries -= 1
            continue



if __name__ == '__main__':
    main()
