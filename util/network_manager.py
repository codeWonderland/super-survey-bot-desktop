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
import time
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

        # the lambda client serves as a factory that just returns
        # the client instance we just created
        purpose = ssl.Purpose.SERVER_AUTH

        if server_name == 'localhost':
            context = ssl.create_default_context(purpose, cafile="../ca.crt")

        else:
            context = ssl.create_default_context(purpose, cafile=None)

        coro = NetworkManager.loop.create_connection(lambda: NetworkManager.client, host=server_name, port=9000, ssl=context,
                                      server_hostname=server_name)

        NetworkManager.loop.run_until_complete(coro)

        # Start a task which reads from standard input
        asyncio.async(handle_user_input(NetworkManager.loop, NetworkManager.client))

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

    # Client sends message
    def send_message(self, data):
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

            # Iterate through JSON keys
            for key in data:

                # Check json key value
                if key == "USER_ID_ACCEPTED":
                    if data[key]:
                        self.is_logged_in = True
                        print('\nSuccessfully Logged In')

                # ----
                elif key == "ANSWER_DATA":
                    self.answer_question(data)

                # ----
                elif key == "QUESTION_REQUEST":
                    self.send_question()

                # Encapsulates error and other servers' additional features
                else:
                    # If we get something we aren't expecting, print it
                    print("UNEXPECTED RESP FROM SERVER" + key + ": " + data[key])

    # TODO: Send question data from main app to server for remote answering
    def send_question(self):
        question_data = NetworkManager.main_app.get_question()



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


@asyncio.coroutine
def handle_user_input(loop, client):
    """reads from stdin in separate thread
    if user inputs 'quit' stops the event loop
    otherwise just echos user input
    """
    # When new/unknown user joins
    while not client.is_logged_in:

        # Use username to login
        login_data = {"USER_ID": client.user_id}
        data_json = json.dumps(login_data)
        data_bytes_json = data_json.encode('ascii')

        # Send message to server
        client.send_message(data_bytes_json)

        # Give server one second delay to push data to it
        yield from asyncio.sleep(1)

        if not client.is_logged_in:
            print("This user has already been signed into the current server session!!!")

    # When user is known and logged into the server
    while client.is_logged_in:
        recip = "ALL"
        message = yield from loop.run_in_executor(None, input, "> ")

        # Checking for DM
        if len(message) != 0 and message[0] == '@':
            index = message.find(' ')
            recip = message[1:index]
            message = message[index + 1:]

        # Checking for command
        elif len(message) != 0 and message[0] == '/':
            if message == '/Quit':
                loop.stop()
                return
            elif message == '/Help':
                print('Chatterbox: The Chat Client You Never Knew You Didn\'t Need')
                print('---')
                print('Commands:')
                print('/Block <username> - blocks messages to and from the specified username')
                print('/Blocked - display a list of all users whom the client has blocked')
                print('/DisplayAllUsers - display all users whom have ever been active')
                print('/DisplayUsers - dispaly all currently active users')
                print('/Help - display all supported commands')
                print('/Name - display current user\'s username')
                print('/Unblock <username> - unblocks messages from the specified username. Note that if the unblocked user has blocked the current client, messages still cannot be sent between the two clients')
                print('/Quit - quits the application')
                print('')
                continue
            else:
                recip = client.user_id

        # Format message object to be encoded and JSONified
        message = {"MESSAGES": [(client.user_id, recip, int(time.time()), message)]}
        message = json.dumps(message)
        message = message.encode('ascii')
        client.send_message(message)

        # Give server one second delay to push data to it
        yield from asyncio.sleep(1)

    return
