# azure-iot

This repository contains command line apps, functions and containers for various Azure IoT services and scenarios.

1. device simulator

    **device_simulator** is a pythonic CLI application for interacting with and simulating various event from IoT Hub and IoT Hub Devices.  It requires an existing IoT Hub instance, along with a device and custom routes.  Additionally, it requires a storage account for storing routed messages and files.

2. edge simulator

    **edge_simulator** contains dockerized python modules to simulate custom modules on an IoT Edge Device.  It requires an existing IoT Hub instance, along with an edge device.

## table of contents

- [getting started with device simulator](#getting-started-with-device-simulator)
- [getting started with edge simulator](#getting-started-with-edge-simulator)

## getting started with device simulator

![device simulator cli](/docs/device_simulator_cli.png)

1. create a virtual environment:

    ```sh
    cd device_simulator

    python3 -m venv .venv

    source .venv/bin/activate

    python3 -m pip install --upgrade pip

    pip install -r requirements.txt
    ```

2. update the `src/main.py` file with your connection strings:

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

## getting started with edge simulator

1. navigate into the receive_msg_module:

    ```sh
    cd edge_simulator/receive_msg_module
    ```

2. update the `src/main.py` with your connection string:

    ```python
    CNX_STR = "change_me"
    ```

3. build the docker container:

    ```sh
    docker build -t receive_msg_module:latest .
    ```

4. run the docker container:

    ```sh
    docker run -p 5000:5000 receive_msg_module:latest
    ```
