# cnb_cli/commands/docker_generator.py
import typer
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from cnb_cli.utils.helper import create_file, modify_file

console = Console()

def generate_docker():
    console.print(Panel.fit("🐳 [bold cyan]Docker Setup Generator[/bold cyan]", border_style="green"))

    # Section 1: Application
    app_choice = questionary.select(
        "Select the main application to include in Docker:",
        choices=[
            "App (FastAPI, Celery, or your main service)",
            "Skip"
        ]
    ).ask()

    console.print(f"[green]✅ Selected Application: {app_choice}[/green]")

    # Section 2: Database
    db_choice = questionary.checkbox(
        "Select database(s) to include in Docker (use space to select, enter to confirm):",
        choices=[
            "Postgres",
            "MySQL",
            "MongoDB",
            "Skip"
        ]
    ).ask()

    console.print(f"[green]✅ Selected Database(s): {', '.join(db_choice)}[/green]")

    # Section 3: Message Brokers & Cache
    services_choice = questionary.checkbox(
        "Select message brokers / cache to include:",
        choices=[
            "Redis",
            "Kafka",
            "RabbitMQ",
            "Skip"
        ]
    ).ask()

    console.print(f"[green]✅ Selected Services: {', '.join(services_choice)}[/green]")

    # Section 4: Logs / Monitoring
    monitoring_choice = questionary.checkbox(
        "Select logging / monitoring tools:",
        choices=[
            "Sentry",
            "Prometheus",
            "Grafana",
            "Skip"
        ]
    ).ask()

    console.print(f"[green]✅ Selected Monitoring: {', '.join(monitoring_choice)}[/green]")

    # Summary
    console.print(Panel.fit(
        Text.from_markup(
            f"🚀 [bold yellow]Docker Configuration Summary[/bold yellow]\n\n"
            f"[bold cyan]Application:[/bold cyan] {app_choice}\n"
            f"[bold cyan]Databases:[/bold cyan] {', '.join(db_choice)}\n"
            f"[bold cyan]Services:[/bold cyan] {', '.join(services_choice)}\n"
            f"[bold cyan]Monitoring:[/bold cyan] {', '.join(monitoring_choice)}\n\n"
            f"💡 Next steps:\n"
            f"1. Files like docker-compose.yml and .env will be created.\n"
            f"2. Customize the service configurations as needed.\n"
            f"3. Run `docker compose up` to start your environment."
        ),
        border_style="blue"
    ))

    # Example: Generate docker-compose.yml (placeholder content)
    docker_compose_content = f"""
version: '3.9'

services:
  app:
    image: your-app-image
    container_name: app
    ports:
      - "8000:8000"
    environment:
      - ENV=development
"""

    if "Postgres" in db_choice:
        docker_compose_content += """
  postgres:
    image: postgres:15
    container_name: postgres
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: app_db
    ports:
      - "5432:5432"
"""

    if "Redis" in services_choice:
        docker_compose_content += """
  redis:
    image: redis:7
    container_name: redis
    ports:
      - "6379:6379"
"""

    # Save docker-compose.yml
    create_file("docker-compose.yml", docker_compose_content)
    console.print("[green]✨ docker-compose.yml created successfully![/green]")
