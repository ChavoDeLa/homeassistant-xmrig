import logging
from homeassistant.components.sensor import SensorEntity
from . import XmrigData

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the XMRIG sensor platform."""
    url = config.get('url')
    xmrig_data = XmrigData(hass, url)
    await xmrig_data.async_update()

    sensors = [
        XmrigSensor(xmrig_data, 'hashrate', 'H/s'),
        XmrigSensor(xmrig_data, 'threads_length', 'threads'),
        XmrigSensor(xmrig_data, 'config', None, True),
    ]
    async_add_entities(sensors, True)

class XmrigSensor(SensorEntity):
    """Representation of an XMRIG sensor."""

    def __init__(self, xmrig_data, sensor_type, unit_of_measurement, is_json=False):
        """Initialize the sensor."""
        self._xmrig_data = xmrig_data
        self._sensor_type = sensor_type
        self._unit_of_measurement = unit_of_measurement
        self._is_json = is_json
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"xmrig_{self._sensor_type}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit_of_measurement

    async def async_update(self):
        """Update the sensor state."""
        await self._xmrig_data.async_update()
        if self._is_json:
            self._state = str(self._xmrig_data.data.get(self._sensor_type))
        else:
            self._state = self._xmrig_data.data.get(self._sensor_type)
