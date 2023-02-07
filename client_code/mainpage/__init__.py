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
import random

def clamp(num, minimum=0, maximum=200):
    return max(min(maximum, num), minimum)

def mc_choice(message):
    return prompt(message).upper()[0] == "Y"
    
class mainpage(mainpageTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        reset = False
        ab_store = indexed_db.create_store('ask_bowl')
        if reset:
            self.pqs = anvil.server.call('get_questions_as_list')
            self.lookup = anvil.server.call("create_categories",self.pqs)
            ab_store["pqs"] = self.pqs
            ab_store["lookup"] = self.lookup
        else:
            self.pqs = ab_store["pqs"]
            self.lookup = ab_store["lookup"] 
        self.sources = list(self.lookup.keys())
        self.all_categories = ["physics","general science","energy","earth and space","earth science","chemistry","biology","astronomy","math","computer science"]    
        self.subject_dropdown.items = [{"key": i, "value": i, "enabled": True} for i in self.all_categories]
        self.sources_dropdown.items = [{"key": i, "value": i, "enabled": True} for i in self.sources]
        self.sources_dropdown.selected = [i["key"] for i in self.sources_dropdown.items]
        self.subject_dropdown.selected = [i["key"] for i in self.subject_dropdown.items]
        self.voices = {i.name:i for i in synth.getVoices()}
        self.voices_dropdown.items = list(self.voices.keys())
        self.current_question = self.load_new_question()
        
    def get_id(self, sources, categories):
        filtered_sources = [i for i in self.lookup.keys() if i in sources]
        good_indices = []
        for i in filtered_sources:
            for j in self.lookup[i]:
                if j in categories:
                    good_indices.extend(self.lookup[i][j])
        return good_indices
        
    def get_question(self,sources,categories):
        indices = self.get_id(sources,categories)
        if indices == []:
            indices = self.get_id(sources,self.all_categories)
        if indices == []:
            indices = self.get_id(self.sources,categories)
        if indices == []:
            indices = self.get_id(self.sources,self.all_categories)
        chosen_index = random.choice(indices)
        print(chosen_index)
        return self.pqs[chosen_index]
        
    def say(self,text,voice = None,volume = 100,rate = 100,pitch = 100):
        text = text.replace("`","")
        if voice == None:
            voice = self.voices[self.voices_dropdown.selected_value]
        utr = anvil.js.window.SpeechSynthesisUtterance(text)
        utr.voice = voice
        utr.volume = volume
        utr.rate = rate
        utr.pitch = pitch
        synth.speak(utr)
    def load_new_question(self):
        return self.get_question([i["key"] for i in self.subject_dropdown.items],[i["key"] for i in self.sources_dropdown.items])
    def next_question_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.current_question = self.load_new_question()

    def read_question_click(self, **event_args):
        """This method is called when the button is clicked"""
        say(self.current_question["question"])

    def read_answer_click(self, **event_args):
        """This method is called when the button is clicked"""
        say(self.current_question["answer"])

    def show_question_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.question_box.content = f"""
        # Question:
        **{self.current_question["question"]}**
        """
    def show_answer_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.question_box.content = f"""
        # Answer:
        **{self.current_question["Answer"]}**
        """












        








