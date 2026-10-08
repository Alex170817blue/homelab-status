# homelab-status

A small Python CLI for monitoring the status of my homelab.

This project started as a learning exercise and is gradually becoming a real tool for managing and monitoring my personal homelab. I'm fighting with my cats while doing it, so it will be a slow process.

    _._     _,-'""`-._
    (,-.`._,'(       |\`-/|
        `-.-' \ )-`( , o o)
            `-    \`_`"'-

The goal is not to build a full monitoring platform, but to create a simple, useful tool while learning good software engineering practices along the way.


## Why this project?

I run a small homelab where I host several services using Docker.

Instead of jumping directly into a large monitoring stack, I wanted to build something myself from the ground up:

* interact with the Docker API
* model application data with Python
* write automated tests
* structure a Python project as a real package
* build a command-line interface
* use Git and GitHub as part of the development workflow
* eventually add CI and other software-engineering practices

The project is intentionally small so that each new feature is an opportunity to understand how and why things work.

## Current status

           .
          ":"
        ___:____     |"\/"|
      ,'        `.    \  /
      |  O        \___/  |
    ~^~^~^~^~^~^~^~^~^~^~^~^~

The application currently connects to the local Docker daemon and reports the status of all containers.

Example:

```text
Homelab status
--------------
Containers: 6
Running:    5
Stopped:    1

adguardhome: running
immich_server: running
immich_postgres: running
immich_machine_learning: running
immich_redis: running
busy_heisenberg: exited
```

The Docker interaction is separated from the CLI logic, and the project includes automated tests using `pytest`.

## Project structure

```text
homelab-status/
├── .gitignore
├── README.md
├── pyproject.toml
├── src/
│   └── homelab_status/
│       ├── __init__.py
│       ├── docker_adapter.py
│       └── main.py
└── tests/
    └── test_docker.py
```

## Technology

* Python 3.14+
* Docker SDK for Python
* pytest
* Git
* GitHub
* Docker

The project is developed directly on my homelab server and accessed remotely through VS Code Remote SSH.

## Development

⠀⠀⠀⠀⠀⠀⠀⢀⣤⣴⣶⣶⣶⣶⣶⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣾⠟⠛⢿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⣿⣄⣀⣼⣿⣿⣿⣿⣿⣿⣿⠀⢀⣀⣀⣀⡀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠉⣿⣿⣿⣿⣿⠀⢸⣿⣿⣿⣿⣦⠀
⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢸⣿⣿⣿⣿⣿⡇
⢰⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⠿⠿⠿⠋⠀⣼⣿⣿⣿⣿⣿⡇
⢸⣿⣿⣿⣿⣿⡿⠉⢀⣠⣤⣤⣤⣤⣤⣤⣤⣴⣾⣿⣿⣿⣿⣿⣿⡇
⢸⣿⣿⣿⣿⣿⡇⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀
⠘⣿⣿⣿⣿⣿⡇⠀⣿⣿⣿⣿⣿⠛⠛⠛⠛⠛⠛⠛⠛⠛⠋⠁⠀⠀
⠀⠈⠛⠻⠿⠿⠇⠀⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⣿⡇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣧⣀⣀⣿⠇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀

The project uses a Python virtual environment.

Activate it with:

```bash
source ~/venvs/homelab-status/bin/activate
```

Then enter the project directory:

```bash
cd /mnt/storage/projects/active/homelab-status
```

Run the tests:

```bash
pytest
```

Run the application:

```bash
python src/homelab_status/main.py
```

## What I am learning

This project is also a personal learning journey.

Some of the topics explored so far:

* Python project structure
* `pyproject.toml`
* virtual environments
* Python packages and imports
* dataclasses
* dependency management
* Docker API interaction
* unit testing
* fake objects for testing
* Git workflows
* GitHub
* remote development with SSH
* VS Code Remote SSH
* separating application logic from infrastructure concerns

One useful lesson already came from a seemingly simple import:

a local module named `docker.py` shadowed the external `docker` Python package.

Renaming the module to `docker_adapter.py` fixed the issue and highlighted how Python's import path and module resolution work.

## Roadmap

The project will evolve gradually.

Planned improvements include:

* [ ] Turn the script into an installable CLI
* [ ] Add a `homelab-status` command
* [ ] Add `--json` output
* [ ] Add filtering options such as `--only-stopped`
* [ ] Improve error handling
* [ ] Add more tests
* [ ] Add GitHub Actions CI
* [ ] Improve documentation
* [ ] Explore Docker health status
* [ ] Add system-level information
* [ ] Eventually contribute some of the experience gained here to an existing open-source project

The roadmap is intentionally flexible. The project is meant to grow as I learn.

## Philosophy

> Build small things, understand how they work, and improve them step by step.

This project is not intended to replace mature monitoring solutions.

It is a way to learn by building something that is actually useful in my own environment.

## License

To be decided.
