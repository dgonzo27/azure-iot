"""device-to-cloud messaging"""
import asyncio
import json
import uuid

from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message, MethodResponse
from structlog import get_logger

from .utils import upload_via_storage_blob

logger = get_logger(__name__)

MESSAGE_TIMEOUT = 10000


async def send_msg(status: str, cnx_str: str) -> None:
    """send a message to IoT Hub"""
    try:
        logger.info("IoT Hub device connecting to client...")
        client = IoTHubDeviceClient.create_from_connection_string(cnx_str)
        await client.connect()

        logger.info("IoT Hub device sending an error message...")
        message = Message(json.dumps({
            "status": f"{status}",
            "message": f"{status}-based message"
        }))
        message.message_id = uuid.uuid4()
        message.content_encoding = "utf-8"
        message.content_type = "application/json"

        logger.info("IoT Hub device adding custom filter property...")
        prop_map = message.custom_properties
        prop_map["customFilterProperty"] = "true"

        logger.info(f"sending the message: {message.data}")
        try:
            await client.send_message(message)
            logger.info("delivery successful!")
        except Exception as ex:
            logger.exception(f"exception occured: {ex}")
            logger.error("error sending message from device...")
    except Exception as iothub_error:
        logger.exception(f"exception occurred: {iothub_error}")
        logger.error("unexpected error from IoT Hub")


async def upload_file(cnx_str: str) -> None:
    """upload a file on the device to azure storage"""
    try:
        logger.info("IoT Hub device connecting to client...")
        client = IoTHubDeviceClient.create_from_connection_string(cnx_str)
        await client.connect()

        blob_name = f"quickstart-{str(uuid.uuid4())}.txt"
        storage_info = await client.get_storage_info_for_blob(blob_name)
        result = {"status_code": -1, "status_description": "N/A"}

        upload_result = await upload_via_storage_blob(storage_info, blob_name)
        if hasattr(upload_result, "error_code"):
            result = {
                "status_code": upload_result.error_code,
                "status_description": "Storage Blob Upload Error",
            }
        else:
            result = {"status_code": 200, "status_description": ""}
        
        upload_status = True if result["status_code"] == 200 else False
        await client.notify_blob_upload_status(
            storage_info["correlationId"],
            upload_status,
            result["status_code"],
            result["status_description"]
        )
        await client.shutdown()

    except Exception as iothub_error:
        logger.exception(f"exception occurred: {iothub_error}")
        logger.error("unexpected error from IoT Hub")


async def receive_msg(cnx_str: str) -> None:
    """listen for messages from IoT Hub"""
    try:
        logger.info("IoT Hub device connecting to client...")
        client = IoTHubDeviceClient.create_from_connection_string(cnx_str)
        await client.connect()

        def message_received_handler(message):
            logger.info(f"message received:\t{json.loads(message.data.decode())}")
            logger.info(f"custom properties:\t{message.custom_properties}")
            logger.info(f"content type:\t{message.content_type}")
        
        client.on_message_received = message_received_handler

        def stdin_listener():
            while True:
                selection = input("enter q and return to quit\n")
                if selection == "Q" or selection == "q":
                    logger.info("quitting...")
                    break
        
        loop = asyncio.get_running_loop()
        user_finished = loop.run_in_executor(None, stdin_listener)

        await user_finished
        await client.shutdown()
    
    except Exception as iothub_error:
        logger.exception(f"exception occurred: {iothub_error}")
        logger.error("unexpected error from IoT Hub")


async def receive_method(cnx_str: str) -> None:
    """listen for direct method requests from IoT Hub"""
    try:
        logger.info("IoT Hub device connecting to client...")
        client = IoTHubDeviceClient.create_from_connection_string(cnx_str)
        await client.connect()

        async def method_request_handler(method_request) -> None:
            if method_request.name == "method1":
                payload = {"result": True, "data": "some data"}
                status = 200
                logger.info("executed method1")
            else:
                payload = {"result": False, "data": "unknown method"}
                status = 400
                logger.error(f"executed unknown method: {method_request.name}")
            method_response = MethodResponse.create_from_method_request(method_request, status, payload)
            await client.send_method_response(method_response)

        client.on_method_request_received = method_request_handler

        def stdin_listener():
            while True:
                selection = input("enter q and return to quit\n")
                if selection == "Q" or selection == "q":
                    logger.info("quitting...")
                    break
        
        loop = asyncio.get_running_loop()
        user_finished = loop.run_in_executor(None, stdin_listener)

        await user_finished
        await client.shutdown()
    
    except Exception as iothub_error:
        logger.exception(f"exception occurred: {iothub_error}")
        logger.error("unexpected error from IoT Hub")
