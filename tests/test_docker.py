from homelab_status.docker_adapter import (
    ContainerStatus,
    SystemStatus,
    get_containers_status,
    get_system_status,
)
import json
import importlib
import pytest
main_module = importlib.import_module("homelab_status.main")

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


def test_get_system_status():
    containers = [
        ContainerStatus("immich_server", "running"),
        ContainerStatus("adguardhome", "running"),
        ContainerStatus("old_container", "exited"),
    ]

    result = get_system_status(containers)

    assert result == SystemStatus(
        total=3,
        running=2,
        stopped=1,
    )

def test_main_json_output(monkeypatch, capsys):
    class FakeClient:
        pass
    
    containers = [
        ContainerStatus("immich_server", "running"),
        ContainerStatus("adguardhome", "running"),
        ContainerStatus("old_container", "exited"),
    ]

    monkeypatch.setattr(main_module.docker, "from_env", lambda: FakeClient())
    monkeypatch.setattr(main_module, "get_containers_status", lambda client: containers)
    monkeypatch.setattr("sys.argv", ["main.py", "--json"]),

    main_module.main()

    output = capsys.readouterr().out
    result = json.loads(output)

    assert result["system"] == {
        "total": 3,
        "running": 2,
        "stopped": 1,
    }

    assert result["containers"] == [
        {"name": "immich_server", "status": "running"},
        {"name": "adguardhome", "status": "running"},
        {"name": "old_container", "status": "exited"},
    ]

def test_main_only_stopped(monkeypatch, capsys):
    class FakeClient:
        pass

    containers = [
        ContainerStatus("immich_server", "running"),
        ContainerStatus("adguardhome", "running"),
        ContainerStatus("old_container", "exited"),
    ]

    monkeypatch.setattr(
        main_module.docker,
        "from_env",
        lambda: FakeClient(),
    )
    monkeypatch.setattr(
        main_module,
        "get_containers_status",
        lambda client: containers,
    )
    monkeypatch.setattr(
        "sys.argv",
        ["homelab-status", "--only-stopped"],
    )

    main_module.main()

    output = capsys.readouterr().out

    assert "old_container: exited" in output
    assert "immich_server: running" not in output
    assert "adguardhome: running" not in output

import pytest

def test_main_docker_error(monkeypatch, capsys):
    def raise_docker_error():
       raise main_module.docker.errors.DockerException("Docker is not running")
    
    monkeypatch.setattr(main_module.docker, "from_env", raise_docker_error)
    monkeypatch.setattr("sys.argv", ["homelab-status"])

    with pytest.raises(SystemExit) as excinfo:
        main_module.main()
    
    assert excinfo.value.code == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert "Unable to connect to Docker" in captured.err