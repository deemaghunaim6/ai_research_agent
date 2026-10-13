import json
from cal import cal
from llm import ask_llm

question = input("Ask a question: ")

response = ask_llm(question)

message = response.choices[0].message

if message.tool_calls:
    for tool_call in message.tool_calls:

        if tool_call.function.name == "cal":
            print("Tool requested:", tool_call.function.name)

            args = json.loads(tool_call.function.arguments)

            result = cal(args["a"], args["b"])

            print("Tool result:", result)
else:
    print("LLM response:", message.content)