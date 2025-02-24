import json
import requests
from homeassistant.helpers.entity import Entity

class XmrigSensor(Entity):
    def __init__(self, name, host, port):
        self._name = name
        self._host = host
        self._port = port
        self._state = None
        self._data = {}
        self.update()

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._data

    def update(self):
        summary_url = f"http://{self._host}:{self._port}/2/summary"
        backends_url = f"http://{self._host}:{self._port}/2/backends"
        config_url = f"http://{self._host}:{self._port}/1/config"

        try:
            # Fetch summary data
            summary_response = requests.get(summary_url)
            summary_data = summary_response.json()
            self._state = summary_data.get("hashrate", {}).get("total", [0])[0]
            self._data.update(summary_data)

            # Fetch backends data
            backends_response = requests.get(backends_url)
            backends_data = backends_response.json()
            threads = backends_data.get("threads", [])
            self._data["threads_count"] = len(threads)

            # Fetch config data
            config_response = requests.get(config_url)
            config_data = config_response.json()
            self._data["config"] = config_data

        except requests.exceptions.RequestException as e:
            self._state = None
            self._data = {"error": str(e)}
