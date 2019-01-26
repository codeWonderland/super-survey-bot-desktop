import shelve


class SSBDataManager:
    def __init__(self):
        self.db = shelve.open('data/ssb_data')

    def input_data(self, data):
        if "question" in data and "answers" in data:
            self.db[data["question"]] = data["answers"]

    def get_answer(self, question):
        if question in self.db.keys():
            return self.db[question]

        else:
            return None

    def __del__(self):
        self.db.close()
