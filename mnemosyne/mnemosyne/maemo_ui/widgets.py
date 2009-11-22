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
Hildon UI. Different widgets.
"""

import gtk
import urllib
import gtkhtml2
import urlparse
from mnemosyne.libmnemosyne.ui_component import UiComponent

def create_gtkhtml():
    """ Create gtkhtml2 widget """

    def request_url(document, url, stream):
        """Get content from url."""
        uri = urlparse.urljoin("", url)
        fpurl = self.htmlopener.open(uri)
        stream.write(fpurl.read())
        fpurl.close()
        stream.close()

    view = gtkhtml2.View()
    document = gtkhtml2.Document()
    document.connect('request_url', request_url)
    view.set_document(document)
    view.document = document
    view.show()
    return view



def create_tags_ui(main_switcher):
    """Creates TagsWidget UI."""

    toplevel_table = gtk.Table(rows=1, columns=2, homogeneous=False)
    # create toolbar container
    toolbar_container = gtk.Notebook()
    toolbar_container.set_show_tabs(False)
    toolbar_container.set_size_request(82, 420)
    toolbar_container.set_name('tags_mode_toolbar_container')
    toolbar_table = gtk.Table(rows=5, columns=1, homogeneous=True)
    # create menu button
    menu_button = gtk.Button()
    menu_button.set_size_request(80, 80)
    menu_button.set_name('tags_mode_main_menu_button')
    # create tags frame
    tags_frame = gtk.Frame()
    tags_frame.set_name('tags_mode_tags_frame')
    tags_eventbox = gtk.EventBox()
    tags_eventbox.set_visible_window(True)
    tags_eventbox.set_name('tags_mode_tags_eventbox')
    tags_scrolledwindow = gtk.ScrolledWindow()
    tags_scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    tags_scrolledwindow.set_name('tags_mode_tags_scrolledwindow')
    tags_viewport = gtk.Viewport()
    tags_viewport.set_name('tags_mode_tags_viewport')
    tags_box = gtk.VBox()
    # packing widgets
    tags_viewport.add(tags_box)
    tags_scrolledwindow.add(tags_viewport)
    tags_eventbox.add(tags_scrolledwindow)
    tags_frame.add(tags_eventbox)
    toolbar_table.attach(menu_button, 0, 1, 4, 5, xoptions=gtk.EXPAND, \
        yoptions=gtk.EXPAND)
    toolbar_container.add(toolbar_table)
    toplevel_table.attach(toolbar_container, 0, 1, 0, 1, \
       xoptions=gtk.SHRINK, yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)
    toplevel_table.attach(tags_frame, 1, 2, 0, 1, \
        xoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, \
        yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, \
        xpadding=30, ypadding=30)
    toplevel_table.show_all()
    return main_switcher.append_page(toplevel_table), tags_box, menu_button


def create_review_ui(main_switcher):
    """Creates ReviewWidget UI."""

    def create_button(name, width=80, height=80):
        button = gtk.Button()
        button.set_size_request(width, height)
        button.set_name(name)
        return button

    toplevel_table = gtk.Table(rows=1, columns=3)
    # create toolbar container   
    toolbar_container = gtk.Notebook()
    toolbar_container.set_show_tabs(False)
    toolbar_container.set_size_request(82, 480)
    toolbar_container.set_name('review_mode_toolbar_container')
    # create grades container
    grades_container = gtk.Notebook()
    grades_container.set_show_tabs(False)
    grades_container.set_size_request(82, 480)
    grades_container.set_name('review_mode_grades_container')
    toolbar_table = gtk.Table(rows=5, columns=1, homogeneous=True)
    grades_table = gtk.Table(rows=6, columns=1, homogeneous=True)
    widgets_box = gtk.VBox(spacing=10)
    question_box = gtk.VBox(homogeneous=True)
    sound_container = gtk.Table(rows=1, columns=10, homogeneous=True)
    sound_button = gtk.Button()
    answer_container = gtk.Frame()
    answer_container.set_name('answer_container')
    question_container = gtk.Frame()
    question_container.set_name('question_container')
    answer_text = create_gtkhtml()
    question_text = create_gtkhtml()
    # create toolbar buttons
    buttons = {}
    buttons[0] = create_button('review_toolbar_tts_button')
    buttons[1] = create_button('review_toolbar_edit_card_button')
    buttons[2] = create_button('review_toolbar_add_card_button')
    buttons[3] = create_button('review_toolbar_delete_card_button')
    buttons[4] = create_button('review_toolbar_main_menu_button') 
    # create grades buttons
    grades = {}
    for num in range(6):
        grades[num] = create_button('grade%s' % num)
    # packing toolbar buttons
    for pos in buttons.keys():
        toolbar_table.attach(buttons[pos], 0, 1, pos, pos + 1, \
            xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
    toolbar_container.add(toolbar_table)
    # packing grades buttons
    for pos in grades.keys():
        grades_table.attach(grades[pos], 0, 1, 5 - pos, 6 - pos, \
            xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
    grades_container.add(grades_table)
    toplevel_table.attach(toolbar_container, 0, 1, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)
    toplevel_table.attach(grades_container, 3, 4, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)
    question_container.add(question_text)
    answer_container.add(answer_text)
    sound_container.attach(sound_button, 3, 7, 0, 1, \
        xoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK, \
        yoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK)
    question_box.pack_start(sound_container)
    question_box.pack_end(question_container)
    widgets_box.pack_start(question_box)
    widgets_box.pack_end(answer_container)
    toplevel_table.attach(widgets_box, 2, 3, 0, 1, ypadding=30,
        xoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, \
        yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, xpadding=30)
    toplevel_table.show_all()
    # hide necessary widgets
    sound_container.hide()
    return main_switcher.append_page(toplevel_table), buttons[0], buttons[1], \
        buttons[3], question_container, answer_container, question_text, \
        answer_text, sound_container, sound_button, grades_table, \
        grades.values(), buttons.values()


def create_input_ui(main_switcher):
    """Creates InputWidget UI."""

    toplevel_table = gtk.Table(rows=1, columns=2)
    # create toolbar container
    toolbar_container = gtk.Notebook()
    toolbar_container.set_show_tabs(False)
    toolbar_container.set_size_request(82, 480)
    toolbar_container.set_name('input_mode_toolbar_container')
    toolbar_table = gtk.Table(rows=5, columns=1, homogeneous=True)
    # create toolbar buttons
    card_type_button = gtk.Button()
    card_type_button.set_size_request(80, 80)
    content_button = gtk.Button()
    content_button.set_size_request(80, 80)
    add_card_button = gtk.Button()
    add_card_button.set_size_request(80, 80)
    add_card_button.set_name('input_mode_toolbar_add_card_w')
    menu_button = gtk.Button()
    menu_button.set_size_request(80, 80)
    menu_button.set_name('input_mode_toolbar_button_back_w')
    widgets_table = gtk.Table(rows=2, columns=1)
    widgets_table.set_row_spacings(14)
    tags_button = gtk.Button()
    tags_button.set_size_request(-1, 60)
    tags_button.set_name('tags_button')
    card_type_switcher = gtk.Notebook()
    card_type_switcher.set_show_tabs(False)
    card_type_switcher.set_show_border(False)
    two_sided_box = gtk.VBox(spacing=10)
    sound_box = gtk.VBox()
    sound_box.set_homogeneous(True)
    sound_container = gtk.Table(rows=1, columns=3, homogeneous=True)
    sound_button = gtk.ToggleButton()
    sound_button.set_name('input_mode_snd_button')
    # create text fields
    question_container = gtk.Frame()
    question_container.set_name('input_mode_question_container')
    question_text = gtk.TextView()
    question_text.set_justification(gtk.JUSTIFY_CENTER)
    question_text.set_wrap_mode(gtk.WRAP_WORD)
    answer_container = gtk.Frame()
    answer_container.set_name('input_mode_answer_container')
    answer_text = gtk.TextView()
    answer_text.set_justification(gtk.JUSTIFY_CENTER)
    answer_text.set_wrap_mode(gtk.WRAP_WORD)
    three_sided_box = gtk.VBox(spacing=10)
    foreign_container = gtk.Frame()
    foreign_container.set_name('input_mode_foreign_container')
    foreign_text = gtk.TextView()
    foreign_text.set_justification(gtk.JUSTIFY_CENTER)
    foreign_text.set_wrap_mode(gtk.WRAP_WORD)
    pronunciation_container = gtk.Frame()
    pronunciation_container.set_name('input_mode_pronun_container')
    pronunciation_text = gtk.TextView()
    pronunciation_text.set_justification(gtk.JUSTIFY_CENTER)
    pronunciation_text.set_wrap_mode(gtk.WRAP_WORD)
    translation_container = gtk.Frame()
    translation_container.set_name('input_mode_translate_container')
    translation_text = gtk.TextView()
    translation_text.set_justification(gtk.JUSTIFY_CENTER)
    translation_text.set_wrap_mode(gtk.WRAP_WORD)
    cloze_box = gtk.VBox()
    cloze_container = gtk.Frame()
    cloze_container.set_name('input_mode_cloze_container')
    cloze_text = gtk.TextView()
    cloze_text.set_justification(gtk.JUSTIFY_CENTER)
    cloze_text.set_wrap_mode(gtk.WRAP_WORD)
    # create new tag elements
    tags_layout = gtk.VBox(spacing=26)
    new_tag_box = gtk.HBox()
    new_tag_label = gtk.Label()
    new_tag_label.set_text('New tag: ')
    new_tag_label.set_name('new_tag_label')
    new_tag_button = gtk.Button()
    new_tag_button.set_size_request(60, 60)
    new_tag_button.set_name('new_tag_button')
    new_tag_frame = gtk.Frame()
    new_tag_frame.set_name('new_tag_frame')
    new_tag_entry = gtk.Entry()
    new_tag_entry.set_name('new_tag_entry')
    # creates 'tags list' elements
    tags_frame = gtk.Frame()
    tags_frame.set_name('tags_frame')
    tags_eventbox = gtk.EventBox()
    tags_eventbox.set_visible_window(True)
    tags_eventbox.set_name('tags_eventbox')
    tags_scrolledwindow = gtk.ScrolledWindow()
    tags_scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, \
        gtk.POLICY_AUTOMATIC)
    tags_scrolledwindow.set_name('tags_scrolledwindow')
    tags_viewport = gtk.Viewport()
    tags_viewport.set_name('tags_viewport')
    tags_box = gtk.VBox()
    tags_box.set_homogeneous(True)
    # packing widgets
    toolbar_table.attach(card_type_button, 0, 1, 0, 1, \
        xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
    toolbar_table.attach(content_button, 0, 1, 1, 2, \
        xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
    toolbar_table.attach(add_card_button, 0, 1, 2, 3, \
        xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
    toolbar_table.attach(menu_button, 0, 1, 4, 5, \
        xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
    toolbar_container.add(toolbar_table)
    toplevel_table.attach(toolbar_container, 0, 1, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)
    widgets_table.attach(tags_button, 0, 1, 0, 1, \
        xoptions=gtk.SHRINK|gtk.FILL|gtk.EXPAND, \
        yoptions=gtk.SHRINK, xpadding=4)
    widgets_table.attach(card_type_switcher, 0, 1, 1, 2, \
        xoptions=gtk.SHRINK|gtk.FILL|gtk.EXPAND, \
        yoptions=gtk.SHRINK|gtk.FILL|gtk.EXPAND)
    card_type_switcher.append_page(two_sided_box)
    card_type_switcher.append_page(three_sided_box)
    card_type_switcher.append_page(cloze_box)
    card_type_switcher.append_page(tags_layout)
    sound_container.attach(sound_button, 1, 2, 0, 1, \
        xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL|gtk.SHRINK)
    question_container.add(question_text)
    sound_box.pack_start(sound_container)
    sound_box.pack_end(question_container)
    answer_container.add(answer_text)
    two_sided_box.pack_start(sound_box)
    two_sided_box.pack_end(answer_container)
    foreign_container.add(foreign_text)
    pronunciation_container.add(pronunciation_text)
    translation_container.add(translation_text)
    three_sided_box.pack_start(foreign_container)
    three_sided_box.pack_start(pronunciation_container)
    three_sided_box.pack_end(translation_container)
    cloze_container.add(cloze_text)
    cloze_box.pack_start(cloze_container)
    new_tag_frame.add(new_tag_entry)
    new_tag_box.pack_start(new_tag_label, expand=False, fill=False, padding=10)
    new_tag_box.pack_start(new_tag_frame, expand=True, fill=True, padding=10)
    new_tag_box.pack_end(new_tag_button, expand=False, fill=False)
    tags_viewport.add(tags_box)
    tags_scrolledwindow.add(tags_viewport)
    tags_eventbox.add(tags_scrolledwindow)
    tags_frame.add(tags_eventbox)
    tags_layout.pack_start(new_tag_box, expand=False, fill=False)
    tags_layout.pack_end(tags_frame, expand=True, fill=True)
    toplevel_table.attach(widgets_table, 1, 2, 0, 1, \
        xoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, xpadding=30, \
        yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, ypadding=30)
    toplevel_table.show_all()
    # hide necessary widgets
    sound_container.hide()
    return main_switcher.append_page(toplevel_table), card_type_button, \
        content_button, menu_button, tags_button, sound_button, question_text, \
        answer_text, foreign_text, pronunciation_text, translation_text, \
        cloze_text, new_tag_button, new_tag_entry, tags_box, \
        card_type_switcher, add_card_button, sound_container, \
        question_container, toolbar_container

def create_media_dialog_ui():
    """Creates MediaDialog UI."""

    def enable_select_button_cb(widget, select_button):
        """If user has select item - enable Select button."""
        select_button.set_sensitive(True)

    #liststore = [text, type, filename, dirname, pixbuf]
    liststore = gtk.ListStore(str, str, str, str, gtk.gdk.Pixbuf)
    dialog = gtk.Dialog()
    dialog.set_decorated(False)
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
    label.set_name('media_selection_dialog_label')
    scrolledwindow_widget = gtk.ScrolledWindow()
    scrolledwindow_widget.set_policy(gtk.POLICY_NEVER, \
        gtk.POLICY_AUTOMATIC)
    scrolledwindow_widget.set_name('scrolledwindow_widget')
    scrolledwindow_widget.add(iconview_widget)
    widgets_table = gtk.Table(rows=1, columns=1)
    widgets_table.attach(scrolledwindow_widget, 0, 1, 0, 1, \
        xpadding=12, ypadding=12)
    dialog.vbox.pack_start(label, expand=False, fill=False, padding=5)
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
    return dialog, liststore, iconview_widget


def create_card_type_dialog_ui(selectors, front_to_back_id, both_ways_id, \
    three_sided_id, cloze_id, card_type_button, current_card_type, callback):
    """Creates CardType dialog UI."""

    button = create_radio_button(None, 'front_to_back_cardtype_button', \
        callback)
    selectors[front_to_back_id]['selector'] = button
    button = create_radio_button(button, 'both_ways_cardtype_button', callback)
    selectors[both_ways_id]['selector'] = button
    button = create_radio_button(button, 'three_sided_cardtype_button', \
        callback)
    selectors[three_sided_id]['selector'] = button
    button = create_radio_button(button, 'cloze_cardtype_button', callback)
    selectors[cloze_id]['selector'] = button
    dialog = gtk.Dialog()
    dialog.set_decorated(False)
    dialog.set_has_separator(False)
    pos_x, pos_y = card_type_button.window.get_origin()
    dialog.move(pos_x, pos_y)
    buttons_table = gtk.Table(rows=1, columns=4, homogeneous=True)
    buttons_table.set_col_spacings(16)
    index = 0
    for selector in selectors.values():
        widget = selector['selector']
        if current_card_type is selector['card_type']:
            widget.set_active(True)
        buttons_table.attach(widget, index, index + 1, 0, 1, \
            xoptions=gtk.EXPAND, xpadding=6)
        index += 1
    dialog.vbox.pack_start(buttons_table, expand=True, fill=False, \
        padding=12)
    buttons_table.show_all()
    dialog.run()


def create_content_dialog_ui(callback, content_button, toolbar_container, \
    current_card_type, front_to_back_id):
    """Creates ContentDialog."""

    text_content_button = create_button('text_content_button', callback, \
        width=72, height=72)
    image_content_button = create_button('image_content_button', callback, \
        width=72, height=72)
    sound_content_button = create_button('sound_content_button', callback, \
        width=72, height=72)
    dialog = gtk.Dialog()
    dialog.set_decorated(False)
    dialog.set_has_separator(False)
    pos_x, pos_y = content_button.window.get_origin()
    dialog.move(pos_x, pos_y + toolbar_container.get_size_request()[1]/5)
    state = current_card_type.id in (front_to_back_id)
    sound_content_button.set_sensitive(state)
    image_content_button.set_sensitive(state)
    buttons_table = gtk.Table(rows=1, columns=3, homogeneous=True)
    buttons_table.set_col_spacings(16)
    buttons_table.attach(text_content_button, 0, 1, 0, 1, \
        xoptions=gtk.EXPAND, xpadding=10)
    buttons_table.attach(sound_content_button, 1, 2, 0, 1, \
        xoptions=gtk.EXPAND, xpadding=10)
    buttons_table.attach(image_content_button, 2, 3, 0, 1, \
        xoptions=gtk.EXPAND, xpadding=10)
    buttons_table.show_all()
    dialog.vbox.pack_start(buttons_table, expand=True, fill=False, \
        padding=8)
    dialog.run()


class BaseHildonWidget(UiComponent):
    """Base widget."""

    def __init__(self, component_manager):
        UiComponent.__init__(self, component_manager)
        self.connections = []
        self.conf = self.config()
        #self.w_tree = self.main_widget().w_tree
        #self.w_tree = self.main_widget().w_tree
        #self.get_widget = self.w_tree.get_widget

    """
    def connect_signals(self, control):

        for wname, signal, callback in control:
            widget = self.get_widget(wname)
            cid = widget.connect(signal, callback)
            self.connections.append((widget, cid))

    def disconnect_signals(self):

        for widget, cid in self.connections:
            widget.disconnect(cid)
        self.connections = []

    """
def create_button(name=None, callback=None, event='clicked', \
    width=80, height=80, label=None):
    """Creates gtkButton widget."""

    button = gtk.Button()
    button.set_size_request(width, height)
    if name is not None:
        button.set_name(name)
    if callback is not None:
        button.connect(event, callback)
    if label is not None:
        button.set_label(label)
    return button


def create_radio_button(group=None, name=None, callback=None, \
     event='released', width=72, height=72):
    """Creates gtkRadioButton widget."""

    button = gtk.RadioButton(group)
    button.set_size_request(width, height)
    if name is not None:
        button.set_name(name)
    if callback is not None:
        button.connect(event, callback)
    return button

    def create_toolbar_container(self, name, show_tabs=False, width=82, \
        height=480):
        """Creates toolbar container."""

        container = gtk.Notebook()
        container.set_show_tabs(show_tabs)
        container.set_size_request(width, height)
        container.set_name(name)
        return container

def create_tag_checkbox(name, active):
    """Create Tag item - GtkHBox with gtk.ToggleButton and gtk.Label."""

    hbox = gtk.HBox(homogeneous=False, spacing=10)
    button = gtk.ToggleButton()
    button.set_size_request(64, 64)
    button.set_active(active)
    button.set_name("tag_check")
    label = gtk.Label(name)
    label.set_name("tag_label")
    hbox.pack_start(button, False)
    hbox.pack_start(label, False)
    hbox.show_all()
    return hbox
