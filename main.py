import os
import random
import sys
from util import (
    create_directory,
    write_questions_to_file,
    read_questions_from_file,
    normalize_response,
    get_questions,
    get_remaining_questions
)

def get_random_question(questions_dict, asked_questions):
    """Get a random question that hasn't been asked yet."""
    available_questions = []
    for category, questions in questions_dict.items():
        for question in questions:
            if question not in asked_questions:
                available_questions.append((category, question))
    
    if not available_questions:
        return None, None
    
    return random.choice(available_questions)

def provide_feedback(response, category):
    """Provide contextual feedback based on the question category."""
    feedbacks = {
        "Personal": [
            "Thanks for sharing that about yourself! ",
            "That's interesting to know about you! ",
            "I appreciate you sharing that personal detail! "
        ],
        "Academic": [
            "That's great to hear about your academic experiences! ",
            "Sounds like you have a good approach to your studies! ",
            "Your academic perspective is valuable! "
        ],
        "College Specific": [
            "Those are thoughtful insights about college! ",
            "You've clearly been thinking about your college journey! ",
            "Great perspective on the college experience! "
        ],
        "Extra Curricular": [
            "It sounds like you have some enriching experiences outside of class! ",
            "Your extracurricular activities seem really meaningful! ",
            "It's great that you're involved in so many activities! "
        ]
    }
    
    default_feedbacks = ["Thanks for sharing! "]
    category_feedbacks = feedbacks.get(category, default_feedbacks)
    return random.choice(category_feedbacks)

def print_farewell_message():
    """Print the farewell message."""
    print("\nChatbot: It was great talking with you!")
    print("Remember to be confident and authentic in your")
    print("college interviews. Best of luck! 🌟")

def print_welcome_message():
    """Print an attractive welcome message formatted for readability."""
    print("\n" + "="*60)
    print(" 🎓 WELCOME TO THE COLLEGE INTERVIEW CHATBOT! 🎓")
    print("="*60)
    print("\nHey there! I'm your virtual college interview coach.")
    print("I'm here to help you prepare for college interviews by asking")
    print("you some questions and having a friendly conversation.")
    print("\nYou can respond with 'yes', 'ya', 'no', or give detailed answers.")
    print("Special commands:")
    print("- 'skip': Skip the current question")
    print("- 'categories': Show remaining questions per category")
    print("- 'help': Show this help message")
    print("- 'exit' or 'quit': End our conversation")
    print("\nLet's get started! 🚀\n")

def show_help():
    """Show available commands."""
    print("\nAvailable commands:")
    print("- skip: Skip the current question")
    print("- categories: Show remaining questions per category")
    print("- help: Show this help message")
    print("- exit or quit: End the conversation")

def show_remaining_questions(questions_dict, asked_questions):
    """Show remaining questions per category."""
    remaining = get_remaining_questions(questions_dict, asked_questions)
    print("\nRemaining questions by category:")
    for category, count in remaining.items():
        print(f"- {category}: {count} question(s)")

