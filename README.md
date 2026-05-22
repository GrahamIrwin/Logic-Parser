# Logic Parser

A Python toolkit for parsing and validating sentential and predicate logic expressions. 
Given a logic formula, the parser determines whether it is well-formed and identifies its main connective. A companion module identifies which inference rule connects a set of premises to a conclusion.

---

## Files

| File | Description |
|------|-------------|
| `SententialLogic_MainConnective_Parser.py` | Checks if a formula is a well-formed formula (WFF) and returns its main connective |
| `SententialLogic_FormulaGenerator.py` | Randomly generates valid (and optionally invalid) WFFs for testing |
| `InferenceRule_Parser.py` | Identifies which inference rule justifies a conclusion from given premises |
| `InferenceRule_Generator.py` | Randomly generates valid inference rule instances for testing |
| `input.txt` / `output.txt` | Main connective parser input/output |
| `testCases_Input.txt` / `testCases_Output.txt` | Labelled test cases for the inference rule parser |

---

## Usage

### Main Connective Parser

Reads from `input.txt`, writes to `output.txt`. Each line of input is a formula; each line of output is its main connective, or `∅` if it is not well-formed.

```bash
python SententialLogic_MainConnective_Parser.py
```

**Example input:**
```
(P ∧ Q)
~P
P → Q
PQ
```

**Example output:**
```
∧
~
→
∅
```

### Inference Rule Parser

Reads from `Input.txt`, writes to `Output.txt`. Test cases are grouped blocks in the format:

```
Output: <conclusion>
Input 1: <premise 1>
Input 2: <premise 2>
```

```bash
python InferenceRule_Parser.py
```

**Example input:**
```
Output: ~((P ∧ R) ∧ (R ∧ R))
Input 1: (((P ∧ R) ∧ (R ∧ R)) → ~(S ∧ S))
Input 2: ~~(S ∧ S)
```

**Example output:**
```
MT
```

### Generating Test Cases

To generate random WFFs into `input.txt`:
```bash
python SententialLogic_FormulaGenerator.py
```

To generate random inference rule instances into `Input.txt`:
```bash
python InferenceRule_Generator.py
```

---

## Supported Logic Symbols

| Symbol | Meaning |
|--------|---------|
| `∧` | Conjunction (and) |
| `∨` | Disjunction (or) |
| `→` | Conditional (if...then) |
| `↔` | Biconditional (if and only if) |
| `~` | Negation (not) |
| `∀` | Universal quantifier (for all) |
| `∃` | Existential quantifier (there exists) |

---

## Supported Inference Rules

| Rule | Description |
|------|-------------|
| **SL** | Simplification Left: `(Φ ∧ Ψ) ⊢ Φ` |
| **SR** | Simplification Right: `(Φ ∧ Ψ) ⊢ Ψ` |
| **ADJ** | Adjunction: `Φ, Ψ ⊢ (Φ ∧ Ψ)` |
| **MP** | Modus Ponens: `(Φ → Ψ), Φ ⊢ Ψ` |
| **MT** | Modus Tollens: `(Φ → Ψ), ~Ψ ⊢ ~Φ` |
| **DSL** | Disjunctive Syllogism Left: `(Φ ∨ Ψ), ~Ψ ⊢ Φ` |
| **DSR** | Disjunctive Syllogism Right: `(Φ ∨ Ψ), ~Φ ⊢ Ψ` |
| **ADD** | Addition: `Φ ⊢ (Φ ∨ Ψ)` |
| **BC** | Biconditional Out: `(Φ ↔ Ψ) ⊢ (Φ → Ψ) ∧ (Ψ → Φ)` |
| **CB** | Biconditional In: `(Φ → Ψ) ∧ (Ψ → Φ) ⊢ (Φ ↔ Ψ)` |
| **DNI** | Double Negation In: `Φ ⊢ ~~Φ` |
| **DNE** | Double Negation Out: `~~Φ ⊢ Φ` |
| **UI** | Universal Instantiation: `∀αΦ ⊢ Φ(α/β)` |
| **EG** | Existential Generalisation: `Φ ⊢ ∃αΦ(α/β)` |
| **EI** | Existential Instantiation: `∃αΦ ⊢ Φ(α/β)`, where β is fresh |