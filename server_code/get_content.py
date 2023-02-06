import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import random
# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
link="https://scibowldb.com/api/questions"

@anvil.server.background_task
def get_questions_as_list():
    raw_questions = anvil.http.request(link,json = True,method = "GET")["questions"]
    processed_questions = []
    for strq in raw_questions:
        del strq["id"]
        del strq["search_vector"]
        del strq["api_url"]
        ctossup = {
                "uri":strq["uri"],
                "answer":strq["bonus_answer"],
                "format":strq["bonus_format"],
                "question":strq["bonus_question"],
                "category": strq["category"].lower(),
                "source":strq["source"].lower(),
                "type":"bonus"
            }
        cbonus = {
                "uri":strq["uri"],
                "answer":strq["tossup_answer"],
                "format":strq["tossup_format"],
                "question":strq["tossup_question"],
                "category": strq["category"].lower(),
                "source": strq["source"].split("-")[0],
                "type":"tossup"
            }
        processed_questions.append(ctossup)
        processed_questions.append(cbonus)
    print(len(processed_questions))
    return processed_questions

@anvil.server.callable
def create_categories():
    pqs = get_questions_as_list()
    categories = {}
    for i,v in enumerate(pqs):
        if categories.get(v["source"],False) == False:
            categories[v["source"]] = {}
        if categories[v["source"]].get(v["category"],False) == False:
            categories[v["source"]][v["category"]] = []
            # print("creating source: ",v["source"]," for category: ",v["category"])  
        categories[v["source"]][v["category"]].append(i)
    return pqs, categories
        