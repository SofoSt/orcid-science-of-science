import pandas as pd
import ast

# Load the dataset
df = pd.read_csv("researcher_overall_domain_affinity.csv", low_memory=False)

# Convert stringified dictionaries to actual dictionaries
df["domain_affinity"] = df["domain_affinity"].apply(ast.literal_eval)

# Split into two DataFrames
df_with_domains = df[df["domain_affinity"].apply(lambda d: len(d) > 0)]
df_without_domains = df[df["domain_affinity"].apply(lambda d: len(d) == 0)]

# Save to separate files
df_with_domains.to_csv("researchers_with_domains.csv", index=False)
df_without_domains.to_csv("researchers_without_domains.csv", index=False)

print(" Saved 'researchers_with_domains.csv' and 'researchers_without_domains.csv'")
