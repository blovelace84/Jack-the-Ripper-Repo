import csv
def load_suspects(filename):
    suspects = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            suspect = {
                "name": row["name"],
                "motive": int(row["motive"]),
                "alibi": int(row["alibi"]),
                "location": int(row["location"]),
                "witness": int(row["witness"]),
                "notes": row["notes"]
            }
            suspects.append(suspect)
        return suspects

def calculate_score(suspect, weights):
    return round(sum(suspect[key] * weights[key] for key in weights), 2)

def analyze_suspects(suspects, weights):
    for suspect in suspects:
        suspect["score"] = calculate_score(suspect, weights)
    return sorted(suspects, key=lambda x: x["score"], reverse=True)

def display_results(suspects, weights=None):
    for s in suspects:
        print(f"{s['name']}: {s['score']} - {s['notes']}")
        
    if __name__ == "__main__":
        suspects = load_suspects("suspects.csv")
        ranked = analyze_suspects(suspects, weights)
        display_results(ranked)

        print("Loaded suspects:", suspects)