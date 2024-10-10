import sys
import logging
import traceback

from fastapi import FastAPI, Depends, Query
from fastapi.responses import JSONResponse

from export.entrypoints.security import basic_auth
from export.service.services import post_transformed_annotation


app = FastAPI()


console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)

logger = logging.getLogger(__name__)
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)


@app.get("/export", dependencies=[Depends(basic_auth)])
async def export_endpoint(
    queue_id: int = Query(...),
    annotation_id: int = Query(...),
):
    try:
        req_id_url = await post_transformed_annotation(queue_id, annotation_id)
        return JSONResponse(
            content={"success": True}, headers={"X-Postbin-Request-Url": req_id_url}
        )
    except Exception as e:
        logger.error(f"Exception {e} occurred:")
        traceback.print_exc()
        return JSONResponse(content={"success": False}, status_code=400)
