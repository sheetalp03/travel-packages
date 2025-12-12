# app.py

# Import necessary Flask modules
from flask import Flask, render_template

# Import the logic function from your Apriori model file
# Make sure 'apriori_model.py' is in the same directory!
# We will assume your Apriori model returns a DataFrame of rules or a similar iterable structure.
from apriori_model import generate_packages 

app = Flask(__name__)

# --- DUMMY DATA ---
# Since we don't have the actual rules data here, 
# we create a placeholder list of rules (similar to the image you shared).
# In a real application, you would load this from a file or a database.
DUMMY_RULES_DATA = [
    {'antecedents': {'Flight'}, 'consequents': {'Hotel'}},
    {'antecedents': {'Hotel'}, 'consequents': {'Local_Tour'}},
    {'antecedents': {'Car_Rental'}, 'consequents': {'Insurance'}},
    # This is a rule that links two items together, which is good for a package
    {'antecedents': {'Flight'}, 'consequents': {'Car_Rental'}}, 
    # Rules with User_ID are usually discarded for package suggestions
    {'antecedents': {'Flight'}, 'consequents': {'User_ID'}}, 
]
# We will convert this into a list that mimics the structure pandas iterrows() uses.
# If you are using pandas in apriori_model.py, ensure you pass the DataFrame directly.

# --- ROUTE TO DISPLAY ATTRACTIVE PACKAGES ---
@app.route('/')
@app.route('/packages')
def show_packages():
    """
    Handles the /packages route. Calls the backend model to get suggested bundles,
    and renders the attractive HTML template to display them to the customer.
    """
    
    try:
        # Step 1: Call the function in your apriori_model.py to process the rules.
        # NOTE: You need to replace DUMMY_RULES_DATA with the function call that 
        # fetches the LATEST raw rules from your Apriori calculation!
        
        # Example if your model uses Pandas (recommended for Apriori output):
        # import pandas as pd
        # rules_df = pd.read_csv('data/apriori_rules.csv') 
        # suggested_packages = generate_packages(rules_df)
        
        # Using the dummy data for this example
        suggested_packages = generate_packages(DUMMY_RULES_DATA)
        
    except Exception as e:
        print(f"Error generating packages: {e}")
        # Fallback in case the model or data file fails
        suggested_packages = [
            {'title': 'Essential Package (Fallback)', 
             'items': ['Flight', 'Hotel'], 
             'description': 'A basic, reliable package. Model failed to load.', 
             'estimated_price_inr': 80000}
        ]
    
    # Step 2: Render the HTML template, passing the clean package data.
    # We assume 'package.html' is set up to loop through the 'packages' list.
    return render_template('package.html', packages=suggested_packages)


# --- ROUTE TO RENDER THE OLD/TECHNICAL ASSOCIATION RULES PAGE (FOR DEBUG/ADMIN ONLY) ---
@app.route('/rules_admin')
def show_rules_admin():
    """
    Renders the raw Association Rule table for an admin/debug view.
    Customers will NOT see this page.
    """
    # Assuming your Apriori model returns the rules directly.
    # In a real app, you would load the full rules DataFrame here.
    return render_template('association_rules_table.html', rules=DUMMY_RULES_DATA)


if __name__ == '__main__':
    # Flask will look for templates in a 'templates' folder by default
    app.run(debug=True)
