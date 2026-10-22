import importlib
import json

import pytest

from homelab_status.docker_adapter import (
    ContainerStatus,
    get_containers_status,
    get_system_status,
)


class FakeContainer:
    def __init__(self, name, status, health=None):
        self.name = name
        self.status = status
        self.attrs = {"State": {}}

        if health is not None:
            self.attrs["State"]["Health"] = {"Status": health}


class FakeContainerCollection:
    def __init__(self, containers):
        self._containers = containers

    def list(self, all=False):
        return self._containers


class FakeDockerClient:
    def __init__(self):
        self.containers = FakeContainerCollection(
            [
                FakeContainer("immich_server", "running", "healthy"),
                FakeContainer("adguardhome", "running"),
                FakeContainer("old_container", "exited"),
            ]
        )


def test_get_containers_status():
    result = get_containers_status(FakeDockerClient())

    assert result == [
        ContainerStatus("immich_server", "running", "healthy"),
        ContainerStatus("adguardhome", "running", "not-configured"),
        ContainerStatus("old_container", "exited", "not-configured"),
    ]


def test_get_system_status():
    containers = [
        ContainerStatus("immich_server", "running", "healthy"),
        ContainerStatus("adguardhome", "running", "not-configured"),
        ContainerStatus("old_container", "exited", "not-configured"),
    ]

    result = get_system_status(containers)

    assert result.total == 3
    assert result.running == 2
    assert result.stopped == 1


def test_main_json_output(monkeypatch, capsys):
    class FakeClient:
        pass

    containers = [
        ContainerStatus("immich_server", "running", "healthy"),
        ContainerStatus("adguardhome", "running", "not-configured"),
        ContainerStatus("old_container", "exited", "not-configured"),
    ]

    main_module = importlib.import_module("homelab_status.main")

    monkeypatch.setattr(main_module.docker, "from_env", lambda: FakeClient())
    monkeypatch.setattr(
        main_module,
        "get_containers_status",
        lambda client: containers,
    )

    monkeypatch.setattr(
        main_module,
        "get_system_status",
        get_system_status,
    )
    monkeypatch.setattr(
        "sys.argv",
        ["homelab-status", "--json"],
    )

    main_module.main()

    result = json.loads(capsys.readouterr().out)

    assert result["system"] == {
        "total": 3,
        "running": 2,
        "stopped": 1,
    }
    assert result["containers"] == [
        {"name": "immich_server", "status": "running", "health": "healthy"},
        {"name": "adguardhome", "status": "running", "health": "not-configured"},
        {"name": "old_container", "status": "exited", "health": "not-configured"},
    ]


def test_main_only_stopped(monkeypatch, capsys):
    class FakeClient:
        pass

    containers = [
        ContainerStatus("immich_server", "running", "healthy"),
        ContainerStatus("adguardhome", "running", "not-configured"),
        ContainerStatus("old_container", "exited", "not-configured"),
    ]

    main_module = importlib.import_module("homelab_status.main")

    monkeypatch.setattr(main_module.docker, "from_env", lambda: FakeClient())
    monkeypatch.setattr(
        main_module,
        "get_containers_status",
        lambda client: containers,
    )
    monkeypatch.setattr(
        main_module,
        "get_system_status",
        get_system_status,
    )
    monkeypatch.setattr(
        "sys.argv",
        ["homelab-status", "--only-stopped"],
    )

    main_module.main()

    output = capsys.readouterr().out

    assert "Containers: 3" in output
    assert "Running:    2" in output
    assert "Stopped:    1" in output
    assert "old_container: exited" in output
    assert "immich_server: running" not in output


def test_main_docker_error(monkeypatch, capsys):
    main_module = importlib.import_module("homelab_status.main")

    def raise_docker_error():
        raise main_module.docker.errors.DockerException("connection failed")

    monkeypatch.setattr(main_module.docker, "from_env", raise_docker_error)
    monkeypatch.setattr(
        "sys.argv",
        ["homelab-status"],
    )

    with pytest.raises(SystemExit) as exc_info:
        main_module.main()

    assert exc_info.value.code == 1

    captured = capsys.readouterr()
    assert "Unable to connect to Docker" in captured.err
    assert captured.out == ""
