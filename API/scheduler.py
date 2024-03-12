import os
import json
import ast
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
        major = requirement.split(' ')[0].upper()
        if major in schedule and requirement in schedule[major]:
            timetables[requirement] = schedule[major][requirement]
        else:
            print(f"No timetable found for requirement: {requirement}")
    return timetables

def query_openai_api(requirements, timetables):
    """
    Query the OpenAI API to get a non-overlapping combination of timeslots.
    """
    instructions = """
    You are a scheduler. You make college schedules. When you are told a list of classes and their days and hours, you find a combination of the possible timeslots
    avoiding any overlap. 
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
    term = input("Enter the term to target (e.g., 'fall-2023', 'spring-2024'): ")
    schedule = load_schedule(term)
    if schedule is not None:
        requirements = get_requirements()
        timetables = get_timetables(requirements, schedule)
        query_openai_api(requirements, timetables)

if __name__ == "__main__":
    main()
