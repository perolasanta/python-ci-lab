import unittest
import json
from app import Handler
from http.server import HTTPServer
from threading import Thread
from urllib.request import urlopen


class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = Thread(
            target=cls.server.serve_forever,
            daemon=True
        )
        cls.thread.start()
        cls.base_url = (
            f"http://127.0.0.1:{cls.server.server_port}"
        )

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def test_home(self):
        with urlopen(self.base_url + "/") as response:
            data = json.loads(response.read())

        self.assertEqual(data["result"], 5)
        self.assertIn("Hello", data["message"])

    def test_health(self):
        with urlopen(self.base_url + "/health") as response:
            data = json.loads(response.read())

        self.assertEqual(data["status"], "healthy")


if __name__ == "__main__":
    unittest.main()
