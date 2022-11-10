"""Solarweb integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from . import hub
from .const import DOMAIN

import logging
#TODO
#from utils import get_tokens_to_burn, burn_carbon_asset
_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from a config entry."""
    _LOGGER.warning("Start setup in init")
    _LOGGER.warning(f"E-mail address: {entry.data['email_address']}")
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = hub.Hub(hass, entry.data["email_address"], entry.data["password"])

    async def handle_datalog(call):
        """Handle the service call."""
        geo = hass.states.get('zone.home')
        geo_str = f'{geo.attributes["latitude"]}, {geo.attributes["longitude"]}'
        #TODO
        # tokens_to_burn: float = get_tokens_to_burn(geo=geo_str, kwh=call.data["count"])
        # tr_hash: str = burn_carbon_asset(seed=seed, tokens_to_burn=tokens_to_burn)
        try:
            with open('from_total.txt', 'r') as f:
                total = f.read()
                if total == '':
                    return
            hass.data[DOMAIN][entry.entry_id].boards[0]._from_grid_total -= call.data["count"]
            with open('from_total.txt', "w") as f:
                f.write(hass.data[DOMAIN][entry.entry_id].boards[0]._from_grid_total)
                hass.data[DOMAIN][entry.entry_id].boards[0].publish_updates()

        except Exception as e:
             self._from_grid_total = 0

    hass.services.async_register(DOMAIN, "burn_footprint", handle_datalog)

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
