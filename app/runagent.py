from agent import run_agent


question = input("Ask a question: ")

answer = run_agent(question)

print("\nAI:")

print(answer)