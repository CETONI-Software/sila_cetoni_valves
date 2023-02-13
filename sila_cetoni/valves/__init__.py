from __future__ import annotations

import logging
import re
from typing import TYPE_CHECKING, Dict, Generic, List, Optional, TypeVar, Union, overload

from qmixsdk import qmixvalve

from sila_cetoni.application.device import CetoniDevice, Device
from sila_cetoni.utils import get_version

from .sila.valve_service.server import Server

if TYPE_CHECKING:
    from sila_cetoni.application.application_configuration import ApplicationConfiguration
    from sila_cetoni.application.cetoni_device_configuration import CetoniDeviceConfiguration


__version__ = get_version(__name__)

logger = logging.getLogger(__name__)

_T = TypeVar("_T")


# currently only a placeholder until we support valves from other manufacturers, as well
class ValveDevice(Device, Generic[_T]):
    """
    Simple class to represent a device with (possibly) multiple valves

    Template Parameters
    -------------------
    _T: type
        The type of the valves (e.g. `qmixvalve.Valve`)
    """

    _valves: List[_T]

    def __init__(self, name: str, manufacturer: str, simulated: bool, *, device_type="valves", **kwargs) -> None:
        # `**kwargs` for additional arguments that are not used and that might come from `ThirdPartyDevice.__init__` as
        # the result of `ThirdPartyValveDevice.__init__`
        super().__init__(name=name, device_type=device_type or "valves", manufacturer=manufacturer, simulated=simulated)
        self._valves = []

    @property
    def valves(self) -> List[_T]:
        return self._valves

    @valves.setter
    def valves(self, valves: List[_T]):
        self._valves = valves


# `CetoniValveDevice` *is* a `ValveDevice`, as well, via duck typing
class CetoniValveDevice(CetoniDevice[qmixvalve.Valve]):
    """
    Simple class to represent a valve device that has an arbitrary number of valves (inherited from the
    `CetoniDevice` class)
    """

    def __init__(self, name: str) -> None:
        super().__init__(name, "valves")


def parse_devices(json_devices: Optional[Dict[str, Dict]]) -> List[CetoniValveDevice]:
    """
    Parses the given JSON configuration `json_devices` and creates the necessary `CetoniValveDevice`s

    Parameters
    ----------
    json_devices: Dict[str, Dict] (optional)
        The `"devices"` section of the JSON configuration file as a dictionary (key is the device name, the value is a
        dictionary with the configuration parameters for the device, i.e. `"type"`, `"manufacturer"`, ...)

    Returns
    -------
    List[CetoniValveDevice]
        A list with all `CetoniValveDevice`s as defined in the JSON config
    """
    # CETONI devices are not defined directly in the JSON config
    return []


@overload
def create_devices(config: ApplicationConfiguration, scan: bool = False) -> None:
    """
    Looks up all controller devices from the current configuration and tries to auto-detect more devices if `scan` is
    `True`

    Parameters
    ----------
    config: ApplicationConfiguration
        The application configuration containing all devices for which SiLA Server and thus device driver instances
        shall be created
    scan: bool (default: False)
        Whether to scan for more devices than the ones defined in `config`
    """
    ...


@overload
def create_devices(config: CetoniDeviceConfiguration) -> List[CetoniValveDevice]:
    """
    Looks up all CETONI devices from the given configuration `config` and creates the necessary `CetoniValveDevice`s for
    them

    Parameters
    ----------
    config: CetoniDeviceConfiguration
        The CETONI device configuration

    Returns
    -------
    List[CetoniValveDevice]
        A list with all `CetoniValveDevice`s from the device configuration
    """
    ...


def create_devices(config: Union[ApplicationConfiguration, CetoniDeviceConfiguration], *args, **kwargs):
    from sila_cetoni.application.application_configuration import ApplicationConfiguration
    from sila_cetoni.application.cetoni_device_configuration import CetoniDeviceConfiguration

    if isinstance(config, ApplicationConfiguration):
        logger.info(
            f"Package {__name__!r} currently only supports CETONI devices. Parameter 'config' must be of type "
            f"'CetoniDeviceConfiguration'!"
        )
        return
    if isinstance(config, CetoniDeviceConfiguration):
        return create_devices_cetoni(config)
    raise ValueError(
        f"Parameter 'config' must be of type 'ApplicationConfiguration' or 'CetoniDeviceConfiguration', not"
        f"{type(config)!r}!"
    )


def create_devices_cetoni(config: CetoniDeviceConfiguration) -> List[CetoniValveDevice]:
    """
    Implementation of `create_devices` for devices from the CETONI device config

    See `create_devices` for an explanation of the parameters and return value
    """

    valve_count = qmixvalve.Valve.get_no_of_valves()
    logger.debug("Number of valves: %s", valve_count)

    devices: List[CetoniValveDevice] = []
    for i in range(valve_count):
        valve = qmixvalve.Valve()
        valve.lookup_by_device_index(i)
        try:
            valve_name = valve.get_device_name()
        except OSError:
            # When there are contiflow pumps in the config the corresponding valves from the original syringe pumps
            # are duplicated internally. I.e. with one contiflow pump made up of two low pressure pumps with their
            # corresponding valves the total number of valves is 4 despite of the actual 2 physical valves
            # available. This leads to an access violation error inside QmixSDK in case the device name of one of
            # the non-existent contiflow valves is requested. We can fortunately mitigate this with this try-except
            # here.
            continue
        logger.debug(f"Found valve {i} named {valve_name}")

        # Using `config.devices` here and operating directly on these devices is somewhat contradictory to the
        # decoupling between sila_cetoni.application and the add-on packages that this method should achieve. However,
        # this seems to be the only viable way for now.
        for device in devices + config.devices:
            if device.name.rsplit("_Pump", 1)[0] in valve_name:
                logger.debug(f"Valve {valve_name} belongs to device {device}")
                if "QmixIO" in device.name:
                    # These valve devices are actually just convenience devices that operate on digital I/O
                    # channels. Hence, they can be just used via their corresponding I/O channel.
                    continue
                device.valves.append(valve)
                break
        else:
            try:
                device_name = re.match(r".*(?=_Valve\d?$)", valve_name).group()
                if "QmixIO" in device_name:
                    # These valve devices are actually just convenience devices that operate on digital I/O
                    # channels. Hence, they can be just used via their corresponding I/O channel.
                    continue
            except AttributeError:
                device_name = valve_name
            logger.debug(f"Standalone valve device {device_name}")
            device = CetoniValveDevice(device_name)
            logger.debug(f"Valve {valve_name} belongs to device {device}")
            device.valves.append(valve)
            devices.append(device)
    return devices


def create_server(device: ValveDevice, **server_args) -> Server:
    """
    Creates the SiLA Server for the given `device`

    Parameters
    ----------
    device: Device
        The device for which to create a SiLA Server
    **server_args
        Additional arguments like server name, server UUID to pass to the server's `__init__` function
    """
    logger.info(f"Creating server for {device}")
    return Server(valves=device.valves, **server_args)
