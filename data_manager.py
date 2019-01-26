import shelve
import uuid


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

    def set_id(self, user_id):
        self.db["user-id"] = user_id

    def get_id(self):
        # Check for existence of user-id
        if "user-id" in self.db.keys():
            return self.db["user-id"]

        else:
            # Generate ID
            user_id = str(uuid.uuid4())

            # Put ID in db
            self.db["user-id"] = user_id

            return user_id

    def __del__(self):
        self.db.close()
