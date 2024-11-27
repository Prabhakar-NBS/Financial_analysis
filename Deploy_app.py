from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import pandas as pd

# Initialize FastAPI app
app = FastAPI(title="Financial Scoring API", version="1.0")

# Define Input and Output Schemas
class FamilyTransactionData(BaseModel):
    family_id: str
    income: float
    savings: float
    dependents: int
    monthly_expenses: float
    loan_payments: float
    transactions: list  # List of dictionaries with category and amount

class FinancialScoreResponse(BaseModel):
    family_id: str
    financial_score: float
    insights: list  # List of strings with key insights
    recommendations: list  # List of recommendations

# Example Scoring Model (simplified logic)
def calculate_financial_score(data):
    """
    Calculates the financial score based on the input data.
    """
    # Extract features
    income = data["income"]
    savings = data["savings"]
    monthly_expenses = data["monthly_expenses"]
    loan_payments = data["loan_payments"]
    dependents = data["dependents"]

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

# Define API Endpoint
@app.post("/calculate_financial_score", response_model=FinancialScoreResponse)
def calculate_score(input_data: FamilyTransactionData):
    try:
        # Parse the input data
        data = input_data.dict()

        # Calculate the financial score
        score, insights, recommendations = calculate_financial_score(data)

        # Build the response
        response = {
            "family_id": data["family_id"],
            "financial_score": round(score, 2),
            "insights": insights,
            "recommendations": recommendations,
        }

        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Run the app (use 'uvicorn filename:app --reload' to run locally)