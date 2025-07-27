import json

with open("linkedin_state.json", "r") as file:
    data = json.load(file)

for cookie in data["cookies"]:
    if cookie["name"] == "li_at":
        print("Your li_at token is:\n", cookie["value"])
