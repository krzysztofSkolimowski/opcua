import logging

from weather_station import WeatherStation


def main():
    logging.basicConfig(level=logging.INFO, filename="weather_station.log", filemode='w',
                        format='%(name)s - %(levelname)s - %(message)s')

    weather_api_key = "8bb678a3a68cc9d446a737556cb27923"
    url = "opc.tcp://127.0.0.1:4840/weather"
    name = "OPC_UA_WEATHER_STATION"
    city = "Krakow,PL"

    station = WeatherStation(url, name, weather_api_key, city)
    station.start()


if __name__ == '__main__':
    main()
