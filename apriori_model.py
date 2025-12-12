import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

def generate_rules():
    df = pd.read_csv("data/travel_dataset.csv")

    # Convert items to one-hot encoded format
    df_encoded = df.drop("Transaction_ID", axis=1)
    df_encoded = df_encoded.astype(bool)

    # Frequent itemsets
    frequent_itemsets = apriori(df_encoded, min_support=0.05, use_colnames=True)

    # Rules
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.3)

    # Convert frozensets to normal lists for display
    rules["antecedents"] = rules["antecedents"].apply(lambda x: list(x))
    rules["consequents"] = rules["consequents"].apply(lambda x: list(x))

    return rules

