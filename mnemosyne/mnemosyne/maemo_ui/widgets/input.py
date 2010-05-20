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
Hildon UI. Widgets for input mode.
"""

import os
import gtk
import hildon
import mnemosyne.maemo_ui.widgets.common as widgets

ICONS_PATH = '/usr/share/icons/hicolor/48x48/hildon/'


def create_input_ui(theme_path):
    """Creates InputWidget UI."""

    # create containers
    toplevel_table = gtk.Table(rows=1, columns=3)
    toolbar_table = gtk.Table(rows=3, columns=1, homogeneous=True)
    toolbar_table.set_row_spacings(2)
    grades_table = gtk.Table(rows=6, columns=1, homogeneous=True)

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
                                            
    card_type_button = create_button('type')
    content_button = create_button()
    tags_button = create_button(image='general_tag.png')
    
    # create sound button
    sound_container = gtk.Frame()
    sound_container.set_name('html_container')
    html = '<html><body><table align="center"><tr><td><img src=%s></td></tr>' \
        '</table></body></html>' % os.path.join(theme_path, "note.png")
    sound_button = widgets.create_gtkhtml(html)
    sound_container.add(sound_button)
    sound_box = gtk.VBox()
    sound_box.set_homogeneous(True)
    
    # create grades buttons
    grades = {}
    for num in range(6):
        grades[num] = create_button(str(num))
        grades[num].set_name('grade%s' % num)

    # create text fields
    def create_text_field():
        """Creates TextView widget."""
        text_widget = gtk.TextView()
        text_widget.set_justification(gtk.JUSTIFY_CENTER)
        text_widget.set_wrap_mode(gtk.WRAP_CHAR)
        return text_widget

    question_text = create_text_field()
    answer_text = create_text_field()
    foreign_text = create_text_field()
    pronunciation_text = create_text_field()
    translation_text = create_text_field()
    cloze_text = create_text_field()

    # create other widgets
    two_sided_box = gtk.VBox()
    two_sided_box.set_homogeneous(True)
    three_sided_box = gtk.VBox()
    three_sided_box.set_homogeneous(True)
    cloze_box = gtk.VBox()
    card_type_switcher = gtk.Notebook()
    card_type_switcher.set_show_tabs(False)
    card_type_switcher.set_show_border(False)
    
    # packing widgets
    toolbar_table.attach(card_type_button, 0, 1, 0, 1, xpadding=2)
    toolbar_table.attach(content_button, 0, 1, 1, 2, xpadding=2)
    toolbar_table.attach(tags_button, 0, 1, 2, 3, xpadding=2)
        
    # packing grades buttons
    for pos in grades.keys():
        grades_table.attach(grades[pos], 0, 1, 5 - pos, 6 - pos, xpadding=2)
            
    # packing other widgets
    toplevel_table.attach(toolbar_table, 0, 1, 0, 1, xpadding=2, ypadding=2, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)
    toplevel_table.attach(grades_table, 3, 4, 0, 1, xpadding=2, ypadding=2, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)
    toplevel_table.attach(card_type_switcher, 1, 2, 0, 1)
    card_type_switcher.append_page(two_sided_box)
    card_type_switcher.append_page(three_sided_box)
    card_type_switcher.append_page(cloze_box)
    sound_box.pack_start(sound_container)
    sound_box.pack_end(question_text)
    two_sided_box.pack_start(sound_box)
    two_sided_box.pack_end(answer_text)
    three_sided_box.pack_start(foreign_text)
    three_sided_box.pack_start(pronunciation_text)
    three_sided_box.pack_end(translation_text)
    cloze_box.pack_start(cloze_text)
   
    # create StackableWindow
    window = hildon.StackableWindow()
    window.add(toplevel_table)

    # create AppMenu
    menu = hildon.AppMenu()
    button_new_tag = hildon.Button(gtk.HILDON_SIZE_AUTO, \
        hildon.BUTTON_ARRANGEMENT_HORIZONTAL, "Add new tag")
    menu.append(button_new_tag)
    menu.show_all()
    window.set_app_menu(menu)
    window.show_all()

    # hide necessary widgets
    sound_container.hide()

    return window, card_type_button, \
        content_button, tags_button, sound_button, question_text, \
        answer_text, foreign_text, pronunciation_text, translation_text, \
        cloze_text, button_new_tag, card_type_switcher, sound_container, \
        question_text, grades, tags_button


def change_content_button_image(button, type):
    """Changes current image for Content button."""

    types_dict = {'text': 'control_pen_input.png', 'image': \
        'general_image.png', 'sound': 'general_audio_file.png'}
    button.set_image(gtk.image_new_from_file( \
        os.path.join(ICONS_PATH, types_dict[type])))
    button.set_alignment(0.8, 0.5, 0, 0)                                    


def create_media_dialog_ui():
    """Creates MediaDialog UI."""

    def enable_select_button_cb(widget, select_button):
        """If user has select item - enable Select button."""
        select_button.set_sensitive(True)

    #liststore = [text, type, filename, dirname, pixbuf]
    liststore = gtk.ListStore(str, str, str, str, gtk.gdk.Pixbuf)
    dialog = gtk.Dialog()
    dialog.set_decorated(False)
    dialog.set_name('dialog')
    dialog.set_has_separator(False)
    dialog.resize(570, 410)
    width, height = dialog.get_size()
    dialog.move((gtk.gdk.screen_width() - width)/2, \
        (gtk.gdk.screen_height() - height)/2)
    iconview_widget = gtk.IconView()
    iconview_widget.set_name('iconview_widget')
    iconview_widget.set_model(liststore)
    iconview_widget.set_pixbuf_column(4)
    iconview_widget.set_text_column(0)
    label = gtk.Label('Select media')
    label.set_name('white_label')
    scrolledwindow_widget = gtk.ScrolledWindow()
    scrolledwindow_widget.set_policy(gtk.POLICY_NEVER, \
        gtk.POLICY_AUTOMATIC)
    scrolledwindow_widget.set_name('scrolledwindow_widget')
    scrolledwindow_widget.add(iconview_widget)
    widgets_table = gtk.Table(rows=1, columns=1)
    widgets_table.attach(scrolledwindow_widget, 0, 1, 0, 1, \
        xpadding=14, ypadding=14)
    dialog.vbox.pack_start(label, expand=False, fill=False, padding=4)
    dialog.vbox.pack_start(widgets_table)
    dialog.vbox.show_all()
    select_button = dialog.add_button('Select', gtk.RESPONSE_OK)
    select_button.set_size_request(262, 60)
    select_button.set_sensitive(False)            
    select_button.set_name('dialog_button')
    iconview_widget.connect('selection-changed', enable_select_button_cb, \
        select_button)
    cancel_button = dialog.add_button('Cancel', gtk.RESPONSE_REJECT)
    cancel_button.set_size_request(232, 60)
    cancel_button.set_name('dialog_button')
    dialog.action_area.set_layout(gtk.BUTTONBOX_SPREAD)
    dialog.action_area.set_homogeneous(True)
    return dialog, liststore, iconview_widget


def create_card_type_dialog_ui(window, card_types_list, current_card_type):
    """Creates CardType dialog UI."""

    selector = hildon.TouchSelector(text=True)
    dialog = hildon.PickerDialog(window)
    dialog.set_title(unicode('Card type'))
    dialog.set_selector(selector)
    
    # fill card types list
    for card_type in card_types_list:
        selector.append_text(card_type.name)

    # activate current card type in cardtypes list
    selector.set_active(0, card_types_list.index(current_card_type))
    
    dialog.run()
    selected_card_type_index = selector.get_active(0)
    dialog.destroy()
    return card_types_list[selected_card_type_index]
                                                                        

def create_content_dialog_ui(window, current_content_type):
    """Creates Content dialog UI."""
    
    selector = hildon.TouchSelector(text=True)
    dialog = hildon.PickerDialog(window)
    dialog.set_title(unicode('Question type'))
    dialog.set_selector(selector)

    # fill content types list
    content_types_list = ["text", "sound", "image"]
    for content_type in content_types_list:
        selector.append_text(content_type.capitalize())
    
    # activate current card type in cardtypes list
    selector.set_active(0, content_types_list.index(current_content_type))

    dialog.run()
    selected_content_type = selector.get_active(0)
    dialog.destroy()
    return content_types_list[selected_content_type]


def create_tags_dialog_ui(window, tags, selected_tags):
    """Creates TagsSelection dialog UI."""

    selector = hildon.TouchSelector(text=True) 

    # fill tags list
    for tag in tags:
        selector.append_text(tag)
    
    selector.set_column_selection_mode( \
        hildon.TOUCH_SELECTOR_SELECTION_MODE_MULTIPLE)
    
    # mark selected tags
    selector.unselect_all(0)
    model = selector.get_model(0)
    for i in range(len(tags)):
        if model[i][0] in selected_tags:
            selector.select_iter(0, model.get_iter(i), False)
        
    dialog = hildon.PickerDialog(window)
    dialog.set_title(unicode("Tags for new card"))
    dialog.set_selector(selector)
    dialog.run()
    indexes_of_selected_tags = [item[0] for item in \
        selector.get_selected_rows(0)]
    model = selector.get_model(0)
    selected_tags = [unicode(model[index][0]) for index in \
        indexes_of_selected_tags]
    dialog.destroy()
    return selected_tags


def create_new_tag_dialog_ui():
    """Creates NewTagDialog UI."""
    
    dialog = hildon.Dialog()
    dialog.set_title(unicode("New tag"))
    entry = hildon.Entry(gtk.HILDON_SIZE_AUTO)
    entry.show()
    dialog.vbox.pack_start(entry)
    dialog.add_button("Add", gtk.RESPONSE_OK)
    dialog.run()
    tag_name = entry.get_text()
    dialog.destroy()
    return tag_name
