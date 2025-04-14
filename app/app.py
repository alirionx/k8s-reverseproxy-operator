from fastapi import FastAPI, Request, HTTPException #, Depends, Header, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi import status as HTTPStatus
from starlette.responses import Response

# from typing import Annotated

from settings import settings
from models import ReverseProxyEntry, ReverseProxyEntrySpec
import app_tools



#-Build and prep the App--------------------------------------------
tags_metadata = [
  {
    "name": "api-root",
    "description": "API State and testing",
  },
  {
    "name": "api-crud",
    "description": "Rest API for k8s-reverseproxy-operator CRUD",
  }
]

app = FastAPI(openapi_tags=tags_metadata)

#-Custom Middleware Functions----------------------------------------
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_methods=["*"],
  allow_headers=["*"],
  allow_credentials=True
) 


#-------------------
@app.middleware("http")
async def deschd_middle(request: Request, call_next):
    
    # import random
    # num = random.randint(1, 100)
    # if num % 2 == 0:
    #     return Response(f"401 Unauthorized - Darfst Du nich weil wegen {num}", status_code=401)


    response = await call_next(request)
    return response


#-------------------
@app.get("/api", tags=["api-root"], response_model=dict)
async def api_root():
    return {"message": "Hello from the k8s-reverseproxy-operator"}

#-------------------
@app.post("/api/reverse-proxy-entries", 
         tags=["api-crud"], response_model=ReverseProxyEntry)
async def api_rpes_post(item:ReverseProxyEntry):
    try:
      app_tools.create_rpe(item=item)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return item

#-------------------
@app.get("/api/reverse-proxy-entries", 
         tags=["api-crud"], response_model=list[ReverseProxyEntry])
async def api_rpes_get():
    rpes = app_tools.get_rpes()
    return rpes

#-------------------
@app.get("/api/reverse-proxy-entries/{namespace}/{name}", 
         tags=["api-crud"], response_model=ReverseProxyEntry)
async def api_rpe_get(namespace:str, name:str):
    try:
      item = app_tools.get_rpe_by_name(name=name, namespace=namespace)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return item

#-------------------
@app.put("/api/reverse-proxy-entries/{namespace}/{name}", 
         tags=["api-crud"], response_model=ReverseProxyEntry)
def api_rpe_put(namespace:str, name:str, item:ReverseProxyEntrySpec):
    try:
      res = app_tools.update_rpe(name=name, namespace=namespace, item=item)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return res

#-------------------
@app.delete("/api/reverse-proxy-entries/{namespace}/{name}", 
         tags=["api-crud"], response_model=None)
async def api_rpe_delete(namespace:str, name:str):
    try:
      app_tools.delete_rpe(name=name, namespace=namespace)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

#-------------------


#-------------------



#-The Runner--------------------------------------------------------
if __name__ == "__main__":
    #check api access and operator installed
    app_tools.get_rpes()

    #start app in desired mode
    import uvicorn
    if settings.app_mode == "dev":
        print("=> API Mode is: DEV")
        uvicorn.run(app="__main__:app", host="0.0.0.0", port=settings.app_port, reload=True)
    else:
        print("=> API Mode is: PROD")
        uvicorn.run(app="__main__:app", host="0.0.0.0", port=settings.app_port)

  
#-------------------------------------------------------------------