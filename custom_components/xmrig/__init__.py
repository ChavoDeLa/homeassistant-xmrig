import logging
import asyncio
import aiohttp
import async_timeout
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=30)

class XmrigData:
    """Class to manage fetching XMRIG data."""

    def __init__(self, hass: HomeAssistant, url: str):
        """Initialize the data object."""
        self._hass = hass
        self._url = url
        self.data = {}
        
    async def async_update(self):
        """Fetch data from XMRIG endpoints."""
        await self._fetch_summary()
        await self._fetch_backends()
        await self._fetch_config()

    async def _fetch_summary(self):
        """Fetch summary data."""
        url = f"{self._url}/2/summary"
        self.data['summary'] = await self._fetch_data(url)

    async def _fetch_backends(self):
        """Fetch backends data."""
        url = f"{self._url}/2/backends"
        backends_data = await self._fetch_data(url)
        self.data['threads_length'] = len(backends_data.get('threads', []))

    async def _fetch_config(self):
        """Fetch config data."""
        url = f"{self._url}/1/config"
        self.data['config'] = await self._fetch_data(url)

    async def _fetch_data(self, url: str):
        """Fetch data from the given URL."""
        try:
            async with async_timeout.timeout(10):
                session = async_get_clientsession(self._hass)
                async with session.get(url) as response:
                    if response.status != 200:
                        _LOGGER.error("Error fetching data from %s, status: %s", url, response.status)
                        return None
                    return await response.json()
        except (asyncio.TimeoutError, aiohttp.ClientError) as err:
            _LOGGER.error("Error fetching data from %s: %s", url, err)
            return None
