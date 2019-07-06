import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

import opcua
import logging

import open_weather


# todo: make server implementation of method work
# @uamethod
# def update_predictions_uamethod():
#     """
#     forces update of predictions in weather station
#     """
#     logging.log(logging.INFO, "updating predictions")
#     weather_station.update_prediction()


class WeatherStation:
    """
    Highest level representation of weather station.
    Contains opc-ua server, weather api client  and necessary methods.
    """

    def __init__(self, opcua_url, server_name, api_key, place, frequency_of_fetching=30):
        """
        :param opcua_url: url of the server endpoint to expose
        :type opcua_url: string
        :param server_name: name of the server
        :type server_name: string
        :param api_key: api key of the open_weather API,
        needs to be obtained via registration of the user on open weather maps platform
        :type api_key: string
        :param place: localization in format "city,country code" e. g. "London,gb"
        :type place: string
        :param frequency_of_fetching: frequency of refreshing of weather measurements in seconds
        :type frequency_of_fetching: int
        """
        self.weather_fetcher = open_weather.Client(api_key, place)

        self.server = opcua.Server()
        self.server.set_endpoint(opcua_url)
        self.server.set_server_name(server_name)
        idx = self.server.register_namespace("namespace")

        days, time_of_last_fetching = self.fetch_prediction()
        time_node = self.server.nodes.objects.add_object(idx, "time")
        self.time_holder = time_node.add_variable(idx, "last_fetching", time_of_last_fetching)

        # todo: make server implementation of method work
        # time_node.add_method(idx, "update_predictions_uamethod", update_predictions_uamethod)
        self.object_variables = {}
        for d in days.keys():
            idx = idx + 1
            obj = self.server.nodes.objects.add_object(idx, d)
            self.object_variables[d] = {}
            for k in days[d].keys():
                variable = obj.add_variable(idx, k, days[d][k])
                self.object_variables[d][k] = variable

        self.frequency_of_fetching = frequency_of_fetching

        # todo - it is work around not working opcua method
        update_predictions = self.update_prediction

        class HTTPRequestHandler(BaseHTTPRequestHandler):
            def do_POST(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                update_predictions()

                self.wfile.write(b'Success!!!')

        self.handler = HTTPRequestHandler

    def fetch_prediction(self):
        """
        fetches new predictions
        :return: predictions {"day":prediction_values}
        :rtype: {string:{string:int}}
        possible prediction params and value types
        "temperature": int [C°],
        "humidity": int [%],
        "pressure": int [hPA],
        "wind_speed": int [m/s],
        "wind_direction": int [°],
        "clouds": int [%],
        "conditions": string [status:string],
        "time": int [int - UNIX TIME],
        """
        logging.log(logging.INFO, "fetching data from https://openweathermap.org/api")
        today, two_days_prediction, time_of_prediction = self.weather_fetcher.fetch_weather(2)
        return {"today": today, "tomorrow": two_days_prediction[0],
                "day_after": two_days_prediction[1]}, time_of_prediction

    def update_prediction(self):
        """
        fetches new predictions and updates opc-ua nodes with them
        :return:
        :rtype:
        """
        logging.log(logging.INFO, "updating predictions")
        prediction, time_of_prediction = self.fetch_prediction()
        self.time_holder.set_value(time_of_prediction)

        for day in self.object_variables.keys():
            variables = self.object_variables[day]
            for v in variables.keys():
                variables[v].set_value(prediction[day][v])

    def start_opcua_server(self):
        """
        starts server and consecutive updates
        in case of any client errors creates a delay,
        leaving previous values as are with specified time
        """
        logging.log(logging.INFO, "Weather station has started")
        self.server.start()
        while True:
            try:
                self.update_prediction()

            finally:
                time.sleep(self.frequency_of_fetching)

    def start_web_server(self):
        httpd = HTTPServer(('localhost', 8000), self.handler)
        print(httpd.serve_forever())

    def start(self):
        """
        Starts two threads
        Necessary to expose rest api enpoint
        """
        t1 = threading.Thread(target=self.start_opcua_server)
        t2 = threading.Thread(target=self.start_web_server)

        t2.start()
        t1.start()
