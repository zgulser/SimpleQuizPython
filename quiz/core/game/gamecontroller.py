from core.game.state.gamestates import *
from core.game.game import Game
import threading
import time
from blinker import signal
from core.game.utils import constants

class GameController:

    current_game = None

    def __init__(self):
        if GameController.current_game == None:
            GameController.current_game = Game()

        self.create_connections()

    def create_connections(self):
        to_waiting_state = signal(constants.TO_WAITING_STATE)
        to_waiting_state.connect(GameController.on_waiting_state_event)

        check_answer = signal("{}".format(constants.CHECK_ANSWER))
        check_answer.connect(self.on_check_answer)

    def on_waiting_state_event(self):
        self.change_state(WaitingToBeAnsweredState())

    def on_check_answer(self, *args, **kwargs):
        option = kwargs["answer"]
        print ("is correct {}".format(self.current_game.check_answer(option)))

    def start_game(self):
        delay_thread = GameController.StateDelayThread("State-Delay-Thread", self)
        delay_thread.start()

        self.change_state(LoadingState())

    def to_next_question(self):
        pass

    def change_state(self, game_state):
        game_state.update(self)
        GameController.current_game.update_current_game_state(game_state)

    def update_view(self):
        # check the current state and update the view
        pass

    def finish_game(self):
        self.change_state(GameOverState())

    def quit_game(self):
        pass

    def get_current_game(self):
        return self.current_game

    class StateDelayThread(threading.Thread):

        def __init__(self, thread_name, game_controller):
            threading.Thread.__init__(self)
            self.thread_name = thread_name
            self.game_controller = game_controller

        def run(self):
            print("{} is executing...".format(self.thread_name))
            time.sleep(3)

            to_waiting_state = signal(constants.TO_WAITING_STATE)
            to_waiting_state.send(self.game_controller)


