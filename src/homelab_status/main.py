from dataclasses import dataclass

import docker


@dataclass
class ContainerStatus:
    name: str
    status: str


def get_containers_status(client):
    containers = client.containers.list(all=True)

    return [
        ContainerStatus(
            name=container.name,
            status=container.status,
        )
        for container in containers
    ]


def main():
    client = docker.from_env()

    for container in get_containers_status(client):
        print(f"{container.name}: {container.status}")


if __name__ == "__main__":
    main()
