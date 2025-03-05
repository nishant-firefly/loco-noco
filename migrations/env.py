from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from config.database import DATABASES
  # Import the DATABASES dictionary

# Load the configuration from alembic.ini
config = context.config

# Get the database type from environment variables (default to PostgreSQL)
import os
db_type = os.getenv("DB_TYPE", "postgres")  # Change the DB_TYPE to switch databases

if db_type not in DATABASES:
    raise ValueError(f"Unsupported database type: {db_type}")

# Override sqlalchemy.url in alembic.ini dynamically
config.set_main_option("sqlalchemy.url", DATABASES[db_type])

# Configure logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import the Base model

from core.models.base import Base
from core.models.models import User, Role, EntityRolePermission, RoleToUserMapping
target_metadata = Base.metadata

  # Ensure this file imports all models

# Create an engine
engine = create_engine(DATABASES[db_type], poolclass=pool.NullPool)

# Run migrations in offline mode
def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(url=DATABASES[db_type], target_metadata=Base.metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

# Run migrations in online mode
def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine.connect()
    with connectable as connection:
        context.configure(connection=connection, target_metadata=Base.metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()





# from logging.config import fileConfig

# from sqlalchemy import engine_from_config
# from sqlalchemy import pool

# from alembic import context

# # this is the Alembic Config object, which provides
# # access to the values within the .ini file in use.
# config = context.config

# # Interpret the config file for Python logging.
# # This line sets up loggers basically.
# if config.config_file_name is not None:
#     fileConfig(config.config_file_name)

# # add your model's MetaData object here
# # for 'autogenerate' support
# # from myapp import mymodel
# # target_metadata = mymodel.Base.metadata
# target_metadata = None

# # other values from the config, defined by the needs of env.py,
# # can be acquired:
# # my_important_option = config.get_main_option("my_important_option")
# # ... etc.


# def run_migrations_offline() -> None:
#     """Run migrations in 'offline' mode.

#     This configures the context with just a URL
#     and not an Engine, though an Engine is acceptable
#     here as well.  By skipping the Engine creation
#     we don't even need a DBAPI to be available.

#     Calls to context.execute() here emit the given string to the
#     script output.

#     """
#     url = config.get_main_option("sqlalchemy.url")
#     context.configure(
#         url=url,
#         target_metadata=target_metadata,
#         literal_binds=True,
#         dialect_opts={"paramstyle": "named"},
#     )

#     with context.begin_transaction():
#         context.run_migrations()


# def run_migrations_online() -> None:
#     """Run migrations in 'online' mode.

#     In this scenario we need to create an Engine
#     and associate a connection with the context.

#     """
#     connectable = engine_from_config(
#         config.get_section(config.config_ini_section, {}),
#         prefix="sqlalchemy.",
#         poolclass=pool.NullPool,
#     )

#     with connectable.connect() as connection:
#         context.configure(
#             connection=connection, target_metadata=target_metadata
#         )

#         with context.begin_transaction():
#             context.run_migrations()


# if context.is_offline_mode():
#     run_migrations_offline()
# else:
#     run_migrations_online()
