import json
import logging
import os
import random
import socket
from logging.handlers import RotatingFileHandler

import protocol

host = "localhost"
port = 12000
# HEADERSIZE = 10

"""
set up inspector logging
"""
inspector_logger = logging.getLogger()
inspector_logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s :: %(levelname)s :: %(message)s", "%H:%M:%S")
# file
if os.path.exists("./logs/inspector.log"):
    os.remove("./logs/inspector.log")
file_handler = RotatingFileHandler('./logs/inspector.log', 'a', 1000000, 1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
inspector_logger.addHandler(file_handler)
# stream
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.WARNING)
inspector_logger.addHandler(stream_handler)


class Player():

    def __init__(self):

        self.end = False
        # self.old_question = ""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def connect(self):
        self.socket.connect((host, port))

    def reset(self):
        self.socket.close()

    def answer(self, question):
        # work
        data = question["data"]
        print("data == ", data)
        i = 0
        qtype = question["question type"]
        print("question", qtype)
        response_index = random.randint(0, len(data) - 1)
        if qtype == "select character":
            while i < len(question["data"]):
                print("character color  is : ", data[i]["color"], " | and his pos is :", data[i]["position"])
                i += 1
            response_index = random.randint(0, len(data) - 1)
            print("response : ", response_index)
        # power = "activate " + data[response_index]['color'] + " power"
        elif qtype == "activate purple power":
            response_index = 1
        elif qtype == "activate red power":
            response_index = 1
        elif qtype == "activate black power":
            response_index = 1
        elif qtype == "activate blue power":
            response_index = 1
        elif qtype == "activate white power":
            response_index = 1
        elif qtype == "activate grey power":
            response_index = 1
        elif qtype == "activate pink power":
            response_index = random.randint(0, len(data) - 1)
        elif qtype == "select position":
            j = 0
            while j < len(question["game state"]["characters"]):
                print("gstate suspect : ", question["game state"]["characters"][j]["suspect"], " | position :",
                  question["game state"]["characters"][j]["position"], " | color : ",
                  question["game state"]["characters"][j]["color"])
                x = 0
                while x < len(data):
                    print(data[x])
                    if data[x] == question["game state"]["characters"][j]["position"]:
                        response_index = x
                        print("if response :", response_index)
                        x = 42
                    x += 1
                j += 1


            print("respone : ", response_index)


        #elif qtype == "activate " + data[response_index]['color']  + " power":
         #   print("YES ACTIVATE ", data[response_index]['color'], " power")



        # log
        inspector_logger.debug("|\n|")
        inspector_logger.debug("inspector answers")
        inspector_logger.debug(f"question type ----- {question['question type']}")
        inspector_logger.debug(f"data -------------- {data}")
        inspector_logger.debug(f"response index ---- {response_index}")
        inspector_logger.debug(f"response ---------- {data[response_index]}")
        return response_index

    def handle_json(self, data):
        data = json.loads(data)
        response = self.answer(data)
        # send back to server
        bytes_data = json.dumps(response).encode("utf-8")
        protocol.send_json(self.socket, bytes_data)

    def run(self):

        self.connect()

        while self.end is not True:
            received_message = protocol.receive_json(self.socket)
            if received_message:
                self.handle_json(received_message)
            else:
                print("no message, finished learning")
                self.end = True


p = Player()

p.run()