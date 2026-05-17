"""
generate_narrative.py
Project: Incident Intelligence Agent
Author: Mayuri Gaikwad
 
Converts each row in incidents.csv into a plain English narrative sentence.
These narratives will later be embedded into vectors for semantic search.
"""

import csv
import json

def load_incidents(filepath):
    with open(filepath, newline='',encoding= 'utf-8-sig') as f:
        return list(csv.DictReader(f))

def to_narrative(row):
    return (
        f"Incident {row['incident_id']} is a {row['category']} issue from {row['source_system']}. "
        f"{row['description']}. "
        f"Root cause: {row['root_cause']}. "
        f"Resolution: {row['resolution']}. "
        f"Amount impacted: {row['amt_impacted']}. "
        f"Status: {row['status']}."
    )
rows = load_incidents("incidents.csv")

narratives =[]
for row in rows:
    narratives.append({
        "incident_id": row["incident_id"],
        "narrative": to_narrative(row)
        })

with open("narratives.json", "w") as f:
    json.dump(narratives, f, indent=2)
 
print(f"Done! {len(narratives)} narratives saved to narratives.json")
 