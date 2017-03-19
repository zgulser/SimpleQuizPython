
class StateHandler():

    def __init__(self, game_screen):
        self.game_screen = game_screen

    def on_loading_state(self, sender):
        print ('in loading state by {}'.format(sender))
        self.game_screen.mainloop()
        pass

    def on_ready_state(self, sender):
        print('in ready stateby {}'.format(sender))
        pass

    def on_waiting_to_be_answered_state(self, sender):
        print('in waiting to be answered state by {}'.format(sender))
        self.game_screen.start_timer_tick_thread()
        pass