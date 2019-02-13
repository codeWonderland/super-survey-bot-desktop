from selenium import webdriver
import time
import platform
import os
import random


class SwagbucksCrawler:
    def __init__(self):
        # determine current os
        system = platform.system()

        # fetch appropriate driver
        self.driver = webdriver.Chrome("drivers/" + system + "/chromedriver")

        # load up the login page
        self.driver.get("https://www.swagbucks.com/p/login")

        # while until the user has logged in
        while "Login | Swagbucks" in self.driver.title:
            time.sleep(5)

        # navigate to the survey page
        self.driver.get("https://www.swagbucks.com/surveys")

        # since we called the survey page via js
        # we wait for the survey page to load
        while "Gold Surveys | Swagbucks" not in self.driver.title:
            time.sleep(5)

    def get_question(self):
        return self.driver.execute_script(open("./js/get_question.js").read())

    def send_answer(self, user_answer):
        # send answer to page
        self.driver.execute_script(open("./js/answer_question.js").read(), user_answer)

        # Emulate decision making time for humans
        time.sleep(random.randint(3, 5))

        # return new question
        return self.get_question()


class SwagbucksTestCrawler():
    def get_question(self):
        return {'ANSWERS': [{'DATA_VALUE': '1', 'TEXT': 'First Person Shooter/Action (e.g. Call of Duty)'}, {'DATA_VALUE': None, 'TEXT': ''}, {'DATA_VALUE': '2', 'TEXT': '3rd Person Shooter/Action (e.g. Gears of War)'}, {'DATA_VALUE': None, 'TEXT': ''}, {'DATA_VALUE': '4', 'TEXT': '3rd Person Adventure (e.g. Super Mario Galaxy)'}, {'DATA_VALUE': None, 'TEXT': ''}, {'DATA_VALUE': '7', 'TEXT': 'Point & Click Adventure (e.g. Monkey Island)'}, {'DATA_VALUE': None, 'TEXT': ''}, {'DATA_VALUE': '8', 'TEXT': 'Life Simulations (e.g. The Sims)'}, {'DATA_VALUE': None, 'TEXT': ''}, {'DATA_VALUE': '10', 'TEXT': 'Music (e.g. Rockband)'}, {'DATA_VALUE': None, 'TEXT': ''}, {'DATA_VALUE': '12', 'TEXT': 'Sports: General  (e.g. FIFA)'}, {'DATA_VALUE': None, 'TEXT': ''}, {'DATA_VALUE': '15', 'TEXT': 'Real Time Strategy (e.g. Command & Conquer)'}, {'DATA_VALUE': None, 'TEXT': ''}, {'DATA_VALUE': '17', 'TEXT': 'Role Playing Game: General (e.g. Final Fantasy)'}, {'DATA_VALUE': None, 'TEXT': ''}, {'DATA_VALUE': '19', 'TEXT': 'Massively Multiplayer Online: Role Playing  (e.g. Warcraft)'}, {'DATA_VALUE': None, 'TEXT': ''}, {'DATA_VALUE': '21', 'TEXT': 'Racing: General (e.g. Need for Speed)'}, {'DATA_VALUE': None, 'TEXT': ''}, {'DATA_VALUE': '23', 'TEXT': 'Flight Simulation (e.g. MS Flight Simulator)'}, {'DATA_VALUE': None, 'TEXT': ''}, {'DATA_VALUE': '25', 'TEXT': 'Fighting (e.g. Street Fighter)'}, {'DATA_VALUE': None, 'TEXT': ''}, {'DATA_VALUE': '28', 'TEXT': 'Puzzle (e.g. Professor Layton)'}, {'DATA_VALUE': None, 'TEXT': ''}, {'DATA_VALUE': '29', 'TEXT': 'Party Games (e.g. Wii Sports)'}, {'DATA_VALUE': None, 'TEXT': ''}, {'DATA_VALUE': '32', 'TEXT': 'Casual (e.g. Facebook games)'}, {'DATA_VALUE': None, 'TEXT': ''}, {'DATA_VALUE': '33', 'TEXT': 'Other'}, {'DATA_VALUE': None, 'TEXT': ''}, {'DATA_VALUE': '34', 'TEXT': "I don't play video/computer games"}], 'QUESTION': 'What kind(s) of video/computer games do you play?', 'TYPE': 'CHECKBOX'}

    def send_answer(self, user_answer):
        print(user_answer)
        return self.get_question()

    @staticmethod
    def answer_question_cli(question_data):
        print(question_data["QUESTION"])

        for answer_option in question_data["ANSWERS"]:
            if answer_option["DATA_VALUE"] is not None:
                print(answer_option["DATA_VALUE"] + ") " + answer_option["TEXT"])

        user_answer = None

        while user_answer is None:
            user_answer = input("Which answer(s) do you choose (enter the number(s) as comma seperated list): ")

            for user_choice in user_answer.split(','):
                if user_choice not in map(lambda choice: choice["DATA_VALUE"], question_data["ANSWERS"]):
                    user_answer = None

        return user_answer
