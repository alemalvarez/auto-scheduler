from openai import OpenAI
import os
import json
import ast


from rich.console import Console
from rich.markdown import Markdown

api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError('Your API is not detected in your environment vars. Double check.')

whole_schedule = {}
with open('../scraper/schedules/fall-2024.json') as f:
    whole_schedule = json.load(f)

print(f'-- {len(whole_schedule.keys())} majors loaded!')

#requirements = ['fin 135', 'econ 100A', 'math 45', 'econ 100B', 'pols 100', 'econ 141']

# Get requirements from command line input
requirements_input = input("Enter the list of requirements separated by commas:.. ")

# Convert input string to list
requirements = list(ast.literal_eval(requirements_input))
number_of_requirements = len(requirements)
print(f'-- {number_of_requirements} requirements loaded!')

requirements_timetables = {}

for requirement in requirements:
    major = requirement.split(' ')[0].upper()
    
    requirements_timetables[requirement] = whole_schedule[major][requirement]

instructions = """
You are a scheduler. You make college schedules. When you are told a list of classes and their days and hours, you find a combination of the possible timeslots
avoiding any overlap. 
"""

prompt = f"""
From this list of classes, pick a non-overlapping combination of timeslots. All classes need to be taken strictly once.
You will respond with a possible schedule including {number_of_requirements} classes, no more, no less.
The list is: {requirements_timetables}
"""
print("-- Prompt crafted. Querying openAI API...")
client = OpenAI()

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