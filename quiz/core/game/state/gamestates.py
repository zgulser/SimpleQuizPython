
from core.game.state.basegamestate import BaseGameState

class IdleState(BaseGameState):
    def update(self, game_controller):
        print("State changed to {}".format(IdleState.__name__))

class LoadingState(BaseGameState):
    def update(self, game_controller):
        print ("State changed to {}".format(LoadingState.__name__))

class ReadyState(BaseGameState):
    def update(self, game_controller):
        print("State changed to {}".format(ReadyState.__name__))

class WaitingToBeAnsweredState(BaseGameState):
    def update(self, game_controller):
        print("State changed to {}".format(WaitingToBeAnsweredState.__name__))

class TimeoutState(BaseGameState):
    def update(self, game_controller):
        print("State changed to {}".format(TimeoutState.__name__))

class CorrectAnswerState(BaseGameState):
    def update(self, game_controller):
        print("State changed to {}".format(CorrectAnswerState.__name__))

class WrongAnswerState(BaseGameState):
    def update(self, game_controller):
        print("State changed to {}".format(WrongAnswerState.__name__))

class GameOverState(BaseGameState):
    def update(self, game_controller):
        print("State changed to {}".format(GameOverState.__name__))

