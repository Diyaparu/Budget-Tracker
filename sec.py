def text():
    import google.generativeai as genai

    # Configure API
    genai.configure(api_key="AIzaSyAWiWqHfQRNdTjpp7hddA_DPaAc_tGD0ZU")

    # Define user inputs
    income = 5000  # Example income
    expenses = {"Rent": 20000, "Food": 10000, "Transport": 5000, "Other": 5000}  # Example expenses

    # Initialize model
    model = genai.GenerativeModel("gemini-2.0-flash-exp")

    # Corrected prompt with actual values
    prompt = f"My monthly income is {income}. My expenses are {expenses}. How can I save more money?"

    # Generate AI response
    response = model.generate_content(prompt)

    # Print AI-generated savings tips
    print(response.text)
def pdf():
    import google.generativeai as genai

    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    sample_pdf = genai.upload_file(media / "test.pdf")
    response = model.generate_content(["Give me a summary of this pdf file.", sample_pdf])
    print(response.text)



