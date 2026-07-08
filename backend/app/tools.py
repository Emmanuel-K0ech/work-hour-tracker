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
    }
]