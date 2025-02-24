from homeassistant.components.sensor import SensorEntity

class XmrigThreadsCountSensor(SensorEntity):
    """Sensor to count threads from XMRig backends."""

    def __init__(self, controller):
        """Initialize the sensor."""
        self.controller = controller
        self._attr_name = "XMRig Threads Count"
        self._attr_unique_id = "xmrig_threads_count"

    @property
    def native_value(self):
        """Return the number of threads."""
        backends_data = self.controller.data.get("backends", {})
        threads = backends_data.get("threads", [])
        return len(threads)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the thread count sensor."""
    controller = hass.data["xmrig"]["controller"][entry.entry_id]
    async_add_entities([XmrigThreadsCountSensor(controller)], update_before_add=True)
