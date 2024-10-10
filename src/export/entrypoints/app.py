from fastapi import FastAPI, Depends, Query
from fastapi.responses import Response

from export.entrypoints.security import basic_auth
from export.service.services import post_transformed_annotation, transform_annotation


app = FastAPI()

from export.service.services import rossum_api


# TODO add service err handler


@app.get("/export", dependencies=[Depends(basic_auth)])
def export_endpoint(
    queue_id: int | None = Query(default=None),
    annotation_id: int | None = Query(default=None),
):
    req_id = post_transformed_annotation(queue_id, annotation_id)
    return {"success": True, "req_id": req_id}


# TEMP


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
