import json

# Load the cookie JSON
with open("linkedin_state.json", "r") as file:
    data = json.load(file)

# Extract cookie dictionary for requests
cookies_dict = {cookie["name"]: cookie["value"] for cookie in data["cookies"]}

# Print cookies
for name, value in cookies_dict.items():
    print(f"{name} = {value}")
