import pandas as pd
from collections import defaultdict
from tqdm import tqdm
import time 


df = pd.read_csv("researcher_domain_affinity.csv", low_memory=False)

print("Processing researcher domain affinity...")

# Parse stringified dictionaries
df["domain_affinity"] = df["domain_affinity"].apply(eval)

# === Manual groupby with tqdm progress ===
grouped = df.groupby("OID")["domain_affinity"]
oids = list(grouped.groups.keys())  # list of OIDs for tqdm

results = []
for i, oid in enumerate(tqdm(oids, desc="Aggregating researcher affinities", ncols=80, dynamic_ncols=True)):
    series = grouped.get_group(oid)
    agg = defaultdict(float)
    for d in series:
        for k, v in d.items():
            agg[k] += v
    total = sum(agg.values())
    normalized = {k: round(v / total, 6) for k, v in agg.items()} if total > 0 else {}
    results.append({"OID": oid, "domain_affinity": normalized})

    if i % 100 == 0:
        print(f"Processed {i} researchers")

# Create DataFrame from results
researcher_affinity_df = pd.DataFrame(results)

# Add researcher metadata
meta_cols = ["OID", "Fname", "Gname", "locale", "Role", "Org"]
researcher_info = df[meta_cols].drop_duplicates(subset=["OID"])
df_final = pd.merge(researcher_info, researcher_affinity_df, on="OID", how="left")

# Save result
df_final.to_csv("researcher_overall_domain_affinity.csv", index=False)
print("✅ Saved to 'researcher_overall_domain_affinity.csv'")
