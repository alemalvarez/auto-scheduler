import os
import json
import ast
import glob
import re
from typing import Dict, List
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown

def load_schedule(term: str) -> Dict[str, Dict]:
    """
    Load the schedule for the given term from a JSON file.

    Args:
        term (str): The term for which to load the schedule.

    Returns:
        Dict[str, Dict]: The loaded schedule as a dictionary.

    Throws:
        FileNotFoundError: If the schedule file for the given term is not found.
    """
    try:
        with open(f'../scraper/schedules/{term}.json') as f:
            return json.load(f)
    except FileNotFoundError as e:
        e.add_note(f"No schedule found for term: {term}")
        raise

def get_requirements() -> List[str]:
    """
    Get the list of requirements from the user input.

    Returns:
        List[str]: The list of requirements entered by the user.
    """
    requirements_input = input("Enter the list of requirements separated by commas: ")
    return list(ast.literal_eval(requirements_input))

def get_timetables(requirements: List[str], schedule: Dict[str, Dict]) -> Dict[str, Dict]:
    """
    Get the timetables for the given requirements from the schedule.

    Args:
        requirements (List[str]): The list of requirements.
        schedule (Dict[str, Dict]): The loaded schedule.

    Returns:
        Dict[str, Dict]: A dictionary containing the timetables for the given requirements.
    """
    timetables = {}
    for requirement in requirements:
        major = re.match(r"^.*?(?=\d)", requirement).group(0).upper()
        course = re.sub(r'\s+', '', requirement).upper()
        if major in schedule and course in schedule[major]:
            timetables[course] = schedule[major][course]
        else:
            print(f"No timetable found for requirement: {requirement}")
    return timetables

def query_openai_api(requirements: List[str], timetables: Dict[str, Dict]) -> None:
    """
    Query the OpenAI API to get a non-overlapping combination of timeslots.

    Args:
        requirements (List[str]): The list of requirements.
        timetables (Dict[str, Dict]): A dictionary containing the timetables for the requirements.
    """
    instructions = """
    You are a scheduler. You make college schedules. When you are told a list of classes and their days and hours, you find a combination of the possible timeslots avoiding any overlap. For each class, return one and only one timeslot.
    """

    prompt = f"""
    From this list of classes, pick a non-overlapping combination of timeslots. All classes need to be taken strictly once.

    You will respond with a possible schedule including {len(requirements)} classes, no more, no less.

    The list is: {timetables}
    """

    print("-- Prompt crafted. Querying openAI API...")
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": prompt}
        ]
    )

    console = Console()
    response = completion.choices[0].message.content
    console.print(Markdown(response))

def main() -> None:
    """
    Main function to run the program.
    """
    # Print the possible schedules
    print("Found schedules:")
    for filename in glob.glob('../scraper/schedules/*.json'):
        print(os.path.basename(filename).split('.')[0])

    term = input("Enter the term to target: ")
    schedule = load_schedule(term)
    requirements = get_requirements()
    timetables = get_timetables(requirements, schedule)
    query_openai_api(requirements, timetables)

if __name__ == "__main__":
    main()