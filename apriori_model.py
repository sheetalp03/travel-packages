# apriori_model.py

# --- Assuming you already have code to generate and store your rules ---
# e.g., rules_df = apriori(transactions, min_support=0.5, ...).
# We'll assume rules_df is a list of dictionaries or a pandas DataFrame
# with 'antecedents', 'consequents', and metrics.

def generate_packages(rules_data):
    """
    Processes the raw association rules to create a clean list of package suggestions.
    
    Args:
        rules_data: The output (e.g., DataFrame or list of dicts) from the
                    Apriori algorithm, containing 'antecedents' and 'consequents'.
                    
    Returns:
        A list of dictionaries, where each dict is a structured package suggestion.
    """
    package_suggestions = []
    
    # Define a set of all unique services available
    all_services = {'Flight', 'Hotel', 'Local_Tour', 'Car_Rental', 'Insurance'}

    # 1. Look for rules where services lead to other services (i.e., a good bundle)
    for index, rule in rules_data.iterrows(): # If using pandas, use iterrows()
        # Combine items from both sides of the rule for the bundle
        antecedents = set(rule['antecedents'])
        consequents = set(rule['consequents'])
        
        # We only want to process rules where neither side is just 'User_ID'
        if 'User_ID' not in antecedents and 'User_ID' not in consequents:
            
            # The package is the union of antecedents and consequents
            suggested_bundle = antecedents.union(consequents)
            
            # Convert set of strings to a user-friendly title
            package_title = ' & '.join(sorted(list(suggested_bundle))) + " Package"
            
            # Create the structured package dictionary
            package = {
                'title': package_title,
                'items': list(suggested_bundle),
                'description': f"A highly-suggested bundle based on customer history with {', '.join(list(suggested_bundle)).replace('_', ' ')}.",
                # The price calculation would be more complex, but we use an estimate here
                'estimated_price_inr': calculate_estimated_price(suggested_bundle)
            }
            
            # Prevent duplicate packages from being added
            if package not in package_suggestions:
                package_suggestions.append(package)

    # 2. Add the comprehensive package manually (as a backup/guarantee)
    comprehensive_bundle = {
        'title': 'The Ultimate Travel Bundle',
        'items': list(all_services),
        'description': 'Our all-inclusive package: Flight, Hotel, Tour, Car & Insurance.',
        'estimated_price_inr': 110000 
    }
    
    if comprehensive_bundle not in package_suggestions:
         package_suggestions.append(comprehensive_bundle)
         
    return package_suggestions

# Dummy function to simulate a price calculation (replace with your actual logic)
def calculate_estimated_price(items):
    base_price = 0
    price_map = {
        'Flight': 45000, 
        'Hotel': 35000, 
        'Local_Tour': 15000, 
        'Car_Rental': 10000, 
        'Insurance': 5000
    }
    for item in items:
        base_price += price_map.get(item, 0)
    
    # Apply a bundle discount for combinations of 3 or more items
    if len(items) >= 3:
        return int(base_price * 0.95) # 5% discount
    return base_price

