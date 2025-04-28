import sys
import logging
from traceback import print_exc

sys.path.append('/app')
sys.path.append('app')

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

import cfg
from api import Routers


app = FastAPI(title=cfg.title, 
              description=cfg.desc, 
              docs_url=cfg.docs, 
              openapi_url=f"{cfg.api}/openapi.json")
Routers(app)
   
@app.exception_handler(Exception)
async def catch_exceptions(request, exc):
    if cfg.debug:
        print_exc()
    logging.error(f"Exception occurred: {exc}")
    return PlainTextResponse(str(exc), status_code=500)
