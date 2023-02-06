from ._anvil_designer import mainpageTemplate
from anvil import *
import anvil.server
import plotly.graph_objects as go
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import time
from anvil.js.window import speechSynthesis as synth
from anvil.js.window import alert, prompt
from anvil_extras.storage import indexed_db

def clamp(num, minimum=0, maximum=200):
    return max(min(maximum, num), minimum)

def mc_choice(message):
    return prompt(message).upper()[0] == "Y"
    
class mainpage(mainpageTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.pqs, self.lookup = anvil.server.call("create_categories")
        ab_store = indexed_db.create_store('ask_bowl')
        ab_store["pqs"] = self.pqs
        ab_store["lookup"] = self.lookup
        self.sources = list(self.lookup.keys())
        self.all_categories = ["physics","general science","energy","earth and space","earth science","chemistry","biology","astronomy","math","computer science"]    
        

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








