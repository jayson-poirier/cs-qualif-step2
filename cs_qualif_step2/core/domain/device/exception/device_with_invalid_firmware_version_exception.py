from cs_qualif_step2.core.domain.exception.ConflictException import ConflictException

class DeviceWithUnsupportedFirmwareVersionException(ConflictException):
    def __init__(self, firmware_version: str):
        self.firmware_version = firmware_version
        super().__init__(f"A device with firmare version {firmware_version} has an unsupported firmware version.")
