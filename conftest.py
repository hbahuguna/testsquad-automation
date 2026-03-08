import socket
import pytest
import os


def is_port_open(host: str, port: int) -> bool:
    """Helper to check if a local port is accepting connections."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        try:
            s.connect((host, port))
            return True
        except (ConnectionRefusedError, TimeoutError, OSError):
            return False


@pytest.fixture(scope="session", autouse=True)
def ensure_infrastructure_running():
    """
    Session-scoped fixture that validates the required TestSquad infrastructure
    is actively running before allowing the E2E suite to execute.
    """
    # Skip checks if explicitly told to via env var (useful for pure CI setups that handle this differently)
    if os.environ.get("SKIP_HEALTH_CHECKS") == "true":
        return

    required_services = {
        "Next.js Frontend": ("localhost", 3000),
        "FastAPI Backend": ("localhost", 8000),
        "PostgreSQL DB": ("localhost", 5432)
    }

    unavailable_services = []

    for name, (host, port) in required_services.items():
        if not is_port_open(host, port):
            unavailable_services.append(name)

    if unavailable_services:
        pytest.exit(
            f"\n[FATAL] E2E Infrastructure not detected! Missing: {', '.join(unavailable_services)}.\n"
            f"Please ensure you have run the bootstrap script to start the DB, Backend, and Frontend.\n"
            f"If you are confident the environment is correct, set SKIP_HEALTH_CHECKS=true."
        )
