"""async_client
Champlain College CSI-235, Spring 2018
Prof. Josh Auerbach
Bare bones example of asynchronously receiving
data from server and user input from stdin

Last modified as 'AsycClient' for 'Chatterbox' by Alice Easter && Eric Cacciavillani on 4/26/18

Last modified as 'NetworkManager' for 'Super Survey Bot Desktop' by Alice Easter on 4/26/18
"""
import json
import ssl
import struct
import asyncio


class NetworkManager:
    loop = None
    client = None
    main_app = None

    def __init__(self, main_app, server_name='localhost'):
        # Establish Connection to Main App
        NetworkManager.main_app = main_app

        # Get Async Event Loop
        NetworkManager.loop = asyncio.get_event_loop()

        # we only need one client instance
        NetworkManager.client = AsyncClient(main_app.get_id())

        coro = NetworkManager.loop.create_connection(lambda: NetworkManager.client,
                                                     host=server_name,
                                                     port=9000)

        # SSL Version
        # the lambda client serves as a factory that just returns
        # the client instance we just created
        # purpose = ssl.Purpose.SERVER_AUTH
        #
        # if server_name == 'localhost':
        #     context = ssl.create_default_context(purpose, cafile="ca.crt")
        #
        # else:
        #     context = ssl.create_default_context(purpose, cafile=None)
        #
        # coro = NetworkManager.loop.create_connection(lambda: NetworkManager.client,
        #                                              host=server_name,
        #                                              port=9000,
        #                                              ssl=context,
        #                                              server_hostname=server_name)

        NetworkManager.loop.run_until_complete(coro)

        # Start a task which reads from standard input
        # asyncio.async(handle_user_input(NetworkManager.loop, NetworkManager.client))

        try:
            NetworkManager.loop.run_forever()
        finally:
            NetworkManager.loop.close()


class AsyncClient(asyncio.Protocol):
    def __init__(self, user_id):
        self.__buffer = ""
        self.is_logged_in = False
        self.user_id = user_id
        self.data_len = 0
        self.device_type = "DESKTOP"
        self.transport = None
        self.has_companion = False

    def connection_made(self, transport):
        self.transport = transport
        self.is_logged_in = False

        self.login()

    def login(self):
        login_data = {
            "DATA_TYPE": "USER_ID",
            "USER_ID": self.user_id
        }

        self.send_message(login_data)

    # Client sends message
    def send_message(self, data):
        data["DEVICE_TYPE"] = self.device_type

        # Encode Data
        data = json.dumps(data)
        data = data.encode("ascii")

        msg = b''
        msg += struct.pack("!I", len(data))
        msg += data
        self.transport.write(msg)

    # Handles the client reciving data
    def data_received(self, data):
        """simply prints any data that is received"""
        # Get data into usable format
        if self.__buffer == '':
            # Find first brace and offset the data by that
            brace_index = data.find(b'{')
            self.data_len = struct.unpack("!I", data[0:brace_index])[0]
            data = data[brace_index:(self.data_len + brace_index)]

        data = data.decode('ascii')
        self.__buffer += data

        # Buffer contains full message
        if len(self.__buffer) == self.data_len:

            # Extract to JSON object
            data = json.loads(self.__buffer)

            # Clear pre and post
            self.__buffer = ''
            self.data_len = 0

            print(data)

            key = data["DATA_TYPE"]

            # Check json key value
            if key == "LOGIN_DATA":
                if data["LOGIN_SUCCESSFUL"]:
                    self.is_logged_in = True
                    print('\nSuccessfully Logged In')
                else:
                    # TODO: CREATE VISUAL FEEDBACK FOR USER
                    print("ISSUE LOGGING IN")

            # ----
            elif key == "ANSWER_DATA":
                self.answer_question(data)

            # ----
            elif key == "QUESTION_REQUEST":
                self.send_question()

            # ----
            elif key == "COMPANION_LOST":
                pass

            # Encapsulates error and other servers' additional features
            else:
                # If we get something we aren't expecting, print it
                print("UNEXPECTED RESP FROM SERVER - " + key)

    # Send question data from main app to server for remote answering
    def send_question(self):
        question_data = NetworkManager.main_app.get_question()
        question_data["DATA_TYPE"] = "QUESTION_DATA"

        self.send_message(question_data)

    # TODO: Send answer data to server for backup
    def send_answer(self, data):
        pass

    # Send answer data to main application
    @staticmethod
    def answer_question(data):
        """
        Take in answer data from server,
        format said data for our answering system,
        then forward the answer to main app
        :param data:
        :return:
        """

        NetworkManager.main_app.answer_question(data)

    # When the client is disconnected from the server
    def connection_lost(self, exc):
        print('Connection to server lost')
        print('(Press RET to exit)')
        self.is_logged_in = False

        NetworkManager.loop.run_in_executor(None, input, "")
        exit(0)
