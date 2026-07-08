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
import json

client = OpenAI(api_key=OPENAI_API_KEY)


def ask_llm(user_message: str) -> str:
    """
    Run the agent with the given user message and return the response.

    Args:
        user_message (str): The message from the user.

    Returns:
        str: The response from the agent.
    """
    response = client.responses.create(
        model="gpt-4o-mini",
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
        # Implement logic to retrieve entries
        return get_entries()
    elif tool_name == "get_summary":
        # Implement logic to retrieve summary
        return get_summary(
            arguments["start_date"],
            arguments["end_date"]
        )
    elif tool_name == "update_entry":
        # Implement logic to update an entry
        return update_entry(
            arguments["date"],
            arguments["hours_worked"],
            arguments["hourly_rate"]
        )
    elif tool_name == "get_entry":
        # Implement logic to retrieve a specific entry
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
    Process the user message, call the LLM,
    and execute any requested tool.
    """

    response = ask_llm(user_message)

    tool_call = extract_tool_call(response)

    if not tool_call:
        return "I could not determine an action."

    tool_name = tool_call["name"]

    arguments = parse_arguments(
        tool_call["arguments"]
    )

    result = execute_tool(
        tool_name,
        arguments
    )

    return result
