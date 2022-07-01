"""cloud-to-device messaging"""
import json

from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod
from structlog import get_logger

logger = get_logger(__name__)


def send_msg(status: str, device_id: str, cnx_str: str) -> None:
    """send a message from IoT Hub to device"""
    try:
        logger.info("IoT Hub registry manager connecting to client...")
        registry_manager = IoTHubRegistryManager.from_connection_string(cnx_str)

        message = json.dumps({
            "status": f"{status}",
            "message": f"{status}-based message"
        })
        logger.info("sending message...")
        registry_manager.send_c2d_message(device_id, message, {"contentType": "application/json"})
        registry_manager = None

    except Exception as iothub_error:
        logger.exception(f"exception occurred: {iothub_error}")
        logger.error("unexpected error from IoT Hub")


def invoke_method(method_name: str, device_id: str, cnx_str: str) -> None:
    """invoke a request method from IoT Hub to device"""
    try:
        logger.info("IoT Hub registry manager connecting to client...")
        registry_manager = IoTHubRegistryManager.from_connection_string(cnx_str)

        device_method = CloudToDeviceMethod(method_name=method_name, payload={"sample": "data"})
        registry_manager.invoke_device_method(device_id, device_method)
        registry_manager = None
    
    except Exception as iothub_error:
        logger.exception(f"exception occurred: {iothub_error}")
        logger.error("unexpected error from IoT Hub")
