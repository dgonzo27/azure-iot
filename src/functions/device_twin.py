"""device twin twin management"""
import asyncio

from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import Twin, TwinProperties
from structlog import get_logger

logger = get_logger(__name__)


def patch_device(device_id: str, cnx_str: str) -> None:
    """update device twin tags and properties"""
    try:
        logger.info("IoT Hub registry manager connecting to client...")
        registry_manager = IoTHubRegistryManager.from_connection_string(cnx_str)
        device_twin = registry_manager.get_twin(device_id)
        if not device_twin:
            logger.error(f"device with id ({device_id}) was not found...")
            return

        patch = Twin()
        patch.properties = TwinProperties(desired={"FPS": 60})
        patch.tags = {"location": {"country": "United States", "city": "Houston", "state": "Texas"}}
     
        registry_manager.update_twin(device_id, patch, device_twin.etag)
        logger.info("device patched successfully!")

    except Exception as iothub_error:
        logger.exception(f"exception occurred: {iothub_error}")
        logger.error("unexpected error from IoT Hub")


async def receive_patch(cnx_str: str) -> None:
    """listen for updates to the desired properties of the device twin"""
    try:
        logger.info("IoT Hub device connecting to client...")
        client = IoTHubDeviceClient.create_from_connection_string(cnx_str)
        await client.connect()

        def twin_patch_handler(patch):
            logger.info(f"data patch: {patch}")
        
        client.on_twin_desired_properties_patch_received = twin_patch_handler

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
