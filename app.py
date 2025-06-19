# import streamlit as st
# import pandas as pd
# from datetime import datetime
# import requests
# import os
# from dotenv import load_dotenv
# from data_utils import extract_contact_data

# # ✅ Load .env
# load_dotenv()
# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# MODEL = "mistralai/mistral-7b-instruct"  # ✅ Use a working OpenRouter model

# # ✅ Streamlit setup
# st.set_page_config(page_title="LinkedIn Message Generator", layout="centered")
# st.title("🤖 LinkedIn Message Generator (from JSON)")

# # ✅ Step 1: Select company JSON file
# json_files = [f for f in os.listdir(".") if f.endswith(".json") and not f.startswith("temp_")]
# selected_file = st.selectbox("📁 Select a company .json file", ["-- Select --"] + json_files)

# # ✅ Step 2: Load selected data
# info = None
# if selected_file and selected_file != "-- Select --":
#     try:
#         info = extract_contact_data(selected_file)
#         st.success(f"✅ Loaded data from {selected_file}")
#         st.write("**Company:**", info['company'])
#         st.write("**Person:**", info['person_name'])
#         st.write("**Role:**", info['role'])
#         st.write("**Background:**", info['background'])
#     except Exception as e:
#         st.error(f"❌ Error reading {selected_file}: {e}")

# # ✅ Step 3: Generate LinkedIn message
# if info and st.button("🚀 Generate LinkedIn Message"):
#     if not OPENROUTER_API_KEY:
#         st.error("⚠️ API key missing. Set it in your .env file.")
#     else:
#         with st.spinner("Generating message..."):
#             prompt = (
#                 f"You are writing a short LinkedIn DM. Do not use a subject line, 'Dear', or email formatting.\n"
#                 f"Write a casual, friendly message to {info['person_name']} at {info['company']} using the background below.\n"
#                 f"Keep it under 60 words. Goal: start a conversation or ask for a quick chat.\n\n"
#                 f"Background info: {info['background']}"
#             )
#             headers = {
#                 "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#                 "HTTP-Referer": "https://chat.openai.com",
#                 "Content-Type": "application/json"
#             }
#             data = {
#                 "model": MODEL,
#                 "messages": [{"role": "user", "content": prompt}]
#             }
#             response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

#             if response.status_code == 200:
#                 ai_message = response.json()["choices"][0]["message"]["content"].strip()
#                 st.session_state.generated_message = ai_message
#                 st.success("✅ Message generated!")
#             else:
#                 st.error(f"❌ API Error {response.status_code}: {response.text}")

# # ✅ Step 4: Display editable message
# final_message = st.text_area("✍️ Edit your LinkedIn message", value=st.session_state.get("generated_message", ""), height=200)

# # ✅ Step 5: Save message to CSV
# if st.button("💾 Save Message"):
#     if final_message.strip() == "":
#         st.warning("Please generate or type a message first.")
#     else:
#         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         word_count = len(final_message.split())
#         entry = {
#             "Company": info['company'],
#             "Person": info['person_name'],
#             "Role": info['role'],
#             "Message": final_message,
#             "Word Count": word_count,
#             "Timestamp": timestamp
#         }
#         filename = "linkedin_messages.csv"
#         if os.path.exists(filename):
#             df = pd.read_csv(filename)
#             df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
#         else:
#             df = pd.DataFrame([entry])
#         df.to_csv(filename, index=False)
#         st.success("✅ Message saved to CSV!")
#         st.session_state.generated_message = ""

# # ✅ Step 6: View saved messages
# if st.checkbox("📄 Show Saved Messages"):
#     if os.path.exists("linkedin_messages.csv"):
#         df = pd.read_csv("linkedin_messages.csv")
#         st.dataframe(df)
#     else:
#         st.info("No saved messages yet.")


# app.py 2
# import os
# import json
# import pandas as pd
# import streamlit as st
# from datetime import datetime
# import requests
# from dotenv import load_dotenv
# from prompt_template import get_linkedin_template
# from data_utils import extract_contact_data

# # Load API Key
# load_dotenv()
# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# MODEL = "mistralai/mistral-7b-instruct"

# # Set Streamlit config
# st.set_page_config(page_title="LinkedIn Message Generator", layout="centered")
# st.title("🤖 LinkedIn Message Generator from JSON")

# # Step 1: Select a JSON file from dropdown
# json_dir = "./"
# json_files = [f for f in os.listdir(json_dir) if f.endswith(".json") and f not in [".env"]]
# selected_file = st.selectbox("📂 Select a company JSON file", json_files)

# if selected_file:
#     st.markdown(f"**Loaded:** `{selected_file}`")

#     try:
#         json_path = os.path.join(json_dir, selected_file)
#         with open(json_path, "r", encoding="utf-8") as f:
#             full_json = json.load(f)

#         # Show raw JSON (optional for debugging)
#         if st.checkbox("🔍 Show full JSON", value=False):
#             st.json(full_json)

#         # Extract structured info using data_utils
#         info = extract_contact_data(json_path)

#         # Format the user prompt
#         template = get_linkedin_template()
#         user_prompt = template.user_prompt.format(
#             company_name=info["company"],
#             person_name=info["person_name"],
#             role=info["role"],
#             background=info["background"]
#         )

