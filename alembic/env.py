# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv
from models import Base  # Import models Base
from utils.database import DATABASE_URL  # Import database URL
import os

# Load environment variables
load_dotenv()
config = context.config
# Add this line before the configuration context
config.set_main_option('sqlalchemy.url', os.getenv('DATABASE_URL'))
# Interpret the config file for Python logging.
fileConfig(context.config.config_file_name)

# Add models here for 'autogenerate' support
target_metadata = Base.metadata


# Database connection
def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        context.config.get_section(context.config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=DATABASE_URL,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
