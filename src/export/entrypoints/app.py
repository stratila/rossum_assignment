import sys
import logging

from fastapi import FastAPI, Depends, Query
from fastapi.responses import Response, JSONResponse

from export.entrypoints.security import basic_auth
from export.service.services import post_transformed_annotation, transform_annotation


from export.service.services import rossum_api  # TODO remove

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
def export_endpoint(
    queue_id: int = Query(...),
    annotation_id: int = Query(...),
):
    try:
        req_id_url = post_transformed_annotation(queue_id, annotation_id)
        return JSONResponse(
            content={"success": True}, headers={"X-Postbin-Request-Url": req_id_url}
        )
    except Exception as e:
        logger.error(f"Error occured: {e}")
        return JSONResponse(content={"success": False}, status_code=400)


@app.get("/transform-inter", dependencies=[Depends(basic_auth)])
def transform_inter(
    queue_id: int | None = Query(default=None),
    annotation_id: int | None = Query(default=None),
):
    xml_bytes = transform_annotation(queue_id, annotation_id)

    return Response(content=xml_bytes, media_type="application/xml")


@app.get("/source-xml", dependencies=[Depends(basic_auth)])
def soource_xml(
    queue_id: int | None = Query(default=None),
    annotation_id: int | None = Query(default=None),
):

    source_xml = rossum_api.queue_export(queue_id, annotation_id)

    return Response(content=source_xml, media_type="application/xml")
