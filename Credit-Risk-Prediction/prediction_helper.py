import math


def calculate_score(age, loan_amount, annual_income, tenure, residence_type, open_accounts, loan_purpose, utilization,
                    loan_type, avg_dpd):
    """
    Upgraded continuous scoring mathematical engine.
    Calibrated to baseline 600.0 so default parameters yield exactly 456.
    """
    score = 600.0

    # 1. Credit Utilization Adjustment (Completely Continuous)
    # 0% utilization = +80 points. 100% utilization = -100 points.
    util_adj = 80.0 - (1.8 * utilization)
    score += util_adj

    # 2. Avg DPD Adjustment (Completely Continuous)
    # 0 DPD = +90 points. Linear penalty of -7.5 points per day of past due.
    # Clamped to -180 maximum penalty (achieved at 36 days past due).
    dpd_penalty = 90.0 - (7.5 * avg_dpd)
    dpd_adj = max(-180.0, dpd_penalty)
    score += dpd_adj

    # 3. Debt-to-Income / Leverage Ratio (Completely Continuous)
    # Ratio = Loan Amount / Annual Income
    ratio = loan_amount / annual_income if annual_income > 0 else 1.0
    # Linear ratio penalty of -150 points per unit of ratio, clamped between +30 and -80.
    ratio_penalty = 30.0 - (150.0 * ratio)
    ratio_adj = max(-80.0, min(30.0, ratio_penalty))
    score += ratio_adj

    # 4. Age Adjustment (Completely Continuous)
    # Linear reward for age starting from 18, clamped between -20 and +40 points.
    age_reward = -20.0 + ((age - 18) * 1.5)
    age_adj = max(-20.0, min(40.0, age_reward))
    score += age_adj

    # 5. Open Accounts Adjustment (Continuous for all active account values)
    if open_accounts == 0:
        oa_adj = -30.0  # Penalty for lack of credit footprint
    else:
        # Reward of +20 for 1 account, up to +50 for 7 accounts, then decays for over-leverage (>10)
        if open_accounts <= 7:
            oa_adj = 20.0 + ((open_accounts - 1) * 5.0)
        elif open_accounts <= 10:
            oa_adj = 50.0
        else:
            oa_adj = max(-40.0, 50.0 - ((open_accounts - 10) * 3.0))
    score += oa_adj

    # 6. Residence Type Adjustment (Categorical)
    if residence_type == 'Owned':
        score += 35.0
    elif residence_type == 'Mortgaged':
        score += 15.0
    else:
        score -= 15.0  # Rented

    # 7. Loan Type Adjustment (Categorical)
    if loan_type == 'Secured':
        score += 25.0
    else:
        score -= 20.0  # Unsecured

    # 8. Loan Purpose Adjustment (Categorical)
    if loan_purpose in ['Home', 'Education']:
        score += 20.0
    elif loan_purpose == 'Business':
        score += 10.0
    else:
        score -= 10.0  # Personal / Other

    # Round and clamp final credit score strictly to standard bureau range [300, 900]
    return max(300, min(900, int(round(score))))


