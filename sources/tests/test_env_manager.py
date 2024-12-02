import docker
import time
from test_config import TEST_ENV_CONFIG

client = docker.from_env()

def start_services(services):
    """
    Start Docker containers based on the service configuration.
    """
    running_containers = {c.name for c in client.containers.list()}
    for service_name, config in services.items():
        container_name = config["container_name"]
        if container_name in running_containers:
            print(f"{container_name} is already running.")
            continue

        print(f"Starting {container_name}...")
        ports = {f"{host_port}/tcp": container_port for host_port, container_port in config["ports"].items()}
        resources = config.get("resources", {})

        client.containers.run(
            config["image"],
            name=container_name,
            environment=config["environment"],
            ports=ports,
            command=config.get("command"),
            detach=True,
            mem_limit=resources.get("mem_limit"),
            cpu_quota=resources.get("cpu_quota"),
        )
        print(f"{container_name} started.")

def stop_services(services):
    """
    Stop and remove Docker containers for the given services.
    """
    for service_name, config in services.items():
        container_name = config["container_name"]
        try:
            container = client.containers.get(container_name)
            print(f"Stopping {container_name}...")
            container.stop()
            container.remove()
        except docker.errors.NotFound:
            print(f"{container_name} is not running.")

def check_service_health(container_name):
    """
    Check the health status of a container.
    """
    try:
        container = client.containers.get(container_name)
        status = container.attrs["State"]["Health"]["Status"]
        print(f"{container_name}: {status}")
        return status == "healthy"
    except docker.errors.NotFound:
        print(f"{container_name}: Not Found")
        return False

def check_all_services(services):
    """
    Verify the health of all services.
    """
    all_healthy = True
    for service_name, config in services.items():
        container_name = config["container_name"]
        healthy = check_service_health(container_name)
        all_healthy = all_healthy and healthy
    return all_healthy

def get_service_status(container_name):
    """
    Get the status of a Docker container.
    """
    try:
        container = client.containers.get(container_name)
        status = container.status
        health = container.attrs.get("State", {}).get("Health", {}).get("Status", "unknown")
        return f"{status} (Health: {health})"
    except docker.errors.NotFound:
        return "Not Found"

def display_service_status(services):
    """
    Display the status of all services.
    """
    for service_name, config in services.items():
        container_name = config["container_name"]
        status = get_service_status(container_name)
        print(f"{service_name}: {status}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Manage test environment.")
    parser.add_argument("--start", action="store_true", help="Start all services.")
    parser.add_argument("--stop", action="store_true", help="Stop all services.")
    parser.add_argument("--status", action="store_true", help="Display the status of all services.")

    args = parser.parse_args()

    if args.start:
        start_services(TEST_ENV_CONFIG["services"])
    elif args.stop:
        stop_services(TEST_ENV_CONFIG["services"])
    elif args.status:
        display_service_status(TEST_ENV_CONFIG["services"])
