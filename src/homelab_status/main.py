import docker

from homelab_status.docker_adapter import get_containers_status


def main():
    client = docker.from_env()

    for container in get_containers_status(client):
        print(f"{container.name}: {container.status}")


if __name__ == "__main__":
    main()
