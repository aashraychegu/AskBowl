from ._anvil_designer import mainpageTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import time
from anvil.js.window import speechSynthesis as synth
from anvil.js.window import alert, prompt

def mc_choice(message):
    return prompt(message).upper()[0] == "Y"
    
class mainpage(mainpageTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        print(mc_choice("unga kabunga"))
    def say(self,text,voice = "",volume = 100,rate = 100,pitch = 100):
        text = text.replace("`","")
        utr = anvil.js.window.SpeechSynthesisUtterance(text)
        utr.voice = voice
        utr.volume = volume
        utr.rate = rate
        utr.pitch = pitch
        synth.speak(utr)
    def read_question_click(self, **event_args):
        """This method is called when the button is clicked"""
        # self.say("hi")

    def rate_pressed_enter(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        pass

    def pause_reading_click(self, **event_args):
        """This method is called when the button is clicked"""
        pass

    def resume_reading_click(self, **event_args):
        """This method is called when the button is clicked"""
        pass








