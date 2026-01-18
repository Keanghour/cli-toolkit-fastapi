# cnb_cli/commands/request.py

import questionary
from pathlib import Path
from openpyxl import Workbook
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.spinner import Spinner
from dotenv import dotenv_values
import time

console = Console()


# ----------------------------
# Load .env variables
# ----------------------------
def load_env(path: str = ".env") -> dict:
    env_path = Path(path)
    if not env_path.exists():
        console.print(f"[red]❌ .env file not found at {path}![/red]")
        return {}
    return dotenv_values(env_path)


# ----------------------------
# Generate Excel file path
# ----------------------------
def get_excel_path(environment: str, job_name: str) -> Path:
    safe_job = job_name.replace(" ", "_")
    return Path(f"{environment}_{safe_job}_env.xlsx")


# ----------------------------
# Save env data to Excel
# ----------------------------
def save_env_to_excel(file_path: Path, env_data: dict):
    wb = Workbook()
    ws = wb.active
    ws.title = "Environment Variables"

    # Header
    ws.append(["Name", "Value"])

    for k, v in env_data.items():
        ws.append([k, v])

    wb.save(file_path)


# ----------------------------
# Generate Request Letter
# ----------------------------
def generate_request_letter(req_type, environment, job, path, docker_image="<replace-with-docker-image>"):
    letter = f"""
Dear IT Team,

1. I would like to request {req_type} as below path:
+ {environment}
{path}
Note: Please refer to the attachment file for configuration

2. Build xxx Version
  - Group: xxxxx
  - Pipeline: {job}
  - Environment: {environment}
  - Docker_Image: {docker_image}

Best Regards,
Your Name
"""
    return letter.strip()


# ----------------------------
# Request Menu
# ----------------------------
def request_menu():
    console.print(Panel.fit(
        "🎫 [bold cyan]Request Management System[/bold cyan]\n\n"
        "Fill in the details to record your deployment or config request.\n"
        "Defaults are provided for convenience.",
        title="Guide",
        style="yellow"
    ))

    # ----------------------------
    # User Inputs
    # ----------------------------
    req_type = questionary.select(
        "What type of request would you like to make?",
        choices=[
            "Add Config Map",
            "Delete Config Map",
            "Update Config Map",
        ]
    ).ask()

    environment = questionary.select(
        "Select target environment",
        choices=["DEV", "UAT", "PROD"]
    ).ask()

    # Default job: short name of API or repo
    default_job = "my_api"
    job = questionary.text("Enter job name", default=default_job).ask()

    # Default path for CI/CD
    default_path = str(Path.cwd())
    path = questionary.text("Enter path (for CI/CD)", default=default_path).ask()

    # Default username & password (from .env or placeholders)
    env_vars = load_env()
    default_username = env_vars.get("USERNAME", "your_AD_user")
    default_password = env_vars.get("PASSWORD", "your_password")

    username = questionary.text("Enter username", default=default_username).ask()
    password = questionary.password("Enter password", default=default_password).ask()

    # ----------------------------
    # Preview .env Variables
    # ----------------------------
    if env_vars:
        table = Table(title=f"{environment} Environment Variables", show_lines=True)
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")

        for k, v in env_vars.items():
            table.add_row(k, v)

        console.print("\nPreview of environment variables:")
        console.print(table)

        save_excel = questionary.confirm("Save these variables to Excel?", default=True).ask()
        if save_excel:
            excel_file = get_excel_path(environment, job)
            with console.status("⠋ Saving Excel...", spinner="dots"):
                time.sleep(1)  # simulate processing
                save_env_to_excel(excel_file, env_vars)
            console.print(f"✅ Excel saved: {excel_file}\n")

    # ----------------------------
    # Request Letter Preview
    # ----------------------------
    letter = generate_request_letter(req_type, environment, job, path)
    console.print(Panel.fit(letter, title="Request Preview", style="green"))

    # Confirm to save request (Excel or letter if needed)
    save_request = questionary.confirm("Do you want to save this request letter to Excel?", default=True).ask()
    if save_request:
        excel_file = get_excel_path(environment, job)
        with console.status("⠋ Saving request...", spinner="dots"):
            time.sleep(1)
            save_env_to_excel(excel_file, {"Request Letter": letter})
        console.print(f"✅ Request saved to {excel_file}")

