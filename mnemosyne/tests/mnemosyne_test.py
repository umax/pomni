#
# mnemosyne_test.py <Peter.Bienstman@UGent.be>
#

import os

from mnemosyne.libmnemosyne import Mnemosyne

class MnemosyneTest():
    
    def setup(self):
        os.system("rm -fr dot_test")
        self.restart()

    def restart(self):
        self.mnemosyne = Mnemosyne()
        self.mnemosyne.components.insert(0, ("mnemosyne.libmnemosyne.translator",
                             "GetTextTranslator"))
        self.mnemosyne.components.append(\
            ("mnemosyne.libmnemosyne.ui_components.main_widget", "MainWidget"))
        self.mnemosyne.components.append(\
            ("mnemosyne.libmnemosyne.ui_components.review_widget", "ReviewWidget"))
        self.mnemosyne.components.append(\
            ("mnemosyne.libmnemosyne.ui_components.dialogs", "ProgressDialog"))
        self.mnemosyne.initialise(os.path.abspath("dot_test"))
        self.review_controller().reset()

    def teardown(self):
        self.mnemosyne.finalise()

    def config(self):
        return self.mnemosyne.component_manager.get_current("config")

    def log(self):
        return self.mnemosyne.component_manager.get_current("log")

    def database(self):
        return self.mnemosyne.component_manager.get_current("database")

    def scheduler(self):
        return self.mnemosyne.component_manager.get_current("scheduler")

    def main_widget(self):
        return self.mnemosyne.component_manager.get_current("main_widget")

    def review_widget(self):
        return self.mnemosyne.component_manager.get_current("review_widget")

    def controller(self):
        return self.mnemosyne.component_manager.get_current("controller")

    def review_controller(self):
        return self.mnemosyne.component_manager.get_current("review_controller")

    def card_types(self):
        return self.mnemosyne.component_manager.get_all("card_type")

    def filters(self):
        return self.mnemosyne.component_manager.get_all("filter")

    def plugins(self):
        return self.mnemosyne.component_manager.get_all("plugin")

    def card_type_by_id(self, id): 
        return self.mnemosyne.component_manager.card_type_by_id[id]

        
