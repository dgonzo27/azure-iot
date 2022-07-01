import asyncio

import click
import structlog

import functions.c2d as c2d
import functions.d2c as d2c
import functions.device_twin as device_twin

logger = structlog.get_logger(__name__)

DEVICE_CNX_STR="change_me"
SERVICE_CNX_STR="change_me"


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def cli() -> None:
    pass


@cli.command("device_to_cloud_msg", short_help="Simulate an IoT D2C message.")
@click.option("--status", prompt="message status", help="error or success")
def device_to_cloud_msg(status: str) -> None:
    logger.info(f"device_to_cloud_msg triggered with status: {status}")
    accepted_statuses = ["error", "success"]
    if status not in accepted_statuses:
        logger.error(f"{status} is not an acceptable status, please use error or success")
        return
    asyncio.run(d2c.send_msg(status, DEVICE_CNX_STR))


@cli.command("file_to_cloud", short_help="Simulate an IoT D2C file upload.")
def file_to_cloud() -> None:
    logger.info("file_to_cloud triggered")
    asyncio.run(d2c.upload_file(DEVICE_CNX_STR))


@cli.command("cloud_to_device_method", short_help="Simulate an IoT C2D method.")
@click.option("--method_name", prompt="method name", help="method1")
@click.option("--device_id", prompt="device id", help="azure id/name for device")
def cloud_to_device_method(method_name: str, device_id: str) -> None:
    logger.info(f"cloud_to_device_method triggered for method: {method_name}")
    c2d.invoke_method(method_name, device_id, SERVICE_CNX_STR)


@cli.command("cloud_to_device_msg", short_help="Simulate an IoT C2D message.")
@click.option("--status", prompt="message status", help="error or success")
@click.option("--device_id", prompt="device id", help="azure id/name for device")
def cloud_to_device_msg(status: str, device_id: str) -> None:
    logger.info(f"cloud_to_device_msg triggered with status: {status}")
    accepted_statuses = ["error", "success"]
    if status not in accepted_statuses:
        logger.error(f"{status} is not an acceptable status, please use error or success")
        return
    c2d.send_msg(status, device_id, SERVICE_CNX_STR)


@cli.command("listen_for_cloud_method", short_help="Simulate a device listener for an IoT C2D method.")
def listen_for_cloud_method() -> None:
    logger.info("listen_for_cloud_method triggered")
    asyncio.run(d2c.receive_method(DEVICE_CNX_STR))


@cli.command("listen_for_cloud_msg", short_help="Simulate a device listener for an IoT C2D message.")
def listen_for_cloud_msg() -> None:
    logger.info("listen_for_cloud_msg triggered")
    asyncio.run(d2c.receive_msg(DEVICE_CNX_STR))


@cli.command("patch_device_twin", short_help="Simulate patching a device twin.")
@click.option("--device_id", prompt="device id", help="azure id/name for device")
def patch_device_twin(device_id: str) -> None:
    logger.info(f"patch_device_twin triggered for device: {device_id}")
    device_twin.patch_device(device_id, SERVICE_CNX_STR)


@cli.command("listen_for_patch", short_help="Simulate a device listener for device twin patches.")
def listen_for_patch() -> None:
    logger.info("listen_for_patch triggered")
    asyncio.run(device_twin.receive_patch(DEVICE_CNX_STR))


if __name__ == "__main__":
    cli()
