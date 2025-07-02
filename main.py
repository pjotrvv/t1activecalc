from decimal import Decimal, getcontext

getcontext().prec = 100  # Set precision for Decimal operations


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


def should_buy_q1(rho, cost):
    return rho > Decimal("10") * cost


def should_buy_q2(rho, cost):
    return rho > Decimal("1.11") * cost


def should_buy_c1(rho, cost, c2ratio):
    return rho < Decimal("1e300") and rho > Decimal("10") * c2ratio * cost


def should_buy_c2(rho, cost, c2ratio):
    return rho < Decimal("1e300") and rho > c2ratio * cost


def should_buy_c3(rho, cost):
    return rho > get_c3_ratio(rho) * cost


def should_buy_c4(rho, cost):
    return (
        rho > cost
    )  # This might aswell be true but then people probably get confused.


def main():
    print("Enter your current ρ (rho) value (e.g, 1e320):")
    rho = Decimal(input("ρ = ").strip())

    print("Enter the costs for each upgrade:")
    cost_q1 = Decimal(input("Cost for Q1: ").strip())
    cost_q2 = Decimal(input("Cost for Q2: ").strip())
    cost_c1 = Decimal(input("Cost for C1: ").strip())
    cost_c2 = Decimal(input("Cost for C2: ").strip())
    cost_c3 = Decimal(input("Cost for C3: ").strip())
    cost_c4 = Decimal(input("Cost for C4: ").strip())

    c2ratio = Decimal("10")  # Use graph interpolation later.

    print("\n--- T1Ratio Strategy Recommendations ---")
    print("Q1:", "Buy" if should_buy_q1(rho, cost_q1) else "Do not buy")
    print("Q2:", "Buy" if should_buy_q2(rho, cost_q2) else "Do not buy")
    print("C1:", "Buy" if should_buy_c1(rho, cost_c1, c2ratio) else "Do not buy")
    print("C2:", "Buy" if should_buy_c2(rho, cost_c2, c2ratio) else "Do not buy")
    print("C3:", "Buy" if should_buy_c3(rho, cost_c3) else "Do not buy")
    print("C4:", "Buy" if should_buy_c4(rho, cost_c4) else "Do not buy")


if __name__ == "__main__":
    main()
