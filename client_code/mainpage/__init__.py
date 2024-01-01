from ._anvil_designer import mainpageTemplate
from anvil import *
import anvil.server
import plotly.graph_objects as go
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import time
from anvil.js.window import speechSynthesis as synth
from anvil.js.window import alert, prompt, confirm
from anvil_extras.storage import indexed_db
import random
import time
from plotly import graph_objects as go

def clamp(num, minimum=0, maximum=200):
    return max(min(maximum, num), minimum)

def sa_choice(message):
    return prompt(message).upper()[0] == "Y"
    
class mainpage(mainpageTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        anvil.server.call('record_visitors')
        self.init_db(confirm("Would you like to resync the database?\nIf this is your first time hit OK"))

        self.sources = list(self.lookup.keys())
        self.all_categories = ["physics","general science","energy","earth and space","earth science","chemistry","biology","astronomy","math","computer science"]    
        self.subject_dropdown.items = [{"key": i, "value": i, "enabled": True} for i in self.all_categories]
        self.sources_dropdown.items = [{"key": i, "value": i, "enabled": True} for i in self.sources]
        self.sources_dropdown.selected = [i["key"] for i in self.sources_dropdown.items]
        self.subject_dropdown.selected = [i["key"] for i in self.subject_dropdown.items]
        self.voices = {i.name:i for i in synth.getVoices()}
        self.voices_dropdown.items = list(self.voices.keys())
        for i in self.voices_dropdown.items:
            if "english" in i.lower() and "online" in i.lower():
                self.voices_dropdown.selected_value = i
                break
        self.current_question = None
        self.next_question_click()
        self.last_time = time.time()
        self.tossups = 0
        self.bonuses = 0
        self.correct_tossups = 0
        self.correct_bonuses = 0
        self.tracked_tossups = {i:0 for i in self.all_categories}
        self.tracked_bonuses = {i:0 for i in self.all_categories}
        self.total_tossups = {i:0 for i in self.all_categories}
        self.total_bonuses = {i:0 for i in self.all_categories}
        self.tplot.layout.template = "material_dark"
        self.tplot.data = self.update_graphs()
        self.past_questions.items = []

    def update_graphs(self):
        return [go.Bar(x = list(self.tracked_tossups.keys()),y = list(self.tracked_tossups.values()),name = "Tossups"),
                go.Bar(x = list(self.tracked_bonuses.keys()),y = list(self.tracked_bonuses.values()),name = "Bonuses",)]
    def cleanup(foo):
        def inner(self,*args,**kwargs):
            # print("cleaning up with",args,kwargs)
            self.stop_reading_click()
            foo(self,*args,**kwargs)
            self.stop_reading_click()
            synth.resume()
        return inner
    def init_db(self,reset):
        ab_store = indexed_db.create_store('ask_bowl')
        if reset:
            self.pqs = anvil.server.call('get_questions_as_list')
            self.lookup = anvil.server.call("create_categories",self.pqs)                
            ab_store["pqs"] = self.pqs
            ab_store["lookup"] = self.lookup
        else:
            self.pqs = ab_store["pqs"]
            self.lookup = ab_store["lookup"] 
            
    def get_id(self, sources, categories):
        filtered_sources = [i for i in self.lookup.keys() if i in sources]
        # print(filtered_sources)
        good_indices = []
        for i in filtered_sources:
            for j in self.lookup[i]:
                if j in categories:
                    good_indices.extend(self.lookup[i][j])
        return good_indices
        
    def get_question(self,categories,sources):
        indices = self.get_id(sources,categories)
        # print(len(sources),len(self.sources))
        # print(len(categories),len(self.all_categories))
        # print("0",len(indices))
        if indices == []:
            indices = self.get_id(sources,self.all_categories)
        if indices == []:
            indices = self.get_id(self.sources,categories)
        if indices == []:
            indices = self.get_id(self.sources,self.all_categories)
        chosen_index = random.choice(indices)
        return self.pqs[chosen_index]
        
    def say(self,text,voice = None,volume = None,rate = None,pitch = None):
        text = text.replace("`","")
        if voice == None:
            voice = self.voices[self.voices_dropdown.selected_value]
        if volume == None:
            volume = int(self.volume.text)/100
        if rate == None:
            rate = int(self.rate.text)/10
        if pitch == None:
            pitch = int(self.pitch.text)/50
        # print(text)
        utr = anvil.js.window.SpeechSynthesisUtterance(text.strip())
        utr.voice = voice
        utr.volume = volume
        utr.rate = rate
        utr.pitch = pitch
        # print(utr.volume, volume,"\n", utr.rate, rate, "\n", utr.pitch, pitch)
        with Notification("Please wait until the question starts",title = "Reading this question",style = "success",timeout=1):
            synth.speak(utr)
    def load_new_question(self):
        return self.get_question(self.subject_dropdown.selected,self.sources_dropdown.selected)
    @cleanup
    def next_question_click(self, **event_args):
        """This method is called when the button is clicked"""
        if self.current_question is not None:
            self.past_questions.items = self.past_questions.items + [{"qtext":f"## {self.question_info.text}\n## {self.current_question['question']}\n## {self.current_question['answer']}","qlink":self.question_link.url}]
        # print(self.past_questions.items)
        self.current_question = self.load_new_question()
        self.question_box.content = ""
        self.answer_box.content = ""
        self.question_info.text = f"{self.current_question['uri'][-4:].replace('/','0')} - {self.current_question['source']} - {self.current_question['format']} - {self.current_question['type']} - {self.current_question['category']}"
        self.question_link.url = self.current_question['uri']

    # @cleanup
    def read_question_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.say(self.current_question["format"] + " " + self.current_question["category"] + " " + self.current_question["question"])
        self.last_time = time.time()
        
    # @cleanup
    def read_answer_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.say(self.current_question["answer"])
        
    @cleanup
    def show_question_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.question_box.content = f"""{self.current_question["question"]}"""
    @cleanup    
    def show_answer_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.answer_box.content = f"""{self.current_question["answer"]}"""
    
    def stop_reading_click(self, **event_args):
        """This method is called when the button is clicked"""
        synth.pause()
        synth.cancel()
        synth.resume()

    def pause_reading_click(self, **event_args):
        """This method is called when the button is clicked"""
        synth.pause()

    def play_reading_click(self, **event_args):
        """This method is called when the button is clicked"""
        synth.resume()

    def refresh_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.init_db(True)
        
    @cleanup
    def answerbox_pressed_enter(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        if self.answerbox.text[0] == "/":
            self.quickcode(self.answerbox.text.replace("/",""))
            return 0
        is_correct = False
        if self.current_question["format"][0].lower() == "s":
            is_correct = self.grade_sa(self.answerbox.text,self.current_question["answer"])
        else:
            is_correct = self.grade_mc(self.answerbox.text,self.current_question["answer"])
            correct_signifier = "correct" if is_correct else "incorrect"          
            text = f"Your answer ({self.answerbox.text}) is {correct_signifier}.\n The correct answer is {self.current_question['answer']}"
            alert(text)
        if self.current_question["type"] == "tossup":
            self.correct_tossups += int(is_correct);
            self.tossups += 1
            self.tracked_tossups[self.current_question["category"]] += int(is_correct)
            self.total_tossups[self.current_question["category"]] += 1
        if self.current_question["type"] == "bonus":
            self.correct_bonuses += int(is_correct);
            self.bonuses += 1
            self.tracked_bonuses[self.current_question["category"]] += int(is_correct)
            self.total_bonuses[self.current_question["category"]] += 1
        self.tossups_text.text = f"Tossups: {self.correct_tossups}/{self.tossups}"
        self.bonus_text.text = f"Bonuses: {self.correct_bonuses}/{self.bonuses}"
        self.tplot.data = self.update_graphs()
        self.answerbox.text = ""
        self.answerbox.focus()
    
    def quickcode(self,code):
        function_map = {
            "n":self.next_question_click,
            "r":self.read_question_click,
            "s":self.stop_reading_click,
            "p":self.pause_reading_click,
            "l":self.play_reading_click,
            "q":self.show_question_click,
            "a":self.show_answer_click,
        }
        function_map.get(code.lower(),self.read_question_click)()
        self.answerbox.text = ""
        
    def grade_mc(self, answer,correct):
        return answer[0].lower() == correct[0].lower()
    def grade_sa(self,answer,correct):
        return sa_choice(f"You answered {answer}\nThe correct answer is {correct}\nIf your answer is correct, type 'yes'")

















        








