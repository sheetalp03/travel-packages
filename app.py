# app.py (Pure Streamlit Application)

import streamlit as st
import pandas as pd
from apriori_model import generate_packages # Import your package generation function

# --- Dummy Rules Data (For testing before connecting to your live model output) ---
# Replace this with the code that loads your actual Apriori rules DataFrame
DUMMY_RULES_DATA = pd.DataFrame([
    {'antecedents': frozenset({'Flight'}), 'consequents': frozenset({'Hotel'}), 'support': 0.8},
    {'antecedents': frozenset({'Hotel'}), 'consequents': frozenset({'Local_Tour'}), 'support': 0.7},
    {'antecedents': frozenset({'Flight'}), 'consequents': frozenset({'Car_Rental'}), 'support': 0.6},
    {'antecedents': frozenset({'Local_Tour'}), 'consequents': frozenset({'Insurance'}), 'support': 0.5},
    # Ensure there's a comprehensive option, which generate_packages should handle
    {'antecedents': frozenset({'Flight', 'Hotel'}), 'consequents': frozenset({'Local_Tour', 'Car_Rental'}), 'support': 0.4},
])


# --- FUNCTION TO GENERATE AND DISPLAY CARDS ---
def display_travel_packages():
    """
    Calls the backend model and uses Streamlit components to display the packages
    in the attractive card format.
    """
    st.title("✨ Explore All Travel Packages")

    try:
        # Get the cleaned list of suggested packages from your model
        # NOTE: Pass your actual rules data here instead of DUMMY_RULES_DATA 
        suggested_packages = generate_packages(DUMMY_RULES_DATA)
    except Exception as e:
        st.error(f"Error loading package suggestions from model: {e}")
        # Use a fallback list if the model fails
        suggested_packages = [
            {'title': 'Essential Package (Fallback)', 
             'items': ['Flight', 'Hotel'], 
             'description': 'Basic package available.', 
             'estimated_price_inr': 80000}
        ]

    # --- CSS for Attractive Card Layout (Embedded in Streamlit) ---
    # This CSS recreates the look we designed for your package.html
    st.markdown("""
        <style>
        .package-card {
            background: #ffffff;
            padding: 20px;
            margin-bottom: 25px;
            border-radius: 15px; 
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            text-align: center;
            border-top: 5px solid transparent; 
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            height: 100%; /* Ensures cards align nicely in columns */
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .package-card:hover {
            transform: translateY(-5px); 
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
            border-top-color: #2ecc71; /* Green accent on hover */
        }
        .package-card h3 {
            color: #34495e;
            font-size: 1.5em;
            margin-bottom: 10px;
        }
        .icon {
            font-size: 40px;
            margin-bottom: 10px;
            /* Gradient effect using transparent text fill */
            background: linear-gradient(45deg, #3498db, #2ecc71);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: block; 
        }
        .price-display {
            font-size: 1.8em;
            color: #e74c3c;
            font-weight: 700;
            margin: 10px 0;
        }
        .book-button {
            display: inline-block;
            margin-top: 15px;
            padding: 10px 20px;
            background-color: #2ecc71; 
            color: white !important; /* Force white text */
            text-decoration: none;
            border-radius: 50px; 
            font-weight: bold;
            border: none;
            cursor: pointer;
            width: 100%; /* Full width button */
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Define a simple icon map for display
    icon_map = {
        'Flight': '✈️', 'Hotel': '🏨', 'Local_Tour': '🚌', 
        'Car_Rental': '🚗', 'Insurance': '🛡️', 'Bundle': '🌍'
    }

    # Streamlit automatically handles responsive columns
    cols = st.columns(3) # Display 3 packages per row

    for i, package in enumerate(suggested_packages):
        col = cols[i % 3] # Cycle through the three columns

        # Determine the primary icon
        if 'Flight' in package['items'] and 'Hotel' in package['items']:
            package_icon = icon_map['Bundle']
        else:
            # Use the first item's icon, or the bundle icon if complex
            first_item = list(package['items'])[0] if package['items'] else 'Bundle'
            package_icon = icon_map.get(first_item, '❓')

        # Use st.markdown to inject the custom HTML for the card
        with col:
            st.markdown(f"""
                <div class="package-card">
                    <div>
                        <div class="icon">{package_icon}</div>
                        <h3>{package['title']}</h3>
                        <p>{package['description']}</p>
                        <p>Items: {', '.join(item.replace('_', ' ') for item in package['items'])}</p>
                    </div>
                    <div>
                        <div class="price-display">
                            ₹ {package['estimated_price_inr']:,}
                        </div>
                        <a href="#" class="book-button">Book Now</a>
                    </div>
                </div>
            """, unsafe_allow_html=True)


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    display_travel_packages()
    
# NOTE: The if __name__ == '__main__': app.run(debug=True) has been completely REMOVED.
