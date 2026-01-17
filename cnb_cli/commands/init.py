from pathlib import Path
from rich.console import Console
import questionary
from cnb_cli.templates import files, project, docker

console = Console()

def init_project():
    console.print("\n🎉 [bold green]Project Initialization[/bold green]\n")

    # Ask user if DB is needed
    need_db = questionary.confirm("Do you need DB connection?", default=True).ask()

    # Prepare folder list
    folders = project.BASE_DIRS.copy()
    if not need_db and "app/db" in folders:
        folders.remove("app/db")  # skip DB folder if not needed
    folders.append("app")  # ensure app/ exists

    # Create folders
    for f in folders:
        Path(f).mkdir(parents=True, exist_ok=True)
        Path(f"{f}/__init__.py").touch(exist_ok=True)

    console.print("🚀 Project folders created successfully!")

    # -------------------------
    # Write template files
    # -------------------------
    files_map = {
        "app/main.py": files.MAIN_PY,
        "app/core/config.py": files.CONFIG_PY,
        "app/utils/encryption.py": files.ENCRYPTION_PY,
        "app/routers/health.py": files.HEALTH_ROUTER,
        ".env": files.ENV_FILE,
        "requirements.txt": files.REQUIREMENTS,
        "pip.conf": files.PIP_CONF,
        "Dockerfile": docker.DOCKERFILE,  # <-- Dockerfile added here
    }

    for path, content in files_map.items():
        dest = Path(path)
        if not dest.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(content)
            console.print(f"📄 [green]{path} created[/green]")

    console.print("\n💡 Next steps:")
    console.print("  1. pip install -r requirements.txt")
    console.print("  2. uvicorn app.main:app --reload\n")