#         if st.button("🚀 Generate LinkedIn Message"):
#             with st.spinner("Generating message using OpenRouter AI..."):
#                 headers = {
#                     "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#                     "HTTP-Referer": "https://chat.openai.com",
#                     "Content-Type": "application/json"
#                 }
#                 data = {
#                     "model": MODEL,
#                     "messages": [
#                         {"role": "system", "content": template.system_prompt},
#                         *[{"role": "user", "content": ex} for ex in template.examples],
#                         {"role": "user", "content": user_prompt}
#                     ]
#                 }

#                 response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

#                 if response.status_code == 200:
#                     ai_message = response.json()["choices"][0]["message"]["content"].strip()
#                     st.session_state.generated_message = ai_message
#                     st.success("✅ Message generated!")
#                 else:
#                     st.error(f"❌ Error: {response.status_code} - {response.text}")

#     except Exception as e:
#         st.error(f"Failed to process file: {e}")

# # Step 3: Editable message + Save
# if "generated_message" in st.session_state:
#     final_message = st.text_area("✍️ Edit the LinkedIn message before saving", st.session_state.generated_message, height=180)

#     if st.button("💾 Save to CSV"):
#         word_count = len(final_message.split())
#         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#         entry = {
#             "Company": info["company"],
#             "Person": info["person_name"],
#             "Role": info["role"],
#             "Message": final_message,
#             "Word Count": word_count,
#             "Timestamp": timestamp
#         }

#         output_file = "linkedin_messages.csv"
#         if os.path.exists(output_file):
#             df = pd.read_csv(output_file)
#             df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
#         else:
#             df = pd.DataFrame([entry])

#         df.to_csv(output_file, index=False)
#         st.success("✅ Message saved to CSV!")

# # Step 4: View previous messages
# if st.checkbox("📄 View saved messages"):
#     if os.path.exists("linkedin_messages.csv"):
#         df = pd.read_csv("linkedin_messages.csv")
#         st.dataframe(df)
#     else:
#         st.info("No messages saved yet.")

#app.py 3
import os
import json
import pandas as pd
import streamlit as st
from datetime import datetime
import requests
from dotenv import load_dotenv
from prompt_template import get_linkedin_template
from data_utils import extract_contact_data

# Load API Key
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "mistralai/mistral-7b-instruct"

# Set Streamlit config
st.set_page_config(page_title="LinkedIn Message Generator", layout="centered")
st.title("🤖 LinkedIn Message Generator from JSON")

# Step 1: Select a JSON file from dropdown
json_dir = "./"
json_files = [f for f in os.listdir(json_dir) if f.endswith(".json") and f not in [".env"]]
selected_file = st.selectbox("📂 Select a company JSON file", json_files)

if selected_file:
    st.markdown(f"**Loaded:** `{selected_file}`")

    try:
        with open(os.path.join(json_dir, selected_file), "r", encoding="utf-8") as f:
            full_json = json.load(f)

        # Show raw JSON (optional for debugging)
        if st.checkbox("🔍 Show full JSON", value=False):
            st.json(full_json)

        # Step 2: Generate Prompt from Template
        template = get_linkedin_template()

        # Build prompt from full JSON
        user_prompt = f"""
Below is a JSON object with company and founder details. Read it fully and generate a concise LinkedIn message following the rules.

JSON Input:
{json.dumps(full_json, indent=2)}

Message:
"""

        prompt = template.system_prompt + "\n\n" + user_prompt

        if st.button("🚀 Generate LinkedIn Message"):
            with st.spinner("Generating message using OpenRouter AI..."):
                headers = {
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "HTTP-Referer": "https://chat.openai.com",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": MODEL,
                    "messages": [
                        {"role": "system", "content": template.system_prompt},
                        *[
                            {"role": "user", "content": ex}
                            for ex in template.examples
                        ],
                        {"role": "user", "content": user_prompt}
                    ]
                }

                response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

                if response.status_code == 200:
                    ai_message = response.json()["choices"][0]["message"]["content"].strip()
                    st.session_state.generated_message = ai_message
                    st.success("✅ Message generated!")
                else:
                    st.error(f"❌ Error: {response.status_code} - {response.text}")

    except Exception as e:
        st.error(f"Failed to read JSON: {e}")

# Step 3: Editable message + Save
if "generated_message" in st.session_state:
    final_message = st.text_area("✍️ Edit the LinkedIn message before saving", st.session_state.generated_message, height=180)

    if st.button("💾 Save to CSV"):
        word_count = len(final_message.split())
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Extract contact data from the JSON file
        contact_info = extract_contact_data(os.path.join(json_dir, selected_file))

        entry = {
            "Company": contact_info["company"],
            "Person": contact_info["person_name"],
            "Role": contact_info["role"],
            "Message": final_message,
            "Word Count": word_count,
            "Timestamp": timestamp
        }
        output_file = "linkedin_messages.csv"
        if os.path.exists(output_file):
            df = pd.read_csv(output_file)
            df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
        else:
            df = pd.DataFrame([entry])

        df.to_csv(output_file, index=False)
        st.success("✅ Message saved to CSV!")

# Step 4: View previous messages
if st.checkbox("📄 View saved messages"):
    if os.path.exists("linkedin_messages.csv"):
        df = pd.read_csv("linkedin_messages.csv")
        st.dataframe(df)
    else:
        st.info("No messages saved yet.")

