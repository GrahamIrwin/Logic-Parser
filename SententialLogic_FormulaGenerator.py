import random

# Configurable parameters
NUM_WFF = 1000           # Total number of valid formulas to generate
NUM_INVALID = 0        # Hardcoded number of malformed formulas
MIN_CONNECTIVES = 0      # Minimum number of connectives per formula
MAX_CONNECTIVES = 3      # Maximum number of connectives per formula
OUTPUT_FILE = "input_sentential.txt"

# Valid components
ATOMICS = ['P', 'Q', 'R', 'S', 'T']
CONNECTIVES = ['∧', '∨', '→', '↔']
NEGATION = '~'

def generate_atomic():
    """Generate a simple atomic sentence"""
    return random.choice(ATOMICS)

def generate_wff(connectives_left):
    """Recursively generate a WFF with exact number of connectives"""
    if connectives_left == 0:
        return generate_atomic()
    
    if random.random() < 0.2:
        return NEGATION + generate_wff(connectives_left - 1)
    else:
        conn = random.choice(CONNECTIVES)
        remaining = connectives_left - 1
        left_conn = random.randint(0, remaining) if remaining > 0 else 0
        right_conn = remaining - left_conn
        
        left = generate_wff(left_conn)
        right = generate_wff(right_conn)
        return f"({left} {conn} {right})"

def generate_invalid_from_valid(valid_expression):
    """Generate an invalid expression by modifying a valid one."""
    if not valid_expression:
        return valid_expression
    
    choice = random.random()
    if choice < 0.5:
        insert_pos = random.randint(0, len(valid_expression))
        replacement_char = random.choice(ATOMICS + CONNECTIVES + ['(', ')'])
        invalid_expression = valid_expression[:insert_pos] + replacement_char + valid_expression[insert_pos:]
    else:
        non_space_indices = [i for i, char in enumerate(valid_expression) if char != ' ']
        if not non_space_indices:
            return valid_expression
        pos = random.choice(non_space_indices)
        char_to_swap = valid_expression[pos]
        
        if char_to_swap in ATOMICS:
            replacement_char = random.choice(CONNECTIVES + [NEGATION])
        elif char_to_swap in CONNECTIVES:
            replacement_char = random.choice(ATOMICS + [NEGATION])
        elif char_to_swap == NEGATION:
            replacement_char = random.choice(ATOMICS + CONNECTIVES)
        else:
            replacement_char = random.choice(ATOMICS + CONNECTIVES + [NEGATION])
        
        invalid_expression = valid_expression[:pos] + replacement_char + valid_expression[pos+1:]
    
    return invalid_expression

def generate_test_cases():
    """Generate valid and invalid test cases"""
    cases = []
    
    for _ in range(NUM_WFF):
        num_conn = random.randint(MIN_CONNECTIVES, MAX_CONNECTIVES)
        wff = generate_wff(num_conn)
        cases.append(wff)
    
    for _ in range(NUM_INVALID):
        valid_expression = generate_wff(random.randint(MIN_CONNECTIVES, MAX_CONNECTIVES))
        invalid_expression = generate_invalid_from_valid(valid_expression)
        cases.append(invalid_expression)
    
    random.shuffle(cases)
    return cases

if __name__ == "__main__":
    test_cases = generate_test_cases()
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for case in test_cases:
            f.write(case + '\n')
    print(f"Generated {len(test_cases)} test cases ({NUM_WFF} valid + {NUM_INVALID} invalid) in {OUTPUT_FILE}")
