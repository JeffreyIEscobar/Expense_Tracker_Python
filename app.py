from flask import Flask, render_template, request, session
from flask_session import Session

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Sample data (replace with your data storage solution)
expenses = [
    {"item": "Groceries", "amount": 50},
    {"item": "Dinner", "amount": 30},
    # ... add more expenses
]

@app.route('/')
def index():
    total = sum(expense['amount'] for expense in expenses)
    return render_template('index.html', expenses=expenses, total=total)

@app.route('/submit_expense', methods=['POST'])
def submit_expense():
    item = request.form.get('item')
    amount = float(request.form.get('amount'))
    currency = request.form.get('currency')
    
    # Conversion rates (replace with accurate rates)
    conversion_rates = {
        "USD": 1.0,
        "JPY": 110.0,
        "CHF": 0.9,
        "GBP": 0.75,
        "CNY": 6.4,
        "EUR": 0.85,
        "AUD": 1.4,
        "INR": 75.0,
        "RUB": 70.0,
        "SEK": 8.8,
        # Add more conversion rates
    }
    
    # Convert amount to USD
    amount_usd = amount / conversion_rates.get(currency, 1.0)
    
    # Add the new expense to the list (replace with your data storage logic)
    expenses.append({"item": item, "amount": amount_usd})
    
    # Store the selected currency in the session
    session['currency'] = currency
    
    return index()  # Redirect back to the index page

@app.route('/remove_expense', methods=['POST'])
def remove_expense():
    expense_index = int(request.form.get('expense_index'))
    if 0 <= expense_index < len(expenses):
        del expenses[expense_index]
    return index()

if __name__ == '__main__':
    app.run(debug=True)
