import csv

#Global weights for each trait
TRAIT_WEIGHTS = {
    "Medical_Knowledge": 2,
    "Location_Match": 3,
    "Motive": 2,
    "Police_Suspicion": 4,
    "Handwriting_Match": 1
}

#Scoring function
def score_suspect(suspect, trait_weights):
    score = 0
    for trait, weight in trait_weights.items():
        value = suspect.get(trait, "No")
        if value in ["Yes", "High"]:
            score += weight
        elif value == "Medium":
            score += weight * 0.5
    return score

#Load suspects from CSV
def load_suspects(file_path):
    with open(file_path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

# Rank Suspects and display results
def rank_suspects(suspects, trait_weights):
    scored = [
        {"Name": s["Name"], "Score": score_suspect(s, trait_weights)}
        for s in suspects
    ]
    return sorted(scored, key=lambda x: x["Score"],reverse=True)

# Main execution
def main():
    suspects = load_suspects("jack_data.csv")
    ranked = rank_suspects(suspects, TRAIT_WEIGHTS)

    print("🔍 Jack the Ripper Suspect Rankings:")
    for entry in ranked:
        print(f"{entry['Name']}: {entry['Score']} points")

if __name__ == "__main__":
    main()
