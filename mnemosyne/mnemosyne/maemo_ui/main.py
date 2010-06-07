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
Main Widget.
"""

import gtk
import gettext
import mnemosyne.maemo_ui.widgets.main as widgets
from mnemosyne.libmnemosyne.ui_components.main_widget import MainWidget

_ = gettext.gettext

class MainWdgt(MainWidget):
    """Main widget class."""

    def __init__(self, component_manager):
        MainWidget.__init__(self, component_manager)
        self.review_window = None
        self.widgets = {}
        self._soundplayer = None

    @property
    def soundplayer(self):
        if not self._soundplayer:
            from mnemosyne.maemo_ui.sound import SoundPlayer
            self._soundplayer = SoundPlayer(self.error_box)
        return self._soundplayer

    def activate(self):
        """Activates Main widget."""

        pass

    def activate_mode(self, mode):
        """Activate mode in lazy way."""

        widget = self.create_mode(mode)
        widget.activate()

    def create_mode(self, mode):
        """Create widget object for selected mode."""

        widget = self.widgets.get(mode, None)
        if not widget: # lazy widget creation
            if mode == 'review':
                self.review_controller().reset()
                widget = self.review_controller().widget
            elif mode == 'menu':
                from mnemosyne.maemo_ui.menu import MenuWidget
                widget = MenuWidget(self.component_manager)
            elif mode == 'help':
                from mnemosyne.maemo_ui.help import HelpWidget
                widget = HelpWidget(self.component_manager)
            elif mode == 'tags':
                from mnemosyne.maemo_ui.tags import TagsWidget
                widget = TagsWidget(self.component_manager)
            elif mode == 'statistics':
                from mnemosyne.maemo_ui.statistics import MaemoStatisticsWidget
                widget = MaemoStatisticsWidget(self.component_manager)

            self.widgets[mode] = widget
        return widget

    def start(self, mode):
        """UI entry point. Activates specified mode."""

        if not mode:
            self.menu_()
            if self.config()['startup_with_review']:
                self.review_()
        gtk.main()


    # modes
    def menu_(self, mode=None):
        """Activates 'Menu' mode."""

        if mode is not None:
            del self.widgets[mode]
        if self.review_window is not None:
            self.review_window.hide()
        self.activate_mode('menu')

    def tags_(self):
        """Activates 'Tags' mode."""

        if 'review' not in self.widgets:
            self.create_mode('review')
        self.component_manager.get_current('activate_cards_dialog') \
            (self.component_manager).activate()

    def input_(self):
        """Activates 'Input' mode."""

        if 'review' not in self.widgets:
            self.create_mode('review')
        self.component_manager.get_current('add_cards_dialog') \
            (self.component_manager).activate()

    def review_(self):
        """Activates 'Review' mode."""

        self.activate_mode('review')

    def statistics_(self):
        """Activates 'Statistics' mode."""

        self.activate_mode('statistics')

    def help_(self):
        """Activates 'Help' mode."""

        self.activate_mode('help')

    @staticmethod
    def exit_(window=None, event=None):
        """Exit from main gtk loop."""

        gtk.main_quit()


    # Main Widget API
    def information_box(self, message):
        """Show Information message."""

        widgets.create_information_dialog(self.review_window, message)

    def error_box(self, message):
        """Error message."""

        widgets.create_information_dialog(self.review_window, message,  \
            title=_('Error'))

    def question_box(self, question, option0, option1, option2):
        """Show Question message."""

        return widgets.create_question_dialog(self.review_window, question)



# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
