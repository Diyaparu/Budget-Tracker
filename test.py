import matplotlib.pyplot as plt

def analyze_budget(income, household, rent, savings):
    """
    Analyzes the budget and generates a pie chart of income distribution.

    Args:
        income (float): Monthly income.
        household (float): Monthly household expenses.
        rent (float): Monthly rent expenses.
        savings (float): Monthly savings.

    Returns:
        None. Displays a pie chart.
    """

    expenses = household + rent
    remaining = income - expenses - savings
    
    if remaining > 2000:
        savings+= remaining
        remaining=0

    labels = ['Household', 'Rent', 'Savings', 'Remaining']
    sizes = [household, rent, savings, remaining]
    
    
    
    
    # Create the pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Income Distribution')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()
    
    
#Angel details
income = 35000
household = 10000
rent = 15000
savings = 2000

analyze_budget(income, household, rent, savings)
