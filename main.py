import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

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

    # t1 = threading.Thread(target=station.start_opcua_server)
    # t2 = threading.Thread(target=station.start_web_server)
    #
    # t2.start()
    # t1.start()

# def start_web_server():
#     httpd = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
#     print(httpd.serve_forever())
#
#
# class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         self.send_response(200)
#         self.end_headers()
#         self.wfile.write(b'Hello, world!')


if __name__ == '__main__':
    main()
