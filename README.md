# Crew Banking Assistant

A Streamlit banking assistant demo powered by CrewAI, Groq, and a local SQLite database. It can answer account balance, transaction, spending, and customer service questions for the seeded demo user.

## Features

- Account balance and account details
- Recent transactions and spending questions
- Account-opening service requests
- Address change, cheque book, and KYC service requests
- Local SQLite demo data
- CrewAI agent orchestration for general banking questions

## Demo context

This is a demo application:

- Authentication is not enabled.
- The fixed demo user is `USER-1001`.
- The default demo account is `ACCT-1001`.
- Data is recreated when the application starts.

## Requirements

- Python 3.10 or newer
- A Groq API key for CrewAI-powered questions

## Setup

Clone the repository and enter the project directory:

```powershell
git clone https://github.com/sparshavsgowda/Crew_AI.git
cd Crew_AI
```

Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create your local environment file:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and set your own credentials:

```env
GROQ_API_KEY="your_groq_api_key_here"
GROQ_MODEL="openai/gpt-oss-120b"
```

Never commit `.env` or expose your API key.

## Run the application

```powershell
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

## Example questions

- `What is my balance?`
- `Show my recent transactions`
- `How much did I spend?`
- `Create my account`
- `Show my service requests`

## Project structure

```text
app.py                    Streamlit entry point
controllers/              Request routing
models/                   SQLite database setup
services/                 CrewAI orchestration
tools/                    Local banking tools
views/                    Streamlit user interface
requirements.txt          Python dependencies
.env.example              Environment variable template
```

## Disclaimer

This project is for demonstration and educational purposes only. It is not connected to a real bank and must not be used with real customer data or production credentials.
