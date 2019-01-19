from selenium import webdriver
import time


class SwagbucksCrawler:
    def __init__(self, is_test = False):
        if not is_test:
            # Set Test Status
            self.is_test = False

            # create instance of driver
            self.driver = webdriver.Chrome()

            # load up the login page
            self.driver.get("https://www.swagbucks.com/p/login")

            # while until the user has logged in
            while "Login | Swagbucks" in self.driver.title:
                time.sleep(5)

            # navigate to the survey page
            self.driver.execute_script(open("./js/open_survey.js").read())

            # since we called the survey page via js
            # we wait for the survey page to load
            while "Gold Surveys | Swagbucks" not in self.driver.title:
                time.sleep(5)

        else:
            # Set Test Status
            self.is_test = True

    def get_question(self):
        if not self.is_test:
            # obtain question from page
            return self.driver.execute_script(open("./js/get_question.js").read())

        else:
            return self.get_test_question()

    @staticmethod
    def get_test_question():
        return {'answers': [{'data-value': '1', 'text': 'First Person Shooter/Action (e.g. Call of Duty)'}, {'data-value': None, 'text': ''}, {'data-value': '2', 'text': '3rd Person Shooter/Action (e.g. Gears of War)'}, {'data-value': None, 'text': ''}, {'data-value': '4', 'text': '3rd Person Adventure (e.g. Super Mario Galaxy)'}, {'data-value': None, 'text': ''}, {'data-value': '7', 'text': 'Point & Click Adventure (e.g. Monkey Island)'}, {'data-value': None, 'text': ''}, {'data-value': '8', 'text': 'Life Simulations (e.g. The Sims)'}, {'data-value': None, 'text': ''}, {'data-value': '10', 'text': 'Music (e.g. Rockband)'}, {'data-value': None, 'text': ''}, {'data-value': '12', 'text': 'Sports: General  (e.g. FIFA)'}, {'data-value': None, 'text': ''}, {'data-value': '15', 'text': 'Real Time Strategy (e.g. Command & Conquer)'}, {'data-value': None, 'text': ''}, {'data-value': '17', 'text': 'Role Playing Game: General (e.g. Final Fantasy)'}, {'data-value': None, 'text': ''}, {'data-value': '19', 'text': 'Massively Multiplayer Online: Role Playing  (e.g. Warcraft)'}, {'data-value': None, 'text': ''}, {'data-value': '21', 'text': 'Racing: General (e.g. Need for Speed)'}, {'data-value': None, 'text': ''}, {'data-value': '23', 'text': 'Flight Simulation (e.g. MS Flight Simulator)'}, {'data-value': None, 'text': ''}, {'data-value': '25', 'text': 'Fighting (e.g. Street Fighter)'}, {'data-value': None, 'text': ''}, {'data-value': '28', 'text': 'Puzzle (e.g. Professor Layton)'}, {'data-value': None, 'text': ''}, {'data-value': '29', 'text': 'Party Games (e.g. Wii Sports)'}, {'data-value': None, 'text': ''}, {'data-value': '32', 'text': 'Casual (e.g. Facebook games)'}, {'data-value': None, 'text': ''}, {'data-value': '33', 'text': 'Other'}, {'data-value': None, 'text': ''}, {'data-value': '34', 'text': "I don't play video/computer games"}, {'data-value': None, 'text': ''}], 'question': 'What kind(s) of video/computer games do you play?', 'type': 'select'}

    def send_answer(self, user_answer):
        if not self.is_test:
            # send answer to page
            self.driver.execute_script(open("./js/answer_question.js").read(), user_answer)

            # TODO: Vary this a bit to emulate people
            time.sleep(3)

            # return new question
            return self.get_question()

        else:
            return self.send_test_answer(self, user_answer)

    @staticmethod
    def send_test_answer(self, user_answer):
        print(user_answer)
        return self.get_test_question()

    @staticmethod
    def answer_question_cli(question_data):
        print(question_data["question"])

        for answer_option in question_data["answers"]:
            if answer_option["data-value"] is not None:
                print(answer_option["data-value"] + ") " + answer_option["text"])

        user_answer = None

        while user_answer is None:
            user_answer = input("Which answer(s) do you choose (enter the number(s) as comma seperated list): ")

            for user_choice in user_answer.split(','):
                if user_choice not in map(lambda choice: choice["data-value"], question_data["answers"]):
                    user_answer = None

        return user_answer
