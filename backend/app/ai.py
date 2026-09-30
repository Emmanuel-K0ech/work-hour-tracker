from openai import OpenAI
from datetime import date
import json

from app.config import OPENAI_API_KEY
from app.tools import tools
from app.services.entry import (
    save_entry,
    get_entries,
    get_summary,
    update_entry,
    get_entry,
)

client = OpenAI(api_key=OPENAI_API_KEY)


def get_instructions():
    today = date.today().isoformat()

    return f"""
You are the AI assistant for a Work Hour Tracker application.

Today's date is {today}.

Your job is to help users manage and understand their recorded work hours
using the application's existing functions.

TOOL USE:
- For requests to save a work entry, use save_entry.
- For requests to retrieve all entries, use get_entries.
- For a request about one specific date, use get_entry.
- For requests to update an existing entry, use update_entry.
- For totals or summaries over a date range, use get_summary.
- Use the appropriate function whenever a request requires work-hour
  information from the database.
- Do not answer database questions from memory or assumptions.
- Do not invent entries, hours, earnings, or monthly totals.
- Base factual answers about work records on the returned tool results.

DISTINGUISH THE REQUEST:
- "How many hours did I work?" asks for a total.
- "How much did I earn?" asks for earnings.
- "Show me my entries" asks for actual recorded entries, not just totals.
- "Break down my hours by month" asks for a monthly breakdown.
  Use get_summary for each requested month, with the correct dates.
- If the available results do not support an answer, explain what
  information could not be retrieved. Never make up missing values.

DATE HANDLING:
- Today is {today}.
- "Today" means {today}.
- "Yesterday" means the previous calendar day.
- "This month" means the first day of the current month through {today}.
- "Last month" means the entire previous calendar month.
- Interpret explicit months and years using their actual calendar dates.
- "January to September 2026" means 2026-01-01 through 2026-09-30.
- Use YYYY-MM-DD for dates passed to tools.
- Do not guess dates.

For ordinary greetings or conversational messages that do not require
work-hour data, respond naturally.
"""


def ask_llm(user_message: str, input_items=None):
    if input_items is None:
        input_items = [{"role": "user", "content": user_message}]

    return client.responses.create(
        model="gpt-4o-mini",
        instructions=get_instructions(),
        input=input_items,
        tools=tools
    )

def parse_arguments(arguments_str: str) -> dict:
    """Convert tool arguments from JSON text into a Python dictionary."""
    try:
        return json.loads(arguments_str)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON format for arguments: {error}"
        )


def execute_tool(tool_name: str, arguments: dict):
    """Execute one of the Work Hour Tracker's existing tools."""

    if tool_name == "save_entry":
        return save_entry(
            arguments["date"],
            arguments["hours_worked"],
            arguments["hourly_rate"]
        )

    elif tool_name == "get_entries":
        return get_entries()

    elif tool_name == "get_summary":
        return get_summary(
            arguments["start_date"],
            arguments["end_date"]
        )

    elif tool_name == "update_entry":
        return update_entry(
            arguments["date"],
            arguments["hours_worked"],
            arguments["hourly_rate"]
        )

    elif tool_name == "get_entry":
        return get_entry(
            arguments["date"]
        )

    else:
        raise ValueError(f"Unknown tool: {tool_name}")


def process_message(user_message: str):
    """
    Process a user message and execute existing tools until the
    assistant can provide a final response.
    """

    input_items = [{"role": "user", "content": user_message}]

    # Prevent an unexpected tool-call loop from running indefinitely.
    for _ in range(5):
        response = ask_llm(user_message, input_items)

        # Check every output item, not only response.output[0].
        tool_calls = [
            item for item in response.output
            if item.type == "function_call"
        ]

        # No more tool calls: return the assistant's final answer.
        if not tool_calls:
            return {
                "success": True,
                "message": response.output_text
            }

        # Preserve the model's response, including its function calls.
        input_items.extend(response.output)

        for tool_call in tool_calls:
            try:
                arguments = parse_arguments(tool_call.arguments)

                result = execute_tool(
                    tool_call.name,
                    arguments
                )

                tool_output = {
                    "success": True,
                    "result": result
                }

            except Exception as error:
                # Return the failure to the model rather than allowing
                # it to assume that the operation succeeded.
                tool_output = {
                    "success": False,
                    "error": str(error)
                }

            # Use the Responses API's proper function-call output format.
            input_items.append({
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": json.dumps(tool_output, default=str)
            })

    return {
        "success": False,
        "message": (
            "I couldn't complete that request because the assistant "
            "exceeded its tool-call limit. Please try again."
        )
    }
