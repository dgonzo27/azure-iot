import asyncio
import json
import signal
import threading

from azure.iot.device.aio import IoTHubModuleClient
from structlog import get_logger

logger = get_logger(__name__)

CNX_STR = "change_me"


stop_event = threading.Event()


def create_client() -> None:
    """listen for messages from another module or edge runtime"""
    try:
        logger.info("IoT Hub device connecting to edge client...")
        client = IoTHubModuleClient.create_from_connection_string(CNX_STR)

        async def receive_message_handler(message):
            logger.info(f"message received:\t{json.loads(message.data.decode())}")
            logger.info(f"custom properties:\t{message.custom_properties}")
            logger.info(f"content type:\t{message.content_type}")
            await client.send_message_to_output(message, "output1")
        
        try:
            client.on_message_received = receive_message_handler
        except:
            client.shutdown()
            raise

        return client
    
    except Exception as iotedge_error:
        logger.exception(f"exception occurred: {iotedge_error}")
        logger.error("unexpected error from IoT edge")


async def run_sample(client: IoTHubModuleClient) -> None:
    while True:
        await asyncio.sleep(1000)


def main():
    client = create_client()

    def module_termination_handler(signal, frame):
        logger.info("IoTHubClient sample stopped by edge")
        stop_event.set()

    signal.signal(signal.SIGTERM, module_termination_handler)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run_sample(client))
    except Exception as ex:
        logger.exception(f"exception occurred: {ex}")
        raise
    finally:
        logger.info("shutting down IoT Hub client...")
        loop.run_until_complete(client.shutdown())
        loop.close()


if __name__ == "__main__":
    main()
