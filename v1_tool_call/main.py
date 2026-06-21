import json
import sys


def multiply(a, b):
    """
    Multiply two integers and return a dict:
    {"result": a*b}
    """
    return {"result": a * b}


TOOLS = {
    "multiply": multiply,
}


class MockLLM:
    def __init__(self, responses):
        self.responses = responses
        self.i = 0

    def generate(self, state):
        """
        Return next JSON string from responses.
        """
        r = self.responses[self.i]
        self.i += 1
        return r


def run_agent(llm, prompt, max_steps=10):
    """
    Minimal ReAct agent:
    - reads JSON from llm.generate()
    - supports type: tool_call and final
    - calls tools
    - replaces {{key}} in final answer using last tool result
    - returns:
        - final answer (string)
        - "Tool not found"
        - "Max steps exceeded"
    """
    state = {"prompt": prompt, "tool_results": []}

    for _ in range(max_steps):
        llm_resp = json.loads(llm.generate(state))

        resp_type = llm_resp.get("type", None)
        if not resp_type:
            return "No type in LLM response"

        if resp_type == "tool_call":
            tool = TOOLS.get(llm_resp.get("tool_name", None), None)
            if not tool:
                return "Tool not found"

            tool_res = tool(**llm_resp["args"])
            state["tool_results"].append(tool_res)
            continue

        if resp_type == "final":
            answer = llm_resp.get("answer", None)
            if answer:
                return answer.replace("{{result}}", str(state["tool_results"][0]["result"]))

    return "Max steps exceeded"


def main():
    """
    Input format:
    line 1: prompt
    line 2: n (number of responses)
    next n lines: JSON strings
    """

    prompt = sys.stdin.readline().rstrip("\n")
    n_line = sys.stdin.readline().strip()
    n = int(n_line) if n_line else 0

    responses = []
    for _ in range(n):
        responses.append(sys.stdin.readline().strip())

    llm = MockLLM(responses)

    result = run_agent(llm, prompt, max_steps=10)
    print(result)


if __name__ == "__main__":
    main()