def main():
    try:
        # Set up the directory structure for the chatbot
        base_dir = "college_interview_chatbot"
        create_directory(base_dir)
        filepath = os.path.join(base_dir, "questions.txt")
        
        # Get the complete list of sample questions
        sample_questions = get_questions()
        
        # Try to read existing questions from file
        questions_dict = read_questions_from_file(filepath)
        
        # If no questions were loaded, create a new questions file
        if not questions_dict:
            print("Creating new questions file...")
            if not write_questions_to_file(filepath, sample_questions):
                print("Warning: Could not create questions file. Using default questions.")
                # Fall back to using the sample questions directly
                questions_dict = {}
                for category, question in sample_questions:
                    questions_dict.setdefault(category, []).append(question)
            else:
                questions_dict = read_questions_from_file(filepath)
                if not questions_dict:
                    print("Warning: Could not read questions file. Using default questions.")
                    questions_dict = {}
                    for category, question in sample_questions:
                        questions_dict.setdefault(category, []).append(question)
        
        # Display welcome message to the user
        print_welcome_message()
        
        # Initialize conversation tracking variables
        asked_questions = []
        conversation_active = True
        
        # Start the conversation with a greeting
        print("Chatbot: Hey there! Excited about starting college soon? 🎉")
        user_input = input("You: ").strip()
        
        # Check if user wants to exit immediately
        if normalize_response(user_input) in ['exit', 'quit']:
            conversation_active = False
        
        # Main conversation loop
        while conversation_active:
            try:
                # Get a random question that hasn't been asked yet
                category, question = get_random_question(questions_dict, asked_questions)
                
                # If all questions have been asked, end the conversation
                if category is None:
                    print("\nChatbot: Wow, we've gone through all the questions!")
                    print("You're well-prepared for college interviews. Good luck! 🍀")
                    break
                
                # Ask the selected question
                print(f"\nChatbot: {question}")
                asked_questions.append(question)
                
                # Get user's response to the question
                user_input = input("You: ").strip()
                normalized_input = normalize_response(user_input)
                
                # Check for special commands
                if normalized_input == 'exit' or normalized_input == 'quit':
                    print_farewell_message()
                    break
                elif normalized_input == 'skip':
                    print("Chatbot: Skipping this question. Let's move on.")
                    continue
                elif normalized_input == 'categories':
                    show_remaining_questions(questions_dict, asked_questions)
                    # Ask the same question again
                    print(f"\nChatbot: {question}")
                    user_input = input("You: ").strip()
                    normalized_input = normalize_response(user_input)
                elif normalized_input == 'help':
                    show_help()
                    # Ask the same question again
                    print(f"\nChatbot: {question}")
                    user_input = input("You: ").strip()
                    normalized_input = normalize_response(user_input)
                
                # Check if user wants to exit after command processing
                if normalized_input == 'exit' or normalized_input == 'quit':
                    print_farewell_message()
                    break
                
                # Provide feedback based on the type of response
                if normalized_input in ['yes', 'no']:
                    # For yes/no responses, ask for elaboration
                    print(f"\nChatbot: {provide_feedback(normalized_input, category)}")
                    print("Would you like to elaborate on that?")
                    elaboration = input("You: ").strip()
                    normalized_elaboration = normalize_response(elaboration)
                    
                    if normalized_elaboration in ['exit', 'quit']:
                        print_farewell_message()
                        break
                    elif normalized_elaboration == 'skip':
                        print("Chatbot: Okay, skipping elaboration.")
                    elif normalized_elaboration == 'categories':
                        show_remaining_questions(questions_dict, asked_questions)
                        # Ask for elaboration again
                        print("Would you like to elaborate on that?")
                        elaboration = input("You: ").strip()
                        normalized_elaboration = normalize_response(elaboration)
                    elif normalized_elaboration == 'help':
                        show_help()
                        # Ask for elaboration again
                        print("Would you like to elaborate on that?")
                        elaboration = input("You: ").strip()
                        normalized_elaboration = normalize_response(elaboration)
                    else:
                        print("\nChatbot: Thanks for sharing those details!")
                else:
                    # For detailed responses, provide contextual feedback
                    print(f"\nChatbot: {provide_feedback(user_input, category)}")
                
                # Ask if user wants to continue with another question
                print("\nChatbot: Want to try another question? (yes/no)")
                continue_input = input("You: ").strip()
                normalized_continue = normalize_response(continue_input)
                
                # Handle user's decision to continue or exit
                if normalized_continue in ['no', 'exit', 'quit']:
                    print_farewell_message()
                    break
                elif normalized_continue == 'yes':
                    print("\nChatbot: Awesome! Let's continue.")
                else:
                    print("\nChatbot: I'll take that as a yes! Let's continue.")
            
            except KeyboardInterrupt:
                print("\n\nChatbot: It looks like you interrupted the conversation.")
                print("No worries! Take your time and come back when you're ready.")
                print("Type 'exit' to quit or press Enter to continue.")
                choice = input("You: ").strip().lower()
                if choice == 'exit':
                    print_farewell_message()
                    conversation_active = False
            except Exception as e:
                print(f"\nChatbot: Oops, something went wrong! Let's try again. ({type(e).__name__}: {e})")
                # Remove the last question from asked_questions so it can be asked again
                if asked_questions:
                    asked_questions.pop()
                continue

    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
