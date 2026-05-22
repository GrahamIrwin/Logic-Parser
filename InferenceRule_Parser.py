import re

####################################
#  Helper Functions: Balancing and Normalization
####################################
def is_balanced(s):
    count = 0
    for char in s:
        if char == '(':
            count += 1
        elif char == ')':
            count -= 1
            if count < 0:
                return False
    return count == 0

def normalize_expr(expr):
    # Remove all whitespace
    expr = expr.replace(" ", "")
    # Remove redundant outer parentheses if they fully enclose the expression
    while expr.startswith("(") and expr.endswith(")") and is_balanced(expr[1:-1]):
        expr = expr[1:-1]
    return expr

def ensure_bracket(expr):
    """
    Ensures that expr is enclosed in a single pair of outer parentheses.
    If not, wrap it with them.
    """
    expr = expr.strip()
    if expr.startswith("(") and expr.endswith(")") and is_balanced(expr[1:-1]):
        return expr
    return "(" + expr + ")"

####################################
#  Helper Functions for WFF
####################################
def instantiate_atoms(expr, constant):
    """
    For every occurrence of an atomic sentence—
    defined as a single uppercase letter optionally followed by a lowercase letter—
    replace it with the uppercase letter followed by the provided constant.
    For example, if expr = "R ∨ R" or "Rx ∨ Ry" and constant = "x",
    both become "Rx ∨ Rx".
    """
    pattern = r'\b([A-Z])([a-z])?\b'
    return re.sub(pattern, lambda m: m.group(1) + constant, expr)

def alpha_replace(expr, alpha, beta):
    pattern = r'\b' + re.escape(alpha) + r'\b'
    return re.sub(pattern, beta, expr)

####################################
#  WFF Checker (modified)
####################################
# Parameter require_inst (default False) means:
# • if True, atomic formulas must match exactly one uppercase letter followed by one lowercase letter.
# • if False, bare uppercase letters are acceptable.
def check_wff(s, require_inst=False):
    s = s.replace(" ", "")
    # Check for atomic sentence.
    if require_inst:
        if re.fullmatch(r'^[A-Z][a-z]$', s):
            return (True, 'atomic', s)
    else:
        if re.fullmatch(r'^[A-Z](?:[a-z])?\'*$', s):
            return (True, 'atomic', s)
    
    # Check for quantifiers (∀ or ∃) at the beginning.
    if s.startswith('∀') or s.startswith('∃'):
        quant = s[0]
        rest = s[1:]
        # Expect a bound variable immediately followed by a fully parenthesized formula.
        match = re.match(r'^([a-zA-Z])(\(.*\))$', rest)
        if match:
            var, formula = match.groups()
            inner_require = True  # in a quantified WFF, atomics must be instantiated
            if formula.startswith("(") and formula.endswith(")"):
                formula_inner = formula[1:-1].strip()
            else:
                formula_inner = formula
            valid, kind, info = check_wff(formula_inner, inner_require)
            if valid:
                return (True, 'quantified', quant)
            else:
                return (False, None, None)
        else:
            return (False, None, None)
    
    # Check balanced parentheses.
    balance = 0
    for i, c in enumerate(s):
        if c == '(':
            balance += 1
        elif c == ')':
            balance -= 1
            if balance < 0:
                return (False, None, None)
    if balance != 0:
        return (False, None, None)
    
    # Remove proper matching outer parentheses.
    if s.startswith('(') and s.endswith(')'):
        balance = 0
        for i, c in enumerate(s):
            if c == '(':
                balance += 1
            elif c == ')':
                balance -= 1
            if balance == 0:
                break
        if i == len(s) - 1:
            s = s[1:-1]
    
    # Look for a top-level binary connective.
    balance = 0
    for i in range(len(s)):
        c = s[i]
        if c == '(':
            balance += 1
        elif c == ')':
            balance -= 1
        elif balance == 0 and c in ['∧', '∨', '→', '↔']:
            left = s[:i]
            right = s[i+1:]
            if check_wff(left, require_inst)[0] and check_wff(right, require_inst)[0]:
                return (True, 'complex', s[i])
    
    # Check for negation.
    if s.startswith('~'):
        valid, kind, info = check_wff(s[1:], require_inst)
        if valid:
            return (True, 'complex', '~')
    
    return (False, None, None)

def is_wff(expr, require_inst=False):
    expr = expr.replace(" ", "")
    valid, _, _ = check_wff(expr, require_inst)
    return valid

