# Taskmaster

Taskmaster is an autonomous workflow execution agent built with **Google ADK** and **Gemini**.

It turns natural-language goals into structured tasks, tracks task progress, and executes available actions while enforcing safety controls around task state, email sending, and external actions.

## Features

* Natural-language workflow planning
* Autonomous multi-step task execution
* Task creation and tracking
* Persistent task storage using **Google Cloud Firestore**
* Controlled task lifecycle management
* Evidence-based task completion
* Gmail integration
* Email preparation and approval workflow
* Explicit user approval required before sending emails
* Google OAuth authentication for Gmail
* Google Calendar event creation
* Cloud-based task persistence across application restarts
* Persistent task state across agent instances
* Safe handling of task and email state
* Google Cloud authentication through Application Default Credentials

## Architecture

```text
                         User
                           │
                           ▼
                   ┌─────────────────┐
                   │    Taskmaster   │
                   │      Agent      │
                   └────────┬────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │  Google ADK +   │
                   │ Gemini 3.5 Flash│
                   └────────┬────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │ Workflow Planning │
                  └─────────┬─────────┘
                            │
             ┌──────────────┴──────────────┐
             │                             │
             ▼                             ▼
    ┌─────────────────────┐       ┌─────────────────────┐
    │ Task Management     │       │ Action Tools        │
    │ Tools               │       │                     │
    │                     │       │ prepare_email       │
    │ create_task         │       │ approve_email       │
    │ list_tasks          │       │ create_calendar_    │
    │ start_task          │       │ event               │
    │ complete_task       │       │                     │
    └──────────┬──────────┘       └──────────┬──────────┘
               │                             │
               ▼                             ├──────────► Gmail API
    ┌──────────────────────┐                 │
    │ Google Cloud         │                 └──────────► Google Calendar API
    │ Firestore            │
    │                      │
    │ Database: taskflow-db│
    │ Collection: tasks    │
    └──────────────────────┘
```

## Google Cloud Integration

Taskmaster uses Google Cloud services as part of its core architecture.

### Google Cloud Firestore

Firestore is used as the persistent task database.

```text
Google Cloud Project
└── gen-lang-client-0349849444
    │
    └── Firestore
        │
        └── taskflow-db
            │
            └── tasks
                ├── 1
                ├── 2
                ├── 3
                └── ...
```

Firestore allows Taskmaster to maintain task state beyond the lifetime of a local Python process.

### Firestore Configuration

| Setting     | Value                        |
| ----------- | ---------------------------- |
| Project ID  | `gen-lang-client-0349849444` |
| Database ID | `taskflow-db`                |
| Collection  | `tasks`                      |
| Edition     | Standard                     |
| Mode        | Firestore Native             |
| Location    | `nam5`                       |

Each task is stored as a Firestore document using the task ID as the document ID.

Example:

```json
{
  "id": 1,
  "title": "Example Task",
  "description": "Example description",
  "status": "pending"
}
```

## Task Lifecycle

Each task follows a controlled lifecycle:

```text
Pending
   │
   ▼
In Progress
   │
   ▼
Completed
```

A task must be started before it can be considered in progress.

A task can only be completed when there is confirmation that the required work was actually performed.

Completed tasks cannot be started again.

Task state is persisted in Google Cloud Firestore, allowing tasks to survive application restarts and remain available across different agent instances.

## Firestore Persistence

Taskmaster uses **Google Cloud Firestore** instead of local JSON storage for task persistence.

The application connects to:

```text
Project:
gen-lang-client-0349849444

Database:
taskflow-db

Collection:
tasks
```

Each task is stored as a Firestore document.

For example:

```text
tasks/1
tasks/2
tasks/3
```

A task document contains:

```json
{
  "id": 1,
  "title": "Example Task",
  "description": "Example description",
  "status": "pending"
}
```

Supported task states are:

```text
pending
in_progress
completed
```

Because task data is stored in Firestore, task state survives application restarts and can be accessed by different instances of the agent.

## Task Management Tools

Taskmaster provides four core task-management tools.

### `create_task`

Creates a new task in Google Cloud Firestore.

```text
create_task
     │
     ▼
Google Cloud Firestore
     │
     ▼
New Task
     │
     ▼
pending
```

Each task receives a numeric task ID.

### `list_tasks`

Retrieves all tasks currently stored in the Firestore `tasks` collection.

Tasks are returned in ascending task ID order.

### `start_task`

Moves a task into the `in_progress` state.

A task that has already been completed cannot be started again.

### `complete_task`

Moves a task into the `completed` state.

Completion requires confirmation that the work was actually performed.

The tool refuses to complete a task when no confirmation is provided.

## Email Workflow

Taskmaster uses a controlled two-step workflow for email actions.

```text
prepare_email
      │
      ▼
Awaiting Approval
      │
      ▼
Explicit User Approval
      │
      ▼
approve_email
      │
      ▼
Gmail API
```

### `prepare_email`

Creates an email for review but does not send the email.

### `approve_email`

Sends the email through Gmail only when explicit user approval is provided.

Valid approval values include:

