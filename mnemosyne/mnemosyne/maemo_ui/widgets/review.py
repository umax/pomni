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

import os
import gtk
import hildon
import mnemosyne.maemo_ui.widgets.common as widgets

ICONS_PATH = '/usr/share/icons/hicolor/48x48/hildon/'

def create_review_ui():
    """Creates ReviewWidget UI."""

    # create containers
    toplevel_table = gtk.Table(rows=1, columns=3)
    toolbar_table = gtk.Table(rows=4, columns=1, homogeneous=True)
    toolbar_table.set_row_spacings(2)
    grades_table = gtk.Table(rows=6, columns=1, homogeneous=True)
    widgets_box = gtk.VBox()
    widgets_box.set_spacing(10)
    
    # create html widgets
    answer_text = widgets.create_gtkhtml()
    question_text = widgets.create_gtkhtml()

    # create toolbar buttons
    def create_button(label=None, image=None):
        button = hildon.Button(gtk.HILDON_SIZE_AUTO, \
            hildon.BUTTON_ARRANGEMENT_HORIZONTAL, label)
        button.set_size_request(104, -1)
        if image is not None:
            button.set_image(gtk.image_new_from_file( \
                os.path.join(ICONS_PATH, image)))
            button.set_alignment(0.8, 0.5, 0, 0)
        return button
    
    button_stats = create_button(image='calendar_todo.png')
    button_speak = create_button(image='general_speaker.png')
    button_edit = create_button(image='general_sketch.png')
    button_delete = create_button(image='general_delete.png')
    
    # create grades buttons
    grades = {}
    for num in range(6):
        grades[num] = create_button(str(num))
        grades[num].set_name('grade%s' % num)
        
    # packing toolbar buttons
    toolbar_table.attach(button_stats, 0, 1, 0, 1, xpadding=2)
    toolbar_table.attach(button_speak, 0, 1, 1, 2, xpadding=2)
    toolbar_table.attach(button_edit, 0, 1, 2, 3, xpadding=2)
    toolbar_table.attach(button_delete, 0, 1, 3, 4, xpadding=2)
    
    # packing grades buttons
    for pos in grades.keys():
        grades_table.attach(grades[pos], 0, 1, 5 - pos, 6 - pos, xpadding=2)

    # packing other widgets
    toplevel_table.attach(toolbar_table, 0, 1, 0, 1, ypadding=2, xpadding=2, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)
    toplevel_table.attach(grades_table, 3, 4, 0, 1, ypadding=2, xpadding=2, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)
    toplevel_table.attach(widgets_box, 1, 2, 0, 1, ypadding=6, xpadding=4)
   
    widgets_box.pack_start(question_text)
    widgets_box.pack_end(answer_text)
    
    window = hildon.StackableWindow()
    window.add(toplevel_table)
    return window, question_text, answer_text, grades_table, grades.values(), \
        button_stats, button_speak, button_edit, button_delete
