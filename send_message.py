import os
import json
import time
import random
from datetime import datetime, timezone

from dotenv import load_dotenv
from azure.iot.device import IoTHubDeviceClient, Message

load_dotenv()

CONNECTION_STRING = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")
MSG_COUNT = 21
MSG_INTERVAL_SEC = 1


def build_message(index: int) -> Message:
    """Build a dummy telemetry message."""
    body = {
        "messageId": index,
        "deviceId": "myDevice01",
        "temperature": round(random.uniform(20.0, 35.0), 2),
        "humidity": round(random.uniform(30.0, 80.0), 2),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    msg = Message(json.dumps(body))
    msg.content_type = "application/json"
    msg.content_encoding = "utf-8"
    msg.custom_properties["source"] = "python-client"
    return msg


def main():
    if not CONNECTION_STRING:
        raise SystemExit(
            "Set IOTHUB_DEVICE_CONNECTION_STRING in .env or as an env var."
        )

    print("Connecting to IoT Hub...")
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    client.connect()
    print("Connected!\n")

    try:
        for i in range(1, MSG_COUNT + 1):
            msg = build_message(i)
            client.send_message(msg)
            print(f"[{i}/{MSG_COUNT}] Sent: {msg.data}")
            time.sleep(MSG_INTERVAL_SEC)
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        client.disconnect()
        print("Disconnected from IoT Hub.")


if __name__ == "__main__":
    main()
