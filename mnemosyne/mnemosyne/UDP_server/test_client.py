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


# Simple example of loading an existing database and doing a review.
if __name__ == "__main__":
    import subprocess
    subprocess.Popen(["./bin/python", "./mnemosyne/UDP_server/server.py",
        str(PORT)])

    import os
    data_dir = os.path.abspath("dot_mnemosyne2")
    filename = "default.db"

    c = Client()
    c.send_command("mnemosyne.initialise(data_dir=\"%s\", filename=\"%s\")" \
        % (data_dir, filename))
    c.send_command("mnemosyne.start_review()")
    c.send_command("mnemosyne.review_controller().show_answer()")
    c.send_command("mnemosyne.review_controller().grade_answer(0)")
    c.send_command("mnemosyne.finalise()")
    c.send_command("exit()")

# This results in the following exchange:

#>># Waiting for server...
#Server listening on port 6666
#>># Waiting for server...
#>>mnemosyne.initialise(
# data_dir="/home/pbienst/source/mnemosyne-proj-pbienst/mnemosyne/dot_mnemosyne2",
# filename="default.db")
#@@main_widget.set_window_title("""Mnemosyne""")
#>>mnemosyne.start_review()
#@@review_widget.set_question_box_visible("""True""")
#@@review_widget.set_question_label("""Question: my tag""")
#@@review_widget.set_question("""
#...html...
#""")
#@@review_widget.clear_answer()
#@@review_widget.update_show_button("""Show answer""","""True""","""True""")
#@@review_widget.set_grades_enabled("""False""")
#@@review_widget.update_status_bar()
#@@main_widget.enable_edit_current_card("""True""")
#@@main_widget.enable_delete_current_card("""True""")
#@@main_widget.enable_browse_cards("""True""")
#>>mnemosyne.review_controller().show_answer()
#@@review_widget.set_answer_box_visible("""True""")
#@@review_widget.set_question_label("""Question: my tag""")
#@@review_widget.set_answer("""
#...html...
#""")
#@@review_widget.update_show_button("""Show answer""","""True""","""False""")
#@@review_widget.set_grades_enabled("""True""")
#@@review_widget.set_default_grade("""4""")
#@@review_widget.update_status_bar()
#@@main_widget.enable_edit_current_card("""True""")
#@@main_widget.enable_delete_current_card("""True""")
#@@main_widget.enable_browse_cards("""True""")
#>>mnemosyne.review_controller().grade_answer(0)
#@@review_widget.set_question_box_visible("""True""")
#@@review_widget.set_question_label("""Question: my tag""")
#@@review_widget.set_question("""
#...html...
#""")
#@@review_widget.clear_answer()
#@@review_widget.update_show_button("""Show answer""","""True""","""True""")
#@@review_widget.set_grades_enabled("""False""")
#@@review_widget.update_status_bar()
#@@main_widget.enable_edit_current_card("""True""")
#@@main_widget.enable_delete_current_card("""True""")
#@@main_widget.enable_browse_cards("""True""")
#>>mnemosyne.finalise()
#>>exit()
