from typing import Dict, Any, List
from pydantic import BaseModel
from app.devices.base_device import BaseDevice
from app.devices.smart_light.routes import router as light_router


class LightState(BaseModel):
    is_on: bool = False
    brightness: int = 100
    color_temperature: int = 4000
    mode: str = "eco"


class BrightnessRequest(BaseModel):
    brightness: int


class TemperatureRequest(BaseModel):
    temperature: int


class ModeRequest(BaseModel):
    mode: str


class SmartLightDevice(BaseDevice):
    def __init__(self, device_id: str = "light_default", host: str = "127.0.0.1", port: int = 8001):
        super().__init__(device_id, "light", host, port)
        self.state = LightState()
        self.available_modes = ["eco", "night", "normal", "party"]
        self.min_temperature = 2000
        self.max_temperature = 8000
        self.app.state.device = self

        self.app.include_router(light_router)

    def get_status(self) -> Dict[str, Any]:
        """Returns the complete status of the light, including current state and settings."""
        return {
            "device_id": self.device_id,
            "device_type": self.device_type,
            "is_on": self.state.is_on,
            "brightness": self.state.brightness,
            "color_temperature": self.state.color_temperature,
            "mode": self.state.mode,
            "available_modes": self.available_modes,
            "min_temperature": self.min_temperature,
            "max_temperature": self.max_temperature,
            "endpoint": f"{self.base_url}/api/light"
        }

    def get_capabilities(self) -> List[str]:
        return [
            "power_control", "brightness_control",
            "temperature_control", "mode_presets",
            "bulk_settings_update"
        ]


if __name__ == "__main__":
    light = SmartLightDevice("kitchen light", "127.0.0.1", 8001)
    light.run_server()