import docker

from homelab_status.docker_adapter import (
    get_containers_status,
    get_system_status,
)


def main():
    client = docker.from_env()

    containers = get_containers_status(client)
    system_status = get_system_status(containers)

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
