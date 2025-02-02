import streamlit as st
import matplotlib.pyplot as plt

def budget_calculator(income, liabilities, expenses):
    """
    Calculate budget breakdown based on income, liabilities, and expense percentages.
    """
    remaining_income = income - liabilities
    remaining_after_expenses = remaining_income
    
    expense_details = {}
    for category, percentage in expenses.items():
        category_amount = remaining_after_expenses * (percentage / 100)
        expense_details[category] = category_amount
        remaining_after_expenses -= category_amount
    
    return expense_details, remaining_after_expenses

def generate_pie_chart(expense_details, remaining_income):
    """
    Generate a pie chart for the budget breakdown.
    """
    labels = list(expense_details.keys()) + ["Remaining Income"]
    sizes = list(expense_details.values()) + [remaining_income]
    
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title('Budget Breakdown')
    
    return fig

# Streamlit UI
st.title("Budget Analyzer with Pie Chart")

# User input for income and liabilities
income = st.number_input("Enter your monthly income:", min_value=0)
liabilities = st.number_input("Enter your monthly liabilities (fees, rent, etc.):", min_value=0)

if liabilities > income:
    st.warning("Your liabilities exceed your income!")
else:
    # Define expense categories with default percentages
    expense_categories = {
        "Food": 40,    # 40% for food
        "Entertainment": 20,  # 20% for entertainment
        "Savings": 15,  # 15% for savings
        "Transportation": 15,  # 15% for transportation
        "Other": 10     # 10% for other expenses
    }

    # Run the budget calculation
    expense_details, remaining_income = budget_calculator(income, liabilities, expense_categories)

    # Display results
    st.write("### Your Budget Breakdown:")
    for category, amount in expense_details.items():
        st.write(f"{category}: ₹{amount:.2f}")

    st.write(f"### Remaining Income: ₹{remaining_income:.2f}")

    # Generate and display the pie chart
    st.write("### Budget Breakdown Pie Chart")
    pie_chart = generate_pie_chart(expense_details, remaining_income)
    st.pyplot(pie_chart)
