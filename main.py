from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import os
import json
import csv

app = FastAPI()

# ---------- Models ----------
class CompanyRequest(BaseModel):
    company: str

class MessageSaveRequest(BaseModel):
    company: str
    person: str
    role: str
    message: str
    word_count: int
    timestamp: str

# ---------- API 1: Fetch Company Data ----------
@app.post("/api/fetch-company-data")
async def fetch_company_data(request: CompanyRequest):
    company = request.company
    file_name = f"{company.lower().replace(' ', '_')}.json"
    file_path = os.path.join(".", file_name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"No JSON found for {company}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading JSON: {e}")

# ---------- API 2: Save Generated Message ----------
@app.post("/api/save-message")
async def save_message(request: MessageSaveRequest):
    file_exists = os.path.isfile("messages.csv")

    try:
        with open("messages.csv", mode="a", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Company", "Person", "Role", "Message", "Word Count", "Timestamp"])
            writer.writerow([
                request.company,
                request.person,
                request.role,
                request.message,
                request.word_count,
                request.timestamp
            ])
        return {"status": "success", "message": "Saved to CSV"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving to CSV: {e}")
