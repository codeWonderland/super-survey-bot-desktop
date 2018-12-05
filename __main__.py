from selenium import webdriver
import time


def start_crawler():
    # get instance of driver
    driver = webdriver.Chrome()

    # load up the login page
    driver.get("https://www.swagbucks.com/p/login")

    # while until the user has logged in
    while "Login | Swagbucks" in driver.title:
        time.sleep(5)

    # navigate to the survey page
    driver.execute_script(open("./js/open_survey.js").read())

    # since we called the survey page via js
    # we wait for the survey page to load
    while "Gold Surveys | Swagbucks" not in driver.title:
        time.sleep(5)

    # this program is meant to just wash, rinse, repeat forever
    while True:
        # grab question data from page
        question_data = driver.execute_script(open("./js/get_question.js").read())

        # delegate decision
        user_answer = answer_question(question_data)

        # send answer to page
        driver.execute_script(open("./js/answer_question.js").read(), user_answer)

        # wait for js to finish and new page to load
        time.sleep(3)


def answer_question(question_data):
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


if __name__ == "__main__":
    start_crawler()
