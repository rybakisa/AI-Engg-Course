import sys


def multiply(a, b):
    """
    Return {"result": a * b}
    """
    return { "result": a * b }


def classify_request(state):
    """
    If 'calculate' is in user_request -> intent = 'math'
    Otherwise -> intent = 'greeting'
    """
    if "calculate" in state["user_request"]:
        return "math"
    else:
        return "greeting"


def math_node(state):
    """
    Use multiply(a, b) and return:
    {"final_answer": "Math result: <result>"}
    """
    res = multiply(state["a"], state["b"])["result"]
    return {"final_answer": f"Math result: {res}"}


def greeting_node(state):
    """
    Return:
    {"final_answer": "Hello from greeting flow"}
    """
    return {"final_answer": "Hello from greeting flow"}


def route_by_intent(state):
    """
    If intent == 'math' -> return 'math_node'
    Else -> return 'greeting_node'
    """
    intent = state["intent"]
    if intent == "math":
        return math_node
    else:
        return greeting_node


def merge_state(state, updates):
    state.update(updates)
    return state


def run_dag_agent(user_request, a, b):
    state = {
        "user_request": user_request,
        "a": a,
        "b": b,
        "intent": None,
        "final_answer": None
    }

    intent = classify_request(state)
    state = merge_state(state, {"intent": intent})

    next_node = route_by_intent(state)
    node_res = next_node(state)

    return node_res["final_answer"]


def main():
    user_request = sys.stdin.readline().strip()
    a = int(sys.stdin.readline().strip())
    b = int(sys.stdin.readline().strip())

    print(run_dag_agent(user_request, a, b))


if __name__ == "__main__":
    main()
