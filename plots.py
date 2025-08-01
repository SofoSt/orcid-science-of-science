import pandas as pd
import ast
import matplotlib.pyplot as plt
import os
from collections import Counter

# === Create 'plots' folder if it doesn't exist ===
os.makedirs("plots", exist_ok=True)

# === Load the dataset ===
df = pd.read_csv("researchers_with_domains.csv")
df["domain_affinity"] = df["domain_affinity"].apply(ast.literal_eval)

# === Plot 1: Bar plot showing how many researchers belong to each domain (with weight >= 30%) ===
domain_counter = Counter()
for d in df["domain_affinity"]:
    for k, v in d.items():
        if v >= 0.3:
            domain_counter[k] += 1

plt.figure(figsize=(20, 8))  # Wider & taller figure

# Sort and plot
domain_series = pd.Series(domain_counter).sort_values(ascending=False)
domain_series.plot(kind="bar")

# Styling
plt.title("Number of Researchers per Scientific Domain (≥ 30%)", fontsize=14)
plt.ylabel("Number of Researchers", fontsize=12)
plt.xlabel("Scientific Domain", fontsize=12)

plt.xticks(
    rotation=75,         # More rotation
    ha='right',          # Right-aligned
    fontsize=10,         # Smaller font
)

plt.tight_layout()
plt.subplots_adjust(bottom=0.35)  # More space for labels
plt.savefig("plots/researchers_by_domain.png")
plt.close()
print(" Saved: plots/researchers_by_domain.png")



# === Plot 2: Pie chart for a specific researcher OID ===
example_oid = "0000-0002-0640-4001"
row = df[df["OID"] == example_oid]

if not row.empty:
    domain_distribution = row.iloc[0]["domain_affinity"]
    plt.figure(figsize=(6, 6))
    plt.pie(domain_distribution.values(), labels=domain_distribution.keys(), autopct="%1.1f%%", startangle=140)
    plt.title(f"Domain Distribution for OID {example_oid}")
    plt.tight_layout()
    plt.savefig(f"plots/domain_distribution_{example_oid}.png")
    plt.close()
    print(f" Saved: plots/domain_distribution_{example_oid}.png")
else:
    print(f" OID {example_oid} not found.")




# === Plot 2: Pie chart for a specific researcher OID ===
example_oid = "0000-0002-0640-4001"
row = df[df["OID"] == example_oid]

if not row.empty:
    domain_distribution = row.iloc[0]["domain_affinity"]
    plt.figure(figsize=(6, 6))
    plt.pie(domain_distribution.values(), labels=domain_distribution.keys(), autopct="%1.1f%%", startangle=140)
    plt.title(f"Domain Distribution for OID {example_oid}")
    plt.tight_layout()
    plt.savefig(f"plots/domain_distribution_{example_oid}.png")
    plt.close()
    print(f" Saved: plots/domain_distribution_{example_oid}.png")
else:
    print(f" OID {example_oid} not found.")


# === Plot 3: Custom Plot for a Specific Researcher ===
target_oid = "0000-0001-8781-4039"

# Filter for that researcher
row = df[df["OID"] == target_oid]

if not row.empty:
    domain_affinity = row.iloc[0]["domain_affinity"]
    department = row.iloc[0]["clean_dept"]
    fname = row.iloc[0]["Fname"]
    gname = row.iloc[0]["Gname"]
    
    # Sort for nicer bar plot
    domain_affinity = dict(sorted(domain_affinity.items(), key=lambda x: x[1], reverse=True))
    
    # Bar Plot
    plt.figure(figsize=(8, 5))
    plt.bar(domain_affinity.keys(), domain_affinity.values())
    plt.title(f"Scientific Domains of {fname} {gname} ({target_oid})\nDepartment: {department}", fontsize=11)
    plt.ylabel("Domain Affinity")
    plt.xticks(rotation=45, ha="right", fontsize=9)
    plt.tight_layout()
    filename = f"plots/domain_affinity_{target_oid}.png"
    plt.savefig(filename)
    plt.close()
    print(f" Saved: {filename}")
else:
    print(f" OID {target_oid} not found in the dataset.")
