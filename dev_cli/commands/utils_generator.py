# cnb_cli/commands/utils_generator.py
from pathlib import Path
from rich.console import Console
import questionary

from cnb_cli.utils.helper import create_file, modify_file

console = Console()

UTILS_TEMPLATES = {
    "RabbitMQ": {
        "config_file": "app/config/rabbitmq.py",
        "utils_file": "app/utils/rabbitmq.py",
        "requirements": ["aio-pika"],
        "placeholder_content": "# RabbitMQ config and utils placeholder\n"
    },
    "Kafka": {
        "config_file": "app/config/kafka.py",
        "utils_file": "app/utils/kafka.py",
        "requirements": ["aiokafka"],
        "placeholder_content": "# Kafka config and utils placeholder\n"
    },
    "Redis": {
        "config_file": "app/config/redis.py",
        "utils_file": "app/utils/redis.py",
        "requirements": ["redis"],
        "placeholder_content": """# Redis config and utils placeholder
from pydantic_settings import BaseSettings
import redis

class RedisConfig(BaseSettings):
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = RedisConfig()

class RedisService:
    def __init__(self):
        self.redis_config = settings
        self.client = redis.StrictRedis(
            host=self.redis_config.redis_host,
            port=self.redis_config.redis_port,
            db=self.redis_config.redis_db
        )

    def set_value(self, key, value, expire_time=None):
        self.client.set(key, value, ex=expire_time)

    def get_value(self, key):
        val = self.client.get(key)
        if val is not None:
            return val.decode('utf-8')
        return None
"""
    }
}


def generate_utils():
    console.print("🔧 [bold cyan]Utility Generation[/bold cyan]\n")

    util_type = questionary.select(
        "Please select the type of utility you want to generate",
        choices=list(UTILS_TEMPLATES.keys())
    ).ask()

    console.print(f"🚀 Generating {util_type} utility...\n")

    template = UTILS_TEMPLATES[util_type]

    # Create config and utils files
    create_file(template["config_file"], template["placeholder_content"])
    create_file(template["utils_file"], template["placeholder_content"])

    # Update .env and requirements.txt
    modify_file(".env", f"{util_type.upper()}_CONFIG_PLACEHOLDER=1\n")
    for req in template["requirements"]:
        modify_file("requirements.txt", f"{req}\n")

    console.print(f"✨ Successfully generated {util_type} utility!")
    console.print(f"📁 File created:\n  • Utility: {template['utils_file']}")
    console.print(
        "💡 Next steps:\n"
        f"  1. Configure {util_type} connection settings in your .env file\n"
        f"  2. Import and use the utility in your application\n"
        "  3. Update connection parameters as needed\n"
    )
