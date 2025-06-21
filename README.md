# 🤖 LinkedIn Message Generator

Generate investor-style LinkedIn outreach messages in one click using FastAPI, Streamlit, and OpenRouter's AI models.

---

## 🚀 Features

- 🔍 Fetches company/founder data via API from local JSON files
- ✨ Uses a strict prompt template to generate short, professional LinkedIn messages
- 🧠 Powered by `mistralai/mistral-7b-instruct` via OpenRouter
- 📝 Edit messages before saving
- 💾 Saves messages to a CSV file for tracking
- 🌐 API-first design (fetch + save via FastAPI backend)

---

## 📂 Project Structure

```bash
Linkedin-Messenger/
├── app.py                 # Streamlit frontend
├── main.py                # FastAPI backend
├── api_utils.py           # Optional helpers to fetch/save data locally
├── data_utils.py          # Extracts structured info from JSON
├── prompt_template.py     # Defines prompt and example messages
├── .env                   # API keys and base URL
├── messages.csv  # Saved message log
├── Json Files/            # All company JSON data files
│   ├── airbnb.json
│   ├── databricks.json
│   └── ...
```

## ⚙️ Requirements

Install the required libraries:

```bash
pip install -r requirements.txt
```
If requirements.txt is missing, manually install:
```bash
pip install streamlit fastapi uvicorn python-dotenv requests pandas
```
## Environment Setup
Create a .env file in the root directory:
```env
OPENROUTER_API_KEY=your_openrouter_api_key
SAASQUATCH_API_BASE=http://localhost:8000
```
## 🧪 Run Locally
- 1. Start the FastAPI backend:
  
```
uvicorn main:app --reload
```
- 2. In another terminal, run the Streamlit frontend:
```
streamlit run app.py
```
## How It Works
- User enters a company name (e.g. "Airbnb")
- /api/fetch-company-data fetches the corresponding airbnb.json file
- Prompt is generated using a strict investor-style message template
- AI model (mistral-7b-instruct) creates a concise, 60-word LinkedIn message
- User can edit the message
- On save, data is POSTed to /api/save-message and stored in messages.csv

## Example Message
Noted Airbnb’s push into luxury rentals. How are you balancing brand trust while scaling into premium markets? Open to a short exchange on this?

##  License
MIT License


Copyright (c) 2025 SK Shaid Hossain

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights  
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell     
copies of the Software, and to permit persons to whom the Software is         
furnished to do so, subject to the following conditions:                      

The above copyright notice and this permission notice shall be included in    
all copies or substantial portions of the Software.                           

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR   
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,     
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER       
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN    
THE SOFTWARE.
