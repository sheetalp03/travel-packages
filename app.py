import streamlit as st
import pandas as pd
from apriori_model import generate_rules
import streamlit.components.v1 as components

# -----------------------------
# PAGE TITLE
# -----------------------------
st.title("🌍 Travel Package Recommendation System")
st.markdown("Using **Association Rule Mining** to suggest bundled services.")

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("data/travel_dataset.csv")
rules = generate_rules()

# -----------------------------
# TABS
# -----------------------------
tab1, tab2 = st.tabs(["🔮 Recommendation System", "🧳 Travel Packages"])

# -----------------------------
# TAB 1 — RECOMMENDER
# -----------------------------
with tab1:
    st.sidebar.header("🧳 Your Selections")

    services = ['Flight', 'Hotel', 'Local_Tour', 'Car_Rental', 'Insurance']
    user_choices = [service for service in services if st.sidebar.checkbox(service)]

    if user_choices:
        st.subheader("📢 Suggested Add-ons")

        # FIX: convert antecedents to set
        filtered_rules = rules[
            rules["antecedents"].apply(lambda x: set(user_choices).issubset(set(x)))
        ]

        if not filtered_rules.empty:
            for _, row in filtered_rules.head(5).iterrows():
                st.markdown(
                    f"➡️ If you selected **{', '.join(row['antecedents'])}**, "
                    f"consider adding **{', '.join(row['consequents'])}** "
                    f"(Confidence: {row['confidence']:.2f})"
                )
        else:
            st.warning("No strong rules found for your selection.")
    else:
        st.info("Select services from the sidebar to get recommendations.")

    st.subheader("📊 Top Association Rules")
    st.dataframe(
        rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(10)
    )

# -----------------------------
# TAB 2 — HTML FILE DISPLAY
# -----------------------------
with tab2:
    st.subheader("✨ Explore All Travel Packages")
    with open("packages.html", "r", encoding="utf-8") as f:
        html_data = f.read()
    components.html(html_data, height=900, scrolling=True)

