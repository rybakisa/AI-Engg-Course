import sys


def fake_order_api(order_id):
    """
    Mock API:
    - ORD-1 -> shipped
    - ORD-2 -> processing
    - otherwise -> not_found
    """
    if order_id == "ORD-1":
        return {
            "status_code": 200,
            "json": {
                "id": "ORD-1",
                "status": "shipped"
            }
        }

    if order_id == "ORD-2":
        return {
            "status_code": 200,
            "json": {
                "id": "ORD-2",
                "status": "processing"
            }
        }

    return {
        "status_code": 404,
        "json": {"error": "not_found"}
    }


def get_order_by_id(order_id):
    """
    Wrap fake_order_api and return:
    - {"ok": True, "order": ...}
    - {"ok": False, "error": ...}
    """
    response = fake_order_api(order_id)

    if response["status_code"] == 200:
        return {"ok": True, "order": response["json"]}

    if response["status_code"] > 400:
        return {"ok": False, "error": response["json"]}

    return {"ok": False, "error": "api_error"}


def fetch_order_node(state):
    """
    Call get_order_by_id and update state fields:
    - order_data
    - api_error
    """
    order = get_order_by_id(state["order_id"])
    if order["ok"]:
        return {"order_data": order["order"]}
    else:
        return {"order": None, "api_error": order["error"]}


def route_order_result(state):
    """
    If order_data exists -> build_found_answer
    Else -> build_not_found_answer
    """
    if state["order_data"]:
        return build_found_answer
    else:
        return build_not_found_answer


def build_found_answer(state):
    """
    Return:
    {"final_answer": "Order found: <status>"}
    """
    order = state["order_data"]
    return { "final_answer": f'Order found: {order["status"]}' }


def build_not_found_answer(state):
    """
    Return:
    {"final_answer": "Order not found"}
    """
    return {"final_answer": "Order not found"}


def merge_state(state, updates):
    state.update(updates)
    return state


def run_order_agent(order_id):
    state = {
        "order_id": order_id,
        "order_data": None,
        "api_error": None,
        "final_answer": None
    }

    state = merge_state(state, fetch_order_node(state))
    next_node = route_order_result(state)

    if next_node == build_found_answer:
        state = merge_state(state, build_found_answer(state))
    else:
        state = merge_state(state, build_not_found_answer(state))

    return state["final_answer"]


def main():
    order_id = sys.stdin.readline().strip()
    print(run_order_agent(order_id))


if __name__ == "__main__":
    main()
