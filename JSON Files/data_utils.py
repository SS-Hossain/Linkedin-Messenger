# import json
# import os

# def extract_contact_data(json_path):
#     if not os.path.exists(json_path):
#         raise FileNotFoundError(f"{json_path} not found.")

#     with open(json_path, 'r', encoding='utf-8') as f:
#         data = json.load(f)

#     founder_list = data.get("founder_names", [])
#     primary_founder = founder_list[0] if founder_list else "Someone"

#     return {
#         "company": data.get("company_name") or data.get("company") or os.path.basename(json_path).replace(".json", ""),
#         "person_name": primary_founder,
#         "role": data.get("role") or "Founder",
#         "background": data.get("company_overview") or data.get("description", "")
#     }

import json
import os


def extract_contact_data(json_path):
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"{json_path} not found.")

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    founder_list = data.get("founder_names", [])
    primary_founder = founder_list[0] if founder_list else "Someone"

    return {
        "company": data.get("company_name") or data.get("company") or os.path.basename(json_path).replace(".json", ""),
        "person_name": primary_founder,
        "role": data.get("role") or "Founder",
        "background": data.get("company_overview") or data.get("description", "")
    }