import flet as ft
import csv

TRAIT_WEIGHTS = {
    "Medical_Knowledge": 2,
    "Location_Match": 3,
    "Motive": 2,
    "Police_Suspicion": 4,
    "Handwriting_Match": 1
}

CSV_FILE = "jack_data.csv"

def score_suspect(suspect):
    score = 0
    for trait, weight in TRAIT_WEIGHTS.items():
        value = suspect.get(trait, "No")
        if value in ["Yes", "High"]:
            score += weight
        elif value == "Medium":
            score += weight * 0.5
    return score

def load_suspects():
    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def add_suspect(data):
    with open(CSV_FILE, "a", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        writer.writerow(data)

def main(page: ft.Page):
    page.title = "Jack the Ripper Suspect Profiler"
    page.scroll = "AUTO"

    name = ft.TextField(label="Name")
    traits = {
        trait: ft.Dropdown(label=trait, options=[
            ft.dropdown.Option("Yes"),
            ft.dropdown.Option("No"),
            ft.dropdown.Option("High"),
            ft.dropdown.Option("Medium"),
            ft.dropdown.Option("Low")
        ]) for trait in TRAIT_WEIGHTS
    }

    result = ft.Column()

    def refresh():
        result.controls.clear()
        suspects = load_suspects()
        ranked = sorted(suspects, key=score_suspect, reverse=True)
        for s in ranked:
            score = score_suspect(s)
            result.controls.append(ft.Text(f"{s['Name']}: {score} points"))
        page.update()

    def on_submit(e):
        new_data = {"Name": name.value}
        for trait, dropdown in traits.items():
            new_data[trait] = dropdown.value or "No"
        add_suspect(new_data)
        name.value = ""
        for dropdown in traits.values():
            dropdown.value = None
        refresh()

    form = ft.Column([
        name,
        *traits.values(),
        ft.ElevatedButton("Add Suspect", on_click=on_submit)
    ])

    page.add(form, ft.Divider(), result)
    refresh()

ft.app(target=main)