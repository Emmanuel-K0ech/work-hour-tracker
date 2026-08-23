from openai import OpenAI
from app.config import OPENAI_API_KEY
from app.services.entry import (
    save_entry, 
    get_entries, 
    get_summary, 
    update_entry, 
    get_entry
)
from app.tools import tools
from datetime import date
import json

client = OpenAI(api_key=OPENAI_API_KEY)


def ask_llm(user_message: str):
    today = date.today().isoformat()

    instructions = f"""
You are the AI assistant for a Work Hour Tracker application.

Today's date is {today}.

Use today's date when interpreting relative dates such as:
- today
- yesterday
- this week
- this month
- last week
- last month

When the user says "today", use {today}.
When the user says "this month", use the first day of the current month through {today}.

Do not guess dates.
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        instructions=instructions,
        input=user_message,
        tools=tools
    )

    return response

def extract_tool_call(response) -> dict:
    """
    Extract the tool call from the agent's response.

    Args:
        response: The response from the agent.

    Returns:
        dict: The tool call if available, otherwise None.
    """
    if response.output:
        tool_call = response.output[0]

        if tool_call.type == "function_call":
            return {
                "name": tool_call.name,
                "arguments": tool_call.arguments
            }
    return None

# Tool executor after response is received
def execute_tool(tool_name, arguments):
    """
    Execute the specified tool with the given arguments.

    Args:
        tool_name (str): The name of the tool to execute.
        arguments (dict): The arguments for the tool.

    Returns:
        dict: The result of the tool execution.
    """
    if tool_name == "save_entry":
        # Here you would implement the logic to save the entry
        # For example, you might call a function that saves to a database
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
        return get_entry(arguments["date"])
    else:
        raise ValueError(f"Unknown tool: {tool_name}")

# parsing string to json  
def parse_arguments(arguments_str: str) -> dict:
    """
    Parse the arguments string into a dictionary.

    Args:
        arguments_str (str): The arguments string in JSON format.

    Returns:
        dict: The parsed arguments as a dictionary.
    """
    try:
        return json.loads(arguments_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format for arguments: {e}")

# Ocherstrate the whole process of asking the LLM, extracting the tool call, and executing the tool
def process_message(user_message: str):
    """
    Process the user message, execute any requested tool,
    and return a natural language response.
    """

    response = ask_llm(user_message)

    tool_call = extract_tool_call(response)

    # No tool required — return normal conversational response
    if not tool_call:
        return {
            "success": True,
            "message": response.output_text
        }

    tool_name = tool_call["name"]

    arguments = parse_arguments(
        tool_call["arguments"]
    )

    result = execute_tool(
        tool_name,
        arguments
    )

    # Send the tool result back to the LLM
    final_response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "user",
                "content": user_message
            },
            {
                "role": "assistant",
                "content": f"Tool used: {tool_name}"
            },
            {
                "role": "user",
                "content": f"Tool result: {json.dumps(result)}"
            }
        ]
    )

    return {
        "success": True,
        "message": final_response.output_text
    }
