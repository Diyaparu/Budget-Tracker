import streamlit as st
import pdfplumber
import google.generativeai as genai
import matplotlib.pyplot as plt

# Configure Gemini AI API
genai.configure(api_key="AIzaSyAWiWqHfQRNdTjpp7hddA_DPaAc_tGD0ZU")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# Function to parse extracted text and extract income & liabilities
def parse_extracted_text(text):
    lines = text.split("\n")
    income, liabilities = 0, 0
    for line in lines:
        if "income" in line.lower():
            income = int(''.join(filter(str.isdigit, line)))
        elif "liabilities" in line.lower() or "rent" in line.lower():
            liabilities = int(''.join(filter(str.isdigit, line)))
    return income, liabilities

# Function to calculate budget breakdown
def budget_calculator(income, liabilities, expenses):
    remaining_income = income - liabilities
    total_expenses = sum(expenses.values())
    
    remaining_after_expenses = remaining_income - total_expenses

    return expenses, remaining_after_expenses


# Function to generate a pie chart
def generate_pie_chart(expense_details, remaining_income):
    labels = list(expense_details.keys()) + ["Remaining"]
    sizes = list(expense_details.values()) + [remaining_income]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title('Income Distribution')

    return fig

# Function to get financial advice from Gemini AI
def get_financial_advice(income, expenses):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  # Updated to latest model
        prompt = f"My monthly income is ₹{income}. My expenses are {expenses}. How can I optimize my savings?"
        response = model.generate_content(prompt)
        return response.text if response else "No response received."
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.title("💰 Budget Analyzer with AI Financial Advice")

# File upload or manual input
uploaded_file = st.file_uploader("📄 Upload a PDF with Income & Liabilities", type=["pdf"])

if uploaded_file is not None:
    extracted_text = extract_text_from_pdf(uploaded_file)
    st.write("### Extracted Text:")
    st.text(extracted_text)

    income, liabilities = parse_extracted_text(extracted_text)
    st.write(f"📌 **Extracted Income:** ₹{income}")
    st.write(f"📌 **Extracted Liabilities:** ₹{liabilities}")
else:
    income = st.number_input("💰 Enter your monthly income:", min_value=0, step=1000)
    liabilities = st.number_input("📉 Enter your monthly liabilities (fees, rent, etc.):", min_value=0, step=1000)

if liabilities > income:
    st.warning("⚠️ Your liabilities exceed your income! Consider reducing expenses.")
else:
    # User-defined expenses
    st.write("### ✏️ Enter Your Monthly Expenses:")
    num_categories = st.number_input("How many expense categories?", min_value=1, step=1, value=3)

    expenses = {}
    for i in range(num_categories):
        category = st.text_input(f"Category {i+1} Name:")
        amount = st.number_input(f"Amount for {category}:", min_value=0, step=500)
        if category and amount > 0:
            expenses[category] = amount

    # Budget calculation
    if st.button("📊 Calculate Budget"):
        expense_details, remaining_income = budget_calculator(income, liabilities, expenses)

        st.write("### 💸 Your Budget Breakdown:")
        for category, amount in expense_details.items():
            st.write(f"📍 {category}: ₹{amount:.2f}")
        st.write(f"### ✅ Remaining Income: ₹{remaining_income:.2f}")

        # Generate and show Pie Chart
        pie_chart = generate_pie_chart(expense_details, remaining_income)
        st.pyplot(pie_chart)

    # Get Financial Advice
    if st.button("🤖 Get AI Financial Tips"):
        financial_advice = get_financial_advice(income, expenses)
        st.write("### 🔥 AI-Generated Financial Advice:")
        st.write(financial_advice)
