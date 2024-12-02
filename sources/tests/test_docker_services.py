import pytest
import docker
from .test_config import TEST_ENV_CONFIG

client = docker.from_env()

def check_service_running(container_name):
    """
    Check if the Docker container exists and is running.
    """
    try:
        container = client.containers.get(container_name)
        return container.status == "running"
    except docker.errors.NotFound:
        return False

@pytest.mark.parametrize(
    "service_name, container_name",
    [(name, config["container_name"]) for name, config in TEST_ENV_CONFIG["services"].items()]
)
def test_docker_service_running(service_name, container_name):
    """
    Test if the Docker container is running (skip health checks).
    """
    print(f"Checking if service {service_name} ({container_name}) is running...")
    is_running = check_service_running(container_name)
    assert is_running, f"Service {service_name} ({container_name}) is not running!"
