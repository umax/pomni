#!/usr/bin/python -tt
# vim: sw=4 ts=4 expandtab ai
#
# Mnemosyne. Learning tool based on spaced repetition technique
#
# Copyright (C) 2008 Pomni Development Team <pomni@googlegroups.com>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301 USA
#

"""
Hildon UI. Statistics widget.
"""

import time
from mnemosyne.libmnemosyne.ui_components.dialogs import StatisticsDialog
from mnemosyne.maemo_ui.widgets.statistics import create_statistics_ui

DAY = 24 * 60 * 60 # Seconds in a day.

class MaemoStatisticsWidget(StatisticsDialog):
    """Statistics Widget."""

    def __init__(self, component_manager, previous_mode=None):
        self.current_card_text = ""
        self.common_text = ""
        StatisticsDialog.__init__(self, component_manager)
        self.prepare_statistics()
        # create widgets
        self.page, self.mode_statistics_switcher, menu_button, \
            current_card_button, common_button = \
            create_statistics_ui(self.main_widget().switcher, \
            self.current_card_text, self.common_text)
        # connect signals
        if previous_mode == 'Menu':
            menu_button.connect('clicked', self.back_to_main_menu_cb)
        else:
            menu_button.connect('clicked', self.back_to_previous_mode_cb)

        current_card_button.connect('released', \
            self.current_card_statistics_cb)
        common_button.connect('released', \
            self.common_statistics_cb)


    def prepare_statistics(self):
        """Preparing statistics text"""

        card = self.review_controller().card
        self.current_card_text = """<span  foreground='white'\
        size="x-large">"""
        if not card:
            self.current_card_text += "No current card."
        elif card.grade == -1:
            self.current_card_text += \
                "Unseen card, no statistics available yet."
        else:
            self.current_card_text += "Grade" + ": %d\n" % card.grade
            self.current_card_text += "Easiness" + ": %1.2f\n" % card.easiness
            self.current_card_text += "Repetitions" + ": %d\n" \
                % (card.acq_reps + card.ret_reps)
            self.current_card_text += "Lapses" + ": %d\n" % card.lapses
            self.current_card_text += "Interval" + ": %d\n" \
                % (card.interval / DAY)
            self.current_card_text += "Last repetition" + ": %s\n" \
                % time.strftime("%B %d, %Y", time.gmtime(card.last_rep))
            self.current_card_text += "Next repetition" + ": %s\n" \
                % time.strftime("%B %d, %Y", time.gmtime(card.next_rep))
            self.current_card_text += \
                "Average thinking time (secs)" + ": %d\n" \
                % self.database().average_thinking_time(card)
            self.current_card_text += "Total thinking time (secs)" + ": %d\n" \
                % self.database().total_thinking_time(card)
        self.current_card_text += "</span>"
        self.common_text = """<span  foreground='white'\
        size="x-large">"""
        grades = range(-1, 6)
        self.common_text += "\n".join([ "Grade  %2i -  %i" % \
                 (grade, self.database().card_count_for_grade\
                            (grade)) for grade in grades])
        self.common_text += "</span>"


    def activate(self):
        """Set necessary switcher page."""

        self.main_widget().switcher.set_current_page(self.page)

    def back_to_previous_mode_cb(self, widget):
        """Returns to previous menu."""

        self.main_widget().switcher.remove_page(self.page)

    def back_to_main_menu_cb(self, widget):
        """Returns to main menu."""

        self.main_widget().switcher.remove_page(self.page)
        self.main_widget().menu_('statistics')

    # callbacks
    def current_card_statistics_cb(self, widget):
        """Switches to the current card statistics page."""

        self.mode_statistics_switcher.set_current_page(0)

    def common_statistics_cb(self, widget):
        """Switches to the current card statistics page."""

        self.mode_statistics_switcher.set_current_page(1)

