![Banner](assets/banner.png)
# 🐍 LLM powered autoscheduler - CSUS DS Club

*Tested and developed using **Python 3.11.5**!*

The **LLM-based Autoscheduler** is a project developed by the Data Science Club at CSUS, aiming to provide an automated scheduling system for students. 📅 The project comprises three main components:

1. **Scraper** 🕵️‍♂️
2. **LLM API Connection** 🤖
3. **User Interface Application** 💻

## 1. Scraper 🕵️‍♂️
⚠️ **Important: The included chromium engine ONLY runs on ARM MacOS (Apple silicon chips). If your system is different, you can find the appropiate version in [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/) ⚠️** <br>
The scraper is a Python-based module that retrieves class schedule data from the CSUS webpage. It utilizes [Selenium](https://www.selenium.dev/documentation/webdriver/) and [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) to navigate the website, render dynamic content, and parse the HTML structure.

The scraper performs the following tasks:
- Retrieves the rendered HTML content of the class schedule page.
- Parses the HTML structure using BeautifulSoup to extract relevant data.
- Stores the extracted data in a structured format (e.g., JSON, CSV) for further processing.

## 2. LLM API Connection 🤖
The LLM (Large Language Model) API Connection module establishes a connection with a language model API, such as OpenAI's GPT-3 or Anthropic's Claude. This module is responsible for sending prompts to the LLM and receiving the generated responses.

The LLM API Connection module performs the following tasks:
- Authenticates with the LLM API service using provided credentials.
- Formats and sends prompts to the LLM API, including the extracted class schedule data.
- Receives and processes the generated responses from the LLM.
- Applies any necessary post-processing or formatting to the LLM responses.

## 3. User Interface Application 💻
The User Interface Application provides a graphical interface for users to interact with the LLM-based Autoscheduler. It acts as a bridge between the user and the underlying scraper and LLM API Connection components.

The User Interface Application offers the following features:
1. A user-friendly interface for inputting preferences and constraints for scheduling (e.g., desired courses, time preferences, workload limitations).
2. Integration with the scraper module to retrieve the latest class schedule data from the CSUS webpage.
3. Integration with the LLM API Connection module to send prompts and receive generated schedules from the LLM.
4. Display of the generated schedules in a clear and organized manner.
5. Ability to save or export the generated schedules for future reference.

## Getting Started! 🎉
To get started with the LLM-based Autoscheduler project, follow these steps:
1. Clone the repository: `git clone https://github.com/yourusername/llm-based-autoscheduler.git`
2. Install the required dependencies.
3. Configure the necessary API keys and credentials for the LLM API and any other required services.
4. Follow the prompts in the application to input your scheduling preferences and generate schedules using the LLM.

## Contributing 🤝
Contributions to the LLM-based Autoscheduler project are welcome! If you'd like to contribute, please follow these steps:
1. Fork the repository
2. Create a new branch: `git checkout -b my-new-feature`
3. Make your changes and commit them: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request

## License
*This project is licensed under the MIT License.* 📜