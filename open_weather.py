import math
import pyowm

hour_unix_time = 3600
day_unix_time = 86400


def hour_of_the_day(unix_time):
    """
    :param unix_time: concrete hour in unix time
    :type unix_time: int
    :return: an hour digit from unix time in 24h format,
    e. g. unix_time: 1562096054,
    what is 07/02/2019 @ 19:34 (UTC), should return 19
    :rtype: int
    """
    return math.floor((unix_time % day_unix_time) / hour_unix_time)


class Client:
    def __init__(self,
                 api_key="8bb678a3a68cc9d446a737556cb27923",
                 place="Krakow,PL",
                 expected_forecast_time=15,
                 station_id="583436dd9643a9000196b8d6"):
        self.owm = pyowm.OWM(api_key)
        self.place = place
        self.expected_reference_time = expected_forecast_time
        self.station = station_id

    def fetch_weather(self, number_of_days=2):
        """
        fetch_weather performs API calls to @link:http://api.openweathermap.org API
        :param number_of_days: number of days to get prediction for beyond today
        e. g. 2 should return weather for tomorrow and the day after tomorrow
        max value for param is 5, due to the limits of free tier API
        :type number_of_days: int
        :return: current
        -:rtype:dict{string:int} - dictionary representing weather params with integer values
        "temperature": int [C°],
        "humidity": int [%],
        "pressure": int [hPA],
        "wind_speed": int [m/s],
        "wind_direction": int [°],
        "clouds": int [%],
        "conditions": string [status:string],
        "time": int [int - UNIX TIME],
        :return: weather in n days
        -:rtype: list[dict{string:int} list of the same dictionaries as current
        :return: reception_time - time of the reception
        -:rtype: int
        """
        w = self.owm.weather_at_place(self.place).get_weather()
        current = {
            "temperature": w.get_temperature('celsius')['temp'],
            "humidity": w.get_humidity(),
            "pressure": w.get_pressure()['press'],
            "wind_speed": w.get_wind()['speed'],
            "wind_direction": w.get_wind()['deg'],
            "clouds": w.get_clouds(),
            "conditions": w.get_detailed_status(),
            "time": w.get_reference_time('unix'),
        }

        five_days = self.owm.three_hours_forecast(self.place).get_forecast()
        reception_time = five_days.get_reception_time()
        weathers_in_five_days = [{
            "temperature": w.get_temperature('celsius')['temp'],
            "humidity": w.get_humidity(),
            "pressure": w.get_pressure()['press'],
            "wind_speed": w.get_wind()['speed'],
            "wind_direction": w.get_wind()['deg'],
            "clouds": w.get_clouds(),
            "conditions": w.get_detailed_status(),
            "time": w.get_reference_time('unix'),
        } for w in five_days.get_weathers()
            if hour_of_the_day(w.get_reference_time()) == self.expected_reference_time]

        if number_of_days >= 5:
            return current, weathers_in_five_days, reception_time

        return current, weathers_in_five_days[:number_of_days], reception_time
