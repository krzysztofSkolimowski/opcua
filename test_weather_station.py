import unittest

import configparser
import opcua
from opcua.ua import LocalizedText

environment = 'TEST'


class TestWeatherStation(unittest.TestCase):
    def setUp(self):
        config = configparser.ConfigParser()
        config.read('.env')

        self.client = opcua.Client(config.get(environment, 'TEST_OPC_URL'))

    def test_workspace(self):
        self.client.connect()

        root = self.client.get_root_node()
        print(root)

        time_node = root.get_child(["0:Objects", "2:time"])
        self.assertEqual(time_node.get_display_name(), LocalizedText("time"))

        today_node = root.get_child(["0:Objects", "3:today"])
        self.assertEqual(today_node.get_display_name(), LocalizedText("today"))

        tomorrow_node = root.get_child(["0:Objects", "4:tomorrow"])
        self.assertEqual(tomorrow_node.get_display_name(), LocalizedText("tomorrow"))

        day_after_node = root.get_child(["0:Objects", "5:day_after"])
        self.assertEqual(day_after_node.get_display_name(), LocalizedText("day_after"))

        self.client.disconnect()


if __name__ == '__main__':
    unittest.main()
