# cnb_cli/commands/api_generator.py
import typer
import questionary
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from cnb_cli.utils.helper import create_file, modify_file

console = Console()

def generate_api():
    console.print(Panel.fit("⚡ [bold cyan]Quick API Creation[/bold cyan]", border_style="green"))

    # API type selection
    api_type = questionary.select(
        "What type of API would you like to create?",
        choices=[
            "CRUD API - Full REST with database (Model, Repository, Service, Controller)",
            "Simple API - Controller & Service only (No database)"
        ]
    ).ask()

    # API name
    api_name = questionary.text(
        "Enter API name (e.g., User, Product, Order):",
        validate=lambda val: val.isidentifier() or "Use valid snake_case name"
    ).ask()

    # Optional folder name
    folder_name = questionary.text(
        "Enter folder name (press Enter to use API name):",
        default=api_name
    ).ask()

    console.print(f"\n🚀 Creating {api_type.split('-')[0].strip()} API: [bold]{api_name}[/bold]")
    console.print("Creating API components...\n")

    base_path = folder_name

    created_files = []

    if "CRUD" in api_type:
        # Models
        model_file = f"app/models/{base_path}/models.py"
        create_file(model_file, f"# Auto-generated models for {api_name}")
        created_files.append(("Model", model_file))

        # Repositories
        repo_file = f"app/repositories/{base_path}/repos.py"
        create_file(repo_file, f"# Auto-generated repository for {api_name}")
        created_files.append(("Repository", repo_file))

        # Services
        service_file = f"app/services/{base_path}/services.py"
        create_file(service_file, f"# Auto-generated service for {api_name}")
        created_files.append(("Service", service_file))

        # Controllers
        controller_file = f"app/controllers/v1/{base_path}/api.py"
        create_file(controller_file, f"# Auto-generated controller for {api_name}")
        created_files.append(("Controller", controller_file))

        # Schemas
        schema_paths = [
            f"app/schemas/{base_path}/create/schema.py",
            f"app/schemas/{base_path}/update/schema.py",
            f"app/schemas/{base_path}/response/list.py",
            f"app/schemas/{base_path}/response/one.py",
            f"app/schemas/{base_path}/response/delete.py",
            f"app/schemas/{base_path}/response/remote.py",
        ]
        for path in schema_paths:
            create_file(path, f"# Auto-generated schema for {api_name}")
            created_files.append(("Schema", path))

        # Register default files if not exist
        create_file("app/controllers/register_api.py", "# Register all APIs")
        create_file("app/models/register_models.py", "# Register all models")

        # Update requirements.txt
        deps = "sqlmodel~=0.0.22, sqlalchemy~=2.0.36, asyncpg, psycopg2-binary\n"
        modify_file("requirements.txt", deps)
        console.print(f"\n[green]Updated requirements.txt with database dependencies: {deps.strip()}[/green]")

    else:  # Simple API
        # Services & Controllers only
        service_file = f"app/services/{base_path}/services.py"
        create_file(service_file, f"# Auto-generated service for {api_name}")
        created_files.append(("Service", service_file))

        controller_file = f"app/controllers/v1/{base_path}/api.py"
        create_file(controller_file, f"# Auto-generated controller for {api_name}")
        created_files.append(("Controller", controller_file))

    # Summary
    console.print(Panel.fit(
        Text.from_markup(
            f"📁 [bold yellow]Files created:[/bold yellow]\n" +
            "\n".join([f"  • {name}: {path}" for name, path in created_files]) +
            "\n\n📋 [bold yellow]Available endpoints:[/bold yellow]\n" +
            "  • POST   /{api_name}/create/\n" +
            "  • POST   /{api_name}/one/{{id}}/\n" +
            "  • PATCH  /{api_name}/update/{{id}}/\n" +
            "  • DELETE /{api_name}/delete/\n" +
            "  • POST   /{api_name}/list/\n" +
            "  • POST   /{api_name}/remote/\n\n" +
            "💡 [bold]Next steps:[/bold]\n" +
            "  1. Update the model fields in app/models/{api_name}/models.py\n" +
            "  2. Run database migrations (alembic revision --autogenerate && alembic upgrade head)\n" +
            "  3. Start your API server and test the endpoints"
        ),
        border_style="blue"
    ))

    console.print(f"\n✨ Successfully created {api_type.split('-')[0].strip()} API: [bold]{api_name}[/bold]!\n")
