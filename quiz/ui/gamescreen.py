from tkinter import *
import tkinter as tk
import threading
import time
from tkinter import font
from tkinter.ttk import *
from PIL import Image, ImageTk
from blinker import *

from ui.statehandler import StateHandler
from ui.widgetmediator import WidgetMediator
from core.game.gameobserver import GameObserver
from core.game.utils import constants
from core.game.state.gamestates import *

class ApplicationUI(Frame, GameObserver):

    widget_mediator = None
    state_handler = None

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.geometry("1000x700+200+150")
        self.pack()
        self.create_state_handler()
        self.create_connections()
        self.create_widgets()
        self.create_widget_mediator()

        print ("Game UI Initialized!")

    def on_change_question(self, *args, **kwargs):
        question = kwargs['question']
        self.update_question_ui(question)

    def create_state_handler(self):
        if ApplicationUI.state_handler == None:
            ApplicationUI.state_handler = StateHandler(self)

    def create_connections(self):
        loading = signal(LoadingState.__name__)
        loading.connect(ApplicationUI.state_handler.on_loading_state)

        ready = signal(ReadyState.__name__)
        ready.connect(ApplicationUI.state_handler.on_ready_state)

        loading = signal(WaitingToBeAnsweredState.__name__)
        loading.connect(ApplicationUI.state_handler.on_waiting_to_be_answered_state)

        timer_tick_rec = signal("{}".format(constants.TIMER_EVENT))
        timer_tick_rec.connect(self.on_timer_tick)

        change_question = signal(constants.CHANGE_QUESTION)
        change_question.connect(self.on_change_question)

    def create_widgets(self):
        self.create_top_panel()
        self.create_mid_panel()
        self.create_bottom_panel()
        self.TOPFRAME.pack()
        self.MIDFRAME.pack(fill="x", expand="yes")
        self.BOTTOMFRAME.pack(fill='x', expand="yes")

    def create_top_panel(self):
        self.create_title_and_logo()

    def create_title_and_logo(self):
        self.TOPFRAME = tk.Frame(self, pady=50)
        self.TOPFRAMESUB = tk.Frame(self.TOPFRAME)

        self.TITLE = tk.Label(self.TOPFRAMESUB, text="Coolest Quiz", font=("Comic Sans MS", 30), fg='#F6292B')
        self.TITLE.pack()
        self.MOTTO = tk.Label(self.TOPFRAMESUB, text="solve, compete, have fun!", font=("Comic Sans MS", 20), fg='#000000')
        self.MOTTO.pack()
        self.TOPFRAMESUB.pack(side=LEFT)

        image = Image.open("../../assets/app_logo_4.jpg")
        photo = ImageTk.PhotoImage(image)
        self.APPLOGO = tk.Label(self.TOPFRAME, image=photo)
        self.APPLOGO.image = photo
        self.APPLOGO.pack(side=LEFT)

    def create_mid_panel(self):
        self.MIDFRAME = tk.LabelFrame(self, pady=20, padx=20, relief=FLAT, borderwidth=5, bg='#F5F5F5')
        self.create_question_panel()

    def create_question_panel(self):
        print(font.families())
        self.create_top_question_panel()
        self.create_mid_question_panel()

    def create_top_question_panel(self):
        self.QUESTIONSFRAME = tk.Frame(self.MIDFRAME, pady=15, padx=15)


        self.QUESTIONLABEL = tk.Label(self.QUESTIONSFRAME, text="Which's the capital of Guatemala?", font=("Helvetica", 18),fg='#282828')
        self.QUESTIONLABEL.pack(side=LEFT, )
        self.DUMMYLABEL = tk.Label(self.QUESTIONSFRAME, padx=100)
        self.DUMMYLABEL.pack(side=LEFT)
        self.TIMERLABEL = tk.Label(self.QUESTIONSFRAME, text="00:30", font=("Helvetica", 20), fg='#CD3333')
        self.TIMERLABEL.pack(side=LEFT)

        self.QUESTIONSFRAME.pack(fill=X, side=TOP)

    def create_mid_question_panel(self):
        self.ANSWERSLABELPARENT = tk.Frame(self.MIDFRAME, pady=15, padx=15)

        self.create_options_AC()
        self.ANSWERSLABELSPACER = tk.Frame(self.ANSWERSLABELPARENT, width=200)
        self.create_options_BD()

        self.ANSWERSLABEL1.pack(side=LEFT)
        self.ANSWERSLABELSPACER.pack(side=LEFT)
        self.ANSWERSLABEL2.pack(side=LEFT)

        self.ANSWERSLABELPARENT.pack(fill=X, side=BOTTOM)

    def create_options_AC(self):
        self.ANSWERSLABEL1 = tk.Frame(self.ANSWERSLABELPARENT)
        self.ANSWERA = tk.Button(self.ANSWERSLABEL1, justify=LEFT, text="A) Ankara", font=("Helvetica", 15),
                                 fg='red', pady=10, command = self.handle_answer_a_click)
        self.ANSWERA.pack(fill=X, side=TOP)
        self.ANSWERB = tk.Button(self.ANSWERSLABEL1, justify=LEFT, text="B) Brussels", font=("Helvetica", 15),
                                 fg='red', pady=10, command = self.handle_answer_b_click)
        self.ANSWERB.pack(fill=X, side=BOTTOM)

    def create_options_BD(self):
        self.ANSWERSLABEL2 = tk.Frame(self.ANSWERSLABELPARENT)
        self.ANSWERC = tk.Button(self.ANSWERSLABEL2, justify=LEFT, text="C) Shieeeaaat!!", font=("Helvetica", 15),
                                 fg='#5B5B5B', pady=10, command = self.handle_answer_c_click)
        self.ANSWERC.pack(fill=X, side=TOP)
        self.ANSWERD = tk.Button(self.ANSWERSLABEL2, justify=LEFT, text="D) Hon", font=("Helvetica", 15),
                                 fg='#5B5B5B', pady=10, command = self.handle_answer_d_click)
        self.ANSWERD.pack(fill=X, side=BOTTOM)

    def create_bottom_panel(self):
        self.BOTTOMFRAME = tk.LabelFrame(self, pady=20, relief=FLAT)

        self.draw_pie_questions_state(6)
        self.draw_total_pts()
        self.add_action_buttons()

    def draw_pie_questions_state(self, left):
        self.PROGRESSCANVAS = tk.Canvas(self.BOTTOMFRAME, bg="white", height=100, width=100)
        coord = 10, 10, 100, 100

        self.PROGRESSCANVAS.create_oval(coord, fill="#F5F5F5", outline='white')
        self.PROGRESSCANVAS.create_arc(coord, start=90, extent=left*36, fill="#A2CD5A", outline="white")
        self.PROGRESSCANVAS.create_text(55, 55, text="6", font=("Helvetica", 20), fill="#5B5B5B")

        self.PROGRESSCANVAS.pack(side=LEFT)

    def draw_total_pts(self):
        pts_string = "Your points: {}".format(120)
        self.PTSLABEL = tk.Label(self.BOTTOMFRAME, text=pts_string, font=("Helvetica", 15), fg='#5B5B5B', padx=20)
        self.PTSLABEL.pack(side=LEFT)

    def add_action_buttons(self):
        self.BOTTOMSUBFRAMERIGHT = tk.Frame(self.BOTTOMFRAME, relief=FLAT, borderwidth=0, bg='white')

        self.ACTIONBUTTON = tk.Button(self.BOTTOMSUBFRAMERIGHT, text='GET MORE QUESTIONS', command = self.handle_get_more_click)
        self.ACTIONBUTTON.pack()

        self.BOTTOMSUBFRAMERIGHT.pack(side=RIGHT)

    def create_widget_mediator(self):
        if ApplicationUI.widget_mediator == None:
            ApplicationUI.widget_mediator = WidgetMediator(self, self.ANSWERA, self.ANSWERB, self.ANSWERC, self.ANSWERD,
                                                           self.ACTIONBUTTON, self.PROGRESSCANVAS, self.PTSLABEL, self.TIMERLABEL)

    def update_question_ui(self, question):
        self.update_question_text(question)
        self.update_question_options(question)
        self.update_question_timer(question)

    def update_question_text(self, question):
        self.QUESTIONLABEL.config(text=question.question)

    def update_question_options(self, question):
        self.ANSWERA.config(text="A) {}".format(question.answer_map["A"]))
        self.ANSWERB.config(text="B) {}".format(question.answer_map["B"]))
        self.ANSWERC.config(text="C) {}".format(question.answer_map["C"]))
        self.ANSWERD.config(text="D) {}".format(question.answer_map["D"]))

    def update_question_timer(self, question):
        pass

    def handle_answer_a_click(self):
        ApplicationUI.widget_mediator.click_button_answer_A()

    def handle_answer_b_click(self):
        ApplicationUI.widget_mediator.click_button_answer_B()

    def handle_answer_c_click(self):
        ApplicationUI.widget_mediator.click_button_answer_C()

    def handle_answer_d_click(self):
        ApplicationUI.widget_mediator.click_button_answer_D()

    def handle_get_more_click(self):
        ApplicationUI.widget_mediator.click_button_get_more()

    def check_answer(self, option):
        timer_tick = signal(constants.CHECK_ANSWER)
        timer_tick.send(self, answer=option)

    def start_timer_tick_thread(self):
        timer_ticker_thread = ApplicationUI.TimerThread("Timer-Ticker-Thread", self)
        timer_ticker_thread.start()

    def on_game_state_changed(self, state):
        pass

    def on_timer_tick(self, *args, **kwargs):
        tick = kwargs['tick']
        print ("Caught signal from {}, data {}".format(self.__class__.__name__, tick))
        ApplicationUI.widget_mediator.handle_timer_text_update(tick)
        pass

    class TimerThread(threading.Thread):

        def __init__(self, thread_name, app_ui):
            threading.Thread.__init__(self)
            self.thread_name = thread_name
            self.app_ui = app_ui

        def run(self):
            print("{} is executing...".format(self.thread_name))
            counter = 30
            while(counter >= 0):
                timer_tick = signal("{}".format(constants.TIMER_EVENT))
                timer_tick.send(self.app_ui, tick=counter)

                print("{} secs left...".format(counter))
                counter = counter - 1
                time.sleep(1)
