import pandas as pd
import joblib

# ---------------------------------------------------
# Load Trained Models
# ---------------------------------------------------

model_young = joblib.load("artifacts/model_young.joblib")
model_rest = joblib.load("artifacts/model_rest.joblib")

# ---------------------------------------------------
# Load Scalers
# ---------------------------------------------------

scaler_young = joblib.load("artifacts/scaler_young.joblib")
scaler_rest = joblib.load("artifacts/scaler_rest.joblib")


# ---------------------------------------------------
# Medical Risk Score
# ---------------------------------------------------

def calculate_normalized_risk(medical_history):
    """
    Convert medical history into a normalized risk score
    between 0 and 1.
    """

    risk_scores = {
        "diabetes": 6,
        "heart disease": 8,
        "high blood pressure": 6,
        "thyroid": 5,
        "no disease": 0,
        "none": 0
    }

    diseases = medical_history.lower().split(" & ")

    total_risk = sum(
        risk_scores.get(disease, 0)
        for disease in diseases
    )

    max_score = 14
    min_score = 0

    normalized_score = (
        (total_risk - min_score)
        /
        (max_score - min_score)
    )

    return normalized_score


# ---------------------------------------------------
# Input Preprocessing
# ---------------------------------------------------

def preprocess_input(input_dict):

    expected_columns = [

        "age",
        "number_of_dependants",
        "income_lakhs",
        "insurance_plan",
        "genetical_risk",
        "normalized_risk_score",

        "gender_Male",

        "region_Northwest",
        "region_Southeast",
        "region_Southwest",

        "marital_status_Unmarried",

        "bmi_category_Obesity",
        "bmi_category_Overweight",
        "bmi_category_Underweight",

        "smoking_status_Occasional",
        "smoking_status_Regular",

        "employment_status_Salaried",
        "employment_status_Self-Employed"

    ]

    insurance_plan_encoding = {
        "Bronze": 1,
        "Silver": 2,
        "Gold": 3
    }

    df = pd.DataFrame(
        0,
        columns=expected_columns,
        index=[0]
    )

    # ----------------------------------------
    # Numerical Features
    # ----------------------------------------

    df["age"] = input_dict["Age"]
    df["number_of_dependants"] = input_dict["Number of Dependants"]
    df["income_lakhs"] = input_dict["Income in Lakhs"]
    df["genetical_risk"] = input_dict["Genetical Risk"]

    df["insurance_plan"] = insurance_plan_encoding.get(
        input_dict["Insurance Plan"],
        1
    )

    # ----------------------------------------
    # Gender
    # ----------------------------------------

    if input_dict["Gender"] == "Male":
        df["gender_Male"] = 1

    # ----------------------------------------
    # Region
    # ----------------------------------------

    if input_dict["Region"] == "Northwest":
        df["region_Northwest"] = 1

    elif input_dict["Region"] == "Southeast":
        df["region_Southeast"] = 1

    elif input_dict["Region"] == "Southwest":
        df["region_Southwest"] = 1

    # ----------------------------------------
    # Marital Status
    # ----------------------------------------

    if input_dict["Marital Status"] == "Unmarried":
        df["marital_status_Unmarried"] = 1

    # ----------------------------------------
    # BMI Category
    # ----------------------------------------

    if input_dict["BMI Category"] == "Obesity":
        df["bmi_category_Obesity"] = 1

    elif input_dict["BMI Category"] == "Overweight":
        df["bmi_category_Overweight"] = 1

    elif input_dict["BMI Category"] == "Underweight":
        df["bmi_category_Underweight"] = 1

    # ----------------------------------------
    # Smoking Status
    # ----------------------------------------

    if input_dict["Smoking Status"] == "Occasional":
        df["smoking_status_Occasional"] = 1

    elif input_dict["Smoking Status"] == "Regular":
        df["smoking_status_Regular"] = 1

    # ----------------------------------------
    # Employment Status
    # ----------------------------------------

    if input_dict["Employment Status"] == "Salaried":
        df["employment_status_Salaried"] = 1

    elif input_dict["Employment Status"] == "Self-Employed":
        df["employment_status_Self-Employed"] = 1

    # ----------------------------------------
    # Medical Risk Score
    # ----------------------------------------

    df["normalized_risk_score"] = calculate_normalized_risk(
        input_dict["Medical History"]
    )

    # ----------------------------------------
    # Scaling
    # ----------------------------------------

    df = handle_scaling(
        input_dict["Age"],
        df
    )

    return df

# ---------------------------------------------------
# Feature Scaling
# ---------------------------------------------------

def handle_scaling(age, df):
    """
    Apply the appropriate scaler based on age.

    Applicants aged 25 or below use the young model scaler.
    Applicants above 25 use the general model scaler.
    """

    if age <= 25:
        scaler_object = scaler_young
    else:
        scaler_object = scaler_rest

    cols_to_scale = scaler_object["cols_to_scale"]
    scaler = scaler_object["scaler"]

    # Dummy column required by the saved scaler
    df["income_level"] = None

    df[cols_to_scale] = scaler.transform(df[cols_to_scale])

    df.drop("income_level", axis=1, inplace=True)

    return df


# ---------------------------------------------------
# Premium Prediction
# ---------------------------------------------------

def predict(input_dict):
    """
    Predict the annual health insurance premium.

    Parameters
    ----------
    input_dict : dict
        Dictionary containing all user inputs from the Streamlit app.

    Returns
    -------
    float
        Predicted insurance premium.
    """

    processed_df = preprocess_input(input_dict)

    if input_dict["Age"] <= 25:
        prediction = model_young.predict(processed_df)
    else:
        prediction = model_rest.predict(processed_df)

    premium = float(prediction[0])

    return round(premium)