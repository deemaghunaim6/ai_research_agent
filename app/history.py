import json
from pathlib import Path
from datetime import datetime


def format_tool_result(result):
    if isinstance(result, (dict, list)):
        return json.dumps(
            result,
            ensure_ascii=False,
            indent=2
        )

    return str(result)


history_dir = Path(__file__).parent.parent / "research_history"


def save_research(question, searches, final_answer):

    history_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    research_data = {
        "question": question,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "searches": searches,
        "final_answer": final_answer
    }

    file_path = history_dir / f"research_{timestamp}.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(
            research_data,
            file,
            ensure_ascii=False,
            indent=2
        )

    return file_path


def save_markdown_report(question, searches, final_answer):

    history_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    report_path = history_dir / f"report_{timestamp}.md"

    report = f"""# AI Research Report

## Research Question

{question}

## Summary

{final_answer}

## Search History

"""

    for index, search in enumerate(searches, start=1):

        report += f"### Search {index}\n\n"
        report += f"Query: {search.get('query', '')}\n\n"

        results = search.get("results", [])

        if isinstance(results, list):

            for result in results:

                if isinstance(result, dict):

                    title = result.get("title", "Untitled")
                    url = result.get("url", "")
                    content = result.get("content", "")

                    report += f"- {title}\n"
                    report += f"  - URL: {url}\n"
                    report += f"  - Details: {content}\n\n"

        report += "\n"

    with open(report_path, "w", encoding="utf-8") as file:
        file.write(report)

    return report_path