"""XMRIG custom component."""
from copy import copy
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv, device_registry as dr

from .const import (
    CONF_ADDRESS,
    CONF_TOKEN,
    DATA_CONTROLLER,
    DOMAIN,
)

from .summary_controller import SummaryController

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """XMRIG custom component."""
    _LOGGER.debug(f"async_setup({config})")
    hass.data[DOMAIN] = {}
    hass.data[DOMAIN][DATA_CONTROLLER] = {}

    return True


async def async_setup_entry(
    hass: HomeAssistant, config_entry: config_entries.ConfigEntry
) -> bool:
    """Set up an XMRIG instance."""
    _LOGGER.debug(
        "async_setup_entry({0}), state: {1}".format(
            config_entry.data[CONF_NAME], config_entry.state
        )
    )

    # Create, initialize, and preserve controller
    controller = SummaryController(hass, config_entry)
    await controller.async_initialize()
    
    # Store controller in Home Assistant data
    hass.data[DOMAIN][DATA_CONTROLLER][config_entry.entry_id] = controller

    # Forward entry setup for existing sensors (new sensors will be registered automatically)
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, "sensor")
    )

    return True


async def async_unload_entry(
    hass: HomeAssistant, config_entry: config_entries.ConfigEntry
) -> bool:
    """Unload a config entry."""
    _LOGGER.debug(
        "async_unload_entry({0}), state: {1}".format(
            config_entry.data[CONF_NAME], config_entry.state
        )
    )
    controller: SummaryController = hass.data[DOMAIN][DATA_CONTROLLER][
        config_entry.entry_id
    ]
    await hass.config_entries.async_forward_entry_unload(config_entry, "sensor")
    await controller.async_reset()
    
    return True
