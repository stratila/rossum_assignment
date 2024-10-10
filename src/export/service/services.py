import re
import io
import xml.etree.ElementTree as ET
import base64
from datetime import datetime
from export.settings import settings
from export.clients.api.rossum import ApiClient as RossumApiClient
from export.clients.api.postbin import ApiClient as PostBinClient
from export.service.transformer import XMLTransformer

import requests  # TO change


rossum_api = RossumApiClient(
    username=settings.rossum_api_email,
    password=settings.rossum_api_password,
    custom_domain=settings.rossum_api_custom_domain,
)


postbin_api = PostBinClient()


def post_transformed_annotation(queue_id, annotation_id):

    # API CALL 1
    source_xml = rossum_api.queue_export(queue_id, annotation_id)
    target_xml = XMLTransformer(source_xml).transform()
    target_xml_b64 = base64.b64encode(target_xml).decode("utf-8")

    # API CALL 2
    req_id = postbin_api.post_data(
        requests, method="POST", json={"content": target_xml_b64}
    )

    return req_id


def transform_annotation(queue_id, annotation_id):
    source_xml = rossum_api.queue_export(queue_id, annotation_id)
    target_xml = XMLTransformer(source_xml)
    return target_xml.transform()
