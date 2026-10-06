from dataclasses import dataclass


@dataclass
class ContainerStatus:
    name: str
    status: str


@dataclass
class SystemStatus:
    total: int
    running: int
    stopped: int


def get_containers_status(client):
    containers = client.containers.list(all=True)

    return [
        ContainerStatus(
            name=container.name,
            status=container.status,
        )
        for container in containers
    ]


def get_system_status(containers):
    running = sum(
        1 for container in containers
        if container.status == "running"
    )

    return SystemStatus(
        total=len(containers),
        running=running,
        stopped=len(containers) - running,
    )
