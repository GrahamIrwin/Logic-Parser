import random
import re
from SententialLogic_FormulaGenerator import generate_wff

def instantiate_atoms(expr, constant):
    """
    For every occurrence of an atomic sentence (a single capital letter among P, Q, R, S, T)
    in the expression, append the chosen lower-case constant.
    For example, if expr = "R ∨ R" and constant = "a", returns "Ra ∨ Ra".
    """
    pattern = r'\b([PQRST])\b'
    return re.sub(pattern, lambda m: m.group(1) + constant, expr)

def alpha_replace(expr, alpha, beta):
    pattern = r'\b' + re.escape(alpha) + r'\b'
    return re.sub(pattern, beta, expr)

def ensure_bracket(expr):
    """
    Ensures that the given expression is enclosed in parentheses.
    If the first non-space character is not '(', adds '(' at the beginning and ')' at the end.
    """
    stripped = expr.lstrip()
    if not stripped.startswith("("):
        return "(" + expr + ")"
    return expr

# Each function below generates one valid inference instance for a specific rule.

def generate_SL():
    # SL: From (Φ ∧ Ψ) derive Φ.
    phi = generate_wff(random.randint(1, 3))
    psi = generate_wff(random.randint(1, 3))
    premise = f"({phi} ∧ {psi})"
    conclusion = phi
    return conclusion, [premise]

def generate_SR():
    # SR: From (Φ ∧ Ψ) derive Ψ.
    phi = generate_wff(random.randint(1, 3))
    psi = generate_wff(random.randint(1, 3))
    premise = f"({phi} ∧ {psi})"
    conclusion = psi
    return conclusion, [premise]

def generate_ADJ():
    # ADJ: From Φ and Ψ derive (Φ ∧ Ψ).
    phi = generate_wff(random.randint(1, 3))
    psi = generate_wff(random.randint(1, 3))
    conclusion = f"({phi} ∧ {psi})"
    return conclusion, [phi, psi]

def generate_MP():
    # MP: From (Φ → Ψ) and Φ derive Ψ.
    phi = generate_wff(random.randint(1, 3))
    psi = generate_wff(random.randint(1, 3))
    premise1 = f"({phi} → {psi})"
    premise2 = phi
    conclusion = psi
    return conclusion, [premise1, premise2]

def generate_MT():
    # MT: From (Φ → Ψ) and ~Ψ derive ~Φ.
    phi = generate_wff(random.randint(1, 3))
    psi = generate_wff(random.randint(1, 3))
    premise1 = f"({phi} → {psi})"
    premise2 = f"~{psi}"
    conclusion = f"~{phi}"
    return conclusion, [premise1, premise2]

def generate_DSL():
    # DSL: From (Φ ∨ Ψ) and ~Ψ derive Φ.
    phi = generate_wff(random.randint(1, 3))
    psi = generate_wff(random.randint(1, 3))
    premise1 = f"({phi} ∨ {psi})"
    premise2 = f"~{psi}"
    conclusion = phi
    return conclusion, [premise1, premise2]

def generate_DSR():
    # DSR: From (Φ ∨ Ψ) and ~Φ derive Ψ.
    phi = generate_wff(random.randint(1, 3))
    psi = generate_wff(random.randint(1, 3))
    premise1 = f"({phi} ∨ {psi})"
    premise2 = f"~{phi}"
    conclusion = psi
    return conclusion, [premise1, premise2]

def generate_ADD():
    # ADD: From Φ derive (Φ ∨ Ψ).
    phi = generate_wff(random.randint(1, 3))
    psi = generate_wff(random.randint(1, 3))
    conclusion = f"({phi} ∨ {psi})"
    return conclusion, [phi]

def generate_BC():
    # BC: From (Φ↔Ψ) derive (Φ→Ψ)∧(Ψ→Φ).
    phi = generate_wff(random.randint(1, 3))
    psi = generate_wff(random.randint(1, 3))
    premise = f"({phi}↔{psi})"
    conclusion = f"({phi}→{psi})∧({psi}→{phi})"
    return conclusion, [premise]

def generate_CB():
    # CB: From (Φ→Ψ)∧(Ψ→Φ) derive Φ↔Ψ.
    phi = generate_wff(random.randint(1, 3))
    psi = generate_wff(random.randint(1, 3))
    premise = f"({phi}→{psi})∧({psi}→{phi})"
    conclusion = f"{phi}↔{psi}"
    return conclusion, [premise]

