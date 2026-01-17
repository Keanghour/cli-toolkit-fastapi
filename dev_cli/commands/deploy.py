# cnb_cli/commands/deploy.py

import typer
import json
import subprocess
from rich.console import Console
from rich.prompt import Prompt, Confirm
from pathlib import Path

console = Console()

def deploy_tool():
    """Docker Deployment Tool command"""
    console.print("\n🚀 [bold cyan]Docker Deployment Tool[/bold cyan]\n")

    # Docker Image Info
    image_name = Prompt.ask("Enter the Docker image name")
    image_tag = Prompt.ask("Enter the image tag", default="latest")

    # Remote Server Info
    console.print("\n📡 Remote Server Information")
    server_host = Prompt.ask("Enter the server host (IP or domain)")
    ssh_user = Prompt.ask("Enter the SSH username")
    ssh_password = Prompt.ask("Enter the SSH password", password=True)

    # Container Config
    console.print("\n🐳 Container Configuration")
    container_name = Prompt.ask("Enter the container name")
    port = Prompt.ask("Enter the port to expose (container port 80)", default="80")
    use_sudo = Confirm.ask("Does the remote user need sudo for Docker commands?", default=True)

    # Deployment Summary
    console.print("\n📋 Deployment Summary:")
    console.print(f"  • Image: {image_name}:{image_tag}")
    console.print(f"  • Server: {ssh_user}@{server_host}")
    console.print(f"  • Container: {container_name}")
    console.print(f"  • Port: {port}:80")
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
    config_file = Path(".cnb_project_deploy.json")
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)
    console.print(f"💾 Saved project deployment configuration to [bold]{config_file}[/bold]")

    console.print("\n✅ Deployment configuration collected successfully!")
    console.print("💡 Extend this command to fully automate remote deployment using paramiko or Ansible.")
