import os
import json
import re
from typing import Dict, List
from openai import OpenAI

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
            timetables[course] = schedule[major][course]['shcedules']
        else:
            print(f"No timetable found for requirement: {requirement}")
    return timetables

def query_openai_api(requirements: List[str], timetables: Dict[str, Dict]) -> str:
    """
    Query the OpenAI API to get a non-overlapping combination of timeslots.

    Args:
        requirements (List[str]): The list of requirements.
        timetables (Dict[str, Dict]): A dictionary containing the timetables for the requirements.

    Returns:
        str: The response from the OpenAI API.
    """
    instructions = """
    You are a scheduler. You make college schedules. When you are told a list of classes and their days and hours, you find a combination of the possible timeslots avoiding any overlap. For each class, return one and only one timeslot.
    """

    prompt = f"""
    From this list of classes, pick a non-overlapping combination of timeslots. All classes need to be taken strictly once.

    You will respond with a possible schedule including {len(requirements)} classes, no more, no less.

    The list is: {timetables}
    """

    client = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY'),
        organization='org-R588VtVPiLayZlPfc2F0DyAI'
        )
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content

import streamlit as st

def app():
    st.title("LLM Powered Autoscheduler")

    # Get the list of available schedules
    schedules = [os.path.basename(filename).split('.')[0] for filename in os.listdir('../scraper/schedules') if filename.endswith('.json')]

    # Create a selection list for the available schedules
    term = st.selectbox("Select the term:", schedules)

    if term:
        schedule = load_schedule(term)
        majors = list(schedule.keys())

        # Create a multi-select dropdown for majors
        selected_majors = st.multiselect("Select the majors:", majors)

        if selected_majors:
            requirements = []
            total_units = 0  # Initialize the total units variable

            for major in selected_majors:
                courses = list(schedule[major].keys())
                selected_courses = st.multiselect(f"Select courses for {major}:", courses, max_selections=10)

                # Add the units of the selected courses to the total units
                for course in selected_courses:
                    total_units += int(schedule[major][course]["units"])

                requirements.extend([f"{course}" for course in selected_courses])

            # Display the total units
            st.write(f"Total units selected: {total_units}")

            if requirements:
                if st.button("Submit"):
                    try:
                        timetables = get_timetables(requirements, schedule)
                        response = query_openai_api(requirements, timetables)
                        st.markdown(f"**Suggested Schedule:**\n\n{response}")
                    except Exception as e:
                        st.error(str(e))

if __name__ == "__main__":
    app()