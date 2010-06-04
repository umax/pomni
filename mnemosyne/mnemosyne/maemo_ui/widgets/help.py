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
Hildon UI. Widgets for Help mode.
"""

import hildon
import gettext
import mnemosyne.maemo_ui.widgets.common as widgets

_ = gettext.gettext


def create_help_ui():
    """Creates HelpWidget UI."""

    window = hildon.StackableWindow()
    window.set_title(_('Help'))
    html_widget = widgets.create_gtkhtml()
    pannable_area = hildon.PannableArea()
    pannable_area.set_property('panning-threshold', 4)
    pannable_area.add(html_widget)
    window.add(pannable_area)

    return window, html_widget, pannable_area
