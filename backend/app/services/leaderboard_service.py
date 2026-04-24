import time
from app.core.redis import redis_client


def update_leaderboard(contest_id, user_id, problem_id, runtime):
    solved_key = f"contest:{contest_id}:user:{user_id}:solved"
    board_key = f"contest:{contest_id}:leaderboard"

    # already solved? ignore duplicate AC
    if redis_client.sismember(solved_key, problem_id):
        return

    redis_client.sadd(solved_key, problem_id)

    solved_count = redis_client.scard(solved_key)

    prev_runtime = redis_client.hget(
        board_key + ":meta",
        f"{user_id}:runtime"
    )

    prev_runtime = float(prev_runtime or 0)

    total_runtime = prev_runtime + runtime

    redis_client.hset(
        board_key + ":meta",
        f"{user_id}:runtime",
        total_runtime
    )

    redis_client.hset(
        board_key + ":meta",
        f"{user_id}:time",
        time.time()
    )

    score = solved_count * 1000000 - int(total_runtime * 1000)

    redis_client.zadd(
        board_key,
        {str(user_id): score}
    )


def get_leaderboard(contest_id):
    board_key = f"contest:{contest_id}:leaderboard"

    users = redis_client.zrevrange(
        board_key,
        0,
        -1,
        withscores=True
    )

    result = []

    rank = 1

    for user_id, score in users:

        solved_key = f"contest:{contest_id}:user:{user_id}:solved"

        solved = redis_client.scard(solved_key)

        runtime = redis_client.hget(
            board_key + ":meta",
            f"{user_id}:runtime"
        )

        result.append({
            "rank": rank,
            "user_id": int(user_id),
            "solved": solved,
            "runtime": float(runtime or 0)
        })

        rank += 1

    return result