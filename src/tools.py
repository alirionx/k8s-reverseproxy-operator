
from setting import finalizer

#--------------------------------
def create_endpoints_doc(name:str, namespace: str, spec: dict) -> dict:
    ep_list = spec["target"]["endpoints"]
    ep_port = spec["target"]["port"]
    targets = [ { "ip": ep } for ep in ep_list ]
    ep_doc = {
        "metadata":{
            "name": name,
            "namespace": namespace,
            "finalizers": [ finalizer ]
        },
        "subsets": [
            {
                "addresses": targets,
                "ports": [
                    {
                        "port": ep_port,
                        "protocol": "TCP"
                    }
                ]
            }
        ]
    }
    return ep_doc


#--------------------------------
def create_service_doc(name:str, namespace: str, spec: dict) -> dict:
    ep_port = spec["target"]["port"]
    svc_doc = {
        "metadata":{
            "name": name,
            "namespace": namespace,
            "finalizers": [ finalizer ]
        },
        "spec":{
            "type": "ClusterIP",
            "ports": [
               {
                  "protocol": "TCP",
                  "port": 8080,
                  "targetPort": ep_port,
               }
            ]
        }
    }
    return svc_doc


#--------------------------------
def create_ingress_doc(name:str, namespace: str, spec: dict) -> dict:
    ing_annos = spec["ingress"].get("annotations", {})
    ing_class = spec["ingress"].get("className", "")
    ing_host = spec["ingress"].get("host", "")
    ing_tls = spec["ingress"].get("tls", False)
    ing_secret = spec["ingress"].get("secretName", name)
    ing_doc = {
        "metadata":{
            "name": name,
            "namespace": namespace,
            "annotations": ing_annos,
            "finalizers": [ finalizer ]
        },
        "spec":{
            "ingressClassName": ing_class,
            "rules": [
                {
                    "host": ing_host,
                    "http": {
                        "paths": [
                            {
                                "path": "/",
                                "pathType": "Prefix",
                                "backend": {
                                    "service": {
                                        "name": name,
                                        "port": {
                                            "number": 8080
                                        }
                                    }
                                }
                            }
                        ]
                    }
                }
            ]
        }
    }
    if ing_tls:
        ing_doc["spec"]["tls"] = [
            {
                "hosts": [ ing_host ],
                "secretName": ing_secret
            }
        ]
    return ing_doc


#--------------------------------



#--------------------------------



#--------------------------------