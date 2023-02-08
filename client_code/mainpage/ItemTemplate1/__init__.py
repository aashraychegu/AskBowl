from ._anvil_designer import ItemTemplate1Template
from anvil import *
import anvil.server

class ItemTemplate1(ItemTemplate1Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.qtext.content = self.item["qtext"]
        self.qlink.text = "Click here to research this question more"
        self.qlink.url = self.item["qlink"]
        # Any code you write here will run before the form opens.
