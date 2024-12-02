import docker
import argparse
from test_config import TEST_ENV_CONFIG

client = docker.from_env()

def start_services(services):
    """
    Start Docker containers based on the service configuration.
    """
    for service_name, config in services.items():
        container_name = config["container_name"]
        try:
            container = client.containers.get(container_name)
            if container.status == "running":
                print(f"{container_name} is already running.")
            else:
                print(f"Starting {container_name} (currently {container.status})...")
                container.start()
                print(f"{container_name} started.")
        except docker.errors.NotFound:
            print(f"{container_name} does not exist. Creating and starting it...")
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
            print(f"{container_name} created and started.")

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
            print(f"{container_name} stopped and removed.")
        except docker.errors.NotFound:
            print(f"{container_name} is not running or does not exist.")

def display_service_status(services):
    """
    Display the status of all services.
    """
    for service_name, config in services.items():
        container_name = config["container_name"]
        try:
            container = client.containers.get(container_name)
            status = container.status
            health = container.attrs["State"].get("Health", {}).get("Status", "unknown")
            print(f"{service_name}: {status} (Health: {health})")
        except docker.errors.NotFound:
            print(f"{service_name}: Not Found")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage test environment.")
    parser.add_argument("--start", action="store_true", help="Start all services.")
    parser.add_argument("--stop", action="store_true", help="Stop all services.")
    parser.add_argument("--status", action="store_true", help="Display the status of all services.")

    args = parser.parse_args()

    # If no arguments are passed, show the help message
    if not any(vars(args).values()):
        parser.print_help()
    else:
        if args.start:
            start_services(TEST_ENV_CONFIG["services"])
        if args.stop:
            stop_services(TEST_ENV_CONFIG["services"])
        if args.status:
            display_service_status(TEST_ENV_CONFIG["services"])
