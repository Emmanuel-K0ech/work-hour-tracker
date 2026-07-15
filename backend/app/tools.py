tools = [
    {
        "type": "function",
        "name": "save_entry",
        "description": "Save a work entry containing the date, hours worked, and hourly rate.",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "Date of work entry (YYYY-MM-DD)"
                },
                "hours_worked": {
                    "type": "number",
                    "description": "Number of hours worked"
                },
                "hourly_rate": {
                    "type": "number",
                    "description": "Hourly pay rate"
                }
            },
            "required": [
                "date",
                "hours_worked",
                "hourly_rate"
            ]
        }
    },
    {
        "type": "function",
        "name": "get_entries",
        "description": "Retrieve all work entries from the database.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "type": "function",
        "name": "get_entry",
        "description": "Retrieve a specific work entry by its date.",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "Date of work entry (YYYY-MM-DD)"
                }
            },
            "required": ["date"]
        }
    },
    {
        "type": "function",
        "name": "update_entry",
        "description": "Update an existing work entry by its date with new hours worked and hourly rate.",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "Date of work entry (YYYY-MM-DD)"
                },
                "hours_worked": {
                    "type": "number",
                    "description": "Number of hours worked"
                },
                "hourly_rate": {
                    "type": "number",
                    "description": "Hourly pay rate"
                }
            },
            "required": ["date", "hours_worked", "hourly_rate"]
        }
    },
    {
        "type": "function",
        "name": "get_summary",
        "description": "Retrieve a summary of work entries within a specified date range.",
        "parameters": {
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "Start date of the summary range (YYYY-MM-DD)"
                },
                "end_date": {
                    "type": "string",
                    "description": "End date of the summary range (YYYY-MM-DD)"
                }
            },
            "required": ["start_date", "end_date"]
        }
    }
]