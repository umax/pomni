#
# test_client.py <Peter.Bienstman@UGent.be>
#

PORT = 6666

import time
import socket

class Client(object):

    """Very simple client illustrating the basic structure of a UDP frontend.
    Also consult 'How to write a new frontend' in the docs of libmnemosyne
    for more information about the interaction between libmnemosyne and a
    frontend.

    """

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.connect(("localhost", PORT))
        connected = False
        while not connected:
            try:
                self.send_command("# Waiting for server...")
                connected = True
            except:
                time.sleep(0.1)

    def send_command(self, command):
        self.socket.send(command)
        f = self.socket.makefile("rb")
        line = f.readline()
        while line != "DONE\n":
            print line
            # If it's a callback command, we need to act upon it immediately,
            # either because the other side is waiting for input from us, or
            # for efficiency reasons, e.g. if the controller says it's already
            # OK to update a widget, best to do it now and not wait for the
            # entire command to finish.
            if line.startswith("@@"):
                # Example of callback which requires user input to be sent
                # immediately back to the server:
                if "main_widget.save_file_dialog" in line:
                    # Normally, we should ask the user which path he chooses,
                    # but here we hardcode an answer.
                    self.send_answer("/home/pbienst/.mnemosyne2/default.db")
                # Handle all the other callbacks:
                # ...
            # Simplistic error handling: just print out traceback, which runs
            # until the final "__DONE__".
            elif line.startswith("__EXCEPTION__"):
                traceback_lines = []
                traceback_lines.append(f.readline())
                while traceback_lines[-1] != "__DONE__\n":
                    traceback_lines.append(f.readline())
                print "".join(traceback_lines[:-1])
                break
            # Read the next line and act on that.
            line = f.readline()

    def send_answer(self, data):
        self.socket.send(str(data) + "\n")


c = Client()
c.send_command("mnemosyne.initialise(data_dir=\"%s\", filename=\"%s\")" % (data_dir, filename))
c.send_command("mnemosyne.start_review()")
c.send_command("mnemosyne.review_controller().show_answer()")
c.send_command("mnemosyne.review_controller().grade_answer(0)")
c.send_command("mnemosyne.finalise()")

c.send_command("mnemosyne.main_widget().show_question(\"a\", \"1\", \"2\", \"3\")")
c.send_command("1/0")

c.send_command("exit()")
