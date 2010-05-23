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
from mnemosyne.libmnemosyne.ui_components.dialogs import ProgressDialog


class MaemoProgressDlg(ProgressDialog):
    """Maemo Progress Dialog."""

    def __init__(self, component_manager):
        ProgressDialog.__init__(self, component_manager)

    def set_range(self, minimum, maximum):
        """Calculate fraction for progressbar."""

        pass

    def set_text(self, text):
        """Set title on progress bar."""

        pass

    def set_value(self, value):
        """Set new value for progess bar."""

        # pending gtk
        while gtk.events_pending():
            gtk.main_iteration(False)

