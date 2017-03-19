from core.questions.parser.jsonquestionparser import JSONQuestionParser
from core.questions.question import Question
from core.game.gamecontroller import GameController
from core.questions.parser import parserutils
from ui.gamescreen import ApplicationUI
from tkinter import *
from blinker import signal
import threading

class Application:

    game_controller = None
    game_ui = None

    def __init__(self):
        print ('App started...')

        print('Initializing app connections...')
        self.init_connections()

        print('Initializing the game...')
        self.init_game_engine()

        print('Initializing the UI...')
        self.init_ui()

        print('Fetching questions...')
        self.fetch_questions()

        print('Starting the game...')
        Application.game_controller.start_game()

    def init_connections(self):
        event_json_file_ready = signal("{}".format(parserutils.JSONEvent))
        event_json_file_ready.connect(Application.start_question_adder)

    def start_question_adder(self):
        print ("sender obj {}".format(self.__class__.__name__))
        print ("thread name 2 {} ".format(threading.current_thread().name))
        Application.addToQuestionsContainer(JSONQuestionParser.get_questions())

    def fetch_questions(self):
        self.questionparser = JSONQuestionParser("/Users/zeki/Desktop/Zeki/code/non-backbase/python/youtube/FlashCardQuizzer/core/questions/parser/questions.txt")
        self.questionparser.parse_file()

    @classmethod
    def addToQuestionsContainer(cls, func_create_questions):
        question_adder_thread = cls.QuestionAdderThread("Question-Adder-Thread", func_create_questions)
        question_adder_thread.start()

    def init_game_engine(self):
        Application.game_controller = GameController()

    def init_ui(self):
        root = Tk()
        self.game_ui = ApplicationUI(master=root)

        game = Application.game_controller.get_current_game()
        game.add_game_observer(self.game_ui)

    class QuestionAdderThread(threading.Thread):

        def __init__(self, thread_name, func_create_questions):
            threading.Thread.__init__(self)

            self.thread_name = thread_name;
            self.func_create_questions = func_create_questions

        def run(self):
            print("{} is executing...".format(self.thread_name))
            question_key = ""
            for item in self.func_create_questions():
                if isinstance(item, Question):
                    GameController.current_game.question_maintainer.add_question(question_key, item)
                    question_key = ""
                else:
                    question_key = item

            print('Number of questions fetched : {}'.format(GameController.current_game.question_maintainer.size()))

if __name__ == '__main__':
    app = Application()