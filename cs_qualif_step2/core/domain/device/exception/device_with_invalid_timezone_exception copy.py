from cs_qualif_step2.core.domain.exception.ConflictException import ConflictException

class DeviceWithUnsupportedTimezoneException(ConflictException):
    def __init__(self, timezone: str):
        self.timezone = timezone
        super().__init__(f"A device with timezone {timezone} has an unsupported timezone.")