```text
yes
approve
approved
send
```

Silence, ambiguity, or a general request to prepare an email is never treated as approval to send.

The Gmail message ID returned by the Gmail API provides evidence that the email was successfully sent.

## Calendar Workflow

Taskmaster can create Google Calendar events through the calendar action tool.

A calendar action can be used as part of a larger workflow where the agent determines that scheduling an event is required.

Example workflow:

```text
User Goal
    │
    ▼
Workflow Planning
    │
    ▼
Create Task
    │
    ▼
Start Task
    │
    ▼
Create Calendar Event
    │
    ▼
Verify Result
    │
    ▼
Complete Task
```

Calendar event creation is performed through the configured Google Calendar integration.

## Agent Behavior

Taskmaster is designed to execute workflows rather than behave as a simple question-and-answer chatbot.

For each user goal, the agent is instructed to:

1. Understand the user's objective.
2. Break the objective into actionable steps.
3. Determine which tools are required.
4. Create tasks for actionable work.
5. Start tasks before performing the associated work.
6. Execute available actions in the correct order.
7. Track progress using the task-management tools.
8. Verify that actions actually succeeded.
9. Complete tasks only when there is evidence that the required work was performed.
10. Report failures instead of falsely claiming success.

The agent is explicitly instructed not to invent task IDs, task states, workflow steps, or successful outcomes.

## Technology Stack

* **Python**
* **Google ADK**
* **Gemini 3.5 Flash**
* **Google GenAI SDK**
* **Google Cloud Firestore**
* **Gmail API**
* **Google Calendar API**
* **Google OAuth 2.0**
* **Application Default Credentials**
* **Uvicorn**

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
├── .gitignore
├── requirements.txt
└── README.md
```

Sensitive local files such as `credentials.json` and `token.json` are not part of the version-controlled source tree.

## Installation

Clone the repository:

```bash
git clone https://github.com/gideonagbavor8/agentic-taskmaster.git
cd agentic-taskmaster
```

Create a virtual environment.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the project dependencies:

```powershell
pip install -r requirements.txt
```

## Environment Configuration

Create the environment file:

```text
agent/.env
```

Add your Gemini API configuration:

```env
GOOGLE_GENAI_USE_ENTERPRISE=0
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

Replace:

```text
YOUR_GEMINI_API_KEY
```

with your actual Gemini API key.

**Never commit API keys or other credentials to Git.**

## Google Cloud Firestore Configuration

Taskmaster uses Google Cloud Firestore for persistent task storage.

The configured Firestore resources are:

```text
Project ID:
gen-lang-client-0349849444

Database ID:
taskflow-db

Collection:
tasks
```

The Firestore database uses:

```text
Edition:
Standard

Mode:
Firestore Native

Location:
nam5
```

### Application Default Credentials

Google Cloud authentication must be configured before using Firestore locally.

Run:

```powershell
gcloud auth application-default login
```

Verify the active Google Cloud account:

```powershell
gcloud auth list
```

Verify that the Firestore database exists:

```powershell
gcloud firestore databases list --project=gen-lang-client-0349849444
```

The application initializes the Firestore client using the configured Google Cloud project and database.

## Gmail Configuration

Taskmaster can send emails through the Gmail API after explicit user approval.

Gmail integration requires:

1. A Google Cloud project
2. Gmail API enabled
3. OAuth credentials for the application
4. OAuth client credentials stored locally as `credentials.json`

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

Taskmaster can turn the goal into an executable workflow:

```text
User Goal
    │
    ▼
Understand Objective
    │
    ▼
Create Tasks
    │
    ▼
Start Task
    │
    ▼
Perform Work
    │
    ▼
Prepare Email
    │
    ▼
Request Explicit Approval
    │
    ▼
Send Through Gmail
    │
    ▼
Verify Result
    │
    ▼
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
* Firestore provides persistent task state.
* API keys and OAuth credentials are excluded from version control.
* Sensitive credentials must never be included in source code.

## Persistence

Taskmaster uses Google Cloud Firestore as its persistence layer.

```text
Google Cloud Firestore
│
└── taskflow-db
    │
    └── tasks
        │
        ├── 1
        ├── 2
        ├── 3
        └── ...
```

Each document contains the information required to track the task lifecycle.

Example:

```json
{
  "id": 1,
  "title": "Example Task",
  "description": "Example description",
  "status": "pending"
}
```

Task states are:

```text
pending
in_progress
completed
```

Task data stored in Firestore survives application restarts and can be accessed by different instances of the agent.

## Firestore Connection Test

The Firestore connection can be tested locally with:

```powershell
.\.venv\Scripts\python -c "from google.cloud import firestore; db=firestore.Client(project='gen-lang-client-0349849444', database='taskflow-db'); print('Firestore connection successful')"
```

A successful connection returns:

```text
Firestore connection successful
```

## Firestore Task Lifecycle Test

The task-management tools can be tested directly.

### Create and list a task

```powershell
.\.venv\Scripts\python -c "from agent.tools import create_task, list_tasks; print(create_task('Firestore integration test', 'Verify Taskmaster can create tasks in Firestore.')); print(list_tasks())"
```

### Start and complete the task

```powershell
.\.venv\Scripts\python -c "from agent.tools import start_task, complete_task, list_tasks; print(start_task(1)); print(complete_task(1, 'Firestore integration test was successfully performed.')); print(list_tasks())"
```

Expected lifecycle:

```text
Create
  │
  ▼
