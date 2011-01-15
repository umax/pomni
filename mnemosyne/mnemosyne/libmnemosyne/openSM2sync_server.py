#
# openSM2sync_server.py <Peter.Bienstman@UGent.be>
#

import os
import mnemosyne.version

from openSM2sync.server import Server
from mnemosyne.libmnemosyne.utils import expand_path
from mnemosyne.libmnemosyne.component import Component


class OpenSM2SyncServer(Component, Server):

    """These are the libmnemosyne-specific parts of the openSH2sync server.
    Code to run the server in a separate thread is not provide here, as this
    is best done at the GUI level in view of the interaction between multiple
    threads and the GUI event loop.

    """

    program_name = "Mnemosyne"
    program_version = mnemosyne.version.version

    def __init__(self, component_manager, ui):
        Component.__init__(self, component_manager)
        Server.__init__(self, self.config().machine_id(),
            self.config()["sync_server_port"], ui)
    
    def authorise(self, username, password):
        return username == self.config()["sync_server_username"] and \
               password == self.config()["sync_server_password"]
    
    def open_database(self, database_name):
        self.old_database = self.config()["path"]      
        if self.old_database != database_name:
            if not os.path.exists(expand_path(database_name,
                self.config().basedir)):
                self.database().new(database_name)
            else:
                self.database().load(database_name)
        return self.database()

    def after_sync(self):
        self.reload_database_after_sync()
        self.redraw_after_sync()

    def reload_database_after_sync(self):
        # If we are closing down the program, and there are still dangling
        # sessions in the server, we cannot continue.
        if not self.database():
            return
        self.database().load(self.old_database)
        self.log().loaded_database()

    def redraw_after_sync(self):
        # Note that the following functions also update the GUI, so depending
        # on the GUI toolkit, they could also best happen in the main thread.
        if self.review_controller():
            self.review_controller().reset_but_try_to_keep_current_card()
            self.review_controller().update_status_bar()
        