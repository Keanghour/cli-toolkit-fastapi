# cnb_cli/commands/generate.py
import typer
import questionary
from rich.console import Console

from cnb_cli.commands.utils_generator import generate_utils
from cnb_cli.commands.consumer_generator import generate_consumer
from cnb_cli.commands.api_generator import generate_api
from cnb_cli.commands.docker_generator import generate_docker

console = Console()
app = typer.Typer(help="Component Generator 🚀")


def _generate_component():
    console.print("\n🚀 [bold cyan]Generate new component[/bold cyan]\n")

    choice = questionary.select(
        "What would you like to generate?",
        choices=[
            "API (Fast - CRUD or Simple)",
            "Consumer",
            "Utils",
            "Docker"
        ]
    ).ask()

    console.print(f"[green]✅ You selected: {choice}[/green]\n")

    if choice == "API (Fast - CRUD or Simple)":
        generate_api()
    elif choice == "Consumer":
        generate_consumer()
    elif choice == "Utils":
        # Pass the selection to utils generator
        generate_utils()
    elif choice == "Docker":
        generate_docker()
    else:
        console.print("[yellow]⚠️ Component creation not implemented[/yellow]")


def generate_menu():
    """Wrapper to maintain backward compatibility with main.py"""
    _generate_component()