def generate_DNI():
    # DNI: From Φ derive ~~Φ.
    phi = generate_wff(random.randint(1, 3))
    conclusion = f"~~{phi}"
    return conclusion, [phi]

def generate_DNE():
    # DNE: From ~~Φ derive Φ.
    phi = generate_wff(random.randint(1, 3))
    premise = f"~~{phi}"
    conclusion = phi
    return conclusion, [premise]

def generate_UI():
    # UI: From ∀αΦ derive Φ(α/constant) where every atomic is modified by the instantiation.
    alpha = random.choice("xyz")
    formula = generate_wff(random.randint(1, 3))
    constant = random.choice("abc")
    # Ensure the formula is bracketed when appended after the quantifier.
    bracketed_instantiation = ensure_bracket(instantiate_atoms(formula, alpha))
    premise = f"∀{alpha}{bracketed_instantiation}"
    conclusion = instantiate_atoms(formula, constant)
    return conclusion, [premise]

def generate_EG():
    # EG: From Φ derive ∃αΦ(α/constant) where α is fresh in Φ.
    while True:
        formula = generate_wff(random.randint(1, 3))
        alpha = random.choice("xyz")
        if alpha not in formula:
            break
    # Wrap the instantiated formula in brackets if necessary.
    bracketed_instantiation = ensure_bracket(instantiate_atoms(formula, alpha))
    conclusion = f"∃{alpha}" + bracketed_instantiation
    premise = formula
    return conclusion, [premise]

def generate_EI(with_extra=False):
    # EI: From ∃αΦ derive Φ(α/constant)
    alpha = random.choice("xyz")
    formula = generate_wff(random.randint(1, 3))
    constant = random.choice("abc")
    # Ensure the part following the quantifier is bracketed.
    bracketed_instantiation = ensure_bracket(instantiate_atoms(formula, alpha))
    premise = f"∃{alpha}" + bracketed_instantiation
    conclusion = instantiate_atoms(formula, constant)
    inputs = [premise]
    if with_extra:
        # For this variant, instantiate extra with a constant DIFFERENT from the main conclusion.
        extra_options = [c for c in "abc" if c != constant]
        extra_constant = random.choice(extra_options)
        extra = instantiate_atoms(formula, extra_constant)
        inputs.append(extra)
    return conclusion, inputs

def generate_EI_extra_same():
    # EI: From ∃αΦ derive Φ(α/constant)
    # In this extra case, the extra premise is instantiated using the SAME constant as the main conclusion.
    alpha = random.choice("xyz")
    formula = generate_wff(random.randint(1, 3))
    constant = random.choice("abc")
    bracketed_instantiation = ensure_bracket(instantiate_atoms(formula, alpha))
    premise = f"∃{alpha}" + bracketed_instantiation
    conclusion = instantiate_atoms(formula, constant)
    # Here, the extra premise uses the SAME constant.
    extra = instantiate_atoms(formula, constant)
    inputs = [premise, extra]
    return conclusion, inputs

# Randomly choose one of the inference-rule generators.
def generate_test_case():
    generators = [
        generate_SL,
        generate_SR,
        generate_ADJ,
        generate_MP,
        generate_MT,
        generate_DSL,
        generate_DSR,
        generate_ADD,
        generate_BC,
        generate_CB,
        generate_DNI,
        generate_DNE,
        generate_UI,
        generate_EG,
        generate_EI,                           # Basic EI (no extra)
        lambda: generate_EI(with_extra=True),  # EI with extra premise (different constant)
        generate_EI_extra_same                 # EI with extra premise (same constant as conclusion) (incorrect)
    ]
    gen_func = random.choice(generators)
    conclusion, inputs = gen_func()
    return conclusion, inputs

def write_random_inference_input(file_name="input_inference.txt", num_cases=1000):
    input_lines = []
    for _ in range(num_cases):
        conclusion, inputs = generate_test_case()
        input_lines.append(f"Output: {conclusion}")
        for idx, inp in enumerate(inputs):
            input_lines.append(f"Input {idx+1}: {inp}")
        input_lines.append("")  # Blank line separating test cases.
    with open(file_name, "w", encoding="utf-8") as f:
        f.write("\n".join(input_lines))
    print(f"Generated {num_cases} test cases in {file_name}")

if __name__ == "__main__":
    write_random_inference_input()
