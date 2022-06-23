"""utility functions"""
import os
import uuid

from typing import Any, Dict

from azure.storage.blob import BlobClient
from structlog import get_logger

logger = get_logger(__name__)


async def upload_via_storage_blob(blob_info: Dict[str, Any], local_file_name: str) -> Dict[str, Any]:
    """helper function to perform upload"""
    logger.info("upload_via_storage_blob")
    sas_url = "https://{}/{}/{}{}".format(
        blob_info["hostName"],
        blob_info["containerName"],
        blob_info["blobName"],
        blob_info["sasToken"],
    )
    blob_client = BlobClient.from_blob_url(sas_url)

    local_file_name = f"files/{local_file_name}"
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), local_file_name)

    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    
    with open(filename, "w") as file:
        file.write("Hello, World!")
    
    logger.info(f"uploading to azure storage as blob: {local_file_name}")
    with open(filename, "rb") as data:
        result = blob_client.upload_blob(data)
    
    return result
