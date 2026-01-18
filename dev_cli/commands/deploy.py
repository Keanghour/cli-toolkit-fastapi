# cnb_cli/commands/deploy.py

import typer
import json
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.spinner import Spinner
import time

console = Console()
CONFIG_FILE = Path(".project_deploy.json")


def load_config():
    """Load existing deployment config if available"""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_config(config: dict):
    """Save deployment config"""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
    console.print(f"💾 Saved deployment configuration to [bold]{CONFIG_FILE}[/bold]")


def deploy_tool():
    """Dynamic Docker Deployment Tool"""
    console.print("\n🚀 [bold cyan]Docker Deployment Tool[/bold cyan]\n")
    console.print("💡 You can press Enter to accept the default value in brackets.\n")

    # Load previous config if exists
    old_config = load_config()

    # Docker Image Info
    image_name = Prompt.ask(
        "Enter Docker image name",
        default=old_config.get("image_name", "my_app")
    )
    image_tag = Prompt.ask(
        "Enter image tag",
        default=old_config.get("image_tag", "latest")
    )

    # Remote Server Info
    console.print("\n📡 Remote Server Information")
    server_host = Prompt.ask(
        "Enter server host (IP or domain)",
        default=old_config.get("server_host", "192.168.0.100")
    )
    ssh_user = Prompt.ask(
        "Enter SSH username",
        default=old_config.get("ssh_user", "root")
    )
    ssh_password = Prompt.ask(
        "Enter SSH password",
        password=True,
        default=old_config.get("ssh_password", "")
    )

    # Container Config
    console.print("\n🐳 Container Configuration")
    container_name = Prompt.ask(
        "Enter container name",
        default=old_config.get("container_name", "my_app_container")
    )
    port = Prompt.ask(
        "Enter host port mapping to container port 80",
        default=old_config.get("port", "8000")
    )
    use_sudo = Confirm.ask(
        "Does the remote user need sudo for Docker commands?",
        default=old_config.get("use_sudo", True)
    )

    # Deployment Summary
    console.print("\n📋 Deployment Summary:")
    console.print(f"  • Image: {image_name}:{image_tag}")
    console.print(f"  • Server: {ssh_user}@{server_host}")
    console.print(f"  • Container: {container_name}")
    console.print(f"  • Port mapping: {port}:80")
    console.print(f"  • Use sudo: {'Yes' if use_sudo else 'No'}")

    if not Confirm.ask("Proceed with deployment?", default=True):
        console.print("[yellow]Deployment canceled[/yellow]")
        raise typer.Exit()

    # Save config for future use
    config = {
        "image_name": image_name,
        "image_tag": image_tag,
        "server_host": server_host,
        "ssh_user": ssh_user,
        "ssh_password": ssh_password,
        "container_name": container_name,
        "port": port,
        "use_sudo": use_sudo
    }

    # Spinner animation for saving
    with console.status("⠹ Saving deployment configuration...", spinner="dots"):
        time.sleep(1)
        save_config(config)

    console.print("\n✅ Deployment configuration collected successfully!")
    console.print(
        "💡 You can extend this command to automate remote deployment with Paramiko or Ansible."
    )