Firestore
  │
  ▼
Pending
  │
  ▼
Start
  │
  ▼
In Progress
  │
  ▼
Complete
  │
  ▼
Completed
```

The Firestore integration has been verified against the actual Google Cloud Firestore database.

## Testing

The task-management system has been tested for:

* Task creation
* Task listing
* Firestore persistence
* Firestore connection
* Firestore document creation
* Starting pending tasks
* Completing tasks
* Complete task lifecycle
* Prevention of completion without confirmation
* Prevention of starting completed tasks
* Unique task IDs
* Email approval safety
* Task persistence across application restarts

The Firestore integration was tested by:

1. Connecting the Python application to the Firestore database.
2. Creating a task through `create_task`.
3. Reading the task through `list_tasks`.
4. Starting the task through `start_task`.
5. Completing the task through `complete_task`.
6. Confirming the resulting completed state.
7. Deleting the temporary integration test document.

## Current Limitations

* The application is currently primarily designed for local development and testing.
* Gmail is currently the primary external communication integration.
* The application depends on Gemini API availability and quota.
* Google Cloud authentication must be configured for Firestore access.
* The current user interface is primarily provided through the Google ADK development interface.
* The application does not currently provide a dedicated production web interface.
* Advanced workflow recovery and retry mechanisms are not yet implemented.
* Firestore task IDs are generated by checking existing task IDs before creating a new task, which could require improved concurrency handling for high-volume production workloads.

## Future Improvements

Potential future extensions include:

* Google Drive integration
* Web research capabilities
* Additional communication platforms
* Cloud Run deployment
* Dedicated web-based user interface
* Advanced workflow retry and recovery
* Scheduled and recurring workflows
* Additional agent tools
* Multi-agent workflow coordination
* Long-running workflow support
* Persistent agent memory
* Improved workflow observability and monitoring
* Better concurrency handling for task ID generation
* Automated testing with a dedicated test suite

## Security

Sensitive configuration should never be committed to the repository.

The project ignores:

```text
credentials.json
token.json
tasks.json
agent/.env
```

`tasks.json` is retained in `.gitignore` to prevent accidental use of an old local persistence file, although the current application uses Firestore for task persistence.

Developers should verify Git status before committing changes:

```powershell
git status
```

If sensitive information appears as a tracked or staged file, remove it before pushing to the repository.

Never include the following in source code or public repositories:

* Gemini API keys
* OAuth client secrets
* Gmail authentication tokens
* Google Cloud service account private keys
* Other private credentials

## Development

Check repository status:

```powershell
git status
```

Run Python syntax checks:

```powershell
python -m py_compile agent/agent.py
python -m py_compile agent/tools.py
python -m py_compile agent/email_tools.py
python -m py_compile agent/calendar_tools.py
python -m py_compile agent/gmail_auth.py
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Check the README and source changes before committing:

```powershell
git diff
```

Check for whitespace errors:

```powershell
git diff --check
```

## Requirements

The project uses the following primary dependencies:

```text
google-adk==2.8.0
google-genai==2.20.0
google-api-python-client==2.199.0
google-auth-oauthlib==1.4.1
python-dotenv==1.2.3
uvicorn==0.52.4
google-cloud-firestore==2.29.0
```

## Google Cloud Project

Taskmaster uses the following Google Cloud project for its cloud services:

```text
Project ID:
gen-lang-client-0349849444
```

Firestore configuration:

```text
Database:
taskflow-db

Collection:
tasks

Edition:
Standard

Mode:
Firestore Native

Location:
nam5
```

The project uses the Gemini API and Google Cloud Firestore as core parts of the agent architecture.

## Hackathon Requirements

Taskmaster is designed for the **All Things Agentic Hackathon** and incorporates the required Google technologies.

### Gemini

Taskmaster uses Gemini as its agent intelligence layer.

Gemini is responsible for understanding natural-language goals, planning workflows, selecting available tools, and coordinating task execution.

### Google Agent Framework

Taskmaster is built using **Google Agent Development Kit (Google ADK)**.

Google ADK provides the agent framework used to define and run the Taskmaster agent and its tools.

### Google Cloud Infrastructure

Taskmaster uses **Google Cloud Firestore** as its persistent cloud database.

Firestore stores task state outside the local application process and allows task data to persist across application restarts and agent instances.

The core Google technology architecture is:

```text
Gemini
   │
   ▼
Google ADK
   │
   ▼
Taskmaster Agent
   │
   ├── Task Management
   │
   ├── Gmail
   │
   └── Google Calendar
   │
   ▼
Google Cloud Firestore
```

## Repository

GitHub repository:

https://github.com/gideonagbavor8/agentic-taskmaster

## License

This project is currently developed as a hackathon project.
