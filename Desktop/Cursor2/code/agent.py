import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("Error: OPENAI_API_KEY not found in .env file")
    sys.exit(1)

client = OpenAI(api_key=api_key)

# Available models
MODELS = {
    "1": "gpt-3.5-turbo",
    "2": "gpt-4",
    "3": "gpt-4-turbo-preview"
}

def select_model():
    print("\nAvailable models:")
    for key, model in MODELS.items():
        print(f"{key}. {model}")
    
    while True:
        choice = input("\nSelect model (1-3) [default=1]: ").strip() or "1"
        if choice in MODELS:
            return MODELS[choice]
        print("Invalid choice. Please select 1-3.")

def main():
    print("Welcome to OpenAI Chat Agent!")
    model = select_model()
    print(f"\nUsing model: {model}")
    print("Type 'quit' to exit, 'model' to change model")
    
    while True:
        # Get user input
        user_input = input("\nEnter your message: ").strip()
        
        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'model':
            model = select_model()
            print(f"\nSwitched to model: {model}")
            continue
            
        try:
            # Send request to OpenAI
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": user_input}
                ]
            )
            
            # Print the response
            print("\nResponse:", response.choices[0].message.content)
            
        except Exception as e:
            error_msg = str(e)
            if "insufficient_quota" in error_msg:
                print("\nError: Insufficient quota or billing issues.")
                print("Please check your OpenAI account at: https://platform.openai.com/account/usage")
            elif "invalid_api_key" in error_msg:
                print("\nError: Invalid API key. Please check your .env file.")
            else:
                print(f"\nError: {error_msg}")

if __name__ == "__main__":
    main()
