import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

def generate_rules(file_path='data/travel_dataset.csv'):
    df = pd.read_csv(file_path)
    df_bool = df[['Flight', 'Hotel', 'Local_Tour', 'Car_Rental', 'Insurance']] == 'Yes'

    freq_items = apriori(df_bool, min_support=0.1, use_colnames=True)
    rules = association_rules(freq_items, metric='lift', min_threshold=1.0)
    rules = rules.sort_values(by='confidence', ascending=False)
    return rules
