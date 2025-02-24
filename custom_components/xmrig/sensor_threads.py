import logging
from homeassistant.components.sensor import SensorEntity

_LOGGER = logging.getLogger(__name__)

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
        _LOGGER.debug(f"Thread count fetched: {len(threads)}")
        return len(threads)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the thread count sensor."""
    _LOGGER.debug("Setting up XMRig Threads Count sensor")
    
    # Access the controller correctly
    controller = hass.data["xmrig"][DATA_CONTROLLER].get(entry.entry_id)
    if not controller:
        _LOGGER.error("XMRig controller not found for Threads Count sensor")
        return

    async_add_entities([XmrigThreadsCountSensor(controller)], update_before_add=True)
