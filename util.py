import os
import sys

def create_directory(path):
    """Create a directory if it doesn't exist."""
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except Exception as e:
        print(f"Error creating directory {path}: {e}")
        sys.exit(1)

def write_questions_to_file(filepath, questions):
    """Write questions to a file in category::question format."""
    try:
        with open(filepath, 'w') as f:
            for category, question in questions:
                f.write(f"{category}::{question}\n")
        return True
    except IOError as e:
        print(f"Error writing to file {filepath}: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error writing to file: {e}")
        return False

def read_questions_from_file(filepath):
    """Read questions from file and organize them by category."""
    questions_2d = {}
    try:
        with open(filepath, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or "::" not in line:
                    print(f"Warning: Skipping malformed line {line_num} in {filepath}")
                    continue
                try:
                    category, question = line.split("::", 1)
                    questions_2d.setdefault(category.strip(), []).append(question.strip())
                except ValueError:
                    print(f"Warning: Skipping malformed line {line_num} in {filepath}")
                    continue
    except FileNotFoundError:
        print(f"Warning: Questions file not found at {filepath}")
        return {}
    except IOError as e:
        print(f"Error reading questions file: {e}")
        return {}
    except Exception as e:
        print(f"Unexpected error reading questions file: {e}")
        return {}
    return questions_2d

def normalize_response(response):
    """Normalize user response to handle variations like 'yes', 'ya', etc."""
    if not isinstance(response, str):
        return ""
    
    response = response.lower().strip()
    if not response:
        return ""
    
    # Check for positive responses
    if response in ['yes', 'ya', 'y', 'yeah', 'yep', 'sure', 'ok', 'yup', 'yessir']:
        return 'yes'
    # Check for negative responses
    elif response in ['no', 'n', 'nope', 'nah', 'no way']:
        return 'no'
    return response

def get_questions():
    """Return the complete list of interview questions organized by category."""
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
        ("College Specific", "What's your intended major and why?"),
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
        ("Extra Curricular", "What's a lesson you've learned from a club or sport?"),
        ("Extra Curricular", "Are you planning to continue these activities in college?"),
        ("Extra Curricular", "How do you handle commitment and teamwork?")
    ]

def get_remaining_questions(questions_dict, asked_questions):
    """Get count of remaining questions per category."""
    remaining = {}
    for category, questions in questions_dict.items():
        remaining[category] = len([q for q in questions if q not in asked_questions])
    return remaining
