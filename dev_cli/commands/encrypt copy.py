# # cnb_cli/commands/encrypt.py

# import questionary
# from cryptography.fernet import Fernet
# from pathlib import Path
# from rich.console import Console

# console = Console()

# # ----------------------------
# # Load KEY from .env
# # ----------------------------
# def load_key() -> str:
#     env_path = Path(".env")
#     if not env_path.exists():
#         console.print("[red]❌ .env file not found! Generate a key first.[/red]")
#         raise FileNotFoundError(".env not found")

#     for line in env_path.read_text().splitlines():
#         if line.startswith("KEY="):
#             return line.split("=", 1)[1]
#     console.print("[red]❌ KEY not found in .env! Generate a key first.[/red]")
#     raise ValueError("KEY not found in .env")

# # ----------------------------
# # Generate KEY
# # ----------------------------
# def generate_key(auto_save: bool = True) -> str:
#     key = Fernet.generate_key().decode()
#     console.print(f"[green]✅ Generated Key:[/green] {key}")

#     if auto_save:
#         env_path = Path(".env")
#         lines = []

#         if env_path.exists():
#             # Read existing lines, remove any existing KEY
#             lines = [l for l in env_path.read_text().splitlines() if not l.startswith("KEY=")]

#         # Write KEY at the top
#         env_path.write_text(f"KEY={key}\n" + "\n".join(lines) + "\n")
#         console.print(f"[green]✅ Key saved at the top of .env[/green]")

#     return key

# # ----------------------------
# # Encrypt single value
# # ----------------------------
# def encrypt_value():
#     key = load_key()
#     value = questionary.text("Enter the value to encrypt").ask()
#     if not value:
#         console.print("[yellow]⚠️ No value entered[/yellow]")
#         return
#     f = Fernet(key.encode())
#     encrypted = f.encrypt(value.encode()).decode()
#     console.print(f"[green]✅ Encrypted value:[/green] {encrypted}")

# # ----------------------------
# # Decrypt single value
# # ----------------------------
# def decrypt_value():
#     key = load_key()
#     value = questionary.text("Enter the value to decrypt").ask()
#     if not value:
#         console.print("[yellow]⚠️ No value entered[/yellow]")
#         return
#     f = Fernet(key.encode())
#     try:
#         decrypted = f.decrypt(value.encode()).decode()
#         console.print(f"[green]✅ Decrypted value:[/green] {decrypted}")
#     except Exception:
#         console.print("[red]❌ Failed to decrypt. Is the value correct?[/red]")

# # ----------------------------
# # Encrypt Entire .env (except KEY)
# # ----------------------------
# def encrypt_entire_env():
#     path = questionary.text("Enter path to .env file", default=".env").ask()
#     env_path = Path(path)
#     if not env_path.exists():
#         console.print(f"[red]❌ File not found: {path}[/red]")
#         return

#     key = load_key()
#     fernet = Fernet(key.encode())

#     lines = env_path.read_text().splitlines()
#     vars_to_encrypt = [(l.split("=",1)[0], l.split("=",1)[1]) for l in lines if l and not l.startswith("KEY=") and not l.startswith("#")]

#     if not vars_to_encrypt:
#         console.print("[yellow]⚠️ No variables to encrypt in .env[/yellow]")
#         return

#     console.print("[cyan]The following variables will be encrypted:[/cyan]")
#     for k, v in vars_to_encrypt:
#         console.print(f"{k} = {v}")

#     confirm = questionary.confirm("Do you want to encrypt these variables?", default=True).ask()
#     if not confirm:
#         console.print("[yellow]Operation cancelled.[/yellow]")
#         return

#     encrypted_lines = []
#     for line in lines:
#         if line.startswith("KEY=") or not line.strip() or line.startswith("#"):
#             encrypted_lines.append(line)
#         else:
#             k, v = line.split("=", 1)
#             encrypted_lines.append(f"{k}={fernet.encrypt(v.encode()).decode()}")

#     out_path = path + ".enc"
#     Path(out_path).write_text("\n".join(encrypted_lines) + "\n")
#     console.print(f"[green]✅ Encrypted .env saved as {out_path}[/green]")

# # ----------------------------
# # Decrypt Entire .env
# # ----------------------------
# def decrypt_entire_env():
#     path = questionary.text("Enter path to encrypted .env file", default=".env.enc").ask()
#     env_path = Path(path)
#     if not env_path.exists():
#         console.print(f"[red]❌ File not found: {path}[/red]")
#         return

#     key = load_key()
#     fernet = Fernet(key.encode())

#     lines = env_path.read_text().splitlines()
#     decrypted_lines = []
#     for line in lines:
#         if line.startswith("KEY=") or not line.strip() or line.startswith("#"):
#             decrypted_lines.append(line)
#         else:
#             k, v = line.split("=", 1)
#             decrypted_lines.append(f"{k}={fernet.decrypt(v.encode()).decode()}")

#     out_path = path.replace(".enc", ".dec")
#     Path(out_path).write_text("\n".join(decrypted_lines) + "\n")
#     console.print(f"[green]✅ Decrypted .env saved as {out_path}[/green]")

# # ----------------------------
# # Encryption menu
# # ----------------------------
# def encrypt_menu():
#     console.print("\n🔐 [bold cyan]Encryption Tools[/bold cyan]\n")
#     choice = questionary.select(
#         "What would you like to do?",
#         choices=[
#             "Generate Key",
#             "Encrypt Value",
#             "Decrypt Value",
#             "Encrypt Entire .env File",
#             "Decrypt Entire .env File"
#         ]
#     ).ask()

#     if choice == "Generate Key":
#         generate_key()
#     elif choice == "Encrypt Value":
#         encrypt_value()
#     elif choice == "Decrypt Value":
#         decrypt_value()
#     elif choice == "Encrypt Entire .env File":
#         encrypt_entire_env()
#     elif choice == "Decrypt Entire .env File":
#         decrypt_entire_env()
