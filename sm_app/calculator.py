# Sales Manager Incentive Calculator
# Monthly Target, Metal Agnostic

# Standard Multiplier For Monthly Target
SM_MULTIPLIER = 600

# Fixed Incentive Parameters
X = 20000        # Base Incentive At TR
CAP_RATE = 0.001 # Max Effective Rate As A Fraction Of AR
CAP_ATTAINMENT = 3  # Cap Binds At Three Times Target Revenue


def compute_target_revenue(salary):
    # Compute Monthly Target Revenue From Salary
    return salary * SM_MULTIPLIER


def compute_slope(salary):
    # Compute Slope Based On Salary
    return 0.9 * salary - 10000


def compute_sm_incentive(ar, salary):
    # Compute Effective Incentive For A Single SM
    tr = compute_target_revenue(salary)
    a = ar / tr if tr > 0 else 0
    y = compute_slope(salary)

    # Piecewise Incentive Function
    if a < 1.0:
        i_raw = 0.0
    else:
        i_raw = X + y * (a - 1)

    # Apply Cap Of Zero Point One Percent Of AR
    cap = CAP_RATE * ar
    i_effective = min(i_raw, cap)

    return {
        "salary": salary,
        "tr": tr,
        "ar": ar,
        "a": a,
        "y": y,
        "i_raw": round(i_raw, 2),
        "cap": round(cap, 2),
        "i_effective": round(i_effective, 2),
    }
