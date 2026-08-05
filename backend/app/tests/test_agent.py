from app.ai import process_message


response = process_message(
    "Update my July 4th, 2026 entry. Change hours worked to 10 and hourly rate to 8."
)

print(response)