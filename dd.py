import streamlit as st
import pdfplumber
import pytesseract
from PIL import Image
import io
import matplotlib.pyplot as plt
import google.generativeai as genai

# Configure Google Gemini API
genai.configure(api_key="AIzaSyAWiWqHfQRNdTjpp7hddA_DPaAc_tGD0ZU")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# Function to extract text from image
def extract_text_from_image(image_file):
    image = Image.open(image_file)
    text = pytesseract.image_to_string(image)
    return text

# Function to parse extracted text
def parse_extracted_text(text):
    lines = text.split("\n")
    income, liabilities = 0, 0
    for line in lines:
        if "income" in line.lower():
            income = int(''.join(filter(str.isdigit, line)))
        elif "liabilities" in line.lower() or "rent" in line.lower():
            liabilities = int(''.join(filter(str.isdigit, line)))
    return income, liabilities

# Function to calculate budget
def budget_calculator(income, liabilities, expenses):
    remaining_income = income - liabilities
    remaining_after_expenses = remaining_income

    expense_details = {}
    for category, amount in expenses.items():
        expense_details[category] = amount
        remaining_after_expenses -= amount

    return expense_details, remaining_after_expenses

# Function to generate AI suggestions using Gemini API
def get_ai_savings_tips(income, expenses):
    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    prompt = f"My monthly income is {income}. My expenses are {expenses}. How can I save more money?"
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI
st.title("Budget Analyzer with AI Savings Tips")

uploaded_file = st.file_uploader("Upload a PDF or Image with Income & Liabilities", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    file_type = uploaded_file.type
    if "pdf" in file_type:
        extracted_text = extract_text_from_pdf(uploaded_file)
    else:
        extracted_text = extract_text_from_image(uploaded_file)

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
    # User input for different expense categories instead of fixed percentages
    food = st.number_input("Enter your monthly expenses for Food:", min_value=0)
    entertainment = st.number_input("Enter your monthly expenses for Entertainment:", min_value=0)
    health = st.number_input("Enter your monthly expenses for Health:", min_value=0)
    transportation = st.number_input("Enter your monthly expenses for Transportation:", min_value=0)
    other = st.number_input("Enter your monthly expenses for Other:", min_value=0)

    # Store user-defined expenses in a dictionary
    expense_categories = {
        "Food": food,
        "Entertainment": entertainment,
        "Health": health,
        "Transportation": transportation,
        "Other": other
    }

    expense_details, remaining_income = budget_calculator(income, liabilities, expense_categories)

    st.write("### Your Budget Breakdown:")
    for category, amount in expense_details.items():
        st.write(f"{category}: ₹{amount:.2f}")

    st.write(f"### Remaining Income: ₹{remaining_income:.2f}")

    # Plot Pie Chart
    fig, ax = plt.subplots()
    labels = expense_details.keys()
    sizes = expense_details.values()
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140, colors=["#ff9999","#66b3ff","#99ff99","#ffcc99","#c2c2f0"])
    ax.axis("equal")  # Equal aspect ratio ensures that pie chart is circular.

    st.pyplot(fig)

    # Generate and Display AI Savings Suggestions
    st.write("### AI-Generated Savings Suggestions:")
    expenses_dict = {key: round(value, 2) for key, value in expense_details.items()}
    ai_tips = get_ai_savings_tips(income, expenses_dict)
    st.write(ai_tips)
