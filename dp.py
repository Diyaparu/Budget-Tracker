import streamlit as st
import pdfplumber

def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def parse_extracted_text(text):
    # Extract numerical values from text (basic approach)
    lines = text.split("\n")
    income, liabilities = 0, 0
    for line in lines:
        if "income" in line.lower():
            income = int(''.join(filter(str.isdigit, line)))
        elif "liabilities" in line.lower() or "rent" in line.lower():
            liabilities = int(''.join(filter(str.isdigit, line)))
    return income, liabilities

def budget_calculator(income, liabilities, expenses):
    remaining_income = income - liabilities
    remaining_after_expenses = remaining_income
    
    expense_details = {}
    for category, percentage in expenses.items():
        category_amount = remaining_after_expenses * (percentage / 100)
        expense_details[category] = category_amount
        remaining_after_expenses -= category_amount
    
    return expense_details, remaining_after_expenses

st.title("Budget Analyzer")

uploaded_file = st.file_uploader("Upload a PDF with Income & Liabilities", type=["pdf"])

if uploaded_file is not None:
    extracted_text = extract_text_from_pdf(uploaded_file)
    
    st.write("Extracted Text:")
    st.text(extracted_text)
    
    income, liabilities = parse_extracted_text(extracted_text)
    st.write(f"Extracted Income: ₹{income}")
    st.write(f"Extracted Liabilities: ₹{liabilities}")
else:
    income = st.number_input("Enter your monthly income:", min_value=0)
    liabilities = st.number_input("Enter your monthly liabilities (fees, rent, etc.):", min_value=0)

if liabilities > income:
    st.warning("Your liabilities exceed your income!")
else:
    expense_categories = {
        "Food": 40,
        "Entertainment": 20,
        "Savings": 15,
        "Transportation": 15,
        "Other": 10
    }

    expense_details, remaining_income = budget_calculator(income, liabilities, expense_categories)
    
    st.write("### Your Budget Breakdown:")
    for category, amount in expense_details.items():
        st.write(f"{category}: ₹{amount:.2f}")
    
    st.write(f"### Remaining Income: ₹{remaining_income:.2f}")


import streamlit as st
import matplotlib.pyplot as plt

"""def generate_pie_chart(income, household, rent, savings):
    """Generates and displays a pie chart of income distribution in Streamlit."""
    
    expenses = household + rent
    remaining = income - expenses - savings
    
    if remaining > 2000:
        savings += remaining
        remaining = 0

    labels = ['Household', 'Rent', 'Savings', 'Remaining']
    sizes = [household, rent, savings, remaining]
    
    # Create the pie chart
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title('Income Distribution')
    
    return fig

# Streamlit UI
st.title("Budget Pie Chart")

# User input fields
income = st.number_input("Enter your monthly income:", min_value=0, value=35000)
household = st.number_input("Enter your monthly household expenses:", min_value=0, value=10000)
rent = st.number_input("Enter your monthly rent:", min_value=0, value=5000)
savings = st.number_input("Enter your monthly savings:", min_value=0, value=2000)"""

if st.button("Generate Pie Chart"):
    pie_chart = generate_pie_chart(income, household, rent, savings)
    st.pyplot(pie_chart)
