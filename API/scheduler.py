import os
import json
import ast
import glob
import re

from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown

def load_schedule(term):
    """
    Load the schedule for the given term from a JSON file.
    """
    try:
        with open(f'../scraper/schedules/{term}.json') as f:
            return json.load(f)
    except FileNotFoundError as e:
        e.add_note(f"No schedule found for term: {term}")
        raise

def get_requirements():
    """
    Get the list of requirements from the user input.
    """
    requirements_input = input("Enter the list of requirements separated by commas: ")
    return list(ast.literal_eval(requirements_input))

def get_timetables(requirements, schedule):
    """
    Get the timetables for the given requirements from the schedule.
    """
    timetables = {}
    for requirement in requirements:
        major = re.match(r"^[^\d\s]+", requirement).group(0).upper()
        course = re.sub(r'\s+', '', requirement).upper()

        if major in schedule and course in schedule[major]:
            timetables[course] = schedule[major][course]
        else:
            print(f"No timetable found for requirement: {requirement}")
    return timetables

def query_openai_api(requirements, timetables):
    """
    Query the OpenAI API to get a non-overlapping combination of timeslots.
    """

    instructions = """
    You are a scheduler. You make college schedules. When you are told a list of classes and their days and hours, you find a combination of the possible timeslots
    avoiding any overlap. For each class, return one and only one timeslot.
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

def main():
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
