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
import mnemosyne.maemo_ui.widgets.statistics as widgets

DAY = 24 * 60 * 60 # Seconds in a day.

class MaemoStatisticsWidget(StatisticsDialog):
    """Statistics Widget."""

    def __init__(self, component_manager, mode=None):
        StatisticsDialog.__init__(self, component_manager)
        self.renderer = self.component_manager.get_current('renderer')
        self.statistics_page = None
        self.html = '<html><head><meta http-equiv="Content-Type" content='\
        '"text/html;charset=UTF-8"><style type="text/css">*{font-size:28px;'\
        'font-family:Nokia Sans} table {height:100%;margin-left:auto;margin-'\
        'right:auto;text-align:center} body{ background-color:black;margin:0;'\
        'padding:0;}</style></head><body><table>'
        # create widgets
        self.window, self.current_stats_button, self.common_stats_button, \
            self.tags_stats_button, self.html_widget = \
                widgets.create_statistics_ui()
        # connect signals
        self.window.connect('destroy', self.back_to_previous_mode_cb)
        self.current_stats_button.connect('clicked', \
            self.current_card_statistics_cb)
        self.common_stats_button.connect('clicked', self.common_statistics_cb)
        self.tags_stats_button.connect('clicked', self.tags_statistics_cb)

    def activate(self):
        """Set necessary switcher page."""

        # change current statistics page
        try:
            self.statistics_page = \
                self.config()["last_variant_for_statistics_page"] 
        except KeyError:
            self.statistics_page = 2

        if self.statistics_page == 0:
            self.current_stats_button.set_active(True)
            self.current_card_statistics_cb(None)
        elif self.statistics_page == 1:
            self.common_stats_button.set_active(True)
            self.common_statistics_cb(None) 
        else:
            self.tags_stats_button.set_active(True)
            self.tags_statistics_cb(None)
 

    # callbacks

    def current_card_statistics_cb(self, widget):
        """Switches to the current card statistics page."""

        self.statistics_page = 0
        card = self.review_controller().card
        html = self.html
        if not card:
            html += "<tr><td><b>No current card</b></td></tr>"
        elif card.grade == -1:
            html += "<tr><td><b>Unseen card, no statistics available " \
                "yet</b></td></tr>"
        else:
            html += "<tr><td><b>Current card statistics<br><br></b></td></tr>"
            html += "<tr><td>Grade" + ": %d</td></tr>" % card.grade
            html += "<tr><td>Easiness" + ": %1.2f</td></tr>" % card.easiness
            html += "<tr><td>Repetitions" + ": %d</td></tr>" % \
                (card.acq_reps + card.ret_reps)
            html += "<tr><td>Lapses" + ": %d</td></tr>" % card.lapses
            html += "<tr><td>Interval" + ": %d</td></tr>" % \
                (card.interval / DAY)
            html += "<tr><td>Last repetition" + ": %s</td></tr>" \
                % time.strftime("%B %d, %Y", time.gmtime(card.last_rep))
            html += "<tr><td>Next repetition" + ": %s</td></tr>" \
                % time.strftime("%B %d, %Y", time.gmtime(card.next_rep))
            html += "<tr><td>Average thinking time (secs): %d</td></tr>"\
                % self.database().average_thinking_time(card)
            html += "<tr><td>Total thinking time (secs): %d</td></tr>" \
                % self.database().total_thinking_time(card)
        html += "</table></body></html>"
        html = self.renderer.change_font_size(html)
        self.renderer.render_html(self.html_widget, html)

    def common_statistics_cb(self, widget):
        """Switches to the common card statistics page."""

        self.statistics_page = 1
        html = self.html
        html += "<tr><td><b>Total cards statistics</b></td></tr>"
        database = self.database()
        html += "<tr><td>Total cards: %d<br><br><br></td></tr>" % \
            sum([database.total_card_count_for__tag_id(tag._id) \
                for tag in database.get_tags()])
        html += "<tr><td><b>Grade statistics for all cards</b></td></tr>"
        for grade in range(-1, 6):
            html += "<tr><td>Grade %2i: %i cards</td></tr>" % \
                (grade, self.database().total_card_count_for_grade(grade))
        html += "</table></body></html>"
        html = self.renderer.change_font_size(html)
        self.renderer.render_html(self.html_widget, html)
        
    def tags_statistics_cb(self, widget):
        """Switches to the tags statistics page."""

        self.statistics_page = 2
        html = self.html
        html += "<tr><td><b>Tags statistics<br></b></td></tr>"
        for _id, name in self.database().get_tags__id_and_name():
            html += "<tr><td><br><br>Tag <b>%s</b></td></tr>" % \
                name.replace('<', '&lt;').replace('>', '&gt;')
            for grade in range(-1, 6):
                html += "<tr><td>Grade %2i: %i cards</td></tr>" % (grade, \
                self.database().total_card_count_for_grade_and__tag_id(\
                    grade, _id))
        html += "</table></body></html>"
        html = self.renderer.change_font_size(html)
        self.renderer.render_html(self.html_widget, html)

    def back_to_previous_mode_cb(self, widget):
        """Returns to previous mode."""

        self.config()["last_variant_for_statistics_page"] = \
            self.statistics_page 
        # FIXME: looks bad
        self.main_widget().widgets['statistics'] = None
        del self.main_widget().widgets['statistics']

