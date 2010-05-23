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
Hildon UI. Menu widget.
"""

import mnemosyne.maemo_ui.widgets.menu as widgets
import mnemosyne.maemo_ui.widgets.dialogs as dialogs
from mnemosyne.libmnemosyne.ui_component import UiComponent

class MenuWidget(UiComponent):
    """Main menu widget."""

    component_type = "menu_widget"

    def __init__(self, component_manager):
        UiComponent.__init__(self, component_manager)
        self._main_widget = self.main_widget()
        # create widgets
        self.window, buttons = widgets.create_menu_ui()
        # connect signals
        self.window.connect('delete_event', self.exit_cb)
        buttons['tags'].connect('clicked', self.tags_cb)
        buttons['review'].connect('clicked', self.review_cb)
        buttons['input'].connect('clicked', self.input_cb)
        buttons['gen_settings'].connect('clicked', self.gen_settings_cb)
        buttons['tts_settings'].connect('clicked', self.tts_settings_cb)
        buttons['import'].connect('clicked', self.importcards_cb)
        buttons['stats'].connect('clicked', self.statistics_cb)
        buttons['help'].connect('clicked', self.help_cb)
        buttons['about'].connect('clicked', self.about_cb)
        buttons['sync'].connect('clicked', self.sync_cb)

    def get_window(self):
        return self.window

    def activate(self):
        """Shows 'Menu' window."""

        self.window.show_all()


    # callbacks

    def tags_cb(self, widget):
        """Go to 'Tags' mode."""

        self._main_widget.tags_()

    def input_cb(self, widget):
        """Go to 'Input' mode."""

        self._main_widget.input_()

    def review_cb(self, widget):
        """Go to 'Review' mode."""

        self._main_widget.review_()

    def sync_cb(self, widget):
        """Go to 'Sync' mode."""

        #self._main_widget.sync_()
        dialogs.show_sync_dialog()

    def gen_settings_cb(self, widget):
        """Show 'General settings' dialog."""

        dialogs.show_general_settings_dialog(self.config())

    def tts_settings_cb(self, widget):
        """Show 'TTS settings' dialog."""

        dialogs.show_tts_settings_dialog(self.config())
        
    def statistics_cb(self, widget):
        """Go to 'Statistics' mode."""

        self._main_widget.statistics_()

    def importcards_cb(self, widget):
        """Go to 'Import' mode."""

        #self._main_widget.import_()
        dialogs.show_import_dialog( \
            self.component_manager.get_all('file_format'),
            self.component_manager.get_current('file_format'),
            self.database(), self.review_controller(),
            self._main_widget.error_box)

    def about_cb(self, widget):
        """Show 'About' dialog."""

        dialogs.show_about_dialog()
        
    def help_cb(self, widget):
        """Go to 'Help' mode."""

        self._main_widget.help_()

    def exit_cb(self, widget, event):
        """Exit program."""

        self._main_widget.exit_()


# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
