import streamlit as st
import pandas as pd
import numpy as np

# Function to calculate financial score
def calculate_financial_score(data):
    """
    Calculates the financial score based on the input data.
    """
    # Extract features
    income = data["Income"]
    savings = data["Savings"]
    monthly_expenses = data["Monthly Expenses"]
    loan_payments = data["Loan Payments"]
    dependents = data["Dependents"]

    # Compute derived metrics
    savings_to_income = savings / income
    expenses_to_income = monthly_expenses / income
    loan_to_income = loan_payments / income

    # Base scoring logic
    score = 100  # Start with a perfect score

    # Penalize high expenses
    if expenses_to_income > 0.5:
        score -= 10 * (expenses_to_income - 0.5)

    # Penalize low savings
    if savings_to_income < 0.2:
        score -= 15 * (0.2 - savings_to_income)

    # Penalize high loan-to-income ratio
    if loan_to_income > 0.3:
        score -= 10 * (loan_to_income - 0.3)

    # Penalize for dependents
    if dependents > 3:
        score -= 5 * (dependents - 3)

    # Generate insights
    insights = []
    if expenses_to_income > 0.5:
        insights.append(f"High expenses (>{expenses_to_income*100:.1f}%) reduce your score by {10 * (expenses_to_income - 0.5):.1f} points.")
    if savings_to_income < 0.2:
        insights.append(f"Low savings (<{savings_to_income*100:.1f}%) reduce your score by {15 * (0.2 - savings_to_income):.1f} points.")
    if loan_to_income > 0.3:
        insights.append(f"High loan payments (>30%) reduce your score by {10 * (loan_to_income - 0.3):.1f} points.")

    # Recommendations
    recommendations = []
    if savings_to_income < 0.2:
        recommendations.append("Consider increasing savings by at least 20% of your income.")
    if expenses_to_income > 0.5:
        recommendations.append("Reduce non-essential expenses to below 50% of income.")

    return max(score, 0), insights, recommendations


# Streamlit App
st.title("Financial Health Scoring App")

# Sidebar for user input
st.sidebar.header("Input Family Data")
income = st.sidebar.number_input("Monthly Income", min_value=1000, step=500)
savings = st.sidebar.number_input("Total Savings", min_value=0, step=100)
monthly_expenses = st.sidebar.number_input("Monthly Expenses", min_value=0, step=100)
loan_payments = st.sidebar.number_input("Loan Payments", min_value=0, step=100)
dependents = st.sidebar.number_input("Number of Dependents", min_value=0, step=1)

# Submit button
if st.sidebar.button("Calculate Financial Score"):
    # Prepare data for the model
    family_data = {
        "Income": income,
        "Savings": savings,
        "Monthly Expenses": monthly_expenses,
        "Loan Payments": loan_payments,
        "Dependents": dependents,
    }

    # Calculate financial score
    score, insights, recommendations = calculate_financial_score(family_data)

    # Display results
    st.subheader(f"Financial Score: {score:.2f}")
    st.write("### Insights")
    for insight in insights:
        st.write(f"- {insight}")

    st.write("### Recommendations")
    for recommendation in recommendations:
        st.write(f"- {recommendation}")