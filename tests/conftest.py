import subprocess
import sys
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent


@pytest.fixture(scope="session")
def server_url():
    proc = subprocess.Popen(
        [
            sys.executable, "-m", "uvicorn",
            "main:app",
            "--host", "127.0.0.1",
            "--port", "8765",
            "--log-level", "critical",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd=ROOT,
    )
    time.sleep(1.0)
    yield "http://127.0.0.1:8765"
    proc.terminate()
    proc.wait()
