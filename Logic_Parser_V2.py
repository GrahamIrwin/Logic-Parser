import re

def is_well_formed(expression):
    """
    Check if the expression is a well-formed sentential logic expression.
    """
    expression = expression.replace(" ", "").replace("\t", "")  # Remove spaces/tabs
    
    if not expression:
        return False, None
    
    if len(expression) == 1 and expression.isalpha() and expression.isupper():
        return True, expression  # Atomic sentence (must be a single letter)
    
    if not is_balanced(expression):
        return False, None  # Unbalanced parentheses
    
    if has_invalid_operators(expression):
        return False, None  # Detect malformed logical operators
    
    main_connective = get_main_connective(expression)
    return (True, main_connective) if main_connective else (False, None)

def is_balanced(expression):
    """Check if parentheses are balanced."""
    stack = []
    for char in expression:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                return False
            stack.pop()
    return not stack

def has_invalid_operators(expression):
    """
    Check for misplaced or duplicated logical operators (excluding valid repeated negations).
    Also ensure that logical operators have valid operands on both sides.
    """
    invalid_patterns = [
        r'\(\)',  # Empty parentheses
        r'∧∧', r'∨∨', r'→→',  # Duplicated operators
        r'~[∧∨→]', r'[∧∨→]~',  # Misplaced negation
        r'^[∧∨→]', r'[∧∨→]$',  # Operators at the start or end
        r'\)\(',  # Misplaced parentheses
        r'[A-Z]{2,}',  # Multiple letters without operators
        r'\([∧∨→]', r'[∧∨→]\)',  # Operators directly inside parentheses
        r'\([^()]*[∧∨→][^()]*\)',  # Operators inside parentheses without valid operands
    ]
    return any(re.search(pattern, expression) for pattern in invalid_patterns)

def get_main_connective(expression):
    """
    Extract the main connective from a well-formed complex sentence.
    """
    expression = expression.strip()
    
    # Remove outer parentheses if they enclose the entire expression
    while expression.startswith('(') and expression.endswith(')') and is_balanced(expression[1:-1]):
        expression = expression[1:-1]
    
    # Handle multiple negations (~) at the start
    while expression.startswith('~'):
        expression = expression[1:]
        if is_well_formed(expression)[0]:
            return '~'  # Unary operator remains the main connective
    
    stack = 0
    main_op = None
    main_op_index = -1
    
    for i, char in enumerate(expression):
        if char == '(':
            stack += 1
        elif char == ')':
            stack -= 1
        elif char in {'∧', '∨', '→'} and stack == 0:
            return char  # Return the first main connective found outside parentheses
    
    return None

def process_file(input_file, output_file):
    """
    Process the input file and write the results to the output file.
    """
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            line = line.strip()
            if not line:
                continue
            
            well_formed, result = is_well_formed(line)
            outfile.write(result if well_formed else '∅')
            outfile.write('\n')

# Example usage
input_file = 'input.txt'
output_file = 'output.txt'
process_file(input_file, output_file)