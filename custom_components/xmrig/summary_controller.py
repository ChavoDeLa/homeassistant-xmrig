"""XMRIG summary controller"""

import asyncio
import json
import logging
from datetime import datetime, timedelta

from typing import Any, Dict, Optional, List

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.components.sensor import SensorEntity

from .const import DOMAIN, CONF_ADDRESS, CONF_TOKEN
from .hwm_controller import HwmController

_LOGGER = logging.getLogger(__name__)

class XmrigConfigSensor(SensorEntity):
    """Sensor to store full XMRig config."""

    def __init__(self, controller):
        """Initialize the sensor."""
        self.controller = controller
        self._attr_name = "XMRig Config"
        self._attr_unique_id = "xmrig_config"

    @property
    def native_value(self):
        """Return a placeholder string (config stored as attributes)."""
        return "Config Data"

    @property
    def extra_state_attributes(self):
        """Return full config data as attributes."""
        return self.controller.data.get("config", {})

class XmrigBackendsSensor(SensorEntity):
    """Sensor to store XMRig backends data."""

    def __init__(self, controller):
        """Initialize the sensor."""
        self.controller = controller
        self._attr_name = "XMRig Backends"
        self._attr_unique_id = "xmrig_backends"

    @property
    def native_value(self):
        """Return a placeholder string (backends stored as attributes)."""
        return "Backends Data"

    @property
    def extra_state_attributes(self):
        """Return full backends data as attributes."""
        return self.controller.data.get("backends", {})

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the config and backends sensors."""
    controller = hass.data[DOMAIN]["controller"][entry.entry_id]
    async_add_entities([XmrigConfigSensor(controller), XmrigBackendsSensor(controller)], update_before_add=True)

class SummaryController(HwmController):
    """XMRIG summary controller class"""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: config_entries.ConfigEntry,
    ) -> None:
        """Initialize controller"""
        self._address: str = config_entry.data[CONF_ADDRESS]
        self._token: str = config_entry.data[CONF_TOKEN]
        super().__init__(DOMAIN, "summary", hass, config_entry)
        self.data = {} # store all data here

    async def async_update(self):
        """Update data from XMRig API."""
        await super().async_update() # get /2/summary data

        config_resource = self._address + "/1/config"
        backends_resource = self._address + "/2/backends"

        headers = self._vGetHeaders(None) # pass None, as config_entry is not needed for headers.

        config_data = await self._rest_request(config_resource, headers)
        backends_data = await self._rest_request(backends_resource, headers)

        if config_data:
            self.data["config"] = config_data
        if backends_data:
            self.data["backends"] = backends_data

    async def _rest_request(self, resource, headers):
        """Helper to make REST API requests."""
        rest = self.RestApiCall(self._hass, "GET", resource, auth=None, headers=headers, params=None, data=None, verify_ssl=True)
        await rest.async_update()
        if rest.data:
            try:
                return json.loads(rest.data)
            except json.JSONDecodeError as e:
                _LOGGER.error(f"Error decoding JSON: {e}")
                return None
        else:
            _LOGGER.warning(f"No data received from {resource}")
            return None

    def _vGetResource(self, config_entry: config_entries.ConfigEntry) -> str:
        """Get RestApiCall resource (unused here)."""
        return self._address + "/2/summary" # used by the super class.

    def _vGetHeaders(self, config_entry: config_entries.ConfigEntry) -> any:  # @type
        """Get RestApiCall headers."""
        if self._token is None:
            return None
        return {"Authorization": "Bearer " + self._token}
