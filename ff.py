import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image

def budget_calculator(income, liabilities, expenses):
    """
    Calculate budget breakdown based on income, liabilities, and expense amounts.
    """
    remaining_income = income - liabilities
    remaining_after_expenses = remaining_income
    
    expense_details = {}
    for category, amount in expenses.items():
        expense_details[category] = amount
        remaining_after_expenses -= amount
    
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
    # User input for expense categories
    food = st.number_input("Enter your monthly expenses for Food:", min_value=0)
    entertainment = st.number_input("Enter your monthly expenses for Entertainment:", min_value=0)
    savings = st.number_input("Enter your monthly expenses for Savings:", min_value=0)
    transportation = st.number_input("Enter your monthly expenses for Transportation:", min_value=0)
    other = st.number_input("Enter your monthly expenses for Other:", min_value=0)

    # Create a dictionary for expenses
    expense_categories = {
        "Food": food,
        "Entertainment": entertainment,
        "Savings": savings,
        "Transportation": transportation,
        "Other": other
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

    # Display a meme pop-up (here, we use a sample meme)
    meme_image = Image.open('meme_sample.jpg')  # Replace with a meme image path or URL
    st.image(meme_image, caption="When you manage your budget like a pro!")





