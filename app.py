import os
import json
import pandas as pd
import streamlit as st
from datetime import datetime
import requests
from dotenv import load_dotenv
from prompt_template import get_linkedin_template

# Load API Keys
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "mistralai/mistral-7b-instruct"
API_BASE = os.getenv("SAASQUATCH_API_BASE", "http://localhost:8000")

st.set_page_config(page_title="LinkedIn Message Generator", layout="centered")
st.title("🤖 LinkedIn Message Generator from API")

# Step 1: Get input from user
company_name = st.text_input("Enter company name (e.g. OpenAI, Airbnb)")

if company_name and st.button("🔍 Fetch & Generate"):
    try:
        # Step 2: Fetch company data from FastAPI
        with st.spinner("Fetching data from Saasquatch API..."):
            res = requests.post(f"{API_BASE}/api/fetch-company-data", json={"company": company_name})
            if res.status_code != 200:
                raise Exception(f"API Error: {res.text}")
            full_json = res.json()
            st.session_state["full_json"] = full_json  # ✅ Store in session
            st.success("✅ Company data loaded!")

        if st.checkbox("🔍 Show full JSON", value=False):
            st.json(full_json)

        # Step 3: Prompt generation
        template = get_linkedin_template()
        user_prompt = f"""
Below is a JSON object with company and founder details. Read it fully and generate a concise LinkedIn message following the rules.

JSON Input:
{json.dumps(full_json, indent=2)}

Message:
"""

        prompt = template.system_prompt + "\n\n" + user_prompt

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
                    *[{"role": "user", "content": ex} for ex in template.examples],
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
        st.error(f"Failed: {e}")

# Step 4: Editable message + Save
if "generated_message" in st.session_state:
    final_message = st.text_area("✍️ Edit the LinkedIn message before saving", st.session_state.generated_message, height=180)

    if st.button("💾 Save to API"):
        word_count = len(final_message.split())
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        data = st.session_state.get("full_json", {})
        person = data.get("founder_names", ["Someone"])[0]
        role = data.get("role") or data.get("title", "Founder")

        payload = {
            "company": company_name,
            "person": person,
            "role": role,
            "message": final_message,
            "word_count": word_count,
            "timestamp": timestamp
        }

        res = requests.post(f"{API_BASE}/api/save-message", json=payload)
        if res.status_code == 200:
            st.success("✅ Message saved via API!")
        else:
            st.error("❌ Failed to save message.")

# Step 5: View saved messages
if st.checkbox("📄 View saved messages"):
    if os.path.exists("messages.csv"):  # match FastAPI output
        df = pd.read_csv("messages.csv")
        st.dataframe(df)
    else:
        st.info("No messages saved yet.")
