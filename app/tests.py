# import pytest 
from time import sleep
import random
import string
import copy

from models import ReverseProxyEntry
import app_tools

#-------------------
rand_name = ''.join(random.sample(string.ascii_lowercase + string.digits, 8))
example_pre = ReverseProxyEntry(
    **{
        "apiVersion": "app-scape.dev/v1",
        "kind": "ReverseProxyEntry",
        "metadata": {
            "name": "pytest-"+rand_name,
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
                "host": f"pytest-{rand_name}.app-scape.de",
                "tls": False,
                "annotations": {
                    "nginx.ingress.kubernetes.io/backend-protocol": "HTTP"
                }
            }
        }
    }
)



#------------------
def test_create_rpe():
    app_tools.create_rpe(item=example_pre)

def test_tools_list_rpes_names():
    res = app_tools.list_rpes_names(namespace="default")
    assert type(res) == list
    print(res)

def test_tools_get_rpes():
    res = app_tools.get_rpes()
    assert type(res) == list

def test_get_rpe_by_name():
    res = app_tools.get_rpe_by_name(
        name=example_pre.metadata.name, 
        namespace=example_pre.metadata.namespace)
    assert res.metadata.name == example_pre.metadata.name

def test_update_rpe():
    updated_pre = copy.deepcopy(example_pre)
    updated_pre.spec.target.port = 8181
    app_tools.update_rpe(
        name=example_pre.metadata.name, 
        namespace=example_pre.metadata.namespace, item=updated_pre.spec)

def test_delete_rpe():
    sleep(5)
    app_tools.delete_rpe(
        name=example_pre.metadata.name, 
        namespace=example_pre.metadata.namespace)

#-------------------