import json
from app.llm import ask_llm
from app.registry import TOOLS
from app.cal import calapp

question = input("Ask a question: ")

conversation = [
    {
        "role": "user",
        "content": question
    }
]

while True:

    response = ask_llm(conversation)

    message = response.choices[0].message

    tool_called = False

    if message.tool_calls:

        tool_called = True

        # نضيف رد الـassistant الذي يحتوي على tool call
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

            print("\nTool requested:", tool_call.function.name)

            args = json.loads(tool_call.function.arguments)

            tool = TOOLS.get(tool_call.function.name)

            if tool is None:
                result = f"Unknown tool: {tool_call.function.name}"

            else:
                result = tool(**args)

            print("\nTool result:")
            print(result)

            # إرسال نتيجة الـtool للـLLM
            conversation.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })

    else:

        print("\nAI:")
        print(message.content)

        break