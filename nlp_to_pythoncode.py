import re

# ============================================================================
# SIMPLE NATURAL LANGUAGE TO PYTHON CODE GENERATOR
# ============================================================================
# How it works:
# 1. Takes English instruction as input (e.g., "print hello")
# 2. Matches it against predefined patterns
# 3. Converts to Python code using the matched pattern
# 4. Returns the generated Python code
# ============================================================================

def generate_python_code(instruction: str) -> str:
    """
    Convert simple English instructions to Python code.
    
    RULE FORMAT:
    (pattern, transformation_function)
    
    pattern: Regex pattern to match the instruction
    transformation_function: Converts matched groups to Python code
    
    The FIRST matching pattern is used.
    """
    
    # Convert to lowercase and remove extra spaces
    instruction = instruction.lower().strip()
    
    # If empty instruction
    if not instruction:
        return "# Please enter an instruction"
    
    # ========================================================================
    # DEFINE ALL PATTERNS AND THEIR TRANSFORMATIONS
    # ========================================================================
    # Order matters! First match wins.
    
    rules = [
        # --------------------------------------------------------------------
        # PATTERN 1: Print plain text
        # --------------------------------------------------------------------
        # Matches: "print hello" or "print good morning"
        # Groups: The text after "print"
        (
            r"print (.+)",  # Pattern
            lambda m: 'print("{}")'.format(m.group(1))  # Transformation
        ),
        
        # --------------------------------------------------------------------
        # PATTERN 2: Print numbers in range
        # --------------------------------------------------------------------
        # Matches: "print numbers from 1 to 10"
        # Groups: start number (1), end number (10)
        (
            r"print numbers from (\d+) to (\d+)",
            lambda m: "for i in range({}, {}):\n    print(i)".format(
                int(m.group(1)),  # Start
                int(m.group(2)) + 1  # End + 1 (to include last number)
            )
        ),
        
        # --------------------------------------------------------------------
        # PATTERN 3: Basic math operations
        # --------------------------------------------------------------------
        # Matches: "add 5 and 3" or "multiply 4 and 6"
        # Groups: operation, first number, second number
        (
            r"(add|subtract|multiply|divide) (\d+) and (\d+)",
            lambda m: "print({} {} {})".format(
                m.group(2),  # First number
                {  # Convert word to operator symbol
                    "add": "+",
                    "subtract": "-", 
                    "multiply": "*",
                    "divide": "/"
                }[m.group(1)],  # Operation symbol
                m.group(3)  # Second number
            )
        ),
        
        # --------------------------------------------------------------------
        # PATTERN 4: Create a list
        # --------------------------------------------------------------------
        # Matches: "create list 1,2,3" or "create list apple,banana"
        # Groups: Comma-separated values
        (
            r"create list (.+)",
            lambda m: "my_list = [{}]".format(
                ", ".join(
                    # Add quotes if value is not a number
                    '"{}"'.format(val.strip()) if not val.strip().isdigit()
                    else val.strip()
                    for val in m.group(1).split(",")
                )
            )
        ),
        
        # --------------------------------------------------------------------
        # PATTERN 5: Append to list
        # --------------------------------------------------------------------
        # Matches: "append 5 to list" or "append hello to list"
        (
            r"append (.+) to list",
            lambda m: 'my_list.append("{}")'.format(m.group(1))
            if not m.group(1).isdigit()
            else "my_list.append({})".format(m.group(1))
        ),
        
        # --------------------------------------------------------------------
        # PATTERN 6: Sort list
        # --------------------------------------------------------------------
        (r"sort list", lambda _: "my_list.sort()"),
        
        # --------------------------------------------------------------------
        # PATTERN 7: Print list
        # --------------------------------------------------------------------
        (r"print list", lambda _: "print(my_list)"),
        
        # --------------------------------------------------------------------
        # PATTERN 8: Square a number
        # --------------------------------------------------------------------
        (r"square (\d+)", lambda m: "print({} ** 2)".format(m.group(1))),
        
        # --------------------------------------------------------------------
        # PATTERN 9: Create a string
        # --------------------------------------------------------------------
        (
            r"create string (.+)",
            lambda m: 'my_string = "{}"'.format(m.group(1))
        ),
        
        # --------------------------------------------------------------------
        # PATTERN 10: Convert string to uppercase
        # --------------------------------------------------------------------
        (r"uppercase string", lambda _: 'my_string = my_string.upper()'),
        
        # --------------------------------------------------------------------
        # PATTERN 11: Print string
        # --------------------------------------------------------------------
        (r"print string", lambda _: "print(my_string)"),
        
        # --------------------------------------------------------------------
        # PATTERN 12: Create a dictionary
        # --------------------------------------------------------------------
        # Matches: "create dictionary name:john, age:25"
        # Groups: Comma-separated key:value pairs
        (
            r"create dictionary (.+)",
            lambda m: "my_dict = {" + ", ".join(
                # Format each key:value pair
                '"{}": {}'.format(
                    key.strip(),  # Key (always string with quotes)
                    # Value: add quotes if not a number
                    '"{}"'.format(val.strip()) if not val.strip().isdigit()
                    else val.strip()
                )
                for pair in m.group(1).split(",")
                for key, val in [pair.split(":")]
            ) + "}"
        ),
        
        # --------------------------------------------------------------------
        # PATTERN 13: Print dictionary
        # --------------------------------------------------------------------
        (r"print dictionary", lambda _: "print(my_dict)"),
        
        # --------------------------------------------------------------------
        # PATTERN 14: Simple if condition
        # --------------------------------------------------------------------
        # Matches: "if x equals 10 then print correct"
        # Groups: variable, value, message
        (
            r"if (\w+) equals (\d+) then print (.+)",
            lambda m: 'if {} == {}: print("{}")'.format(
                m.group(1), m.group(2), m.group(3)
            )
        ),
        
        # --------------------------------------------------------------------
        # PATTERN 15: Loop through list
        # --------------------------------------------------------------------
        (r"loop list", lambda _: "for item in my_list:\n    print(item)"),
        
        # --------------------------------------------------------------------
        # PATTERN 16: Get user input
        # --------------------------------------------------------------------
        (
            r"ask input (.+)",
            lambda m: 'user_input = input("{}")'.format(m.group(1))
        ),
        
        # --------------------------------------------------------------------
        # PATTERN 17: Help command
        # --------------------------------------------------------------------
        (
            r"help|show commands",
            lambda _: '''# Available commands:
# print [text]  - Print any text
# print numbers from X to Y - Print range of numbers
# add/subtract/multiply/divide X and Y - Math operations
# create list X,Y,Z - Create a list
# append X to list - Add to list
# sort list - Sort the list
# print list - Print the list
# square X - Square a number
# create string X - Create a string
# uppercase string - Convert to uppercase
# print string - Print the string
# create dictionary key:value - Create dictionary
# print dictionary - Print dictionary
# if X equals Y then print Z - Simple if statement
# loop list - Loop through list
# ask input [message] - Get user input
# help - Show this message'''
        ),
    ]
    
    # ========================================================================
    # MATCH INSTRUCTION AGAINST RULES
    # ========================================================================
    
    for pattern, action in rules:
        # Try to match the instruction with current pattern
        match = re.fullmatch(pattern, instruction)
        
        if match:
            # If match found, execute the transformation function
            return action(match)
    
    # ========================================================================
    # NO MATCH FOUND
    # ========================================================================
    
    return "# I don't understand. Type 'help' for available commands."


