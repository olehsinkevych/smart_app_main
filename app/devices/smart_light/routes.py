from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import Dict, Any


router = APIRouter(prefix="/api/light", tags=["light"])


class LightSettingsUpdate(BaseModel):
    is_on: bool
    brightness: int
    color_temperature: int
    mode: str


def get_device(request: Request):
    return request.app.state.device


@router.get("/status", response_model=Dict[str, Any])
async def get_status(device = Depends(get_device)):
    """Returns the current state and settings of the light."""
    return device.get_status()


# Add more endpoints for completeness
@router.post("/power")
async def set_power(is_on: bool, device = Depends(get_device)):
    """Turn the light on or off."""
    device.state.is_on = is_on
    return {"status": "success", "is_on": is_on}


@router.post("/brightness")
async def set_brightness(brightness: int, device = Depends(get_device)):
    """Set brightness level (0-100)."""
    if not 0 <= brightness <= 100:
        raise HTTPException(status_code=400, detail="Brightness must be between 0 and 100")
    device.state.brightness = brightness
    return {"status": "success", "brightness": brightness}


@router.post("/temperature")
async def set_temperature(temperature: int, device = Depends(get_device)):
    """Set color temperature."""
    if not device.min_temperature <= temperature <= device.max_temperature:
        raise HTTPException(status_code=400,
                            detail=f"Temperature must be between {device.min_temperature} and {device.max_temperature}")
    device.state.color_temperature = temperature
    return {"status": "success", "temperature": temperature}


@router.post("/mode")
async def set_mode(mode: str, device = Depends(get_device)):
    """Set light mode."""
    if mode not in device.available_modes:
        raise HTTPException(status_code=400, detail=f"Mode must be one of: {', '.join(device.available_modes)}")
    device.state.mode = mode
    return {"status": "success", "mode": mode}


@router.put("/settings")
async def update_settings(settings: LightSettingsUpdate, device = Depends(get_device)):
    """Update multiple settings at once."""
    # Validate brightness
    if not 0 <= settings.brightness <= 100:
        raise HTTPException(status_code=400, detail="Brightness must be between 0 and 100")

    # Validate temperature
    if not device.min_temperature <= settings.color_temperature <= device.max_temperature:
        raise HTTPException(status_code=400,
                            detail=f"Temperature must be between {device.min_temperature} and {device.max_temperature}")

    # Validate mode
    if settings.mode not in device.available_modes:
        raise HTTPException(status_code=400, detail=f"Mode must be one of: {', '.join(device.available_modes)}")

    # Update all settings
    device.state.is_on = settings.is_on
    device.state.brightness = settings.brightness
    device.state.color_temperature = settings.color_temperature
    device.state.mode = settings.mode

    return {"status": "success", "settings": settings.model_dump()}