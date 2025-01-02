from fabric import Connection, task
from getpass import getpass

# Define your remote server connection
REMOTE_HOST = "s7.wservices.ch"
REMOTE_USER = "bozka"
REMOTE_PROJECT_DIR = "~/carabana"
INIT_SCRIPT = "~/init/carabana"  # Path to your init script

def get_connection():
    password = getpass("Enter SSH password: ")
    return Connection(
        host=REMOTE_HOST,
        user=REMOTE_USER,
        connect_kwargs={"password": password}
    )

@task
def deploy(c):
    # Push changes to the remote repository
    print("Pushing local changes to remote repository...")
    c.local("git push")

    # Connect to the remote server
    conn = get_connection()

    # Pull the latest code
    print("Pulling latest changes on the server...")
    conn.run(f"cd {REMOTE_PROJECT_DIR} && git pull")

    # Restart the application
    restart(conn)

@task
def restart(c):
    conn = get_connection()
    print("Restarting the application on remote server...")
    conn.run(f"{INIT_SCRIPT} restart")

@task
def stop(c):
    conn = get_connection()
    print("Stopping the application...")
    conn.run(f"{INIT_SCRIPT} stop")

@task
def start(c):
    conn = get_connection()
    print("Starting the application...")
    conn.run(f"{INIT_SCRIPT} start")