####################################
#  Inference Rule Identifier
####################################
# For each formula, if it starts with a quantifier we require its atomic formulas
# to be in instantiated form. Otherwise we use a looser check.
def beta_appears_free(beta, *args):
    return any(beta in arg for arg in args)

def identify_inference_rule(output, *inputs):
    output = output.strip()
    inputs = [inp.strip() for inp in inputs]
    
    # Process each formula using the appropriate atomic criteria.
    all_args = [output] + list(inputs)
    for arg in all_args:
        if arg.startswith('∀') or arg.startswith('∃'):
            if not is_wff(arg, True):
                return f"Not WF: {arg}"
        else:
            if not is_wff(arg, False):
                return f"Not WF: {arg}"
    
    # Helper: parse a top-level binary connective.
    def parse_binary(expr, conn):
        expr = expr.strip()
        if expr.startswith('(') and expr.endswith(')'):
            balance = 0
            for i, c in enumerate(expr):
                if c == '(':
                    balance += 1
                elif c == ')':
                    balance -= 1
                if balance == 0:
                    break
            if i == len(expr) - 1:
                expr = expr[1:-1].strip()
        balance = 0
        for i in range(len(expr)):
            if expr[i] == '(':
                balance += 1
            elif expr[i] == ')':
                balance -= 1
            elif balance == 0 and expr[i] == conn:
                left = expr[:i].strip()
                right = expr[i+1:].strip()
                return left, right
        return None, None

    # =====================================================
    # One-input rules
    # =====================================================
    if len(inputs) == 1:
        # SL: From (Φ ∧ Ψ) derive Φ.
        left, right = parse_binary(inputs[0], '∧')
        if left and normalize_expr(output) == normalize_expr(left):
            return "SL"
        # SR: From (Φ ∧ Ψ) derive Ψ.
        if right and normalize_expr(output) == normalize_expr(right):
            return "SR"
        # ADD: From Φ derive (Φ ∨ Ψ) for some Ψ.
        parsed, _ = parse_binary(output, '∨')
        if parsed and normalize_expr(parsed) == normalize_expr(inputs[0]):
            return "ADD"
        # BC: From (Φ↔Ψ) derive (Φ→Ψ)∧(Ψ→Φ).
        left_bi, right_bi = parse_binary(inputs[0], '↔')
        if left_bi and normalize_expr(output) == normalize_expr(f"({left_bi}→{right_bi})∧({right_bi}→{left_bi})"):
            return "BC"
        # CB: From (Φ→Ψ)∧(Ψ→Φ) derive Φ↔Ψ.
        bi_left, bi_right = parse_binary(output, '↔')
        if bi_left and normalize_expr(inputs[0]) == normalize_expr(f"({bi_left}→{bi_right})∧({bi_right}→{bi_left})"):
            return "CB"
        # DNI: From Φ derive ~~Φ.
        if normalize_expr(output) == normalize_expr("~~" + inputs[0]):
            return "DNI"
        # DNE: From ~~Φ derive Φ.
        if inputs[0].startswith("~~") and normalize_expr(output) == normalize_expr(inputs[0][2:]):
            return "DNE"
        # UI: From ∀αΦ derive Φ(α/β) where β does not occur in Φ.
        m = re.match(r'^∀([a-zA-Z])(\(.*\))$', inputs[0])
        if m:
            alpha, phi = m.groups()
            if phi.startswith("(") and phi.endswith(")"):
                phi = phi[1:-1].strip()
            if alpha not in phi:  # vacuous case
                if normalize_expr(output) == normalize_expr(phi):
                    return "UI"
                else:
                    return "No rule found"
            else:
                for beta in "abc":
                    if normalize_expr(output) == normalize_expr(instantiate_atoms(phi, beta)):
                        return "UI"
                return "No rule found"
        # EG: From Φ derive ∃αΦ(α/α) by instantiating each atomic with the bound variable.
        m = re.match(r'^∃([a-zA-Z])(\(.*\))$', output)
        if m:
            alpha, _ = m.groups()
            # Expected: the output should equal "∃{alpha}" concatenated with the instantiation of input[0] using alpha.
            expected = f"∃{alpha}" + ensure_bracket(instantiate_atoms(inputs[0], alpha))
            if normalize_expr(output) == normalize_expr(expected):
                return "EG"
            else:
                return "No rule found"
        # EI: From ∃αΦ derive Φ(α/β), with β not in Φ.
        m = re.match(r'^∃([a-zA-Z])(\(.*\))$', inputs[0])
        if m:
            alpha, phi_body = m.groups()
            if phi_body.startswith("(") and phi_body.endswith(")"):
                phi_body = phi_body[1:-1].strip()
            if alpha not in phi_body:
                if normalize_expr(output) == normalize_expr(phi_body):
                    return "EI"
                else:
                    return "No rule found"
            else:
                for beta in "abc":
                    if normalize_expr(output) == normalize_expr(instantiate_atoms(phi_body, beta)):
                        return "EI"
                return "No rule found"
    
    # =====================================================
    # Two-input rules
    # =====================================================
    if len(inputs) == 2:
        # ADJ: From Φ and Ψ derive (Φ ∧ Ψ).
        if normalize_expr(output) == normalize_expr(f"({inputs[0]}∧{inputs[1]})"):
            return "ADJ"
        # MP: From (Φ → Ψ) and Φ derive Ψ.
        left_imp, right_imp = parse_binary(inputs[0], '→')
        if left_imp and normalize_expr(inputs[1]) == normalize_expr(left_imp) and normalize_expr(output) == normalize_expr(right_imp):
            return "MP"
        # MT: From (Φ → Ψ) and ~Ψ derive ~Φ.
        if left_imp:
            if normalize_expr(inputs[1]) == normalize_expr("~" + right_imp) and normalize_expr(output) == normalize_expr("~" + left_imp):
                return "MT"
        # DSL: From (Φ ∨ Ψ) and ~Ψ derive Φ.
        left_or, right_or = parse_binary(inputs[0], '∨')
        if left_or and right_or:
            if normalize_expr(inputs[1]) == normalize_expr("~" + right_or) and normalize_expr(output) == normalize_expr(left_or):
                return "DSL"
        # DSR: From (Φ ∨ Ψ) and ~Φ derive Ψ.
        if left_or and right_or:
            if normalize_expr(inputs[1]) == normalize_expr("~" + left_or) and normalize_expr(output) == normalize_expr(right_or):
                return "DSR"
        # EI with extra premise:
        m = re.match(r'^∃([a-zA-Z])(\(.*\))$', inputs[0])
        if m:
            alpha, phi_body = m.groups()
            if phi_body.startswith("(") and phi_body.endswith(")"):
                phi_body = phi_body[1:-1].strip()
            if alpha not in phi_body:
                if normalize_expr(output) == normalize_expr(phi_body):
                    return "EI"
                else:
                    return "No rule found"
            else:
                for beta in "abc":
                    if normalize_expr(output) == normalize_expr(instantiate_atoms(phi_body, beta)):
                        if beta_appears_free(beta, inputs[1]):
                            return "No rule found"
                        return "EI"
                return "No rule found"
    
    # =====================================================
    # Three-input rules (only EI with extra premises)
    # =====================================================
    if len(inputs) == 3:
        m = re.match(r'^∃([a-zA-Z])(\(.*\))$', inputs[0])
        if m:
            alpha, phi_body = m.groups()
            if phi_body.startswith("(") and phi_body.endswith(")"):
                phi_body = phi_body[1:-1].strip()
            if alpha not in phi_body:
                if normalize_expr(output) == normalize_expr(phi_body):
                    return "EI"
                else:
                    return "No rule found"
            else:
                for beta in "abc":
                    if normalize_expr(output) == normalize_expr(instantiate_atoms(phi_body, beta)):
                        if beta_appears_free(beta, inputs[1], inputs[2]):
                            return "No rule found"
                        return "EI"
                return "No rule found"
    
    return "No rule found"

####################################
#  Main Routine: Process Input
####################################
if __name__ == "__main__":
    with open("input_inference.txt", "r", encoding="utf-8") as infile, \
         open("output_inference.txt", "w", encoding="utf-8") as outfile:
        lines = [line.strip() for line in infile if line.strip()]
        grouped = []
        i = 0
        while i < len(lines):
            if lines[i].startswith("Output:"):
                output = lines[i].replace("Output:", "").strip()
                i += 1
                inputs = []
                while i < len(lines) and lines[i].startswith("Input"):
                    inputs.append(lines[i].split(":", 1)[1].strip())
                    i += 1
                grouped.append((output, inputs))
            else:
                i += 1

        for output, inputs in grouped:
            result = identify_inference_rule(output, *inputs)
            outfile.write(result + "\n")
