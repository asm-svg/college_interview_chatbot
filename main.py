import os
import random
from lib import (
    create_directory,
    write_questions_to_file,
    read_questions_from_file,
    normalize_response,
    get_questions
)

def get_random_question(questions_dict, asked_questions):
    available_questions = []
    for category, questions in questions_dict.items():
        for question in questions:
            if question not in asked_questions:
                available_questions.append((category, question))
    
    if not available_questions:
        return None, None
    
    category, question = random.choice(available_questions)
    return category, question

def provide_feedback(response, category):
    if category == "Personal":
        feedbacks = [
            "Thanks for sharing that about yourself! ",
            "That's interesting to know about you! ",
            "I appreciate you sharing that personal detail! "
        ]
    elif category == "Academic":
        feedbacks = [
            "That's great to hear about your academic experiences! ",
            "Sounds like you have a good approach to your studies! ",
            "Your academic perspective is valuable! "
        ]
    elif category == "College Specific":
        feedbacks = [
            "Those are thoughtful insights about college! ",
            "You've clearly been thinking about your college journey! ",
            "Great perspective on the college experience! "
        ]
    elif category == "Extra Curricular":
        feedbacks = [
            "It sounds like you have some enriching experiences outside of class! ",
            "Your extracurricular activities seem really meaningful! ",
            "It's great that you're involved in so many activities! "
        ]
    else:
        feedbacks = ["Thanks for sharing! "]
    
    return random.choice(feedbacks)

def print_welcome_message():
    print("\n" + "="*60)
    print(" 🎓 WELCOME TO THE COLLEGE INTERVIEW CHATBOT! 🎓")
    print("="*60)
    print("\nHey there! I'm your virtual college interview coach.")
    print("I'm here to help you prepare for college interviews by asking")
    print("you some questions and having a friendly conversation.")
    print("\nYou can respond with 'yes', 'ya', 'no', or give detailed answers.")
    print("Type 'exit' or 'quit' at any time to end our conversation.")
    print("\nLet's get started! 🚀\n")

def main():
    base_dir = "college_interview_chatbot"
    create_directory(base_dir)
    filepath = os.path.join(base_dir, "questions.txt")
    
    sample_questions = get_questions()
    
    questions_dict = read_questions_from_file(filepath)
    
    if not questions_dict:
        print("Creating new questions file...")
        try:
            write_questions_to_file(filepath, sample_questions)
            questions_dict = read_questions_from_file(filepath)
        except Exception as e:
            print(f"Error creating questions file: {e}")
            
            questions_dict = {}
            for category, question in sample_questions:
                questions_dict.setdefault(category, []).append(question)
    
    print_welcome_message()
    
    asked_questions = []
    conversation_active = True
    
    print("Chatbot: Hey there! Excited about starting college soon? 🎉")
    user_input = input("You: ")
    
    if normalize_response(user_input) == 'exit' or normalize_response(user_input) == 'quit':
        conversation_active = False
    
    while conversation_active:
        category, question = get_random_question(questions_dict, asked_questions)
        
        if category is None:
            print("\nChatbot: Wow, we've gone through all the questions! You're well-prepared for college interviews. Good luck! 🍀")
            break
        
        print(f"\nChatbot: {question}")
        asked_questions.append(question)
        
        user_input = input("You: ")
        normalized_input = normalize_response(user_input)
        
        if normalized_input == 'exit' or normalized_input == 'quit':
            print("\nChatbot: It was great talking with you! Remember to be confident and authentic in your college interviews. Best of luck! 🌟")
            break
        
        if normalized_input == 'yes' or normalized_input == 'no':
            print(f"\nChatbot: {provide_feedback(normalized_input, category)}Would you like to elaborate on that?")
            elaboration = input("You: ")
            if normalize_response(elaboration) == 'exit' or normalize_response(elaboration) == 'quit':
                print("\nChatbot: It was great talking with you! Remember to be confident and authentic in your college interviews. Best of luck! 🌟")
                break
            else:
                print("\nChatbot: Thanks for sharing those details!")
        else:
            print(f"\nChatbot: {provide_feedback(user_input, category)}")
        
        print("\nChatbot: Want to try another question? (yes/no)")
        continue_input = input("You: ")
        normalized_continue = normalize_response(continue_input)
        
        if normalized_continue == 'no' or normalized_continue == 'exit' or normalized_continue == 'quit':
            print("\nChatbot: It was great talking with you! Remember to be confident and authentic in your college interviews. Best of luck! 🌟")
            break
        elif normalized_continue == 'yes':
            print("\nChatbot: Awesome! Let's continue.")
        else:
            print("\nChatbot: I'll take that as a yes! Let's continue.")

if __name__ == "__main__":
    main()
