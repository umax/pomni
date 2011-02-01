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
Hildon UI. Help Widget.
"""

import os
import mnemosyne.maemo_ui.widgets.help as widgets
from mnemosyne.libmnemosyne.ui_component import UiComponent


class HelpWidget(UiComponent):
    """Help Widget."""

    def __init__(self, component_manager):
        UiComponent.__init__(self, component_manager)
        # create widgets
        self.window, self.help_html, pannable_area = widgets.create_help_ui()
        pannable_area.connect('panning-started', self.on_start_panning)
        pannable_area.connect('panning-finished', self.on_stop_panning)
        pannable_area.connect('horizontal-movement', self.on_hor_panning)
        self.render_chain().renderer_for_card_type(None).render_html( \
            self.help_html, open(os.path.join(self.config()['help_path'], \
            'help.html')).read())

    def activate(self):
        """Shows window."""

        self.window.show_all()

    def on_start_panning(self, widget):
        """Temporary disable widget to avoid text selection."""

        self.help_html.set_sensitive(False)

    def on_stop_panning(self, widget):
        """Temporary disable widget to avoid text selection."""

        self.help_html.set_sensitive(True)

    def on_hor_panning(self, widget, opt1, opt2, opt3):
        """Temporary disable widget to avoid text selection."""

        self.help_html.set_sensitive(False)
