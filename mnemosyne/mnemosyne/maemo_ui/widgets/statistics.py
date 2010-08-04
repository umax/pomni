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

import gtk
import hildon
from gettext import gettext as _
from mnemosyne.maemo_ui.widgets.common import create_gtkhtml


def create_statistics_ui():
    """Creates MaemoStatisticsWidget UI."""

    window = hildon.StackableWindow()
    window.set_title(_('Statistics'))

    menu = hildon.AppMenu()

    # create widgets for current card statistics
    current_stats_filter = gtk.RadioButton(None, _('Current'))
    current_stats_filter.set_mode(False)
    menu.add_filter(current_stats_filter)

    # create widgets for all card statistics
    all_stats_filter = gtk.RadioButton(current_stats_filter, _('All'))
    all_stats_filter.set_mode(False)
    menu.add_filter(all_stats_filter)

    # create widgets for tags statistics
    tags_stats_filter = gtk.RadioButton(current_stats_filter, _('Tags'))
    tags_stats_filter.set_mode(False)
    menu.add_filter(tags_stats_filter)

    widgets_box = gtk.VBox()
    html_widget = create_gtkhtml()
    html_widget.set_sensitive(False)
    pannable_area = hildon.PannableArea()
    pannable_area.set_property('vovershoot-max', 0)
    pannable_area.add(html_widget)
    label = gtk.Label()
    label.set_justify(gtk.JUSTIFY_CENTER)

    widgets_box.pack_start(label, expand=True, fill=False)
    widgets_box.pack_start(pannable_area)

    window.set_app_menu(menu)
    window.add(widgets_box)
    menu.show_all()
    window.show_all()

    return window, current_stats_filter, all_stats_filter, tags_stats_filter, \
        html_widget, pannable_area, label
