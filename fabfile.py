from fabric import Connection, task
from invoke import Responder
from getpass import getpass

# Define directories and paths
PROJECT="carabana"
PROJECT_DIR = f"~/{PROJECT}"
INIT_SCRIPT = f"~/init/{PROJECT}"  # Path to your init script
REPO_URL = "git@github.com:76house/carabana.git"
REPO_DIR = f"~/github-{PROJECT}"
VENV_DIR = f"~/.virtualenvs/{PROJECT}"
PYTHON_BIN = f"{VENV_DIR}/bin/python"
PIP_BIN = f"{VENV_DIR}/bin/pip"

def get_connection(host):
    password = getpass("Enter SSH password: ")
    return Connection(
        host=host,
        connect_kwargs={"password": password}
    )

@task
def restart(c, host):
    """
    Restarts the application on the specified host.

    Example:
    fab restart --host=user@ssh.server.com
    """
    conn = get_connection(host)
    print("Restarting the application on remote server...")
    conn.run(f"{INIT_SCRIPT} restart")

@task
def stop(c, host):
    """
    Stops the application on the specified host.

    Example:
    fab stop --host=user@ssh.server.com
    """
    conn = get_connection(host)
    print("Stopping the application on remote server...")
    conn.run(f"{INIT_SCRIPT} stop")

@task
def start(c, host):
    """
    Starts the application on the specified host.

    Example:
    fab start --host=user@ssh.server.com
    """
    conn = get_connection(host)
    print("Starting the application on remote server...")
    conn.run(f"{INIT_SCRIPT} start")

@task
def deploy(c, host):
    """
    Deploys the application to the specified host.

    Example:
    fab deploy --host=user@ssh.server.com
    """
    conn = get_connection(host)

    # Clone or pull the repository
    print("Pulling latest changes from Github...")
    if not conn.run(f"test -d {REPO_DIR}", warn=True).ok:
        conn.run(f"git clone {REPO_URL} {REPO_DIR}")
    else:
        conn.run(f"cd {REPO_DIR} && git pull && cd ~")

    print("Stopping the application on remote server...")
    conn.run(f"{INIT_SCRIPT} stop", warn=True)

    # Remove the virtual environment
    print("Removing the virtual environment...")
    conn.run(f"rm -rf {VENV_DIR}", warn=True)

    # Remove the `blog` app
    print("Removing the blog app...")
    conn.run(f"rm -rf {PROJECT_DIR}/blog", warn=True)

    # Copy the `blog` app to project directory
    print("Copying files to project directory...")
    conn.run(f"cp -r {REPO_DIR}/blog {PROJECT_DIR}/blog")

    # Copy the `urls.py` file to project config directory
    conn.run(f"yes | cp {REPO_DIR}/{PROJECT}/urls.py {PROJECT_DIR}/config")

    # Copy the `requirements.txt` file to project requirements directory
    conn.run(f"yes | cp {REPO_DIR}/requirements.txt {PROJECT_DIR}/requirements/{PROJECT}.txt")

    # Re-create virtual environment by entering the project directory
    print("Re-creating virtual environment...")
    conn.run(f"python3 -m venv {VENV_DIR} && source {VENV_DIR}/bin/activate")

    # Install global and project-specific dependencies in the virtual environment
    print("Installing dependencies in virtual environment...")
    conn.run(f"{PIP_BIN} install -r {PROJECT_DIR}/requirements/production.txt")
    conn.run(f"{PIP_BIN} install -r {PROJECT_DIR}/requirements/{PROJECT}.txt")

    # Collect static files
    print("Collecting static files...")
    conn.run(f"cd {PROJECT_DIR} && {PYTHON_BIN} manage.py collectstatic --noinput")

    # Apply database migrations
    print("Running database mingrations...")
    conn.run(f"cd {PROJECT_DIR} && {PYTHON_BIN} manage.py migrate")

    print("Starting the application on remote server...")
    conn.run(f"{INIT_SCRIPT} start", warn=True)

    print(f"Deployment to {host} successful.")
    print(f"Note: This script does not update INSTALLED APPS in carabana/config/settings/common.py")