# ============================================================================
# TEST THE CODE GENERATOR
# ============================================================================

def test_generator():
    """Test the code generator with sample instructions."""
    
    print("=" * 60)
    print("NATURAL LANGUAGE TO PYTHON CODE GENERATOR")
    print("=" * 60)
    
    # Test cases with expected outputs
    test_cases = [
        ("print hello world", 'print("hello world")'),
        ("print numbers from 1 to 5", "for i in range(1, 6):\n    print(i)"),
        ("add 10 and 20", "print(10 + 20)"),
        ("create list 1,2,3,4,5", "my_list = [1, 2, 3, 4, 5]"),
        ("append 6 to list", "my_list.append(6)"),
        ("sort list", "my_list.sort()"),
        ("print list", "print(my_list)"),
        ("square 5", "print(5 ** 2)"),
        ("create string hello python", 'my_string = "hello python"'),
        ("uppercase string", 'my_string = my_string.upper()'),
        ("print string", "print(my_string)"),
        ("create dictionary name:john, age:25", 'my_dict = {"name": "john", "age": 25}'),
        ("print dictionary", "print(my_dict)"),
        ("if x equals 10 then print correct", 'if x == 10: print("correct")'),
        ("loop list", "for item in my_list:\n    print(item)"),
        ("ask input Enter your name:", 'user_input = input("Enter your name:")'),
        ("help", "# Available commands:"),  # Truncated for brevity
    ]
    
    # Run tests
    for instruction, expected in test_cases:
        print(f"\nInstruction: {instruction}")
        print("-" * 40)
        result = generate_python_code(instruction)
        print(f"Generated: {result}")
        
        # Check if result contains expected pattern
        if expected in result:
            print("✓ Test PASSED")
        else:
            print("✗ Test FAILED")
            print(f"Expected to contain: {expected}")
    
    print("\n" + "=" * 60)
    print("INTERACTIVE MODE - Try your own instructions!")
    print("Type 'exit' to quit")
    print("=" * 60)

# ============================================================================
# MAIN PROGRAM
# ============================================================================

if __name__ == "__main__":
    # Run tests first
    test_generator()
    
    # Interactive mode
    while True:
        try:
            user_input = input("\nYour instruction: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("Goodbye!")
                break
            
            code = generate_python_code(user_input)
            print("\nGenerated Python code:")
            print("-" * 40)
            print(code)
            print("-" * 40)
            
            # Option to execute the code
            if input("\nRun this code? (y/n): ").lower() == 'y':
                try:
                    # Safe execution environment
                    exec_env = {
                        'my_list': [],
                        'my_string': '',
                        'my_dict': {},
                    }
                    
                    exec(code, exec_env)
                    print("✓ Code executed successfully!")
                    
                except Exception as e:
                    print(f"✗ Error: {e}")
                    print("Tip: Make sure to create variables before using them!")
                    
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break