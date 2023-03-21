import openai
import re

openai.api_key = "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"

def generate_solution(prompt):
    """Generate a solution to the coding question using the GPT-3 API."""
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.5,
    )
    solution = response.choices[0].text.strip()
    return solution

def parse_solution(solution):
    """Parse the generated solution and return Python code."""
    # Remove any non-Python code
    solution = re.sub(r"([^\n]*#.*\n?)|(\n?[^\n]*return.*\n?)", "", solution)
    # Add indentations
    solution = re.sub(r"^", "    ", solution, flags=re.M)
    # Add function definition and comments
    function_definition = re.match(r"def (.*)\(", solution).group(0)
    comments = f"'''{solution.strip()}\n'''"
    code = f"{function_definition}\n{comments}\n{solution}"
    return code

def generate_code(prompt):
    """Generate Python code for the coding question."""
    solution = generate_solution(prompt)
    code = parse_solution(solution)
    return code

# Example usage
prompt = "Given an array of integers, find two numbers such that they add up to a specific target."
code = generate_code(prompt)
print(code)
