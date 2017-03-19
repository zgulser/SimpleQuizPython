from core.questions.parser.questionparser import QuestionParser
from core.questions.questionfactory import QuestionFactory
from core.questions.parser import parserutils
import json
import threading
from blinker import signal

class JSONQuestionParser(QuestionParser):

    question_str = ""

    def __init__(self, path):
        super().__init__(path)

    def parse_file(self):
        parser_thread = self.ParserThread(self, "Question-Parser-Thread", self.filepath)
        parser_thread.start()

    @classmethod
    def set_questions_str(cls, questions_str):
        cls.question_str = questions_str

    @classmethod
    def get_questions(cls):
        print("questions content 2 : {} ".format(cls.question_str))
        parsed = json.loads(cls.question_str)

        def create_questions(): # closure closed on 'parsed' variable
            for item in parsed:
                yield item
                yield QuestionFactory.create_question(parsed, item)

        return create_questions

    class ParserThread(threading.Thread):

        def __init__(self, json_parser_obj, thread_name, filepath):
            threading.Thread.__init__(self)

            self.json_parser_obj = json_parser_obj
            self.thread_name = thread_name;
            self.filepath = filepath

        def run(self):
            print("{} is executing...".format(self.thread_name))
            with open(self.filepath, 'r') as foq:
                questions_str = foq.read()
                JSONQuestionParser.set_questions_str(questions_str)

            event_json_file_ready = signal("{}".format(parserutils.JSONEvent))
            event_json_file_ready.send(self)

            print("Game QUESIOTNS fetched!")
