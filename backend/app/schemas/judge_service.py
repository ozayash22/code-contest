import os
import uuid
import time
import subprocess

from sqlalchemy.orm import Session
from app.models.test_case import TestCase


TEMP_DIR = "/tmp/codecontest"


def run_python(code: str, input_data: str, timeout_sec=2):
    os.makedirs(TEMP_DIR, exist_ok=True)

    uid = str(uuid.uuid4())
    folder = f"{TEMP_DIR}/{uid}"

    os.makedirs(folder)

    file_path = f"{folder}/main.py"

    with open(file_path, "w") as f:
        f.write(code)

    start = time.time()

    try:
        result = subprocess.run(
            [
                "docker", "run",
                "--rm",
                "--network", "none",
                "--memory", "128m",
                "--cpus", "0.5",
                "-v", f"{folder}:/code",
                "codejudge-python"
            ],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=timeout_sec
        )

        runtime = round(time.time() - start, 3)

        return {
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "runtime": runtime
        }

    except subprocess.TimeoutExpired:
        return {
            "timeout": True
        }


def judge_submission(code, language, problem_id, db: Session):

    if language != "python":
        return {
            "status": "LANGUAGE_NOT_SUPPORTED",
            "runtime": 0
        }

    tests = db.query(TestCase).filter(
        TestCase.problem_id == problem_id
    ).all()

    max_runtime = 0

    for tc in tests:

        result = run_python(code, tc.input_data)

        if result.get("timeout"):
            return {
                "status": "TIME_LIMIT_EXCEEDED",
                "runtime": max_runtime
            }

        if result["stderr"]:
            return {
                "status": "RUNTIME_ERROR",
                "runtime": max_runtime
            }

        max_runtime = max(max_runtime, result["runtime"])

        if result["stdout"] != tc.expected_output.strip():
            return {
                "status": "WRONG_ANSWER",
                "runtime": max_runtime
            }

    return {
        "status": "ACCEPTED",
        "runtime": max_runtime
    }