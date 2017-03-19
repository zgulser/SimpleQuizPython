from blinker import signal
from core.game.utils import constants

class QuestionMaintainer:

    def __init__(self):
        self.questions = {}

    def add_question(self, question_identifier, question):
        self.questions[question_identifier] = question
        self.notify_add_question(question_identifier)

    def notify_add_question(self, question_identifier):
        add_question = signal(constants.QUESTION_ADDED)
        add_question.send(self, key=question_identifier)

    def get_questions(self):
        return self.questions

    def get_question(self, question_identifier):
        return self.questions[question_identifier]

    def is_empty(self):
        return self.questions.__len__() == 0

    def size(self):
        return self.questions.__len__()
