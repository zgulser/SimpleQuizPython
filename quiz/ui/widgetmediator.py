from tkinter import messagebox
from core.game.utils.utilities import Utilities

class WidgetMediator():

    def __init__(self, MAINFRAME, BUTTONANSWERA, BUTTONANSWERB, BUTTONANSWERC, BUTTONANSWERD, BUTTONGETMORE, PROGRESSCANVAS, POINTSLABEL, TIMERLABEL):
        self.MAINFRAME = MAINFRAME
        self.BUTTONANSWERA = BUTTONANSWERA
        self.BUTTONANSWERB = BUTTONANSWERB
        self.BUTTONANSWERC = BUTTONANSWERC
        self.BUTTONANSWERD = BUTTONANSWERD
        self.BUTTONGETMORE = BUTTONGETMORE

        self.PROGRESSCANVAS = PROGRESSCANVAS
        self.POINTSLABEL = POINTSLABEL

        self.TIMERLABEL = TIMERLABEL

    def click_button_answer_A(self):
        self.BUTTONANSWERB.config(state="disabled")
        self.BUTTONANSWERC.config(state="disabled")
        self.BUTTONANSWERD.config(state="disabled")
        self.BUTTONGETMORE.config(state="disabled")

        self.handle_messagebox_click('A')

    def click_button_answer_B(self):
        self.BUTTONANSWERA.config(state="disabled")
        self.BUTTONANSWERC.config(state="disabled")
        self.BUTTONANSWERD.config(state="disabled")
        self.BUTTONGETMORE.config(state="disabled")

        self.handle_messagebox_click('B')

    def click_button_answer_C(self):
        self.BUTTONANSWERA.config(state="disabled")
        self.BUTTONANSWERB.config(state="disabled")
        self.BUTTONANSWERD.config(state="disabled")
        self.BUTTONGETMORE.config(state="disabled")

        self.handle_messagebox_click('C')

    def click_button_answer_D(self):
        self.BUTTONANSWERA.config(state="disabled")
        self.BUTTONANSWERB.config(state="disabled")
        self.BUTTONANSWERC.config(state="disabled")
        self.BUTTONGETMORE.config(state="disabled")
        self.BUTTONGETMORE.config(state="active")

        self.handle_messagebox_click('D')

    def handle_messagebox_click(self, option):
        if messagebox.askyesno("Coolest Quiz!", "Are you sure about option {} ?".format(option)) == True:
            self.MAINFRAME.check_answer(option)
        else:
            print ('no')

        self.enable_all_buttons()

    def handle_timer_text_update(self, tick):
        self.TIMERLABEL.config(text=Utilities.get_formatted_tick_str(tick))
        if (tick == 0):
            pass #TODO

    def enable_all_buttons(self):
        self.BUTTONANSWERA.config(state="normal")
        self.BUTTONANSWERB.config(state="normal")
        self.BUTTONANSWERC.config(state="normal")
        self.BUTTONANSWERD.config(state="normal")
        self.BUTTONGETMORE.config(state="normal")

    def click_button_get_more(self):
        pass




