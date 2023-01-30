import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


link="https://askbowl3backend.anvil.app/_/api/return_table"

@anvil.server.callable
def get_questions_as_dict_background():
    anvil.server.launch_background_task('get_questions_as_dict')
    
@anvil.server.background_task
def update_server():
    anvil.http.request("https://askbowl3backend.anvil.app/_/api/update")
    
@anvil.server.callable
@anvil.server.background_task
def get_questions_as_dict():
    return anvil.http.request(link,method = "GET",json= True)["questions"]
    
    
@anvil.server.callable
def get_questions_as_str():
    return anvil.http.request(link,method = "GET")

@anvil.server.callable
def get_num_questions():
    anvil.server.launch_background_task('update_server')
    return int(anvil.http.request("https://askbowl3backend.anvil.app/_/api/number_of_questions").get_bytes())

@anvil.server.callable
def record_visitors():
    anvil.server.launch_background_task('b_record_visitors')
    
@anvil.server.background_task
def b_record_visitors():
    anvil.http.request("https://askbowl3backend.anvil.app/_/api/record_visitors")