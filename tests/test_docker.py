from homelab_status.docker_adapter import ContainerStatus, get_containers_status


class FakeContainer:
    def __init__(self, name, status):
        self.name = name
        self.status = status


class FakeContainerManager:
    def list(self, all=True):
        return [
            FakeContainer("immich_server", "running"),
            FakeContainer("adguardhome", "running"),
            FakeContainer("old_container", "exited"),
        ]


class FakeDockerClient:
    containers = FakeContainerManager()


def test_get_containers_status():
    result = get_containers_status(FakeDockerClient())

    assert result == [
        ContainerStatus("immich_server", "running"),
        ContainerStatus("adguardhome", "running"),
        ContainerStatus("old_container", "exited"),
    ]
