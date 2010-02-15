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

def create_menu_ui(exit_callback):
    """Creates MenuWidget UI."""

    # create Menu window
    window = hildon.StackableWindow()
    window.set_title("Mnemosyne for Maemo")
    window.connect("delete_event", exit_callback)
    # create menu buttons
    buttons_table = gtk.Table(rows=2, columns=2)
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
    button_settings = hildon.Button(gtk.HILDON_SIZE_AUTO, \
        hildon.BUTTON_ARRANGEMENT_HORIZONTAL, "Settings")
    button_import = hildon.Button(gtk.HILDON_SIZE_AUTO, \
        hildon.BUTTON_ARRANGEMENT_HORIZONTAL, "Import")
    button_help = hildon.Button(gtk.HILDON_SIZE_AUTO, \
        hildon.BUTTON_ARRANGEMENT_HORIZONTAL, "Help")
    menu.append(button_settings)
    menu.append(button_import)
    menu.append(button_help)
    menu.show_all()
    # packing window elements
    window.add(buttons_table)
    window.set_app_menu(menu)
    window.show_all()
    return window, button_review
