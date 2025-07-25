from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from models import Base
from database import SQLALCHEMY_DATABASE_URL

config = context.config
config.set_main_option('sqlalchemy.url', SQLALCHEMY_DATABASE_URL)
fileConfig(config.config_file_name)
connectable = engine_from_config(
    config.get_section(config.config_ini_section),
    prefix='sqlalchemy.',
    poolclass=pool.NullPool)

with connectable.connect() as connection:
    context.configure(
        connection=connection,
        target_metadata=Base.metadata
    )

    with context.begin_transaction():
        context.run_migrations()
