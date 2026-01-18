# cnb_cli/commands/consumer_generator.py
import questionary
from rich.console import Console
from cnb_cli.utils.helper import create_file, modify_file

console = Console()

def generate_consumer():
    console.print("🔌 [bold cyan]Consumer Generation[/bold cyan]\n")

    connection_type = questionary.select(
        "Select connection to use",
        choices=["RabbitMQ", "Kafka"]
    ).ask()

    consumer_name = questionary.text(
        "Enter consumer name (snake_case only)"
    ).ask()

    topic_name = questionary.text(
        "Enter Topic name"
    ).ask()

    console.print(f"🚀 Creating {connection_type} consumer: {consumer_name}")
    console.print(f"Topic: {topic_name}")

    consumer_file = f"app/consumers/{consumer_name}.py"
    core_file = "app/core/core_consumer.py"
    register_file = "app/consumers/register.py"

    content = f"""from app.utils.{connection_type.lower()} import {connection_type}
from app.core.core_consumer import CoreConsumer
from loguru import logger

class {consumer_name.title().replace('_','')}Consumer(CoreConsumer):
    def __init__(self):
        self.connection = {connection_type}()
        self.topic = "{topic_name}"

    async def process(self, message, request_id):
        logger.info(f"{{request_id}} - Processing message: {{message}}")
"""

    create_file(consumer_file, content)
    create_file(core_file, "# Core consumer base placeholder\n")
    create_file(register_file, "# Consumer register placeholder\n")

    modify_file(".env", f"{connection_type.upper()}_{topic_name.upper()}_TOPIC={topic_name}\n")

    console.print(f"✨ Successfully created consumer: {consumer_name.title().replace('_','')}Consumer")
    console.print(f"📁 Files created:\n  • Consumer: {consumer_file}\n")
