
chat_messages = []

def create_message(message, role):
  return {
    'role': role,
    'content': message
  }

def ask(message):
  chat_messages.append(
    create_message(message, 'user')
  )
  print(f'\n\n--{message}--\n\n')

def respond(message):
    chat_messages.append(
        create_message(message, 'assistant')
    )
    print(f'\n\n--{message}--\n\n')

