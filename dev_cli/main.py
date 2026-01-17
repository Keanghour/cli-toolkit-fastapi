import typer
from xxx_cli.commands.init import init_project
from xxx_cli.commands.encrypt import encrypt_menu
from xxx_cli.commands.docker import docker_menu
from xxx_cli.commands.deploy import deploy_tool
from xxx_cli.commands.generate import generate_menu
from xxx_cli.commands.request import request_menu

from xxx_cli.commands.pip_guide import PIP_GUIDE

from rich.console import Console
from rich.markup import escape

app = typer.Typer(help="xxx CLI 🚀")

console = Console()

# ----------------------------
# Callback for --helper or no command
# ----------------------------
@app.callback(invoke_without_command=True)
def main(ctx: typer.Context, helper: bool = typer.Option(False, "--helper", help="Show help message")):
    """
    xxx CLI: FastAPI project helper, encryption, Docker, request management
    """
    if helper or ctx.invoked_subcommand is None:
        typer.echo(app.get_help(ctx))
        raise typer.Exit()

# ----------------------------
# CLI Commands
# ----------------------------

@app.command("i")
def i():
    """[bold green]xxx i[/bold green] – Initialize a new FastAPI project ⚡"""
    init_project()

@app.command("init")
def init():
    """[bold green]xxx init[/bold green] – Initialize a new FastAPI project ⚡"""
    init_project()

@app.command("e")
def e():
    """[bold yellow]xxx e[/bold yellow] – Encryption Tools 🔐"""
    encrypt_menu()

@app.command("b")
def b():
    """[bold blue]xxx b[/bold blue] – Docker Build Tools 🐳"""
    docker_menu()

@app.command("d")
def d():
    """[bold magenta]xxx d[/bold magenta] – Docker Deployment Tool 🚀"""
    deploy_tool()

@app.command("g")
def g():
    """[bold cyan]xxx g[/bold cyan] – Component Generator 🛠️"""
    generate_menu()

@app.command("r")
def r():
    """[bold red]xxx r[/bold red] – Request Management System 🎫"""
    request_menu()

@app.command("zackry")
def zackry():
    """[bold blue]xxx zackry[/bold blue] - Show Pip & FastAPI Guide / About the Creator"""
    console.print(PIP_GUIDE)


def main():
    app() 

if __name__ == "__main__":
    main()
