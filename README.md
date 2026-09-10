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

## MVC architecture

The application follows a Model-View-Controller structure with service and tool layers for orchestration and data access.

### Model

The `models/` package manages the SQLite database, schema, and seeded demo data. The database model is defined in `models/database.py`.

### View

The `views/` package contains the Streamlit interface. `views/streamlit_view.py` displays the chat, collects user prompts, and renders responses.

### Controller

The `controllers/` package handles user requests and routes them to the appropriate local banking tool or CrewAI service. `controllers/banking_controller.py` also provides direct handling for common balance, transaction, spending, and account-opening requests.

### Service and tool layers

- `services/crew_service.py` builds the CrewAI agents and coordinates general banking questions.
- `tools/mcp_tools.py` provides SQLite-backed tools for accounts, transactions, and service requests.

### Request flow

```text
User prompt
	|
	v
Streamlit View
	|
	v
Banking Controller
	|----------------------|
	v                      v
Local Banking Tools     CrewAI Service
	|                      |
	v                      v
SQLite Model          Agent Specialists
```

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
