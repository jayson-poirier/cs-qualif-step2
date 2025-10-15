from http.client import HTTPResponse
import hashlib

from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from cs_qualif_step2.core.application.dto.device_config import DeviceConfig
from cs_qualif_step2.config.get_device_service import get_device_service
from cs_qualif_step2.core.api.dto.request.register_device_request import DeviceRegistrationRequest
from cs_qualif_step2.core.application.device_service import DeviceService

device_router = APIRouter(
    prefix="/api/v1/devices",
    tags=["devices"]
)


@device_router.post("")
def register_device(
    device_registration_request: DeviceRegistrationRequest,
    device_service: DeviceService = Depends(get_device_service),
):
    device_config = DeviceConfig(
        macAddress=device_registration_request.macAddress,
        model=device_registration_request.model,
        firmwareVersion=device_registration_request.firmwareVersion,
        serialNumber=device_registration_request.serialNumber,
        displayName=device_registration_request.displayName,
        location=device_registration_request.location,
        timezone=device_registration_request.timezone,
    )
    device_id = device_service.register_device(device_config)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"device_id": device_id}
    )

@device_router.get("/{deviceId}/config")
def get_device_config(
    deviceId: str,
    device_service: DeviceService = Depends(get_device_service),
):
    device_config = device_service.get_device_config(deviceId)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=device_config
    )

@device_router.put("/{deviceId}")
def update_device_config(
    deviceId: str,
    device_service: DeviceService = Depends(get_device_service),
):

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Device updated successfully"}
    )