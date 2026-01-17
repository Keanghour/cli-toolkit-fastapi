# cnb_cli/generators/project.py

from cnb_cli.templates.project import BASE_DIRS
from cnb_cli.templates import files, docker
from cnb_cli.utils.fs import mkdir, touch, write_file

def generate_project():
    # Create folders + __init__.py
    for d in BASE_DIRS:
        mkdir(d)
        touch(f"{d}/__init__.py")

    # Create files
    write_file("app/main.py", files.MAIN_PY)
    write_file("app/config.py", files.CONFIG_PY)
    write_file("app/utils/encryption.py", files.ENCRYPTION_PY)
    write_file("app/routers/health.py", files.HEALTH_ROUTER)

    write_file(".env", files.ENV_FILE)
    write_file("requirements.txt", files.REQUIREMENTS)
    write_file("Dockerfile", docker.DOCKERFILE)
    write_file("pip.conf", files.PIP_CONF)
