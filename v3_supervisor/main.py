import sys


def supervisor_route(state):
    """
    If 'reverse' is in user_request -> task_type = 'reverse'
    Otherwise -> task_type = 'length'
    """
    req = state["user_request"]
    if "reverse" in req:
        return { "task_type": "reverse" }

    return { "task_type": "length" }


def reverse_worker(state):
    """
    Return:
    {"worker_result": "Reversed: <reversed payload>"}
    """
    return { "worker_result": f'Reversed: { state["payload"][::-1] }' }


def length_worker(state):
    """
    Return:
    {"worker_result": "Length: <len(payload)>"}
    """
    return { "worker_result": f'Length: { len(state["payload"]) }' }


def supervisor_finalize(state):
    """
    Return:
    {"final_answer": state["worker_result"]}
    """
    return {"final_answer": state["worker_result"]}


def merge_state(state, updates):
    state.update(updates)
    return state

def choose_worker(state):
    if state["task_type"] == "reverse":
        return reverse_worker

    return length_worker


def run_supervisor_worker_agent(user_request, payload):
    state = {
        "user_request": user_request,
        "payload": payload,
        "task_type": None,
        "worker_result": None,
        "final_answer": None
    }

    # 1. supervisor_route
    state = merge_state(state, supervisor_route(state))
    # 2. choose correct worker
    worker = choose_worker(state)
    state = merge_state(state, worker(state))
    # 3. supervisor_finalize
    state = merge_state(state, supervisor_finalize(state))
    # 4. return final_answer
    return state["final_answer"]


def main():
    user_request = sys.stdin.readline().strip()
    payload = sys.stdin.readline().rstrip("\n")

    print(run_supervisor_worker_agent(user_request, payload))


if __name__ == "__main__":
    main()
