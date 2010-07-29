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
from gettext import gettext as _
import mnemosyne.maemo_ui.widgets.common as widgets
from mnemosyne.libmnemosyne.card_types.front_to_back import FrontToBack
from mnemosyne.libmnemosyne.card_types.both_ways import BothWays
from mnemosyne.libmnemosyne.card_types.three_sided import ThreeSided
from mnemosyne.libmnemosyne.card_types.cloze import Cloze

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

    card_type_button = create_button()
    content_button = create_button()
    tags_button = create_button(image='general_tag.png')

    # create media button
    #images_dict = {'image': 'filemanager_image_folder.png', 'sound': '\
    #    filemanager_audio_folder.png'}
    media_button = widgets.create_gtkhtml()
    media_container = gtk.Table()
    #'<html><body><table align="center">' \
    #    '<tr><td><img src=%s></td></tr></table></body></html>' % os.path.join( \
    #    theme_path, images_dict[content_type]))

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
        text_container = hildon.PannableArea()
        text_container.set_property('mov-mode', hildon.MOVEMENT_MODE_VERT)
        text_container.add(text_widget)
        return text_widget, text_container

    question_text, question_container = create_text_field()
    answer_text, answer_container = create_text_field()
    foreign_text, foreign_container = create_text_field()
    pronunciation_text, pronunciation_container = create_text_field()
    translation_text, translation_container = create_text_field()
    cloze_text, cloze_container = create_text_field()

    # create other widgets
    question_box = gtk.VBox()
    question_box.set_homogeneous(True)
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

    media_container.attach(media_button, 0, 1, 0, 1, xpadding=5, ypadding=4)
    question_box.pack_start(media_container)
    question_box.pack_end(question_container)
    two_sided_box.pack_start(question_box)
    two_sided_box.pack_end(answer_container)
    three_sided_box.pack_start(foreign_container)
    three_sided_box.pack_start(pronunciation_container)
    three_sided_box.pack_end(translation_container)
    cloze_box.pack_start(cloze_container)

    # create StackableWindow
    window = hildon.StackableWindow()
    window.add(toplevel_table)

    # create AppMenu
    menu = hildon.AppMenu()
    button_new_tag = hildon.Button(gtk.HILDON_SIZE_AUTO, \
        hildon.BUTTON_ARRANGEMENT_HORIZONTAL, _('Add new tag'))
    menu.append(button_new_tag)
    menu.show_all()
    window.set_app_menu(menu)
    window.show_all()

    # hide necessary widgets
    media_container.hide()

    return window, card_type_button, content_button, tags_button, \
        question_text, answer_text, foreign_text, pronunciation_text, \
        translation_text, cloze_text, button_new_tag, card_type_switcher, \
        media_button, media_container, grades, tags_button, question_container


def change_content_button_image(button, c_type):
    """Changes current image for Content button."""

    images_dict = {'text': 'control_pen_input.png', 'image': \
        'general_image.png', 'sound': 'general_audio_file.png'}
    button.set_image(gtk.image_new_from_file( \
        os.path.join(ICONS_PATH, images_dict[c_type])))
    button.set_alignment(0.8, 0.5, 0, 0)


def change_cardtype_button_image(button, c_type, config):
    """Changes current image for CardType button."""

    images_dict = {FrontToBack.id: 'front_to_back.png', BothWays.id: \
        'both_ways.png', ThreeSided.id: 'three_sided.png', Cloze.id: \
        'cloze.png'}
    button.set_image(gtk.image_new_from_file( \
        os.path.join(config['theme_path'], images_dict[c_type.id])))
    button.set_alignment(0.8, 0.5, 0, 0)


def change_media_button_image(button, c_type, renderer, folder_mode=True, \
    fname=None, fname_is_html=False):
    """Changes current image for Media button."""

    images_dict = {'image': 'filemanager_image_folder.png', 'sound': \
        'filemanager_audio_folder.png'}
    if folder_mode:
        renderer.render_media_button(button, os.path.join(ICONS_PATH, \
            images_dict[c_type]))
    else:
        if fname is not None:
            renderer.render_media_button(button, fname, fname_is_html)
        else:
            renderer.render_media_button(button, os.path.join(ICONS_PATH, \
                'general_audio_file.png'))
