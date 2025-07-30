import os
from lib import (
    create_directory,
    write_questions_to_file,
    read_questions_from_file,
    print_questions_by_category,
    get_questions
)

def main():
    base_dir = "college_interview_chatbot"
    create_directory(base_dir)
    filepath = os.path.join(base_dir, "questions.txt")

    # Load all questions from lib
    sample_questions = get_questions()


    if not os.path.exists(filepath):
        write_questions_to_file(filepath, sample_questions)


    questions_dict = read_questions_from_file(filepath)
  
    print("Welcome to the College Interview Chatbot!\n")
    print_questions_by_category(questions_dict)

if __name__ == "__main__":
    main()

