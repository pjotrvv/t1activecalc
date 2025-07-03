import math
import json
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 100  # Set precision for Decimal operations


# Constants
C2_RATIO_POINTS = [
    (Decimal("1e25"), 2),
    (Decimal("1e50"), 10),
    (Decimal("1e75"), 50),
    (Decimal("1e100"), 120),
    (Decimal("1e125"), 80),
    (Decimal("1e150"), 10),
    (Decimal("1e175"), 5),
    (Decimal("1e200"), 10),
    (Decimal("1e225"), 20),
    (Decimal("1e250"), 50),
    (Decimal("1e275"), 100),
    (Decimal("1e300"), 200),
    (Decimal("1e325"), 300),
    (Decimal("1e350"), 400),
    (Decimal("1e375"), 500),
]


# Utility functions
def interpolate_log(x, x0, y0, x1, y1):
    logx = math.log10(x)
    logx0 = math.log10(x0)
    logx1 = math.log10(x1)
    slope = (y1 - y0) / (logx1 - logx0)
    return y0 + slope * (logx - logx0)


def get_c2_ratio(rho: Decimal) -> Decimal:
    for i in range(len(C2_RATIO_POINTS) - 1):
        r0, ratio0 = C2_RATIO_POINTS[i]
        r1, ratio1 = C2_RATIO_POINTS[i + 1]
        if r0 <= rho < r1:
            return Decimal(
                interpolate_log(float(rho), float(r0), ratio0, float(r1), ratio1)
            )
    if rho < C2_RATIO_POINTS[0][0]:
        return Decimal(C2_RATIO_POINTS[0][1])
    return Decimal(C2_RATIO_POINTS[-1][1])


def get_c3_ratio(rho: Decimal) -> Decimal:
    if rho < Decimal("1e300"):
        return Decimal("1")
    elif rho < Decimal("1e450"):
        return Decimal("1.1")
    elif rho < Decimal("1e550"):
        return Decimal("2")
    elif rho < Decimal("1e655"):
        return Decimal("5")
    else:
        return Decimal("10")


def parse_rho(rho_input: str):
    if "e" in rho_input:
        base_str, exp_str = rho_input.split("e")
        base = int(Decimal(base_str))
        exp = int(exp_str)
    else:
        base = int(Decimal(rho_input))
        exp = 0
    return base, exp


def format_rho(base: int, exp: int) -> Decimal:
    return Decimal(f"{base}e{exp}")


def increment_rho(base: int, exp: int):
    base += 1
    if base == 10:
        base = 1
        exp += 1
    return base, exp


def show_strategy(rho: Decimal):
    c2ratio = get_c2_ratio(rho)
    print("\n--- T1Ratio Strategy Recommendations ---")
    print(f"Q1  cost threshold: {(rho / Decimal('10')):.2e}")
    print(f"Q2  cost threshold: {(rho / Decimal('1.11')):.2e}")

    if rho < Decimal("1e300"):
        print(f"C1  cost threshold: {(rho / (Decimal('10') * c2ratio)):.2e}")
        print(f"C2  cost threshold: {(rho / c2ratio):.2e}")
    else:
        print("C1/C2: Do NOT buy (rho >= 1e300)")

    print(f"C3  cost threshold: {(rho / get_c3_ratio(rho)):.2e}")


def main():
    print("Welcome to the T1Ratio Strategy Calculator")
    current_base = None
    current_exp = None

    while True:
        try:
            user_input = input("\nEnter ρ (rho), or 'exit': ").strip().lower()

            if user_input == "exit":
                print("Exiting the calculator. Goodbye!")
                break

            elif user_input == "":
                if current_base is None or current_exp is None:
                    print("No previous ρ value found. Please enter a new ρ value.")
                    continue
                current_base, current_exp = increment_rho(current_base, current_exp)
            else:
                try:
                    current_base, current_exp = parse_rho(user_input)
                except ValueError:
                    print(
                        "Invalid input format. Please enter a valid ρ value (e.g., '1e25')."
                    )
                    continue

            rho = format_rho(current_base, current_exp)
            show_strategy(rho)
        except Exception as e:
            print(f"An error occurred: {e}. Please try again.")
