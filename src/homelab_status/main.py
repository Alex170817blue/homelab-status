import argparse
import json
import sys

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
    parser.add_argument(
        "--only-stopped",
        action="store_true",
        help="Only show stopped containers",
    )

    args = parser.parse_args()

    try:
        client = docker.from_env()
        containers = get_containers_status(client)
        system_status = get_system_status(containers)
    except docker.errors.DockerException:
        print("Error: Unable to connect to Docker. Is the Docker daemon running?", file=sys.stderr)
        sys.exit(1)
   
    if args.only_stopped:
        containers = [c for c in containers if c.status != "running"]

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
                    "health": container.health,
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
        print(f"{container.name}: {container.status}",
              f"(health: {container.health})")

if __name__ == "__main__":
    main()
