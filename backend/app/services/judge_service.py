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
                "docker", "run", "-i",
                "--rm",
                "--network", "none",
                "--memory", "128m",
                "--cpus", "0.5",
                "-v", f"{folder}:/code",
                "codejudge-python"
            ],
            input=(input_data or "") + "\n",
            text=True,
            capture_output=True,
            timeout=timeout_sec
        )

        runtime = round(time.time() - start, 3)

        return {
            "stdout": (result.stdout or "").strip(),
            "stderr": (result.stderr or "").strip(),
            "runtime": runtime,
            "returncode": result.returncode
        }

    except subprocess.TimeoutExpired as e:
        runtime = round(time.time() - start, 3)
        return {
            "timeout": True,
            "runtime": runtime,
            "stdout": "",
            "stderr": f"timeout: {str(e)}",
            "returncode": None
        }


def judge_submission(problem_id, language, code, db: Session, stop_on_first_failure=True):
    if language != "python":
        return {
            "status": "LANGUAGE_NOT_SUPPORTED",
            "runtime": 0,
            "passed_count": 0,
            "failed_count": 0,
            "total": 0
        }

    tests = db.query(TestCase).filter(
        TestCase.problem_id == problem_id
    ).all()

    if not tests:
        return {
            "status": "NO_TESTS",
            "runtime": 0,
            "passed_count": 0,
            "failed_count": 0,
            "total": 0
        }

    total = len(tests)
    passed = 0
    failed = 0
    max_runtime = 0

    for tc in tests:
        result = run_python(code, tc.input_data)

        timeout = result.get("timeout")
        stderr = (result.get("stderr") or "").strip()
        stdout = (result.get("stdout") or "").strip()
        runtime = result.get("runtime", 0)
        max_runtime = max(max_runtime, runtime)

        if timeout:
            failed += 1
            if stop_on_first_failure:
                return {
                    "status": "TIME_LIMIT_EXCEEDED",
                    "runtime": max_runtime,
                    "passed_count": passed,
                    "failed_count": failed,
                    "total": total
                }
            continue

        if stderr:
            failed += 1
            if stop_on_first_failure:
                return {
                    "status": "RUNTIME_ERROR",
                    "runtime": max_runtime,
                    "passed_count": passed,
                    "failed_count": failed,
                    "total": total,
                    "details": stderr
                }
            continue

        if stdout != tc.expected_output.strip():
            failed += 1
            if stop_on_first_failure:
                return {
                    "status": "WRONG_ANSWER",
                    "runtime": max_runtime,
                    "passed_count": passed,
                    "failed_count": failed,
                    "total": total,
                    "details": {"expected": tc.expected_output.strip(), "got": stdout}
                }
            continue

        passed += 1

    # final overall status
    status = "ACCEPTED" if failed == 0 else "WRONG_ANSWER"
    return {
        "status": status,
        "runtime": max_runtime,
        "passed_count": passed,
        "failed_count": failed,
        "total": total
    }