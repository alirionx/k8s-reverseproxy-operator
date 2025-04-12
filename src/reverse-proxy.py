from datetime import datetime
import kopf
import logging
from kr8s.objects import Endpoints, Service, Ingress

from setting import finalizer
import tools

#-Base operator config-------------------------------------------
@kopf.on.startup()
def configure(settings: kopf.OperatorSettings, **_):
    settings.persistence.finalizer = finalizer


#-Create the set-------------------------------------------------
@kopf.on.create('reverseproxyentrys')
def create_fn(body, **kwargs):
    logging.info(f"A CREATE handler is called with body: {body}")
    
    #-Collect parameters---------------------------
    name = body["metadata"]["name"]
    namespace = body["metadata"]["namespace"]
    childs_name = "rpe-"+name
    
    #-The Endpoints--------------------------------
    ep_doc = tools.create_endpoints_doc(
        name=childs_name, namespace=namespace, spec=body["spec"])
    kopf.adopt(ep_doc)
    ep = Endpoints(ep_doc)
    ep.create()

    #-The Service---------------------------------
    svc_doc = tools.create_service_doc(
        name=childs_name, namespace=namespace, spec=body["spec"])
    kopf.adopt(svc_doc)
    svc = Service(svc_doc)
    svc.create()

    #-The Ingress---------------------------------
    ing_doc = svc_doc = tools.create_ingress_doc(
        name=childs_name, namespace=namespace, spec=body["spec"])
    kopf.adopt(ing_doc)
    ing = Ingress(ing_doc)
    ing.create()

    #--------------------------
    res = {
        "Endpoints": { namespace+"/"+childs_name: str(datetime.now()) },
        "Service": { namespace+"/"+childs_name: str(datetime.now()) },
        "Ingress": { namespace+"/"+childs_name: str(datetime.now()) },
    }
    return res


#-Change the set-------------------------------------------------
@kopf.on.update('reverseproxyentrys')
def update_fn(old, new, diff, **kwargs):
    # logging.info(f"A UPDATE handler is called with body: {new}")
    # print(old, new, diff)
    # print(kwargs)

    #--------------------------
    name = kwargs["body"]["metadata"]["name"]
    namespace = kwargs["body"]["metadata"]["namespace"]
    childs_name = "rpe-"+name
    res = {}

    #--------------------------
    if old["spec"]["target"] != new["spec"]["target"]:
        ep_doc = tools.create_endpoints_doc(
            name=childs_name, namespace=namespace, spec=new["spec"])
        elm = Endpoints.get(name=childs_name, namespace=namespace)
        elm.patch(
            [{"op": "replace", "path": "/subsets", "value": ep_doc["subsets"]}],
            type="json",
        )
        res["Endpoints"] = { namespace+"/"+childs_name: str(datetime.now()) }
        
    #--------------------------
    if old["spec"]["ingress"] != new["spec"]["ingress"]:
        ing_doc = tools.create_ingress_doc(
            name=childs_name, namespace=namespace, spec=new["spec"])
        elm = Ingress.get(name=childs_name, namespace=namespace)
        elm.patch(
            [{"op": "replace", "path": "/spec", "value": ing_doc["spec"]}],
            type="json",
        )
        res["Ingress"] = { namespace+"/"+childs_name: str(datetime.now()) }
    
    #--------------------------
    return res



#-Delete the set-------------------------------------------------
@kopf.on.delete('reverseproxyentrys')
def delete_fn(body, **kwargs):
    logging.info(f"A DELETE handler is called with body: {body}")

    name = body["metadata"]["name"]
    namespace = body["metadata"]["namespace"]
    childs_name = "rpe-"+name

    for knd in [Endpoints, Service, Ingress]:
        try:
            elm = knd.get(name=childs_name, namespace=namespace)
        except:
            continue
        if "finalizers" in elm.metadata:
            elm.patch(
                [{"op": "remove", "path": "/metadata/finalizers"}],
                type="json",
            )


#-The Runner----------------------------------------------------
if __name__ == "__main__":
    from kopf.cli import main
    main()
