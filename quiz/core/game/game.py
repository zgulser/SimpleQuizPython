from core.questions.question import Question
from core.game.gameobserver import GameObserver
from core.exceptions.exceptions import Exceptions
from core.questions.questionmaintainer import QuestionMaintainer
from blinker import signal
from core.game.utils import constants

class Game():

    current_question = None

    def __init__(self, player_name='Zeki'):
        self.create_connections()

        self.question_maintainer = QuestionMaintainer()
        self.game_subscribers = None
        self.game_observers = []

        self.current_question = None

        self.total_questions_wrongly_answered = []
        self.total_questions_correctly_answered = []
        self.total_questions_answered = [self.total_questions_wrongly_answered, self.total_questions_correctly_answered]

        self.current_question_count = 1
        self.current_pts = 0

        self.player_name = player_name

    # Note: if you pass Game.on_question_added, self is the sender.
    #       if you pass self.on_question_added, self is 'this' object
    def create_connections(self):
        question_added = signal(constants.QUESTION_ADDED)
        question_added.connect(self.on_question_added)

    def on_question_added(self, *args, **kwargs):
        key = kwargs['key']
        if key == "Q1":
            self.current_question = self.question_maintainer.get_question(key)
            self.send_change_question_req()

    def add_game_observer(self, game_observer):
        if issubclass(type(game_observer), GameObserver):
            self.game_observers.append(game_observer)
        else:
            Exceptions.raiseException("Subscriber isn't a subclass of {}".format(GameObserver.__name__))

    def remove_game_observer(self, game_observer):
        pass

    def check_answer(self, option):
        is_answered_correctly = self.current_question.is_correct_answer(option)
        self.update_question_lists(is_answered_correctly)
        self.load_next_question()

    def load_next_question(self):
        self.current_question = None
        self.send_change_question_req()

    def send_change_question_req(self):
        timer_tick = signal(constants.CHANGE_QUESTION)
        timer_tick.send(self, question=self.current_question)

    def update_question_lists(self, is_answered_correctly):
        self.total_questions_answered.append(self.current_question)
        if is_answered_correctly:
            self.total_questions_correctly_answered.append(self.current_question)
        else:
            self.total_questions_wrongly_answered.append(self.current_question)

    def increment_current_question(self):
        self.current_question_count += 1

    def decrement_current_question(self):
        self.current_question_count -= 1

    def update_current_game_state(self, state):
        self.current_game_state = state
        self.notify_via_blinker(state)

    # this is custom observer. it's not used for now. but you can switch to this method instead of using 'Blinker'
    def notify_observers(self, state):
        for observer in self.game_observers:
            observer.onGameStateChanged(self.current_game_state)

    def notify_via_blinker(self, state):
        state = signal(type(state).__name__)
        state.send(self)
        print(state.name)

    def get_current_game_state(self):
        return self.current_game_state

    def calculate_current_pts(self):
        total_pts = 0
        correctly_answered_questions = self.total_questions_answered[1]
        for question in correctly_answered_questions:
            if isinstance(question, Question):
                total_pts += question.difficulty * 10
            else:
                pass