from app.ai import process_message


response = process_message(
    "I worked 10 hours on October 4th and my rate is $10"
)

print(response)