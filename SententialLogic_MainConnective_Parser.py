import re

def check_wff(s):
    # Check for atomic sentence
    if re.fullmatch(r'^[A-Z]\'*$', s):
        return (True, 'atomic', s)
    
    # Check for top-level binary connective first
    balance = 0
    connective_pos = -1
    for i, c in enumerate(s):
        if c == '(':
            balance += 1
        elif c == ')':
            balance -= 1
            if balance < 0:
                return (False, None, None)
        if balance == 0 and c in ['∧', '∨', '→', '↔']:
            if connective_pos == -1:
                connective_pos = i
            else:
                return (False, None, None)  # Multiple connectives
    
    # Handle valid top-level connective
    if connective_pos != -1:
        left = s[:connective_pos]
        right = s[connective_pos+1:]
        left_valid, _, _ = check_wff(left)
        right_valid, _, _ = check_wff(right)
        if left_valid and right_valid:
            return (True, 'complex', s[connective_pos])
    
    # Check for negation
    if s.startswith('~'):
        rest_valid, _, _ = check_wff(s[1:])
        if rest_valid:
            return (True, 'complex', '~')
    
    # Check parentheses (only allowed if necessary)
    if s.startswith('(') and s.endswith(')'):
        inner = s[1:-1]
        inner_valid, _, inner_info = check_wff(inner)
        if inner_valid:
            # Reject redundant parentheses (e.g., ((P∧Q)) 
            if inner.startswith('(') and inner.endswith(')'):
                inner_inner = inner[1:-1]
                if check_wff(inner_inner)[0]:
                    return (False, None, None)  # Redundant parentheses
            return (True, 'complex', inner_info)
    
    return (False, None, None)

def process_line(line):
    stripped = re.sub(r'\s+', '', line.rstrip('\n'))
    if not stripped:
        return '∅'
    valid, _, info = check_wff(stripped)
    return info if valid else '∅'

# Process input and write output
with open('input.txt', 'r', encoding='utf-8') as infile, \
     open('output.txt', 'w', encoding='utf-8') as outfile:
    for line in infile:
        result = process_line(line)
        outfile.write(result + '\n')