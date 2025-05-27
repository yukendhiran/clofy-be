import os

from dotenv import load_dotenv
from invoke.tasks import task
from sqlalchemy import create_engine


# Load environment variables from .env file
_ = load_dotenv()


# --- Configuration ---
# Get database URL from Invoke config (defined in pyproject.toml)
# or from environment variable (useful for production)
def get_db_url(c):
    """Retrieves the database URL, prioritizing environment variable."""
    return os.getenv("DATABASE_URL", c.config.db.url)


# --- Common Helper for Database Operations ---
def get_engine(c):
    db_url = get_db_url(c)
    return create_engine(db_url)


@task
def alembic_init(c):
    """Initializes Alembic in the current directory."""
    print("Initializing Alembic...")
    c.run(
        "alembic init -t async migrations"
    )  # Use async template for modern FastAPI/SQLModel apps
    print("Alembic initialized. Remember to review env.py and script.py.mako.")


@task
def alembic_revision(c, message=None, autogenerate=False):
    """Creates a new Alembic migration revision."""
    cmd = "alembic revision"
    if message:
        cmd += f" -m '{message}'"
    if autogenerate:
        cmd += " --autogenerate"
    print(f"Creating Alembic revision: {cmd}")
    c.run(cmd)
    print("Alembic revision created.")


@task
def migrate(c):
    """Applies pending database migrations (upgrades to head)."""
    print("Applying database migrations...")
    c.run("alembic upgrade head")
    print("Migrations applied.")


@task
def downgrade(c, revision="base"):
    """Downgrades database to a specific revision (or 'base')."""
    print(f"Downgrading database to revision: {revision}")
    c.run(f"alembic downgrade {revision}")
    print("Database downgraded.")


# --- Development & Testing Tasks ---


@task
def dev(c):
    """Starts the FastAPI development server with auto-reload."""
    print("Starting FastAPI development server...")
    c.run("uv run fastapi dev")


@task
def start(c):
    """Starts the FastAPI production server (no reload)."""
    print("Starting FastAPI production server...")
    # For production, you might want Gunicorn or more workers, e.g.:
    # c.run("gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app")
    c.run("uv run fastapi run")


@task
def test(c):
    """Runs pytest for unit and integration tests."""
    print("Running tests...")
    c.run("pytest")


@task
def lint(c):
    """Runs Ruff linter and formatter checks."""
    print("Running Ruff linting...")
    c.run("ruff check . --fix")
    print("Running Ruff formatting check...")
    c.run("ruff format --check .")


@task
def format(c):
    """Automatically formats code using Ruff."""
    print("Running Ruff auto-formatter...")
    c.run("ruff format .")


# --- CI/CD Pipeline Task ---


@task(pre=[lint, test, migrate])  # Runs linting, testing, and migrations in sequence
def ci(c):
    """Runs all continuous integration checks."""
    print("All CI checks passed!")
