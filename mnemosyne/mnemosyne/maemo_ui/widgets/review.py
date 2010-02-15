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
Hildon UI. Widgets for review.
"""

import gtk
import hildon
import mnemosyne.maemo_ui.widgets.common as widgets

def create_review_ui():
    """Creates ReviewWidget UI."""

    # create containers
    toplevel_table = gtk.Table(rows=1, columns=3)
    toolbar_table = gtk.Table(rows=4, columns=1, homogeneous=True)
    grades_table = gtk.Table(rows=6, columns=1, homogeneous=True)
    widgets_box = gtk.VBox()
    # create html widgets
    #answer_container = hildon.Button(gtk.HILDON_SIZE_AUTO, \
    #    hildon.BUTTON_ARRANGEMENT_HORIZONTAL)
    answer_container = gtk.Frame()
    answer_container.set_name('html_container')
    answer_text = widgets.create_gtkhtml()
    answer_container.add(answer_text)
    #question_container = hildon.Button(gtk.HILDON_SIZE_AUTO, \
    #    hildon.BUTTON_ARRANGEMENT_HORIZONTAL)
    question_container = gtk.Frame()
    question_container.set_name('html_container')
    question_text = widgets.create_gtkhtml()
    question_container.add(question_text)
    # create toolbar buttons
    def create_button():
        button = hildon.Button(gtk.HILDON_SIZE_AUTO, \
            hildon.BUTTON_ARRANGEMENT_HORIZONTAL)
        button.set_size_request(105, -1)
        return button
    
    button_stats = create_button()
    button_stats.set_title('stats')
    button_speak = create_button()
    button_speak.set_title('speak')
    button_edit = create_button()
    button_edit.set_title('edit')
    button_delete = create_button()
    button_delete.set_title('del')
    # create grades buttons
    grades = {}
    for num in range(6):
        grades[num] = create_button()
        grades[num].set_title(str(num))
    # packing toolbar buttons
    toolbar_table.attach(button_stats, 0, 1, 0, 1)
    toolbar_table.attach(button_speak, 0, 1, 1, 2)
    toolbar_table.attach(button_edit, 0, 1, 2, 3)
    toolbar_table.attach(button_delete, 0, 1, 3, 4)
    # packing grades buttons
    for pos in grades.keys():
        grades_table.attach(grades[pos], 0, 1, 5 - pos, 6 - pos, \
            xoptions=gtk.EXPAND, yoptions=gtk.EXPAND|gtk.FILL)
    # packing other widgets
    toplevel_table.attach(toolbar_table, 0, 1, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)
    toplevel_table.attach(grades_table, 3, 4, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)
    widgets_box.pack_start(question_container)
    widgets_box.pack_end(answer_container)
    toplevel_table.attach(widgets_box, 1, 2, 0, 1)
    window = hildon.StackableWindow()
    window.set_title("Review")
    window.add(toplevel_table)
    window.show_all()
    return window, question_text, answer_text, grades_table, grades.values(), \
        button_stats, button_speak, button_edit, button_delete
