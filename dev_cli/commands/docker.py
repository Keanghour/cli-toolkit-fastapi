# cnb_cli/commands/docker.py

import typer
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from pathlib import Path
import subprocess
import platform
import shlex

console = Console()
app = typer.Typer(help="Docker Build Tools 🐳")

IS_LINUX = platform.system() == "Linux"
IS_MAC = platform.system() == "Darwin"
IS_WINDOWS = platform.system() == "Windows"


# ----------------------------
# Helpers
# ----------------------------
def check_docker_installed() -> bool:
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
        return True
    except Exception:
        return False


def run_command(cmd: list[str], show_spinner: bool = True) -> bool:
    """Run a command, optionally showing a spinner during execution"""
    command_str = ' '.join(shlex.quote(c) for c in cmd)

    if show_spinner:
        with Progress(
            SpinnerColumn(),
            TextColumn("[cyan]{task.description}[/cyan]"),
            transient=True,
            console=console
        ) as progress:
            task = progress.add_task(f"$ {command_str}", start=False)
            try:
                progress.start_task(task)
                subprocess.run(cmd, check=True)
                return True
            except subprocess.CalledProcessError as e:
                console.print(f"[red]✗ Command failed[/red]")
                console.print(e)
                return False
    else:
        console.print(f"[cyan]$ {command_str}[/cyan]")
        try:
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError as e:
            console.print(f"[red]✗ Command failed[/red]")
            console.print(e)
            return False


def ensure_dockerfile(path: Path) -> Path:
    dockerfile = path / "Dockerfile"
    if not dockerfile.exists():
        console.print("[yellow]⚠️ Dockerfile not found! Creating a minimal Dockerfile...[/yellow]")
        dockerfile.write_text(
            "FROM python:3.11-slim\n"
            "WORKDIR /app\n"
            "COPY . /app\n"
            "CMD [\"python3\", \"--version\"]\n"
        )
    return dockerfile


def image_exists(image: str) -> bool:
    """Check if a Docker image exists locally"""
    result = subprocess.run(
        ["docker", "images", "-q", image],
        capture_output=True,
        text=True
    )
    return bool(result.stdout.strip())


def get_docker_service_guide() -> str:
    if IS_LINUX:
        return (
            "🛠 Docker service commands:\n"
            "• Check status:       sudo systemctl status docker\n"
            "• Start Docker:       sudo systemctl start docker\n"
            "• Stop Docker:        sudo systemctl stop docker\n"
            "• Restart Docker:     sudo systemctl restart docker\n"
        )
    elif IS_MAC:
        return (
            "🛠 Docker service info:\n"
            "• On macOS, Docker runs via Docker Desktop\n"
            "• Open Docker Desktop to start/stop the service\n"
            "• Check running containers: docker ps\n"
        )
    elif IS_WINDOWS:
        return (
            "🛠 Docker service info:\n"
            "• On Windows, Docker runs via Docker Desktop\n"
            "• Open Docker Desktop to start/stop the service\n"
            "• Check running containers: docker ps\n"
        )
    else:
        return "🛠 Docker service commands may vary on your OS"


# ----------------------------
# Build & Run Local Docker
# ----------------------------
def build_and_run_local():
    project_dir = Path.cwd()
    ensure_dockerfile(project_dir)

    image_name = questionary.text(
        "Enter Docker image name",
        default="repo_name"
    ).ask()

    tag = questionary.text(
        "Enter Docker image tag (default: latest)",
        default="latest"
    ).ask()

    host_port = questionary.text(
        "Enter host port (maps to container port 80)",
        default="8000"
    ).ask()

    full_image = f"{image_name}:{tag}"

    if not image_exists(full_image):
        console.print("\n🚀 Building Docker image...\n")
        if not run_command([
            "docker", "build",
            "-t", full_image,
            "."
        ]):
            console.print(f"[red]❌ Build failed: {full_image}[/red]")
            return
    else:
        console.print(f"[green]✅ Using existing image: {full_image}[/green]\n")

    if questionary.confirm("Run container now?", default=True).ask():
        console.print("\n▶️ Running container...\n")
        run_command([
            "docker", "run",
            "-p", f"{host_port}:80",
            full_image
        ])

    # Display guide
    console.print(Panel.fit(
        f"💡 Guide:\n"
        "1️⃣ Builds Docker image from current directory (or uses existing)\n"
        "2️⃣ Maps host port → container port 80\n"
        "3️⃣ Runs container locally\n\n"
        f"{get_docker_service_guide()}"
        "• List all containers:       docker ps -a\n"
        "• Remove container:          docker rm <container_id>\n"
        "• Remove image:              docker rmi <image_name>:<tag>\n\n"
        "Created by: Hour Zackry",
        title="Guide",
        style="yellow"
    ))


# ----------------------------
# Build & Export TAR
# ----------------------------
def build_docker_tar():
    project_dir = Path.cwd()

    image_name = questionary.text(
        "Enter the Docker image name",
        default="app_repo"
    ).ask()

    tag = questionary.text(
        "Enter the tag (default: latest)",
        default="latest"
    ).ask()

    full_image = f"{image_name}:{tag}"
    tar_file = project_dir / f"{image_name}_{tag}.tar"

    console.print("\n🚀 Exporting Docker image to tar file...")
    console.print(f"Image: {full_image}")
    console.print(f"Output: {tar_file.name}\n")

    if not image_exists(full_image):
        ensure_dockerfile(project_dir)
        console.print(f"[yellow]⚠️ Image {full_image} not found locally. Building it now...[/yellow]\n")
        if not run_command([
            "docker", "build",
            "-t", full_image,
            "."
        ]):
            console.print(f"[red]❌ Build failed: {full_image}[/red]")
            return
    else:
        console.print(f"[green]✅ Using existing image: {full_image}[/green]\n")

    if run_command([
        "docker", "save",
        "-o", str(tar_file),
        full_image
    ]):
        console.print(f"\n✅ Saving Docker image {full_image} completed successfully!\n")
        console.print("✨ Docker image saved successfully!\n")
        console.print("📁 File created:")
        console.print(f"  • {tar_file.name}\n")
        console.print("💡 Next steps:")
        console.print(f"  1. Transfer the tar file to another machine")
        console.print(f"  2. Load it with: docker load -i {tar_file.name}")
        console.print(f"  3. Run it with: docker run {full_image}\n")
        console.print("Created by: Hour Zackry")


# ----------------------------
# Menu
# ----------------------------
def docker_menu():
    console.print("\n🐳 [bold cyan]Docker Build Tools[/bold cyan]\n")

    if not check_docker_installed():
        console.print("[red]❌ Docker is not installed or not running[/red]")
        return

    choice = questionary.select(
        "What would you like to do?",
        choices=[
            "Build and Run Local Docker",
            "Build Docker Image as Tar",
            "Exit"
        ]
    ).ask()

    if choice == "Build and Run Local Docker":
        build_and_run_local()
    elif choice == "Build Docker Image as Tar":
        build_docker_tar()
    else:
        console.print("[green]✅ Exiting Docker menu[/green]")
        return

