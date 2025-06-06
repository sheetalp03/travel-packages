import streamlit as st
import pandas as pd
from apriori_model import generate_rules

st.title("🌍 Travel Package Recommendation System")
st.markdown("Using Association Rule Mining to suggest bundled services")

df = pd.read_csv('C:/Users/shrip/OneDrive/Desktop/travel-packages-master/data/travel_dataset.csv')

rules = generate_rules()

services = ['Flight', 'Hotel', 'Local_Tour', 'Car_Rental', 'Insurance']
st.sidebar.header("🧳 Your Current Selection")
user_choices = [service for service in services if st.sidebar.checkbox(service)]

if user_choices:
    st.subheader("📢 Suggested Add-ons:")
    filtered_rules = rules[rules['antecedents'].apply(lambda x: set(user_choices).issubset(x))]
    if not filtered_rules.empty:
        for _, row in filtered_rules.head(5).iterrows():
            st.markdown(f"➡️ If you selected **{', '.join(row['antecedents'])}**, consider adding **{', '.join(row['consequents'])}** (Confidence: {row['confidence']:.2f})")
    else:
        st.warning("No strong rules found for your selection.")
else:
    st.info("Select services from the sidebar to get recommendations.")

st.subheader("📊 Association Rules")
st.dataframe(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(10))
