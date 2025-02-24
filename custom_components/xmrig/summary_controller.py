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

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the config sensor."""
    controller = hass.data["xmrig"]["controller"][entry.entry_id]
    async_add_entities([XmrigConfigSensor(controller)], update_before_add=True)

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

    def _vGetResource(self, config_entry: config_entries.ConfigEntry) -> str:
        """Get RestApiCall resource"""
        return self._address + "/2/summary"

    def _vGetHeaders(self, config_entry: config_entries.ConfigEntry) -> any:  # @type
        """Get RestApiCall headers"""
        if self._token is None:
            return None
        return {"Authorization": "Bearer " + self._token}
