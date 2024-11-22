import pyttsx3
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Speak engine setup
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Select the second voice (usually female)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Define example data for intent classification
intent_data = [
    ("hello", "greeting"),
    ("hi", "greeting"),
    ("how are you", "greeting"),
    ("what is your name", "question"),
    ("how old are you", "question"),
    ("tell me a joke", "joke"),
    ("another joke", "joke"),
    ("joke please", "joke"),
    ("bye", "farewell"),
    ("goodbye", "farewell"),
    ("tell me a riddle", "riddle"),
    ("another riddle", "riddle"),
]

# Separate inputs (X) and labels (y)
X, y = zip(*intent_data)

# Create a pipeline model with CountVectorizer and Naive Bayes classifier
model = make_pipeline(CountVectorizer(), MultinomialNB())
model.fit(X, y)  # Train the model with our example data

# Response dictionary based on detected intent
responses = {
    "greeting": "Hello! I'm here to help you. What would you like to know?",
    "question": "That's a great question! Can you tell me a bit more?",
    "farewell": "Goodbye! Hope to chat with you again soon!",
    "riddle": "I have a riddle for you, try to solve it!"
}

# Store told jokes to avoid repeats
told_jokes = set()

# Function to fetch a joke from the icanhazdadjoke API
def fetch_joke():
    headers = {
        "Accept": "application/json",
        "User-Agent": "Python Joke Bot for Kids"
    }
    response = requests.get("https://icanhazdadjoke.com/", headers=headers)
    
    # Check if the response is successful
    if response.status_code == 200:
        joke_data = response.json()
        joke = joke_data['joke']
        
        # Check if the joke has already been told
        if joke not in told_jokes:
            told_jokes.add(joke)  # Add joke to told list
            return joke
        else:
            # If joke has been told, fetch a new one
            return fetch_joke()
    else:
        return "Sorry, I couldn't fetch a joke at the moment."

# Function to fetch a riddle from JokeAPI
def fetch_riddle():
    JOKE_API_URL = "https://v2.jokeapi.dev/joke/Miscellaneous?type=twopart&lang=en"
    try:
        response = requests.get(JOKE_API_URL)
        response.raise_for_status()  # Ensure the request was successful
        data = response.json()
        
        if data["type"] == "twopart":
            question = data["setup"]
            answer = data["delivery"]
            return question, answer
        else:
            return None, None  # Handle cases where joke format is not two-part
    except requests.exceptions.RequestException as e:
        print(f"Error fetching riddle: {e}")
        return None, None

# Function to classify intent and generate a response
def teacher_response(user_input):
    # Predict intent
    intent = model.predict([user_input])[0]
    
    if intent == "joke":
        # If intent is to tell a joke, fetch and return a joke
        return fetch_joke()
    elif intent == "riddle":
        # If intent is to tell a riddle, fetch and return a riddle
        riddle, answer = fetch_riddle()
        if riddle and answer:
            return riddle, answer
        else:
            return "Sorry, I couldn't fetch a riddle at the moment."
    else:
        # Otherwise, respond based on the intent from the response dictionary
        return responses.get(intent, "I'm not sure how to respond to that.")

# Simple math operations functions
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y != 0:
        return x / y
    else:
        return "Cannot divide by zero!"

# Alphabet tuple
alphabet = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z")

def speak_alphabets():
    for letter in alphabet:
        print(f"\033[1m{letter.upper()}\033[0m")  # Print in bold (simulated in terminal)
        speak(letter)  # Speak each letter

def speak_numbers(limit):
    # Loop through the first 'limit' numbers (up to 500)
    for num in range(limit):
        print(f"\033[1m{num}\033[0m")  # Print in bold (simulated in terminal)
        speak(str(num))  # Speak the number

# Main program loop
def main():
    print("Welcome to the Teacher Bot with Alphabets, Numbers, Math Operations, Jokes, and Riddles!")
    speak("Welcome to the Teacher Bot with Alphabets, Numbers, Math Operations, Jokes, and Riddles!")
    
    while True:
        user_input = input("What would you like me to do? Type 'math', 'alphabets', 'numbers', 'joke', 'riddle', 'exit', or ask a question: ").strip().lower()
        
        # Speak the user's input
        speak(f"You selected: {user_input}")
        
        if user_input == "math":
            # Simple math operations menu
            print("\nSelect operation:")
            print("1. Add")
            print("2. Subtract")
            print("3. Multiply")
            print("4. Divide")
            print("5. Exit")
            
            choice = input("Enter choice (1/2/3/4/5): ").strip()

            # Check if the user wants to exit from math operations
            if choice == '5':
                print("Goodbye!")
                speak("Goodbye!")
                break

            if choice in ('1', '2', '3', '4'):
                try:
                    num1 = float(input("Enter the first number: "))
                    num2 = float(input("Enter the second number: "))
                except ValueError:
                    print("Invalid input! Please enter valid numbers.")
                    continue

                # Perform the chosen operation
                if choice == '1':
                    result = add(num1, num2)
                    print(f"The result of {num1} + {num2} is: {result}")
                    speak(f"The result of {num1} + {num2} is {result}")
                elif choice == '2':
                    result = subtract(num1, num2)
                    print(f"The result of {num1} - {num2} is: {result}")
                    speak(f"The result of {num1} minus {num2} is {result}")
                elif choice == '3':
                    result = multiply(num1, num2)
                    print(f"The result of {num1} * {num2} is: {result}")
                    speak(f"The result of {num1} multiplied by {num2} is {result}")
                elif choice == '4':
                    result = divide(num1, num2)
                    print(f"The result of {num1} / {num2} is: {result}")
                    speak(f"The result of {num1} divided by {num2} is {result}")
            else:
                print("Invalid choice! Please enter a number between 1 and 5.")
                speak("Invalid choice. Please enter a number between 1 and 5.")
        
        elif user_input == "alphabets":
            speak_alphabets()
        
        elif user_input == "numbers":
            # Ask for confirmation before speaking numbers 0-500
            confirm = input("This will speak numbers from 0 to 500. Are you sure? (yes/no): ").strip().lower()
            if confirm == 'yes':
                speak_numbers(501)  # Speak all numbers from 0 to 500
            elif confirm == 'no':
                # Ask how many numbers they want to hear
                while True:
                    try:
                        count = int(input("How many numbers would you like to hear? (1-500): ").strip())
                        if 1 <= count <= 500:
                            speak_numbers(count)  # Speak the given number of numbers
                            break
                        else:
                            print("Please enter a number between 1 and 500.")
                            speak("You want me tell upto")
                            speak(count)
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")
            else:
                print("Operation cancelled.")
        
        elif user_input == "joke":
            response = teacher_response(user_input)
            print(f"Teacher: {response}")
            speak(response)
        
        elif user_input == "riddle":
            riddle, answer = teacher_response(user_input)
            if riddle:
                print(f"Teacher: Here's a riddle for you: {riddle}")
                speak(f"Here's a riddle for you: {riddle}")
                input("Press Enter when you're ready for the answer...")
                print(f"Teacher: The answer is: {answer}")
                speak(f"The answer is: {answer}")
            else:
                print("Sorry, I couldn't fetch a riddle.")
                speak("Sorry, I couldn't fetch a riddle.")
        
        elif user_input == "exit":
            print("Goodbye!")
            speak("Goodbye!")
            break
        else:
            response = teacher_response(user_input)
            print(f"Teacher: {response}")
            speak(response)

if __name__ == "__main__":
    main()