# cnb_cli/commands/encrypt.py

import questionary
from cryptography.fernet import Fernet
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.spinner import Spinner
from time import sleep

console = Console()

# ----------------------------
# Helpers
# ----------------------------
def load_key() -> str:
    env_path = Path(".env")
    if not env_path.exists():
        console.print("[red]❌ .env file not found! Generate a key first.[/red]")
        raise FileNotFoundError(".env not found")

    for line in env_path.read_text().splitlines():
        if line.startswith("KEY="):
            return line.split("=", 1)[1]

    console.print("[red]❌ KEY not found in .env! Generate a key first.[/red]")
    raise ValueError("KEY not found in .env")


def spinner_task(message: str, func, *args, **kwargs):
    """Show spinner while task is running"""
    with console.status(f"[cyan]{message}...", spinner="dots") as status:
        result = func(*args, **kwargs)
        return result


# ----------------------------
# Generate KEY
# ----------------------------
def generate_key(auto_save: bool = True) -> str:
    key = Fernet.generate_key().decode()
    console.print(f"[green]✅ Generated Key:[/green] {key}")

    if auto_save:
        env_path = Path(".env")
        lines = []
        if env_path.exists():
            lines = [l for l in env_path.read_text().splitlines() if not l.startswith("KEY=")]
        env_path.write_text(f"KEY={key}\n" + "\n".join(lines) + "\n")
        console.print(f"[green]✅ Key saved in .env[/green]")

    return key


# ----------------------------
# Encrypt single value
# ----------------------------
def encrypt_value():
    try:
        key = load_key()
    except Exception:
        return

    value = questionary.text("Enter the value to encrypt").ask()
    if not value:
        console.print("[yellow]⚠️ No value entered[/yellow]")
        return

    f = Fernet(key.encode())
    encrypted = spinner_task("Encrypting value", f.encrypt, value.encode()).decode()
    console.print(f"[green]✅ Encrypted value:[/green] {encrypted}")


# ----------------------------
# Decrypt single value
# ----------------------------
def decrypt_value():
    try:
        key = load_key()
    except Exception:
        return

    value = questionary.text("Enter the value to decrypt").ask()
    if not value:
        console.print("[yellow]⚠️ No value entered[/yellow]")
        return

    f = Fernet(key.encode())
    try:
        decrypted = spinner_task("Decrypting value", f.decrypt, value.encode()).decode()
        console.print(f"[green]✅ Decrypted value:[/green] {decrypted}")
    except Exception:
        console.print("[red]❌ Failed to decrypt. Is the value correct?[/red]")


# ----------------------------
# Encrypt Entire .env (in-place)
# ----------------------------
def encrypt_entire_env():
    env_path = Path(".env")
    if not env_path.exists():
        console.print("[red]❌ .env file not found![/red]")
        return

    try:
        key = load_key()
    except Exception:
        return

    fernet = Fernet(key.encode())
    lines = env_path.read_text().splitlines()
    vars_to_encrypt = [(l.split("=", 1)[0], l.split("=", 1)[1])
                       for l in lines if l and not l.startswith("KEY=") and not l.startswith("#")]

    if not vars_to_encrypt:
        console.print("[yellow]⚠️ No variables to encrypt[/yellow]")
        return

    console.print("[cyan]Variables to encrypt:[/cyan]")
    for k, v in vars_to_encrypt:
        console.print(f"{k} = {v}")

    if not questionary.confirm("Encrypt these variables?", default=True).ask():
        console.print("[yellow]Operation cancelled.[/yellow]")
        return

    encrypted_lines = []
    for line in lines:
        if line.startswith("KEY=") or not line.strip() or line.startswith("#"):
            encrypted_lines.append(line)
        else:
            k, v = line.split("=", 1)
            encrypted_lines.append(f"{k}={fernet.encrypt(v.encode()).decode()}")

    console.print("\nPreview of encrypted .env:")
    for line in encrypted_lines:
        console.print(line)

    if questionary.confirm("Save changes to .env?", default=True).ask():
        spinner_task("Saving .env", lambda: env_path.write_text("\n".join(encrypted_lines) + "\n"))
        console.print("[green]✅ .env encrypted in-place[/green]")
    else:
        console.print("[yellow]Operation cancelled, .env not modified[/yellow]")


# ----------------------------
# Decrypt Entire .env (in-place)
# ----------------------------
def decrypt_entire_env():
    env_path = Path(".env")
    if not env_path.exists():
        console.print("[red]❌ .env file not found![/red]")
        return

    try:
        key = load_key()
    except Exception:
        return

    fernet = Fernet(key.encode())
    lines = env_path.read_text().splitlines()
    decrypted_lines = []
    to_decrypt = []

    for line in lines:
        if line.startswith("KEY=") or not line.strip() or line.startswith("#"):
            decrypted_lines.append(line)
        else:
            k, v = line.split("=", 1)
            try:
                decrypted_val = fernet.decrypt(v.encode()).decode()
            except Exception:
                decrypted_val = v  # keep as-is if not encrypted
            decrypted_lines.append(f"{k}={decrypted_val}")
            to_decrypt.append((k, decrypted_val))

    if not to_decrypt:
        console.print("[yellow]⚠️ No variables to decrypt[/yellow]")
        return

    console.print("[cyan]Preview of decrypted .env:[/cyan]")
    for line in decrypted_lines:
        console.print(line)

    if questionary.confirm("Save decrypted values to .env?", default=True).ask():
        spinner_task("Saving .env", lambda: env_path.write_text("\n".join(decrypted_lines) + "\n"))
        console.print("[green]✅ .env decrypted in-place[/green]")
    else:
        console.print("[yellow]Operation cancelled, .env not modified[/yellow]")


# ----------------------------
# Encryption menu
# ----------------------------
def encrypt_menu():
    console.print("\n🔐 [bold cyan]Encryption Tools[/bold cyan]\n")
    choice = questionary.select(
        "Choose an action",
        choices=[
            "Generate Key",
            "Encrypt Value",
            "Decrypt Value",
            "Encrypt Entire .env File",
            "Decrypt Entire .env File"
        ]
    ).ask()

    if choice == "Generate Key":
        generate_key()
    elif choice == "Encrypt Value":
        encrypt_value()
    elif choice == "Decrypt Value":
        decrypt_value()
    elif choice == "Encrypt Entire .env File":
        encrypt_entire_env()
    elif choice == "Decrypt Entire .env File":
        decrypt_entire_env()


# ----------------------------
# Guide Panel (optional for menu)
# ----------------------------
def show_encrypt_guide():
    console.print(Panel.fit(
        "💡 Encryption Guide\n"
        "• Generate Key → stores KEY in .env\n"
        "• Encrypt/Decrypt Value → single value\n"
        "• Encrypt/Decrypt Entire .env → in-place with preview\n"
        "\nCreated by: Hour Zackry",
        title="Guide",
        style="yellow"
    ))
