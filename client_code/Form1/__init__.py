from ._anvil_designer import Form1Template
from anvil import *
import plotly.graph_objects as go
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import time
from anvil.js.window import speechSynthesis as synth


    
class Form1(Form1Template):
    
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        synth.getVoices()[0]
        # Any code you write here will run when the form opens.
    def say(self,text,voice = synth.getVoices()[0],volume = 100,rate = 100,pitch = 100):
        text = text.replace("`","")
        utr = anvil.js.window.SpeechSynthesisUtterance(text)
        utr.voice = voice
        utr.volume = volume
        utr.rate = rate
        utr.pitch = pitch
        synth.speak(utr)
    def read_question_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.say("hi")

