from util.swagbucks import SwagbucksCrawler
from util.swagbucks import SwagbucksTestCrawler
from util.data_manager import SSBDataManager

import kivy

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from views.question_screen import QuestionScreen

kivy.require('1.0.6')

Builder.load_string("""
<SBContainer>:
    do_default_tab: False
    TabbedPanelItem:
        text: 'Dashboard'
        Label:
            text: 'Dashboard content area'
""")


class SSBContainer(TabbedPanel):
    def __init__(self, test_mode, **kwargs):
        super(SSBContainer, self).__init__(**kwargs)

        # Some Default Attribute Values
        self.current_question = ""

        # Establish Test Status
        self.test_mode = test_mode

        if self.test_mode:
            self.crawler = SwagbucksTestCrawler()

        else:
            self.crawler = SwagbucksCrawler()

        # Create Data Manager Instance
        self.data_manager = SSBDataManager()

        # Create Answering Interface Tab
        self.answering_interface = TabbedPanelHeader(text="Answer Questions")

        self.add_widget(self.answering_interface)

        self.answering_interface.content = QuestionScreen()

        # Fetch Question
        question_data = self.crawler.get_question()

        self.delegate_answering(question_data)

    def answer_question(self, data):
        # Make sure question is still unanswered
        if "question" in data and data["question"] == self.current_question:
            # Send data to crawler
            if "answer_values" in data:
                self.crawler.send_answer(data["answer_values"])

            # Record non-test data in db
            if not self.test_mode and "question" in data and "answer_labels" in data:
                self.record_answer(data["question"], data["answer_labels"])

            # Start next question
            self.delegate_answering(self.crawler.get_question())

    def delegate_answering(self, question_data):
        # Update Current Question
        self.current_question = question_data["question"]

        # Send Question to Answering Interface
        self.answering_interface.content.set_question(question_data)

    def record_answer(self, question, answers):
        data = {
            "question": question,
            "answers": answers
        }

        self.data_manager.input_data(data)

    def get_id(self):
        return self.data_manager.get_id()


class SurveyBot(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.title = 'Super Survey Bot-Inator 9000'
        return SSBContainer(test_mode=True)


if __name__ == "__main__":
    SurveyBot().run()
