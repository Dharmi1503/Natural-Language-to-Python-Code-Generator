import re

def generate_python_code(instruction):
    instruction = instruction.lower()

    # Rule 1: Print numbers from X to Y
    match = re.search(r'print numbers from (\d+) to (\d+)', instruction)
    if match:
        start = match.group(1)
        end = match.group(2)
        return f"""for i in range({start}, {int(end)+1}):
    print(i)"""

    # Rule 2: Print a message
    match = re.search(r'print (.+)', instruction)
    if match:
        message = match.group(1)
        return f'print("{message}")'

    return "# Instruction not recognized"


# ---- Main Program ----
user_input = input("Enter instruction: ")
python_code = generate_python_code(user_input)

print("\nGenerated Python Code:\n")
print(python_code)
