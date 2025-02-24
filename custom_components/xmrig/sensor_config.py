from homeassistant.components.sensor import SensorEntity

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
