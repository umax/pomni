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
Hildon UI. Import widget.
"""

import gtk
import mnemosyne.maemo_ui.widgets.common as widgets


def show_filechooser_dialog(main_window):
    """Show FileChooser dialog."""

    try:
        import hildon
        dlg = hildon.FileChooserDialog(main_window, \
            gtk.FILE_CHOOSER_ACTION_OPEN)
    except ImportError:
        dlg = gtk.FileChooserDialog(parent=main_window, \
            action=gtk.FILE_CHOOSER_ACTION_OPEN)
        dlg.set_decorated(False)
        dlg.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        dlg.add_button(gtk.STOCK_OPEN, gtk.RESPONSE_OK)

    fname = None
    response = dlg.run() 
    if response == gtk.RESPONSE_OK:
        fname = dlg.get_filename()
    dlg.destroy()
    return fname


def create_importcard_ui(main_switcher, format_desc):
    """Creates MaemoImportWidget UI."""

    # create containers
    toplevel_table = gtk.Table(rows=1, columns=2)
    toolbar_container = widgets.create_toolbar_container('one_button_container')
    toolbar_table = gtk.Table(rows=5, columns=1, homogeneous=True)
    switcher = gtk.Notebook()
    switcher.set_show_tabs(False)
    switcher.set_show_border(False)
    widgets_table = gtk.Table(rows=3, columns=1, homogeneous=True)
    # create toolbar buttons
    menu_button = widgets.create_button('main_menu_button')
    # create format selector widgets
    format_table = gtk.Table(rows=1, columns=3, homogeneous=False)
    format_button = widgets.create_button('labels_container', \
        width=-1, height=76)
    format_label = gtk.Label(format_desc)
    format_label.set_name('config_import_label')
    format_prev_button = widgets.create_button( \
        'left_arrow', width=60, height=60)
    format_next_button = widgets.create_button( \
        'right_arrow', width=60, height=60)
    # packing format selector widgets
    format_button.add(format_label)
    format_table.attach(format_prev_button, 0, 1, 0, 1, \
       xoptions=gtk.SHRINK, yoptions=gtk.EXPAND)
    format_table.attach(format_button, 1, 2, 0, 1, \
        xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.SHRINK, xpadding=8)
    format_table.attach(format_next_button, 2, 3, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
    # create file chooser button
    file_chooser_button = widgets.create_button('labels_container', \
        width=-1, height=80)
    file_name_label = gtk.Label('Press to select file to import from ...')
    file_name_label.set_name('config_import_label')
    file_name_label.set_line_wrap(True)
    file_chooser_button.add(file_name_label)
    # create tags button
    #tags_button = widgets.create_button('labels_container', \
    #    width=-1, height=80)
    #tags_name_label = gtk.Label('Press to select tags for importing cards ...')
    #tags_name_label.set_name('config_import_label')
    #tags_name_label.set_line_wrap(True)
    #tags_button.add(tags_name_label)
    # create convert button
    convert_button = widgets.create_button('labels_container')
    convert_label = gtk.Label('Convert!')
    convert_label.set_name('config_import_label')
    convert_button.set_sensitive(False)
    convert_button.add(convert_label)
    # create tags widgets
    tags_layout = gtk.VBox(spacing=26)
    tags_note_label = gtk.Label()
    tags_note_label.set_text('Select tags for imported cards')
    tags_note_label.set_name('white_label')
    tags_note_label.set_justify(gtk.JUSTIFY_LEFT)
    tags_note_label.set_single_line_mode(True)
    tags_frame = gtk.Frame()
    tags_frame.set_name('html_container')
    tags_eventbox = gtk.EventBox()
    tags_eventbox.set_visible_window(True)
    tags_eventbox.set_name('viewport_widget')
    tags_scrolledwindow = gtk.ScrolledWindow()
    tags_scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    tags_scrolledwindow.set_name('scrolled_window')
    tags_viewport = gtk.Viewport()
    tags_viewport.set_shadow_type(gtk.SHADOW_NONE)
    tags_viewport.set_name('viewport_widget')
    tags_box = gtk.VBox()
    # packing tags widgets
    tags_viewport.add(tags_box)
    tags_scrolledwindow.add(tags_viewport)
    tags_eventbox.add(tags_scrolledwindow)
    tags_frame.add(tags_eventbox)
    tags_layout.pack_start(tags_note_label, expand=False, fill=False)
    tags_layout.pack_end(tags_frame, expand=True, fill=True)
    # packing toolbar buttons
    toolbar_table.attach(menu_button, 0, 1, 4, 5, xoptions=gtk.SHRINK, \
        yoptions=gtk.EXPAND)
    toolbar_container.add(toolbar_table)
    # packing other widgets
    widgets_table.attach(format_table, 0, 1, 0, 1, \
        xoptions=gtk.EXPAND|gtk.FILL|gtk.EXPAND, \
        yoptions=gtk.SHRINK|gtk.EXPAND)
    widgets_table.attach(file_chooser_button, 0, 1, 1, 2, \
        xoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, \
        yoptions=gtk.EXPAND|gtk.FILL)
    #widgets_table.attach(tags_button, 0, 1, 2, 3, \
    #    xoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, \
    #    yoptions=gtk.SHRINK|gtk.EXPAND)
    widgets_table.attach(convert_button, 0, 1, 2, 3, \
        xoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, \
        yoptions=gtk.SHRINK|gtk.EXPAND)
    toplevel_table.attach(toolbar_container, 0, 1, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)
    toplevel_table.attach(switcher, 1, 2, 0, 1, \
        xoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, xpadding=30, \
        yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, ypadding=30)
    switcher.append_page(widgets_table)
    switcher.append_page(tags_layout)
    toplevel_table.show_all()
    return main_switcher.append_page(toplevel_table), switcher, format_label, \
        format_button, tags_box, file_chooser_button, file_name_label, \
        menu_button, convert_button, format_prev_button, format_next_button
