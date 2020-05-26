import modules.data_handling
from unittest import TestCase, main, mock
import json


class TestDataHandling(TestCase):
    _test_path1 = "resources/test_resources/test1.json"
    _test_path2 = "resources/test_resources/test2.json"
    _test_path3 = "resources/test_resources/test3.json"

    @mock.patch("modules.data_handling.get_now")
    def test__create_new_player_info(self, mock_get_now):
        mock_get_now.return_value = "today"
        expected = {"name": "sergey",
                    "registration_date": "today",
                    "highscores": {"best_time": {"level1": 100000},
                                   "best_score": {"level1": 10}},
                    "statistics": {}}
        self.assertEqual(modules.data_handling._create_new_player_info("sergey", mock_get_now()), expected)

    def test_update_statistics(self):
        modules.data_handling._PLAYER_DATA_FILE = self._test_path1
        expected = {"123456": {
            "name": "sergey", "registration_date": "2020-05-12 19:16:15.129169",
            "highscores": {"best_time": {"level1": 100000}, "best_score": {"level1": 10}},
            "time_in_game": 0,
            "statistics": {}
        }
        }
        with open(modules.data_handling._PLAYER_DATA_FILE, "w") as file:
            json.dump(expected, file)
        player_id = "123456"
        new_highscores = {"best_time": {"level1": 100}, "best_score": {"level1": 100}}
        new_statistics = {"time_in_game": 10000, "kills": 25, "deaths": 3}
        modules.data_handling.update_statistics(player_id, new_statistics, new_highscores)
        expected[player_id]["highscores"] = new_highscores
        expected[player_id]["statistics"] = new_statistics
        with open(modules.data_handling._PLAYER_DATA_FILE, "r") as file:
            real = json.load(file)
            self.assertEqual(expected, real)

    def test_update_highscores(self):
        modules.data_handling._HIGHSCORES_DATA_FILE = self._test_path1
        expected = {"best_time": {"level1": [[5000, "123456"]]}, "best_score": {"level1": [[100, "123456"]]}}
        with open(modules.data_handling._HIGHSCORES_DATA_FILE, "w") as file:
            json.dump(expected, file)
        player_id = "234567"
        new_highscores = {"best_time": {"level1": 7000}, "best_score": {"level1": 50}}
        modules.data_handling.update_highscores(player_id, new_highscores)
        expected["best_time"]["level1"] = [[5000, "123456"], [7000, "234567"]]
        expected["best_score"]["level1"] = [[50, "234567"], [100, "123456"]]
        with open(modules.data_handling._HIGHSCORES_DATA_FILE, "r") as file:
            real = json.load(file)
            self.assertEqual(expected, real)

    def test__update_and_download_to_json(self):
        expected = {"A": {"B": 10, "C": 20}, "E": 7}
        with open(self._test_path1, "w") as file:
            json.dump(expected, file)
        player_id = "123456"
        modules.data_handling._update_and_download_to_json(self._test_path1, ["E", "F"], [14, 10])
        modules.data_handling._update_and_download_to_json(self._test_path1, ["B", "Q"], [1, 2], "A")
        expected["A"]["B"] = 1
        expected["A"]["Q"] = 2
        expected["E"] = 14
        expected["F"] = 10
        with open(self._test_path1, "r") as file:
            real = json.load(file)
            self.assertEqual(expected, real)

    @mock.patch("modules.data_handling.get_now")
    @mock.patch("uuid.uuid4")
    def test_create_player(self, mock_id, mock_get_now):
        mock_id.return_value = "123456"
        mock_get_now.return_value = "today"
        modules.data_handling._PLAYER_DATA_FILE = self._test_path1
        modules.data_handling._BASE_DATA_FILE = self._test_path2
        modules.data_handling._SECURITY_DATA_FILE = self._test_path3

        player_expected = {}

        base_expected = {"name_by_id": {},
                         "id_by_name": {}}

        security_expected = {}

        for file_path, expected in zip([self._test_path1, self._test_path2, self._test_path3],
                                       [player_expected, base_expected, security_expected]):
            with open(file_path, "w") as file:
                json.dump(expected, file)

        player_expected = {"123456": {"name": "sergey",
                                      "registration_date": "today",
                                      "highscores": {"best_time": {"level1": 100000},
                                                     "best_score": {"level1": 10}},
                                      "statistics": {}}}

        base_expected = {"name_by_id": {"123456": "sergey"},
                         "id_by_name": {"sergey": "123456"}}

        security_expected = {"123456": {"name": "sergey",
                                        "pass": "helloworld"}}

        modules.data_handling.create_player("sergey", "helloworld")

        for file_path, expected in zip([self._test_path1, self._test_path2, self._test_path3],
                                       [player_expected, base_expected, security_expected]):
            with open(file_path, "r") as file:
                real = json.load(file)
                self.assertEqual(real, expected)

    def test_check_login(self):
        modules.data_handling._SECURITY_DATA_FILE = self._test_path1
        modules.data_handling._BASE_DATA_FILE = self._test_path2

        security_expected = {"123456": {"name": "sergey", "pass": "helloworld"}}
        base_expected = {"name_by_id": {"123456": "sergey"}, "id_by_name": {"sergey": "123456"}}
        with open(modules.data_handling._BASE_DATA_FILE, "w") as file:
            json.dump(base_expected, file)

        with open(modules.data_handling._SECURITY_DATA_FILE, "w") as file:
            json.dump(security_expected, file)

        self.assertEqual(modules.data_handling.check_login("sergey", "helloworld"), "123456")
        self.assertEqual(modules.data_handling.check_login("sergey", "hello_world"), None)
        self.assertEqual(modules.data_handling.check_login("michael", "helloworld"), None)

    def test_get_stats(self):
        modules.data_handling._PLAYER_DATA_FILE = self._test_path1
        expected = {"123456": {"name": "sergey",
                               "registration_date": "today",
                               "highscores": {"best_time": {"level1": 100000},
                                              "best_score": {"level1": 10}},
                               "statistics": {"time_in_game": 10000}}}

        with open(modules.data_handling._PLAYER_DATA_FILE, "w") as file:
            json.dump(expected, file)
        self.assertEqual(modules.data_handling.get_stats("123456"), expected["123456"])
        with self.assertRaises(ValueError) as er:
            modules.data_handling.get_stats("123457")

    def test_get_highscores(self):
        modules.data_handling._HIGHSCORES_DATA_FILE = self._test_path1
        expected = {"best_time": {"level1": [[3000, "345678"],
                                             [4000, "234567"],
                                             [5000, "123456"]]},
                    "best_score": {"level1": [[70, "345678"],
                                              [90, "234567"],
                                              [100, "123456"]]}
                    }
        with open(modules.data_handling._HIGHSCORES_DATA_FILE, "w") as file:
            json.dump(expected, file)

        new_player_highscores = {"best_time": {"level1": 6000}, "best_score": {"level1": 80}}
        expected = {"best_time": {"level1": [[3000, "345678"],
                                             [4000, "234567"],
                                             [5000, "123456"],
                                             [6000, "456789"]]},
                    "best_score": {"level1": [[70, "345678"],
                                              [80, "456789"],
                                              [90, "234567"],
                                              [100, "123456"]]}
                    }

        modules.data_handling.update_highscores("456789", new_player_highscores)
        self.assertEqual(modules.data_handling.get_highscores(), expected)


if __name__ == '__main__':
    main()
