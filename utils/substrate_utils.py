"""
This file contains functions to burn carbon assets in IPCI network and update burns history in local DB.

"""

from logging import getLogger
from substrateinterface import SubstrateInterface, Keypair

from .constants import IPCI_REMOTE_WS, IPCI_TYPE_REGISTRY, IPCI_SS58_ADDRESS_TYPE

logger = getLogger(__name__)


def create_instance() -> SubstrateInterface:
    """
    Create on IPCI Substrate instance.

    :return: IPCI Substrate instance.

    """

    interface: SubstrateInterface = SubstrateInterface(
        url=IPCI_REMOTE_WS,
        ss58_format=IPCI_SS58_ADDRESS_TYPE,
        type_registry_preset="substrate-node-template",
        type_registry=IPCI_TYPE_REGISTRY,
    )

    return interface


def create_keypair(seed: str) -> Keypair:
    """
    Create a keypair using an `os.getenv()`-provided seed.

    :param seed: Offsetting agent seed in any form.

    :return: substrateinterface Keypair.

    """

    if seed.startswith("0x"):
        return Keypair.create_from_seed(seed_hex=hex(int(seed, 16)), ss58_format=IPCI_SS58_ADDRESS_TYPE)
    else:
        return Keypair.create_from_mnemonic(seed, ss58_format=IPCI_SS58_ADDRESS_TYPE)
