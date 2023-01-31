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
def store_to_local_storage():
    try:
        content = anvil.server.call("get_questions_as_dict")
    except Exception as e:
        import json

        content = (
            json.loads(
                str(
                    anvil.server.call("get_questions_as_str")
                    .get_bytes()
                    .decode("utf-8")
                )
            )
        )
        print(content)

    try:
        local_storage["questions"] = content
    except:
        pass
    return content


def get_questions_as_dict():
    if anvil.server.is_app_online():
        if (
            local_storage.get("questions") is None
            or (
                local_storage.get("questions") is not None
                and anvil.server.call_s("get_num_questions")
                > len(local_storage["questions"])
            )
            or randint(0, 20) > 18
        ):
            return store_to_local_storage()
    return local_storage["questions"]


def clamp(num, minimum=0, maximum=200):
    return max(min(maximum, num), minimum)

def mc_choice(message):
    return prompt(message).upper()[0] == "Y"
    
class mainpage(mainpageTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        content = store_to_local_storage()
        # Any code you write here will run when the form opens.
        # print(mc_choice("unga kabunga"))
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








