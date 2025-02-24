import logging
import json
from homeassistant.components.sensor import SensorEntity

from .const import DATA_CONTROLLER, CONF_NAME  # Import constants

_LOGGER = logging.getLogger(__name__)

class XmrigConfigSensor(SensorEntity):
    """Sensor to store full XMRig config."""

    def __init__(self, controller):
        """Initialize the sensor."""
        self.controller = controller
        self._attr_name = f"{controller._name} Config" # use name from controller
        self._attr_unique_id = f"{controller.entity_id}_xmrig_config" # use entity_id from controller

    @property
    def native_value(self):
        """Return full config data as json string."""
        config_data = self.controller.data.get("config", {})
        if not config_data:
            return "No Config Data"
        try:
            return json.dumps(config_data)
        except TypeError:
            _LOGGER.warning("Config data is not JSON serializable.")
            return "Config data error"

    @property
    def extra_state_attributes(self):
        """Return full config data as attributes."""
        config_data = self.controller.data.get("config", {})
        _LOGGER.debug(f"Config Data Fetched: {config_data}")
        return config_data

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the config sensor."""
    _LOGGER.debug("Setting up XMRig Config sensor")

    # Access the controller correctly using constant
    controller = hass.data["xmrig"][DATA_CONTROLLER].get(entry.entry_id)
    if not controller:
        _LOGGER.error("XMRig controller not found for Config sensor")
        return

    async_add_entities([XmrigConfigSensor(controller)], update_before_add=True)
