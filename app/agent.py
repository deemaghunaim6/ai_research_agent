import json
from app.llm import ask_llm
from app.registry import TOOLS
from app.history import save_research , save_markdown_report



MAX_TOOL_CALLS = 5
def run_agent(question):

    conversation = [
        {
            "role": "user",
            "content": question
        }
    ]

    tool_calls_count = 0
    searches = []

    while True:

        response = ask_llm(conversation)

        message = response.choices[0].message

        if message.tool_calls:

            # Save the assistant's tool request
            conversation.append({
                "role": "assistant",
                "content": message.content or "",
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments
                        }
                    }
                    for tool_call in message.tool_calls
                ]
            })

            for tool_call in message.tool_calls:

                tool_calls_count += 1

                print("\n Tool requested:", tool_call.function.name)

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

                print("✅ Tool finished")

                if tool_call.function.name == "search_web":
                    searches.append({
                        "query": args.get("query"),
                        "results": result
                    })

                conversation.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })

        else:

            final_answer = message.content or ""

            final_path = save_research(
                question,
                searches,
                final_answer
            )
            report_path=save_markdown_report(
                question,
                searches,
                final_answer

            )

            print(f"\nResearch saved to: {final_path}")
            print(f"\nMarkdown saved to: {report_path}")

            return final_answer