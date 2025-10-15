import hashlib
import re
import pytz

from cs_qualif_step2.core.domain.device.device_repository import DeviceRepository
from cs_qualif_step2.core.application.dto.device_config import DeviceConfig
from cs_qualif_step2.core.domain.device.devicefactory import DeviceFactory
from cs_qualif_step2.core.domain.device.exception.device_with_same_mac_address_exception import \
    DeviceWithSameMacAddressException
from cs_qualif_step2.core.domain.device.exception.device_with_invalid_firmware_version_exception import \
    DeviceWithUnsupportedFirmwareVersionException
from cs_qualif_step2.core.domain.device.exception.device_with_invalid_timezone_exception import \
    DeviceWithUnsupportedTimezoneException


class DeviceService:
    def __init__(self, device_repository: DeviceRepository, device_factory: DeviceFactory) -> None:
        self.device_repository = device_repository
        self.device_factory = device_factory

    def register_device(self, device_config: DeviceConfig) -> str:
        device_with_same_mac_address = self.device_repository.find_by_mac_address(device_config.macAddress)

        firmware_pattern = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+", re.IGNORECASE)

        if(not firmware_pattern.fullmatch(device_config.firmwareVersion)):
            raise DeviceWithUnsupportedFirmwareVersionException(device_config.firmwareVersion)

        if device_config.timezone not in pytz.all_timezones:
            raise DeviceWithUnsupportedTimezoneException(device_config.timezone)

        if device_with_same_mac_address is not None:
            raise DeviceWithSameMacAddressException(device_with_same_mac_address.get_mac_address())

        device = self.device_factory.create_device(device_config)

        self.device_repository.save(device)

        return str(device.get_device_id())
    
    def get_device_config(self, device_id: str) -> dict:
        device = self.device_repository.find_by_id(device_id)

        if device is None:
            return {}

        device_config = device.get_device_config()

        return {
            "channels": device_config.channels,
            "applications": device_config.applications,
            "networkSettings": device_config.networkSettings,
            "displaySettings": device_config.displaySettings
        }
