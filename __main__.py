from swagbucks import SwagbucksCrawler

import kivy
kivy.require('1.0.6')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty
from kivy.uix.togglebutton import ToggleButton

Builder.load_string("""
<QuestionScreen>:
    id: question_screen
    cols: 1
    Label:
        id: question_text
        text: root.current_question
        size_hint_y: None
        height: '48dp'
    GridLayout:
        id: answer_container
        cols: 2
        padding: 5,5,5,5
    AnchorLayout:
        size_hint_y: None
        height: '48dp'
        Button:
            id: answer_button
            size_hint_y: None
            height: '48dp'
            size_hint_x: None
            width: '80dp'
            text: 'Confirm'
            anchor_x: 'center'
            on_press: root.answer_question()
    
""")


class QuestionScreen(GridLayout):
    current_question = StringProperty()

    def __init__(self, **kwargs):
        super(QuestionScreen, self).__init__(**kwargs)

        self.crawler = SwagbucksCrawler(True)
        self.current_question = 'Hello World!'

        question_data = self.crawler.get_question()

        self.set_question(question_data)

    def set_question(self, question_data):
        if question_data is not None:
            self.current_question = question_data["question"]

            if question_data["type"] == 'select':
                for answer_option in question_data["answers"]:
                    if answer_option["data-value"] is not None:
                        option = ToggleButton(
                            text=answer_option["text"],
                            id=answer_option["data-value"]
                        )

                        self.ids['answer_container'].add_widget(option)

            elif question_data["type"] == 'checkbox':
                for answer_option in question_data["answers"]:
                    if answer_option["data-value"] is not None:
                        option = ToggleButton(
                                text=answer_option["text"],
                                id=answer_option["data-value"],
                                group='radio'
                            )

                        self.ids['answer_container'].add_widget(option)

    def answer_question(self):
        # Get list of all answer options
        answers = self.ids['answer_container'].children

        # Filter answers for selected ones
        answers = list(
            filter(
                lambda x: x.state == 'down',
                answers
            )
        )

        # Get answer id list
        answers = list(
            map(
                lambda x: x.id,
                answers)
        )

        # Formatting Data
        answers = ','.join(answers)

        # Send answer and get new question
        new_question = self.crawler.send_answer(answers)

        # Clear the board
        self.ids['answer_container'].clear_widgets()

        # Set Next Question
        self.set_question(new_question)


class SurveyBot(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.title = 'Super Survey Bot-Inator 9000'
        return QuestionScreen()


if __name__ == "__main__":
    SurveyBot().run()
