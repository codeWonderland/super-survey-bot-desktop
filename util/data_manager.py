import shelve
import uuid


class SSBDataManager:
    def __init__(self):
        self.db = shelve.open('data/ssb_data')

    def input_data(self, data):
        if "QUESTION" in data and "ANSWERS" in data:
            self.db[data["QUESTION"]] = data["ANSWERS"]

    def get_answer(self, question):
        if question in self.db.keys():
            return self.db[question]

        else:
            return None

    def set_id(self, user_id):
        self.db["USER_ID"] = user_id

    def get_id(self):
        # Check for existence of USER_ID
        if "USER_ID" in self.db.keys():
            return self.db["USER_ID"]

        else:
            # Generate ID
            user_id = str(uuid.uuid4())

            # Put ID in db
            self.db["USER_ID"] = user_id

            return user_id

    def __del__(self):
        self.db.close()
