# Sales Incentive Calculator
# Core Logic For Gold And Silver Tiers

# Tier Multipliers
GOLD_MULTIPLIER = 6
SILVER_MULTIPLIER = 2

# Fixed Incentive Parameters
X = 200          # Base Incentive At TR
CAP_RATE = 0.01  # Max Effective Rate As A Fraction Of AR
CAP_ATTAINMENT = 3  # Cap Binds At Three Times Target Revenue


def get_multiplier(tier):
    # Return Multiplier Based On Tier
    tier = tier.strip().lower()
    if tier == "gold":
        return GOLD_MULTIPLIER
    elif tier == "silver":
        return SILVER_MULTIPLIER
    else:
        raise ValueError(f"Invalid Tier: {tier}. Must Be Gold Or Silver.")


def compute_slope(salary, tier):
    # Compute Slope Based On Salary And Tier
    tier = tier.strip().lower()
    if tier == "gold":
        return 0.09 * salary - 100
    elif tier == "silver":
        return 0.03 * salary - 100
    else:
        raise ValueError(f"Invalid Tier: {tier}. Must Be Gold Or Silver.")


def compute_incentive(ar, salary, tier):
    # Compute Effective Incentive For A Single SA
    multiplier = get_multiplier(tier)
    tr = salary * multiplier
    a = ar / tr if tr > 0 else 0
    y = compute_slope(salary, tier)

    # Piecewise Incentive Function
    if a < 1.0:
        i_raw = 0.0
    else:
        i_raw = X + y * (a - 1)

    # Apply One Percent Cap
    cap = CAP_RATE * ar
    i_effective = min(i_raw, cap)

    return {
        "salary": salary,
        "tier": tier.capitalize(),
        "tr": tr,
        "ar": ar,
        "a": a,
        "y": y,
        "i_raw": round(i_raw, 2),
        "cap": round(cap, 2),
        "i_effective": round(i_effective, 2),
    }


def split_pair_revenue(salary_1, salary_2, pair_revenue):
    # Split Pair Revenue In Ratio Of Salaries
    total_salary = salary_1 + salary_2
    ar_1 = pair_revenue * (salary_1 / total_salary)
    ar_2 = pair_revenue * (salary_2 / total_salary)
    return ar_1, ar_2


def compute_pair_incentives(
    name_1, salary_1,
    name_2, salary_2,
    pair_revenue, tier
):
    # Compute Incentives For Both SAs In A Pair
    ar_1, ar_2 = split_pair_revenue(salary_1, salary_2, pair_revenue)
    result_1 = compute_incentive(ar_1, salary_1, tier)
    result_2 = compute_incentive(ar_2, salary_2, tier)
    result_1["name"] = name_1
    result_2["name"] = name_2
    return result_1, result_2
