from openai import OpenAI
from config import OPENAI_API_KEY
from tools import tools

client = OpenAI(api_key=OPENAI_API_KEY)


def run_agent(user_message: str) -> str:
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
        from services.entry_service import save_entry
        return save_entry(
            arguments["date"],
            arguments["hours_worked"],
            arguments["hourly_rate"]
        )