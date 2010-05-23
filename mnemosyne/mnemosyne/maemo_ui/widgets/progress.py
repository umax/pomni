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
Hildon UI. Widget for progressbar window.
"""

import gtk
import hildon
from mnemosyne.libmnemosyne.ui_components.dialogs import ProgressDialog


class MaemoProgressDlg(ProgressDialog):
    """Maemo Progress Dialog."""

    def __init__(self, component_manager):
        ProgressDialog.__init__(self, component_manager)
        self.fraction = 0.0
        self.pbar = hildon.hildon_banner_show_progress( \
            self.main_widget().widgets['menu'].window, gtk.ProgressBar(), '')
        self.pbar.show()

    def set_range(self, minimum, maximum):
        """Calculate fraction for progressbar."""

        self.fraction = float(1.0 / (maximum - minimum))

    def set_text(self, text):
        """Set title on progress bar."""

        self.pbar.set_text(text)

    def set_value(self, value):
        """Set new value for progess bar."""

        self.pbar.set_fraction(value * self.fraction)
        if value * self.fraction > 0.9:
            self.pbar.destroy()
        # pending gtk
        while gtk.events_pending():
            gtk.main_iteration(False)

