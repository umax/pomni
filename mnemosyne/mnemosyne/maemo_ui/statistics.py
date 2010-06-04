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
import gettext
import mnemosyne.maemo_ui.widgets.statistics as widgets
from mnemosyne.libmnemosyne.ui_components.dialogs import StatisticsDialog

_ = gettext.gettext

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
        self.window, self.current_button, self.common_button, self.tags_button,\
            self.html_widget, self.html_container, self.info_label = \
                widgets.create_statistics_ui()
        # connect signals
        self.window.connect('destroy', self.back_to_previous_mode_cb)
        self.current_button.connect('clicked', self.current_card_statistics_cb)
        self.common_button.connect('clicked', self.common_statistics_cb)
        self.tags_button.connect('clicked', self.tags_statistics_cb)

    def activate(self):
        """Set necessary switcher page."""

        # change current statistics page
        try:
            last_page = self.config()['last_variant_for_statistics_page']
        except KeyError:
            last_page = 2

        if last_page == 0:
            self.tags_button.set_active(True)
            self.tags_statistics_cb(None)
        elif last_page == 1:
            self.common_button.set_active(True)
            self.common_statistics_cb(None)
        else:
            self.current_button.set_active(True)
            self.current_card_statistics_cb(None)


    # callbacks

    def current_card_statistics_cb(self, widget):
        """Switches to the current card statistics page."""

        self.window.set_title(_('Current card statistics'))
        self.html_container.hide()
        self.info_label.hide()
        card = self.review_controller().card
        if not card:
            self.info_label.set_text(_('There is no current card'))
            self.info_label.show()
        elif card.grade == -1:
            self.info_label.set_text(_('Unseen card, no statistics available'))
            self.info_label.show()
        else:
            self.html_container.show()
            html = self.html
            html += "<tr><td><br><br>" + _('Grade') + ": %d</td></tr>" % \
                card.grade
            html += "<tr><td>" + _('Easiness') + ": %1.2f</td></tr>" % \
                card.easiness
            html += "<tr><td>" + _('Repetitions') + ": %d</td></tr>" % \
                (card.acq_reps + card.ret_reps)
            html += "<tr><td>" + _('Lapses') + ": %d</td></tr>" % card.lapses
            html += "<tr><td>" + _('Interval') + ": %d</td></tr>" % \
                (card.interval / DAY)
            html += "<tr><td>" + _('Last repetition') + ": %s</td></tr>" \
                % time.strftime("%B %d, %Y", time.gmtime(card.last_rep))
            html += "<tr><td>" + _('Next repetition') + ": %s</td></tr>" \
                % time.strftime("%B %d, %Y", time.gmtime(card.next_rep))
            html += "<tr><td>" + _('Average thinking time (secs)') + ": %d" \
                "</td></tr>" % self.database().average_thinking_time(card)
            html += "<tr><td>" + _('Total thinking time (secs)') + ": %d</td>" \
                "</tr>" % self.database().total_thinking_time(card)
            html += "</table><br><br></body></html>"
            html = self.renderer.change_font_size(html)
            self.renderer.render_html(self.html_widget, html)

    def common_statistics_cb(self, widget):
        """Switches to the common card statistics page."""

        self.window.set_title(_('All cards statistics'))
        self.html_container.show()
        self.info_label.hide()
        database = self.database()
        html = self.html
        html += "<tr><td><br><br>" + _('Total cards') + ": %d<br><br><br>" \
            "</td></tr>" % sum([database.total_card_count_for__tag_id(tag._id) \
                for tag in database.get_tags()])
        html += "<tr><td><b>" + _('Grade statistics for all cards') + "</b>" \
            "</td></tr>"
        for grade in range(-1, 6):
            html += "<tr><td>" + _('Grade') + " %2i: %i cards</td></tr>" % \
                (grade, self.database().total_card_count_for_grade(grade))
        html += "</table><br><br></body></html>"
        html = self.renderer.change_font_size(html)
        self.renderer.render_html(self.html_widget, html)

    def tags_statistics_cb(self, widget):
        """Switches to the tags statistics page."""

        self.window.set_title(_('Tags statistics'))
        self.html_container.hide()
        self.info_label.hide()
        tags = [(_id, name) for (_id, name) in \
            self.database().get_tags__id_and_name()]
        if not tags:
            self.info_label.set_text(_('There are no tags'))
            self.info_label.show()
        else:
            self.html_container.show()
            html = self.html
            for _id, name in tags:
                html += "<tr><td><br><br>" + _('Tag') + " <b>%s</b></td></tr>" \
                    % name.replace('<', '&lt;').replace('>', '&gt;')
                for grade in range(-1, 6):
                    html += "<tr><td>" + _('Grade') + " %2i: %i cards</td>" \
                        "</tr>" % (grade, self.database(). \
                        total_card_count_for_grade_and__tag_id(grade, _id))
            html += "</table><br><br></body></html>"
            html = self.renderer.change_font_size(html)
            self.renderer.render_html(self.html_widget, html)

    def back_to_previous_mode_cb(self, widget):
        """Returns to previous mode."""

        for radio_button in self.current_button.get_group():
            if radio_button.get_active():
                self.config()["last_variant_for_statistics_page"] = \
                    radio_button.get_group().index(radio_button)
                break
        self.main_widget().widgets['statistics'] = None
        del self.main_widget().widgets['statistics']
