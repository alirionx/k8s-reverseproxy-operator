import app_tools
from models import ReverseProxyEntry

app_tools.get_rpe_by_name(name="example-rpe", namespace="default")


example_pre = ReverseProxyEntry(
    **{
        "apiVersion": "app-scape.dev/v1",
        "kind": "ReverseProxyEntry",
        "metadata": {
            "name": "pytest-example-rpe",
            "namespace": "default"
        },
        "spec": {
            "target": {
            "endpoints": [
                "192.168.10.111"
            ],
            "port": 8080
            },
            "ingress": {
                "className": "nginx",
                "targetProtocol": "http",
                "host": "pytest-example-rpe.app-scape.de",
                "tls": False,
                "annotations": {
                    "nginx.ingress.kubernetes.io/backend-protocol": "HTTP"
                }
            }
        }
    }
)
app_tools.create_rpe(item=example_pre)
