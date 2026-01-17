# cnb_cli/commands/docker.py

import typer
import questionary
from rich.console import Console
from rich.panel import Panel
import subprocess

console = Console()
app = typer.Typer(help="Docker Build Tools 🐳")

def check_docker_installed() -> bool:
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def run_command(cmd: list[str]) -> bool:
    console.print(f"$ {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"[red]✗ Command failed: {' '.join(cmd)}[/red]")
        console.print(f"[red]{e}[/red]")
        return False

def build_and_run_local():
    image_name = questionary.text("Enter the Docker image name", default="cnb_app").ask()
    host_port = questionary.text("Enter the port to map to container's port 80", default="8000").ask()

    console.print(f"\n🚀 Building and running Docker container...\nImage: {image_name}\nPort: {host_port}:80\n")
    console.print("Step 1: Building Docker image...")
    if not run_command(["docker", "build", "--no-cache", "-t", image_name, "."]):
        console.print(f"❌ Docker build failed: {image_name}")
        return

    if questionary.confirm("Do you want to run this container now?").ask():
        console.print("Step 2: Running Docker container...")
        if not run_command(["docker", "run", "-p", f"{host_port}:80", image_name]):
            console.print(f"❌ Docker run failed: {image_name}")
        else:
            console.print(f"[green]✅ Container is running on port {host_port}[/green]")

def build_docker_tar():
    image_name = questionary.text("Enter the Docker image name", default="cnb_app").ask()
    tag = questionary.text("Enter the tag", default="latest").ask()
    tar_file = questionary.text("Enter the tar filename", default=f"{image_name}.tar").ask()

    console.print(f"\n🚀 Exporting Docker image to tar file...\nImage: {image_name}:{tag}\nOutput: {tar_file}\n")
    console.print("Step 1: Building Docker image...")
    if not run_command(["docker", "build", "--no-cache", "-t", f"{image_name}:{tag}", "."]):
        console.print(f"❌ Docker build failed: {image_name}:{tag}")
        return

    console.print("Step 2: Saving Docker image to tar file...")
    if not run_command(["docker", "save", "-o", tar_file, f"{image_name}:{tag}"]):
        console.print(f"❌ Docker save failed: {image_name}:{tag}")
    else:
        console.print(f"[green]✅ Image saved as {tar_file}![/green]")

def docker_menu():
    console.print("\n🐳 [bold cyan]Docker Build Tools[/bold cyan]\n")
    choice = questionary.select(
        "What would you like to do?",
        choices=[
            "Build and Run Local Docker",
            "Build Docker Image as Tar"
        ]
    ).ask()

    if not check_docker_installed():
        console.print("[red]❌ Docker CLI not found! Please install Docker first.[/red]")
        return

    if choice == "Build and Run Local Docker":
        build_and_run_local()
        console.print(Panel.fit(
            "💡 Guide:\n"
            "1️⃣ Builds your Docker image locally.\n"
            "2️⃣ Maps host port → container port 80.\n"
            "3️⃣ Optionally runs the container after building.",
            title="Guide", style="yellow"
        ))
    else:
        build_docker_tar()
        console.print(Panel.fit(
            "💡 Guide:\n"
            "1️⃣ Builds your Docker image locally.\n"
            "2️⃣ Saves it as a tar file for deployment.\n"
            "3️⃣ Can be loaded on other systems with `docker load -i <file>.tar`.",
            title="Guide", style="yellow"
        ))
