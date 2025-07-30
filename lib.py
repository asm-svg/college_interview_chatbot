import os

def create_directory(path):
    """Create the directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)

def write_questions_to_file(filepath, questions):
    """Write question list to text file."""
    with open(filepath, 'w') as f:
        for category, question in questions:
            f.write(f"{category}::{question}\n")

def read_questions_from_file(filepath):
    """Read questions and return a 2D list by category."""
    questions_2d = {}
    with open(filepath, 'r') as f:
        for line in f:
            if "::" in line:
                category, question = line.strip().split("::", 1)
                questions_2d.setdefault(category, []).append(question)
    return questions_2d

def print_questions_by_category(questions_dict):
    """Nicely print questions grouped by category."""
    for category, questions in questions_dict.items():
        print(f"\n[{category.upper()}]")
        for q in questions:
            print(f"- {q}")

def get_questions():
    """Returns a list of (category, question) tuples."""
    return [
       
        ("Personal", "Tell me about yourself"),
        ("Personal", "What do you do outside of school?"),
        ("Personal", "Have you volunteered before?"),
        ("Personal", "How do you handle stress?"),
        ("Personal", "What are your goals for college?"),
        ("Personal", "How do you work in a team?"),
        ("Personal", "What did you learn from a mistake?"),
        ("Personal", "How do you spend your free time?"),

        ("Academic", "What's your favorite subject in school?"),
        ("Academic", "How do you manage your study time?"),
        ("Academic", "What academic achievement are you proud of?"),
        ("Academic", "How do you learn best?"),
        ("Academic", "What's a challenging assignment you've done?"),
        ("Academic", "How do you stay organized?"),

        ("College Specific", "Why do you want to go to college?"),
        ("College Specific", "What are you looking for in a college?"),
        ("College Specific", "How will college differ from high school?"),
        ("College Specific", "What’s your intended major and why?"),
        ("College Specific", "What concerns you about starting college?"),
        ("College Specific", "How will you manage your time in college?"),
        ("College Specific", "How do you feel about living away from home?"),

        ("Extra Curricular", "What extracurricular activities are you involved in?"),
        ("Extra Curricular", "What role do you play in your school clubs or teams?"),
        ("Extra Curricular", "How have extracurriculars shaped who you are?"),
        ("Extra Curricular", "What activity are you most passionate about and why?"),
        ("Extra Curricular", "Tell me about a time you led a group or team."),
        ("Extra Curricular", "Have you competed in any events? How did it go?"),
        ("Extra Curricular", "How do you balance extracurriculars with academics?"),
        ("Extra Curricular", "What's a lesson you’ve learned from a club or sport?"),
        ("Extra Curricular", "Are you planning to continue these activities in college?"),
        ("Extra Curricular", "How do you handle commitment and teamwork?")
    ]



