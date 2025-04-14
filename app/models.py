from pydantic import BaseModel
from typing import Literal


class ReverseProxyEntryMeta(BaseModel):
    name: str
    namespace: str

class Target(BaseModel):
    endpoints: list[str] 
    port: int

class Ingress(BaseModel):
    className: str | None = "nginx"
    targetProtocol:  Literal["http", "https"] | None = "http"
    host: str
    tls: bool | None = False
    secretName: str | None = None
    annotations: dict | None = {}
    @property
    def secret_name_valid(self) -> bool:
        return self.secretName is None or len(self.secretName) >= 3

class ReverseProxyEntrySpec(BaseModel):
    target: Target 
    ingress: Ingress

class ReverseProxyEntry(BaseModel):
    apiVersion: str | None = "app-scape.dev/v1"
    kind: str | None = "ReverseProxyEntry"
    metadata: ReverseProxyEntryMeta
    spec: ReverseProxyEntrySpec

    @property
    def apiversion_valid(self) -> bool:
        return self.apiVersion == "app-scape.dev/v1"
    @property
    def apiversion_valid(self) -> bool:
        return self.apiVersion == "ReverseProxyEntry"