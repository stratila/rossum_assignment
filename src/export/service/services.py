import base64
from export.settings import settings
from export.clients.api.rossum import ApiClient as RossumApiClient
from export.clients.api.postbin import ApiClient as PostBinClient
from export.service.transformer import XMLTransformer

import aiohttp

rossum_api = RossumApiClient(
    username=settings.rossum_api_email,
    password=settings.rossum_api_password,
    custom_domain=settings.rossum_api_custom_domain,
)


postbin_api = PostBinClient()


async def post_transformed_annotation(queue_id, annotation_id):
    async with aiohttp.ClientSession() as session:
        rossum_api.set_client_session(session)
        postbin_api.set_client_session(session)

        # Get source XML
        source_xml = await rossum_api.queue_export(queue_id, annotation_id)

        # Transform the source XML to the target format
        target_xml = XMLTransformer(source_xml).transform()
        target_xml_b64 = base64.b64encode(target_xml).decode("utf-8")

        # Post target XML to the Postbin
        req_id_url = await postbin_api.post_data(
            method="POST", json={"content": target_xml_b64}
        )

        return req_id_url
