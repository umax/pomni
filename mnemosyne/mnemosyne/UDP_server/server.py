#
# server.py <Peter.Bienstman@UGent.be>
#

import sys
import select
import SocketServer

from mnemosyne.libmnemosyne import Mnemosyne


class MnemosyneThread(threading.Thread):

    def __init__(self, data_dir, filename):
        threading.Thread.__init__(self)
        self.data_dir = data_dir
        self.filename = filename

    def run(self):
        self.mnemosyne = Mnemosyne()
        self.mnemosyne.components.insert(0,
            ("mnemosyne.libmnemosyne.translator", "GetTextTranslator"))
        self.mnemosyne.components.append(\
            ("mnemosyne.UDP_server.UDP_main_window",
             "UDP_MainWindow"))
        self.mnemosyne.components.append(\
            ("mnemosyne.UDP_server.UDP_review_widget",
             "UDP_ReviewWidget"))
        self.mnemosyne.initialise(self.data_dir, self.filename,
            automatic_upgrades=False)
        # The next calls will be executed in the handler thread, so we release
        # the database connection
        self.mnemosyne.database().release_connection()


class MyHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        mnemosyne = self.server.mnemosyne
        # We use  the component manager to store some more global data there.
        mnemosyne.component_manager.socket = socket
        mnemosyne.component_manager.client_address = self.client_address
        if data != "exit()":
            exec(data)
        else:
            self.server.stopped = True
        socket.sendto("DONE\n", self.client_address)

        # Wait for buffer lock?
        
        socket.sendto(mnemosyne.main_widget().buffer, self.client_address)
        mnemosyne.main_widget().buffer = ""


class Server(SocketServer.UDPServer):

    def __init__(self, port):
        self.mnemosyne = Mnemosyne()
        self.mnemosyne.components.insert(0,
            ("mnemosyne.libmnemosyne.translator", "GetTextTranslator"))
        self.mnemosyne.components.append(\
            ("mnemosyne.UDP_server.UDP_main_window",
             "UDP_MainWindow"))
        self.mnemosyne.components.append(\
            ("mnemosyne.UDP_server.UDP_review_widget",
             "UDP_ReviewWidget"))    
        SocketServer.UDPServer.__init__(self, ("localhost", port), MyHandler)
        print "Server listening on port", port
        self.stopped = False
        while not self.stopped:
            # We time out every 0.25 seconds, so that we changing
            # self.stopped can have an effect.
            if select.select([self.socket], [], [], 0.25)[0]:
                self.handle_request()
        self.socket.close()

if __name__ == "__main__":
    port = int(sys.argv[1])
    server = Server(port)




