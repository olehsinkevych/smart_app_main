from typing import List, Dict, Any, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.devices.base_device import BaseDevice


class LightState(BaseModel):
    is_on: bool = False
    brightness: int = 100
    color_temperature: int = "4000"
    mode: str = "eco"


class BrightnessRequest(BaseModel):
    brightness: int


class TemperatureRequest(BaseModel):
    temperature: int


class ModeRequest(BaseModel):
    mode: str


class SmartLightDevice(BaseDevice):
    """
    Smart Light Microservice
    Runs as independent FastAPI server on specific port
    """

    def __init__(
            self,
            device_id: str,
            host: str = "127.0.0.1", port: int = 8001
    ) -> None:
        super().__init__(device_id, "light", host, port)
        self.state = LightState()
        self.available_modes = [
            "eco", "night", "normal", "party",
        ]
        self.min_temperature: int = 2000
        self.max_temperature: int = 8000

    def _setup_routes(self):
        """Setup light-specific API routes"""
        app = self.app

        @app.get("/api/light/status")
        async def get_status():
            return self.get_status()

        @app.post("/api/light/power/{state}")
        async def set_power(state: str):
            if state == "on":
                self.state.is_on = True
                message = "Light turned on"
            elif state == "off":
                self.state.is_on = False
                message = "Light turned off"
            else:
                raise HTTPException(status_code=400, detail="Invalid power state. Use 'on' or 'of'")
            return {"status": "success", "message": message, "is_on": self.state.is_on}

        # TODO: implement brightness, modes, temperature

        @app.get("api/light/settings")
        async def get_settings():
            return{
                "available_modes": self.available_modes,
                "temperature_range": {
                    "min": self.min_temperature,
                    "max": self.max_temperature
                }
            }

        @app.put("/api/light/settings")
        async def update_settings(settings: LightState):
            """Update multiple settings at once using Pydantic model"""
            # TODO: implement the logic
            return {
                "status": "success",
                "message": "Light settings updated successfully",
                "settings": self.state.model_dump()
            }

    def get_status(self) -> Dict[str, Any]:
        return {
            "device_id": self.device_id,
            "device_type": self.device_type,
            "is_on": self.state.is_on,
            "brightness": self.state.brightness,
            "color_temperature": self.state.color_temperature,
            "mode": self.state.mode,
            "available_modes": self.available_modes,
            "endpoint": f"{self.base_url}/api/light"
        }

    def get_capabilities(self) -> List[str]:
        return [
            "power_control", "brightness control",
            "temperature_control", "mode_presets",
            "bulk_settings_update"
        ]

if __name__ == "___main__":
    light = SmartLightDevice("kitchen light", "127.0.0.1", 8001)
    light.register()