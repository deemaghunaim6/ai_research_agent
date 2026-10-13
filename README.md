AI Research Agent

An AI-powered research assistant that searches the web, analyzes information, and generates structured research reports.

Features

Understands research questions.

Searches the web using Tavily.

Uses LLM tool calling to decide when to use available tools.

Analyzes search results and generates structured answers.

Supports multiple tools through a tool registry.

Saves research reports in JSON and Markdown formats.

Provides a REST API using FastAPI.

Includes a simple web interface.

Tech Stack

Python

OpenRouter API

DeepSeek model

Tavily Search API

FastAPI

HTML, CSS, JavaScript

Project Structure

ai-research-agent/ 
|___ app/
|___ frontend/
|___ research_history/ 
|___ .env
|___ .gitignore 
|___ requirements.txt 
|___ README.md 

Setup

Clone the repository.

Create and activate a Python virtual environment.

Install dependencies:
pip install -r requirements.txt

Create a .env file and configure your API keys:
OPENROUTER_API_KEY=your_openrouter_api_key
TAVILY_API_KEY=your_tavily_api_key

Start the API:
python -m uvicorn app.coremain:app --host 127.0.0.1 --port 8001 --reload

Open the API documentation at http://127.0.0.1:8001/docs.

Open frontend/index.html in your browser to use the web interface.

How It Works

The agent sends the research question to an LLM. When the model requests a tool, the application executes the corresponding function and returns its result to the model. The agent continues until it produces a final answer or reaches its tool-call limit.

Security

Never commit API keys or the .env file to version control.

Project Status

Functional prototype — further testing and improvements are ongoing.