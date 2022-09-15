from ._anvil_designer import Form1Template
from anvil import *
import plotly.graph_objects as go
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import time
class Form1(Form1Template):

    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        print("1")
        time.sleep(5)
        print("2")
        self.init_components(**properties)
        print(3)
        time.sleep(5)
        print(4)
#     alert(title="hello")
#     Notification(timeout=None, title="hello").show()

        # Any code you write here will run when the form opens.
