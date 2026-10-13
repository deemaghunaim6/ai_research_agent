import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

MODEL = "deepseek/deepseek-v4-flash-0731"

tools = [
    {
        "type": "function",
        "function": {
            "name": "cal",
            "description": "Add two numbers together",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "The first number",
                    },
                    "b": {
                        "type": "number",
                        "description": "The second number",
                    },
                },
                "required": ["a", "b"],
                "additionalProperties": False,
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for current information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query",
                    },
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
    }
]

instructions = """
[10/9/2026 5:21 AM] Deema Ghunaim: tool_calls_count += 1

print("\n🔧 Tool requested:", tool_call.function.name)

if tool_calls_count > MAX_TOOL_CALLS:
    return "The agent reached the maximum number of tool calls."

args = json.loads(tool_call.function.arguments)

if tool_call.function.name == "search_web":
    print("🔎 Search query:", args.get("query"))

tool = TOOLS.get(tool_call.function.name)

if tool is None:
    result = f"Unknown tool: {tool_call.function.name}"
else:
    result = tool(**args)

print("Tool finished")

conversation.append({
    "role": "tool",
    "tool_call_id": tool_call.id,
    "content": str(result)
})
[10/9/2026 5:25 AM] Deema Ghunaim: You are an AI Research Agent.

Your task is to research the user's question using available tools.

Rules:
1. Understand the user's research question.
2. Use search_web when web research is needed.
3. Choose specific search queries that help answer different parts of the question.
4. Never repeat the same search query.
5. Use at most 2 searches for one research task.
6. After the searches, analyze the available results and provide the final answer.
7. If information is missing, clearly explain what could not be verified.
8. Do not invent facts, course details, or sources.
9. Structure comparisons clearly when the user asks to compare options.
10. Always provide a final answer instead of continuing to search indefinitely.
"""


def ask_llm(conversation):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": instructions
            },
            *conversation
        ],
        tools=tools,
    )

    return response