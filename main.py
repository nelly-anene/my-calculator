import json
import os

HIST_FILE = "historique.json"

# ---------- Utils (input) ----------
def ask_number(msg):
    while True:
        try:
            return float(input(msg))
        except ValueError:
            print("Erreur: entrez un nombre valide (ex: 12 ou 12.5).")

# ---------- History ----------
def load_history():
    if not os.path.exists(HIST_FILE):
        return []
    try:
        with open(HIST_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []

def save_history(history):
    with open(HIST_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def add_history(expression, result):
    history = load_history()
    history.append({"expression": expression, "resultat": result})
    save_history(history)

def clear_history():
    save_history([])

def show_history(limit=10):
    hist = load_history()
    if not hist:
        print("Historique vide.")
        return
    for item in hist[-limit:]:
        print(f"{item['expression']} = {item['resultat']}")

# ---------- Math (manual) ----------
def factorial(n):
    if n != int(n) or n < 0:
        raise ValueError("fact: uniquement entier >= 0.")
    n = int(n)
    res = 1
    for i in range(2, n + 1):
        res *= i
    return res

# ---------- Priority calculation (3 passes) ----------
def compute_with_priority(nums, ops):
    # Pass 1: powers ^
    i = 0
    while i < len(ops):
        if ops[i] == "^":
            nums[i] = nums[i] ** nums[i + 1]
            nums.pop(i + 1)
            ops.pop(i)
        else:
            i += 1

    # Pass 2: * and /
    i = 0
    while i < len(ops):
        if ops[i] in ("*", "/"):
            a = nums[i]
            b = nums[i + 1]
            if ops[i] == "/":
                if b == 0:
                    raise ZeroDivisionError("Division par zéro.")
                nums[i] = a / b
            else:
                nums[i] = a * b
            nums.pop(i + 1)
            ops.pop(i)
        else:
            i += 1

    # Pass 3: + and -
    res = nums[0]
    for j, op in enumerate(ops):
        if op == "+":
            res += nums[j + 1]
        elif op == "-":
            res -= nums[j + 1]
    return res

# ---------- Main program ----------
def main():
    print("Calculatrice – La Pascaline")
    print("Projet Python sans eval() et sans math")
    print("Opérations: +  -  *  /  ^  | Unaires: sqrt, fact | '=' pour terminer")
    print("Commandes: h (voir historique), clear (effacer historique)")
    print("Exemple: 2 + 3 * 4 =\n")

    # Menu historique (minimum demandé)
    cmd = input("Commande (h/clear/Entrée): ").strip().lower()
    if cmd == "h":
        show_history(10)
        print()
    elif cmd == "clear":
        clear_history()
        print("Historique réinitialisé.\n")

    nums = [ask_number("Nombre 1: ")]
    ops = []

    while True:
        op = input("Opération (+,-,*,/,^,sqrt,fact,=): ").strip().lower()

        if op == "=":
            break

        # unary operations apply to last number
        if op == "sqrt":
            if nums[-1] < 0:
                print("Erreur: sqrt d'un nombre négatif interdit.")
                continue
            nums[-1] = nums[-1] ** 0.5
            print("OK sqrt ->", nums[-1])
            continue

        if op == "fact":
            try:
                nums[-1] = float(factorial(nums[-1]))
                print("OK fact ->", nums[-1])
            except ValueError as e:
                print("Erreur:", e)
            continue

        # binary operations
        if op not in ("+", "-", "*", "/", "^"):
            print("Opération invalide.")
            continue

        nb = ask_number("Nombre suivant: ")
        if op == "/" and nb == 0:
            print("Erreur: division par zéro interdite.")
            continue

        ops.append(op)
        nums.append(nb)

    try:
        if len(nums) < 2:
            print("Il faut au minimum 2 nombres.")
            return

        result = compute_with_priority(nums[:], ops[:])
        result_show = int(result) if abs(result - int(result)) < 1e-12 else result
        print("\nRésultat final:", result_show)

        expr = str(nums[0])
        for k in range(len(ops)):
            expr += f" {ops[k]} {nums[k+1]}"
        add_history(expr, result_show)
        print("Historique enregistré dans historique.json")

    except Exception as e:
        print("Erreur:", e)

if __name__ == "__main__":
    main()