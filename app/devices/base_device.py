from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any, Optional

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

class DeviceInfo(BaseModel):
    device_id: str
    device_type: str
    host: str
    port: int
    status: str
    capabilities: List[str]
    registered_at: Optional[str] = None


class BaseDevice(ABC):
    def __init__(
            self,
            device_id: str,
            device_type:str,
            host:str = "127.0.0.1", port: int = 800
    ) -> None:

        self.device_id: str = device_id
        self.device_type: str = device_type
        self.host: str = host
        self.port: int = port
        self.base_url: str = f"http://{host}: {port}"
        self.api_base: str = f"/api/{device_type}"
        self.app: FastAPI = FastAPI(
            title=f"{device_type.title()} - {device_id}",
            description=f"Microservice for {self.device_type} device",
            version="1.0.0"
        )

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        ...

    @abstractmethod
    def get_capabilities(self) -> List[str]:
        ...

    def register(self, controller):
        try:
            _ = controller.register_device(self)
            print(f"Device {self.device_id} registered successfully with controller")
        except Exception as e:
            print(f"Failed to register device {self.device_id} with controller: {e}")
            raise

    def run_server(self):
        print(f"Starting server of {self.device_type} on {self.host}: {self.port}")
        uvicorn.run(
            self.app, host=self.host, port=self.port, log_level="info"
        )

