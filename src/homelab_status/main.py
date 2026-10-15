import argparse
import json

import docker

from homelab_status.docker_adapter import (
    get_containers_status,
    get_system_status,
)


def main():
    parser = argparse.ArgumentParser(
        description="Show the status of your homelab Docker containers."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output status as JSON",
    )
    args = parser.parse_args()

    client = docker.from_env()

    containers = get_containers_status(client)
    system_status = get_system_status(containers)

    if args.json:
        result = {
            "system": {
                "total": system_status.total,
                "running": system_status.running,
                "stopped": system_status.stopped,
            },
            "containers": [
                {
                    "name": container.name,
                    "status": container.status,
                }

                for container in containers
            ],
        }
        print(json.dumps(result, indent=2))
        return

    print("Homelab status")
    print("--------------")
    print(f"Containers: {system_status.total}")
    print(f"Running:    {system_status.running}")
    print(f"Stopped:    {system_status.stopped}")
    print()

    for container in containers:
        print(f"{container.name}: {container.status}")


if __name__ == "__main__":
    main()
