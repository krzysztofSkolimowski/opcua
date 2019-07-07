import logging
import configparser
from weather_station import WeatherStation


def main():
    config = configparser.ConfigParser()
    config.read('.env')

    environment = 'DEV'
    station = WeatherStation(
        server_name=config.get(environment, 'NAME'),
        opcua_url=config.get(environment, 'OPC_URL'),
        api_key=config.get(environment, 'WEATHER_API_KEY'),
        place=config.get(environment, 'CITY'),
        frequency_of_fetching=int(config.get(environment, 'FREQUENCY_OF_FETCHING')),
        address=config.get(environment, 'API_URL'),
        port=int(config.get(environment, 'PORT')),
    )
    station.start()

    fmt = '%(asctime)s [%(levelname)s] - %(name)s  - %(message)s'
    logging.basicConfig(level=int(config.get(environment, 'LOG_LEVEL')),
                        filename=config.get(environment, 'LOGS_FILENAME'),
                        filemode='w',
                        format=fmt)


if __name__ == '__main__':
    main()
