import json


# Mocked LLM
class MockLLM:
    def __init__(self, responses: list[str]):
        self.responses = responses
        self.i = 0

    def generate(self, state: dict) -> str:
        r = self.responses[self.i]
        self.i += 1
        return r


# Tools Methods
def print_hi(name):
    print(f'Hi, {name}')

def add_numbers(a: int, b: int) -> dict:
    return {"result": a + b}


# Tools Registry
TOOLS = {
    "add_numbers": add_numbers,
}


# Agent
def run_agent(llm: MockLLM, prompt: str, max_steps: int = 3) -> str:
    state = {"prompt": prompt, "tool_results": []}

    for _ in range(max_steps):
        raw = llm.generate(state)
        msg = json.loads(raw) # JSON -> dict

        if msg["type"] == "tool_call":
            tool = TOOLS[msg["tool_name"]]
            result = tool(**msg["args"])
            state["tool_results"].append(result)
            continue

        if msg["type"] == "final":
            return msg["answer"]

    return "Max steps exceeded"


# Entry Point
def main():
    llm = MockLLM([
        '{"type":"tool_call","tool_name":"add_numbers","args":{"a":2,"b":3}}',
        '{"type":"final","answer":"2 + 3 = 5"}'
    ])

    answer = run_agent(llm, "Sum 2 and 3", max_steps=3)
    print(answer)


if __name__ == '__main__':
    main()
