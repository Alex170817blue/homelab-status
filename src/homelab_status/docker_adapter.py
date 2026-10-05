from dataclasses import dataclass


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
