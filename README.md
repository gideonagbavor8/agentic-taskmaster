# Taskmaster

Taskmaster is an autonomous workflow execution agent built with **Google ADK** and **Gemini**. It turns natural-language goals into structured tasks, tracks their progress, and executes available actions while enforcing safety controls.

## Features

* Natural-language workflow planning
* Task creation and tracking
* Persistent task storage using a local JSON file
* Task lifecycle management
* Evidence-based task completion
* Gmail integration
* Email preparation and approval workflow
* Explicit user approval required before sending emails
* Google OAuth authentication for Gmail
* Safe handling of task and email state
* Google Calendar event creation

## Architecture

```text
User
  ↓
Taskmaster Agent
  ↓
Workflow Planning
  ↓
Task Management Tools
  ├── create_task
  ├── list_tasks
  ├── start_task
  └── complete_task
  ↓
Action Tools
  ├── prepare_email
  └── approve_email
  ↓
Gmail
```

## Task Lifecycle

Each task follows a controlled lifecycle:

```text
Pending
   ↓
In Progress
   ↓
Completed
```

A task must be started before it can be considered in progress.

A task can only be completed when there is confirmation that the required work was actually performed.

Task state is persisted locally in `tasks.json`, allowing tasks to survive application restarts.

## Email Workflow

Taskmaster uses a two-step workflow for email actions:

```text
prepare_email
      ↓
Awaiting Approval
      ↓
Explicit User Approval
      ↓
approve_email
      ↓
Gmail
```

`prepare_email` creates an email for review but does not send it.

`approve_email` sends the email through Gmail only when explicit approval is provided.

Valid approval values include:

* `yes`
* `approve`
* `approved`
* `send`

The Gmail message ID returned by the Gmail API is used as evidence that the message was successfully sent.

## Technology Stack

* **Python**
* **Google ADK**
* **Gemini API**
* **Google GenAI SDK**
* **Gmail API**
* **Google OAuth 2.0**
* **FastAPI / Uvicorn**
* **JSON-based persistence**

## Project Structure

```text
agentic-taskmaster/
│
├── agent/
│   ├── __init__.py
│   ├── agent.py
│   ├── tools.py
│   ├── email_tools.py
│   ├── gmail_auth.py
│   ├── calendar_tools.py
│   └── .env
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/gideonagbavor8/agentic-taskmaster.git
cd agentic-taskmaster
```

Create a virtual environment:

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the project dependencies:

```powershell
pip install -r requirements.txt
```

## Environment Configuration

Create a file at:

```text
agent/.env
```

Add your Gemini API configuration:

```env
GOOGLE_GENAI_USE_ENTERPRISE=0
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

Replace `YOUR_GEMINI_API_KEY` with your actual API key.

**Never commit API keys or other credentials to Git.**

## Gmail Configuration

Taskmaster can send emails through the Gmail API after explicit user approval.

Gmail integration requires:

1. A Google Cloud project
2. Gmail API enabled
3. OAuth credentials for the application
4. The OAuth client credentials stored locally as `credentials.json`

On the first Gmail authentication, an OAuth token is generated locally.

The following files contain sensitive information and must remain outside version control:

```text
credentials.json
token.json
agent/.env
```

## Running Taskmaster

From the project root, activate the virtual environment and run:

```powershell
adk web
```

This starts the Google ADK development interface where the Taskmaster agent can be tested.

## Example Workflow

A user could provide a goal such as:

> Prepare a client meeting agenda and send it to the client by email.

Taskmaster can break the goal into actionable work:

```text
User Goal
   ↓
Understand Objective
   ↓
Create Tasks
   ↓
Start Task
   ↓
Perform Work
   ↓
Prepare Email
   ↓
Request Explicit Approval
   ↓
Send Through Gmail
   ↓
Verify Result
   ↓
Complete Task
```

The agent is instructed to use the task-management tools throughout the workflow rather than simply claiming that work was completed.

## Safety Design

Taskmaster is designed around controlled execution and evidence-based state changes.

Important safeguards include:

* Tasks must be created through the task-management tools.
* Pending tasks must be started before execution.
* Tasks cannot be completed without confirmation.
* Completed tasks cannot be started again.
* Emails must be prepared before they can be sent.
* Emails cannot be sent without explicit user approval.
* Failed actions are reported instead of being falsely marked as successful.
* The agent must not invent task IDs or task statuses.
* Gmail message IDs provide evidence of successful email transmission.
* API keys and OAuth credentials are excluded from version control.

## Persistence

Taskmaster currently uses a local JSON file for task persistence:

```text
tasks.json
```

The file stores task information such as:

```json
{
  "id": 1,
  "title": "Example Task",
  "description": "Example description",
  "status": "pending"
}
```

The task state can transition between:

```text
pending
in_progress
completed
```

Because the task data is stored on disk, task state survives application restarts.

## Testing

The task-management system has been tested for:

* Task creation
* Task listing
* Task persistence
* Starting pending tasks
* Completing tasks
* Complete task lifecycle
* Prevention of completion without confirmation
* Email approval safety
* Unique task IDs

Example lifecycle:

```text
Create
  ↓
Pending
  ↓
Start
  ↓
In Progress
  ↓
Complete
  ↓
Completed
```

## Current Limitations

* Task persistence currently uses a local JSON file.
* Gmail is currently the primary external action integration.
* The application depends on Gemini API availability and quota.
* The current application is primarily designed for local development and testing.
* Additional external services have not yet been integrated.

## Future Improvements

Potential future extensions include:

* Google Calendar integration
* Google Drive integration
* Web research capabilities
* Additional communication platforms
* Cloud-based task persistence
* Cloud SQL or Firestore integration
* Cloud Run deployment
* Web-based user interface
* Advanced workflow retry and recovery
* Scheduled and recurring workflows
* Additional agent tools

## Security

Sensitive configuration should never be committed to the repository.

The project ignores:

```text
credentials.json
token.json
tasks.json
agent/.env
```

Developers should verify Git status before committing changes:

```powershell
git status
```

If sensitive information appears as a tracked or staged file, remove it before pushing to the repository.

## Development

Check the repository status:

```powershell
git status
```

Run Python syntax checks:

```powershell
python -m py_compile agent/agent.py
```

Install dependencies from the lock-style requirements file:

```powershell
pip install -r requirements.txt
```

## Repository

GitHub repository:

`https://github.com/gideonagbavor8/agentic-taskmaster`

## License

This project is currently developed as a hackathon project.
