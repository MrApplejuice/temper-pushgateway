import time
import argparse

from temperusb import temper
import prometheus_client as prom

from prometheus_client.exposition import basic_auth_handler

def user_auth_handler(username, password):
    
    def handler(url, method, timeout, headers, data):
        return basic_auth_handler(url, method, timeout, headers, data, username, password)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Record temperature metrics from temper temperature monitor')
    parser.add_argument(
        'room',
        type=str,
        help='The room name to record metrics for.'
    )
    parser.add_argument(
        'server',
        type=str,
        help='The server to push metrics to.'
    )
    parser.add_argument(
        '--username',
        type=str,
        default="",
        help='The authentication username to use - will not use authentication if not specified'
    )
    parser.add_argument(
        '--password',
        type=str,
        default="",
        help='The password to use for authentication. Will default to empty-password.'
    )

    args = parser.parse_args()
        
    while True:
        handler = temper.TemperHandler()
        devices = handler.get_devices()

        registry = prom.CollectorRegistry()
        gauge = prom.Gauge("room_temp", "Room temperature per room", labelnames=("room", "index"), registry=registry)
        for device_i, device in enumerate(devices):
            print(f"Temperature device {device_i + 1}: {device.get_temperatures()[0]['temperature_c']}")
            gauge.labels(room=args.room, index=device_i).set(device.get_temperatures()[0]['temperature_c'])
        prom.push_to_gateway(
            args.server,
            job=f"room_temp_{args.room}",
            registry=registry,
            handler=user_auth_handler(args.username, args.password) if args.username else basic_auth_handler
        )
        time.sleep(5)

