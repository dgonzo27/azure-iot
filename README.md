# azure-iot

This repository contains a pythonic CLI application for interacting with and simulating various events from IoT Hub and IoT Hub Devices.  It requires an existing IoT Hub instance, along with a device and custom routes.  Additionally, it requires a storage account for storing messages and files.

## getting started

1. create a virtual environment:

    ```sh

    python3 -m venv .venv

    source .venv/bin/activate

    python3 -m pip install --upgrade pip

    pip install -r requirements.txt
    ```

2. update the `main.py` file with your connection strings:

    ```python
    DEVICE_CNX_STR="change_me"
    SERVICE_CNX_STR="change_me"
    ```

3. run the CLI for help about available commands:

    ```sh
    python3 src/main.py # OR

    python3 src/main.py -h # OR

    python3 src/main.py --help
    ```
