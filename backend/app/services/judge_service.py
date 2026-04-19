import time

def judge_submission(code: str, language: str):
    """
    Temporary mock judge.
    Docker integration next upgrade.
    """

    start = time.time()

    time.sleep(1)

    runtime = round(time.time() - start, 3)

    if "return" in code or "print" in code:
        return {
            "status": "ACCEPTED",
            "runtime": runtime
        }

    return {
        "status": "WRONG_ANSWER",
        "runtime": runtime
    }