def get_factor_details(score, avg_dpd, utilization, open_accounts, loan_amount, annual_income):
    """
    Returns granular factor assessments based on user profile inputs.
    """
    # Factor 1: Payment History
    if avg_dpd == 0:
        pay_badge = "Excellent"
        pay_progress = 100
        pay_desc = "0 DPD indicates a flawless repayment history with no outstanding payment delays."
    elif avg_dpd <= 10:
        pay_badge = "Good"
        pay_progress = 75
        pay_desc = f"{avg_dpd} days average DPD is moderate. Clear them immediately to keep payments flawless."
    elif avg_dpd <= 30:
        pay_badge = "Fair"
        pay_progress = 50
        pay_desc = f"{avg_dpd} days average DPD is starting to represent serious risk to underwriting teams."
    else:
        pay_badge = "Poor"
        pay_progress = 20
        pay_desc = f"{avg_dpd} days DPD is critical and represents extreme financial risk. Credit-building programs advised."

    # Factor 2: Credit Utilization
    if utilization <= 30:
        util_badge = "Excellent"
        util_progress = 100
        util_desc = f"With {utilization}% utilization, you operate safely within credit limits. High scoring boost."
    elif utilization <= 50:
        util_badge = "Good"
        util_progress = 75
        util_desc = f"With {utilization}% utilization, you keep balances moderate. Close to premium score levels."
    elif utilization <= 70:
        util_badge = "Fair"
        util_progress = 50
        util_desc = f"Your utilization of {utilization}% is elevated. Lower total balances below 30% to maximize score."
    else:
        util_badge = "Poor"
        util_progress = 20
        util_desc = f"Excessive credit usage ({utilization}%) signals high dependency on credit limits and limits approvals."

    # Factor 3: Credit Age & Mix
    if open_accounts == 0:
        mix_badge = "Poor"
        mix_progress = 10
        mix_desc = "0 open accounts represents a lack of credit history. Lenders cannot evaluate behavior."
    elif open_accounts <= 2:
        mix_badge = "Good"
        mix_progress = 65
        mix_desc = f"{open_accounts} open account provides some history. Adding a mix of secured/unsecured loans will build depth."
    elif open_accounts <= 6:
        mix_badge = "Excellent"
        mix_progress = 100
        mix_desc = f"{open_accounts} accounts represents an ideal diversified credit mix of files, reducing overall risk."
    else:
        mix_badge = "Fair"
        mix_progress = 55
        mix_desc = f"Large number of open accounts ({open_accounts}) may represent an elevated loan-taking pattern."

    # Factor 4: Debt Load / LTI
    dti_val = (loan_amount / annual_income * 100) if annual_income > 0 else 100.0
    if dti_val <= 15:
        dti_badge = "Excellent"
        dti_progress = 100
        dti_desc = f"Outstanding DTI ratio of {dti_val:.1f}%. You are exceptionally safe and have extreme repaying capacity."
    elif dti_val <= 35:
        dti_badge = "Good"
        dti_progress = 80
        dti_desc = f"DTI ratio of {dti_val:.1f}% is highly moderate and keeps risk extremely low during evaluations."
    elif dti_val <= 65:
        dti_badge = "Fair"
        dti_progress = 50
        dti_desc = f"DTI of {dti_val:.1f}% is elevated. Reducing loans or increasing annual income improves capacity."
    else:
        dti_badge = "Poor"
        dti_progress = 20
        dti_desc = f"Extremely high leverage of {dti_val:.1f}%. Total outstanding exceeds standard safe limits."

    return {
        "payment_history": {"badge": pay_badge, "progress": pay_progress, "desc": pay_desc},
        "credit_utilization": {"badge": util_badge, "progress": util_progress, "desc": util_desc},
        "credit_mix": {"badge": mix_badge, "progress": mix_progress, "desc": mix_desc},
        "debt_to_income": {"badge": dti_badge, "progress": dti_progress, "desc": dti_desc}
    }


def predict_score_and_metrics(data):
    """
    Takes raw dictionary of input data, parses fields, calculates score,
    and returns a complete dynamic analytical payload for API consumption.
    """
    try:
        age = int(data.get("age", 28))
        loan_amount = float(data.get("loan_amount", 2560000))
        annual_income = float(data.get("annual_income", 12000000))
        tenure = int(data.get("tenure", 36))
        residence_type = data.get("residence_type", "Rented")
        open_accounts = int(data.get("open_accounts", 1))
        loan_purpose = data.get("loan_purpose", "Home")
        utilization = float(data.get("utilization", 90))
        loan_type = data.get("loan_type", "Unsecured")
        avg_dpd = int(data.get("avg_dpd", 20))
    except (ValueError, TypeError):
        # Fallback defaults
        age, loan_amount, annual_income, tenure = 28, 2560000, 12000000, 36
        residence_type, open_accounts, loan_purpose = "Rented", 1, "Home"
        utilization, loan_type, avg_dpd = 90.0, "Unsecured", 20

    score = calculate_score(age, loan_amount, annual_income, tenure, residence_type, open_accounts, loan_purpose,
                            utilization, loan_type, avg_dpd)

    # Probability of Default
    pd = (900 - score) / 600.0 * 100.0
    pd = round(pd, 2)

    # Status & Advice - MAPPED EXACTLY TO THE 4-TIER MODEL SCALE CARDS (Average instead of Fair!)
    if score <= 500:
        status = "Poor"
        advice = "⚠️ Work on reducing your credit utilization and paying on time to improve your score."
    elif score <= 650:
        status = "Average"
        advice = "⚠️ Your credit score is average. Work on lowering outstanding card balances and establishing on-time payment streams."
    elif score <= 750:
        status = "Good"
        advice = "👍 Solid credit! Keep doing what you're doing, and maintain card utilization under 30% to advance further."
    else:
        status = "Excellent"
        advice = "✨ Outstanding credit! You qualify for our absolute lowest prime interest rates and exclusive elite credit offers."

    factors = get_factor_details(score, avg_dpd, utilization, open_accounts, loan_amount, annual_income)

    return {
        "score": score,
        "pd": f"{pd:.2f}",
        "status": status,
        "advice": advice,
        "factors": factors
    }