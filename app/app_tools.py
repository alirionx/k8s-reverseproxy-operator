from fastapi import HTTPException
import kr8s
from kr8s.objects import new_class

from models import ReverseProxyEntry, ReverseProxyEntrySpec

#-------------------
RPE = new_class(
    kind="ReverseProxyEntry",
    version="app-scape.dev/v1",
    namespaced=True,
)
    

#-------------------
def create_rpe(item:ReverseProxyEntry):
    rpe = RPE(item.model_dump())
    rpe.create()

#-------------------
def list_rpes_names(namespace:str) -> list[str]:
    rpes = kr8s.get("reverseproxyentrys", namespace=namespace) 
    res = [ item["metadata"]["name"] for item in rpes]
    return res

#-------------------
def get_rpes() -> list[ReverseProxyEntry]:
    rpes = list(kr8s.get("reverseproxyentrys", namespace=kr8s.ALL))
    res = [ ReverseProxyEntry(**item) for item in rpes ]
    return res

#-------------------
def get_rpe_by_name(name:str, namespace:str) -> ReverseProxyEntry:
    rpe = RPE.get(name=name, namespace=namespace)
    res = ReverseProxyEntry(**rpe)
    return res

#-------------------
def update_rpe(name:str, namespace:str, item:ReverseProxyEntrySpec) -> ReverseProxyEntry:
    rpe = RPE.get(name=name, namespace=namespace)
    rpe.patch(
        patch= {
            "spec": item.model_dump()
        }
    )
    res = ReverseProxyEntry(**rpe)
    return res

#-------------------
def delete_rpe(name:str, namespace:str):
    rpe = RPE.get(name=name, namespace=namespace)
    rpe.delete()


#-------------------


#-------------------