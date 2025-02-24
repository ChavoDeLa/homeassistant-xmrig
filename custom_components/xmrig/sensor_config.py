import logging
from homeassistant.components.sensor import SensorEntity

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
        config_data = self.controller.data.get("config", {})
        _LOGGER.debug(f"Config Data Fetched: {config_data}")
        return config_data

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the config sensor."""
    _LOGGER.debug("Setting up XMRig Config sensor")

    # Access the controller correctly
    controller = hass.data["xmrig"][DATA_CONTROLLER].get(entry.entry_id)
    if not controller:
        _LOGGER.error("XMRig controller not found for Config sensor")
        return

    async_add_entities([XmrigConfigSensor(controller)], update_before_add=True)
