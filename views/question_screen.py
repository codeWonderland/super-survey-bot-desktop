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

        self.current_question = 'Hello World!'

    def set_question(self, question_data):
        print(question_data)
        if question_data is not None:
            self.current_question = question_data["QUESTION"]

            if question_data["TYPE"] == 'CHECKBOX':
                for answer_option in question_data["ANSWERS"]:
                    if answer_option["DATA_VALUE"] is not None:
                        option = ToggleButton(
                            text=answer_option["TEXT"],
                            id=answer_option["DATA_VALUE"]
                        )

                        self.ids['answer_container'].add_widget(option)

            elif question_data["TYPE"] == 'SELECT':
                for answer_option in question_data["ANSWERS"]:
                    print("OKAY")
                    if answer_option["DATA_VALUE"] is not None:
                        option = ToggleButton(
                            text=answer_option["TEXT"],
                            id=answer_option["DATA_VALUE"],
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

        # Get text of answers
        answer_labels = list(
            map(
                lambda x: x.text,
                answers
            )
        )

        # Get answer id list
        answer_values = list(
            map(
                lambda x: x.id,
                answers
            )
        )

        # Formatting Data
        answer_values = ','.join(answer_values)

        # Clear the board
        self.ids['answer_container'].clear_widgets()

        # Send back data
        self.parent.parent.answer_question({
            "QUESTION": self.current_question,
            "ANSWER_LABELS": answer_labels,
            "ANSWER_VALUES": answer_values
        })
