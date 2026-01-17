# cnb_cli/commands/generate.py
import typer
import questionary
from rich.console import Console

console = Console()
app = typer.Typer(help="Component Generator 🚀")

def generate_menu():
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

    console.print(f"[green]✅ You selected: {choice}[/green]")
    console.print("[yellow]⚠️ Component creation not fully implemented[/yellow]")
