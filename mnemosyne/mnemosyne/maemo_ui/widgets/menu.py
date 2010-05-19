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
Hildon UI. Widgets for menu.
"""

import gtk
import hildon
import gettext

_ = gettext.gettext

def create_menu_ui():
    """Creates MenuWidget UI."""

    toplevel_table = gtk.Table(rows=1, columns=1)
    
    # create Menu window
    window = hildon.StackableWindow()
    window.set_title(unicode("Mnemosyne for Maemo"))

    # create menu buttons
    buttons_table = gtk.Table(rows=2, columns=2)
    buttons_table.set_row_spacings(4)
    buttons_table.set_col_spacings(4)
    button_review = hildon.Button(gtk.HILDON_SIZE_AUTO, \
        hildon.BUTTON_ARRANGEMENT_HORIZONTAL, "Review")
    button_input = hildon.Button(gtk.HILDON_SIZE_AUTO, \
        hildon.BUTTON_ARRANGEMENT_HORIZONTAL, "Input")
    button_tags = hildon.Button(gtk.HILDON_SIZE_AUTO, \
        hildon.BUTTON_ARRANGEMENT_HORIZONTAL, "Tags")
    button_stats = hildon.Button(gtk.HILDON_SIZE_AUTO, \
        hildon.BUTTON_ARRANGEMENT_HORIZONTAL, "Stats")
    buttons_table.attach(button_review, 0, 1, 0, 1)
    buttons_table.attach(button_input, 1, 2, 0, 1)
    buttons_table.attach(button_tags, 0, 1, 1, 2)
    buttons_table.attach(button_stats, 1, 2, 1, 2)
    
    # create AppMenu
    menu = hildon.AppMenu()
    button_general_settings = hildon.Button(gtk.HILDON_SIZE_AUTO, \
        hildon.BUTTON_ARRANGEMENT_HORIZONTAL, _('General settings'))
    button_tts_settings = hildon.Button(gtk.HILDON_SIZE_AUTO, \
        hildon.BUTTON_ARRANGEMENT_HORIZONTAL, _('TTS settings'))
    button_import = hildon.Button(gtk.HILDON_SIZE_AUTO, \
        hildon.BUTTON_ARRANGEMENT_HORIZONTAL, _('Import'))
    button_sync = hildon.Button(gtk.HILDON_SIZE_AUTO, \
        hildon.BUTTON_ARRANGEMENT_HORIZONTAL, _('Sync'))
    button_help = hildon.Button(gtk.HILDON_SIZE_AUTO, \
        hildon.BUTTON_ARRANGEMENT_HORIZONTAL, _('Help'))
    button_about = hildon.Button(gtk.HILDON_SIZE_AUTO, \
        hildon.BUTTON_ARRANGEMENT_HORIZONTAL, _('About'))
    menu.append(button_general_settings)
    menu.append(button_tts_settings)
    menu.append(button_import)
    menu.append(button_sync)
    menu.append(button_help)
    menu.append(button_about)
    menu.show_all()
    
    # packing window elements
    toplevel_table.attach(buttons_table, 0, 1, 0, 1, xpadding=6, ypadding=6)
    window.add(toplevel_table)
    window.set_app_menu(menu)
    
    return window, {'tags': button_tags, 'review': button_review, \
        'input': button_input, 'stats': button_stats, 'gen_settings': \
        button_general_settings, 'tts_settings': button_tts_settings, \
        'import': button_import, 'help': button_help, 'about': button_about, \
        'sync': button_sync}
