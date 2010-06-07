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
Hildon UI. Widgets for main.
"""

import gtk
import hildon
import gettext

_ = gettext.gettext


def create_question_dialog(window, text):
    """Create QuestionDialog UI."""

    if 'Activate cards' in text:
        text = _('Delete this card and 1 related card?')
    label = gtk.Label(text)
    dialog = hildon.Dialog()
    dialog.set_title(_('Card deletion'))
    dialog.vbox.add(label)
    dialog.vbox.show_all()
    dialog.add_button(_('Yes'), gtk.RESPONSE_YES)
    dialog.add_button(_('No'), gtk.RESPONSE_NO)
    response = dialog.run()
    dialog.destroy()
    if response == gtk.RESPONSE_YES:
        return False
    return True


def create_information_dialog(window, text, title=_('Information')):
    """Create InformationDialog UI."""

    dialog = hildon.Dialog()
    dialog.set_title(title)
    label = gtk.Label()
    label.set_justify(gtk.JUSTIFY_CENTER)
    label.set_text('\n' + text + '\n')
    dialog.vbox.add(label)
    dialog.vbox.show_all()
    dialog.run()
    dialog.destroy()
