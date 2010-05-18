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
Hildon UI. Dialogs.
"""

import gtk
import hildon
import gettext

_ = gettext.gettext

MIN_FONT_SIZE = 10
MAX_FONT_SIZE = 60


def show_about_dialog(image_name):
    dialog = hildon.Dialog()
    dialog.set_title('About')
    program_box = gtk.HBox()
    program_logo = gtk.Image()
    program_logo.set_from_file(image_name)
    program_name_label = gtk.Label()
    program_name_label.set_justify(gtk.JUSTIFY_CENTER)
    program_name_label.set_use_markup(True)
    program_name_label.set_markup("<span foreground='white' size='large'><b>" \
        "Mnemosyne for Maemo</b></span>\n<span foreground='white' size=" \
        "'large'>version 2.0.0~beta11</span>")
    program_box.pack_start(program_logo)
    program_box.pack_start(program_name_label)
    program_box.show_all()
    dialog.vbox.add(program_box)
    dialog.run()
    dialog.destroy()


def show_general_settings_dialog(config):
    """Shows General settings dialog."""

    dialog = hildon.Dialog()
    dialog.set_title(_("General settings"))
    
    def choose_directory_cb(widget, args=dialog):
        """Shows FileChooser dialog."""

        chooser = hildon.FileChooserDialog(args, \
            gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, hildon.FileSystemModel())
        chooser.run()
        folder = chooser.get_filename()
        if folder:
            widget.set_value(folder)
        chooser.destroy()

    
    def show_font_size_dialog(widget, args=dialog):
        """Shows FontSize dialog."""

        selector = hildon.TouchSelector(text=True)
        dialog = hildon.PickerDialog(args)
        dialog.set_title(_("Font size"))
        dialog.set_selector(selector)
        selector.set_column_selection_mode( \
            hildon.TOUCH_SELECTOR_SELECTION_MODE_SINGLE)
        
        # fill font size list
        current_size = int(widget.get_value())
        sizes_dict = dict([(index, size) for index, size in \
            enumerate(range(MIN_FONT_SIZE, MAX_FONT_SIZE))])
        for size in sizes_dict.values():
            selector.append_text(str(size))
        for key in sizes_dict:
            if sizes_dict[key] == current_size:
                selector.set_active(0, key)
                break

        dialog.run()
        widget.set_value(str(sizes_dict[selector.get_active(0)]))
        dialog.destroy()


    # create widgets
    general_settings_box = gtk.VBox()
    general_settings_box.set_spacing(4)
    sound_button = hildon.Button(gtk.HILDON_SIZE_AUTO | \
        gtk.HILDON_SIZE_FINGER_HEIGHT, hildon.BUTTON_ARRANGEMENT_VERTICAL, \
        _("Sound directory"), config['sounddir']) 
    sound_button.set_style(hildon.BUTTON_STYLE_PICKER)
    sound_button.set_alignment(0, 0, 0, 0)
    sound_button.connect('clicked', choose_directory_cb)
    general_settings_box.pack_start(sound_button, expand=False, fill=False)
    
    image_button = hildon.Button(gtk.HILDON_SIZE_AUTO | \
        gtk.HILDON_SIZE_FINGER_HEIGHT, hildon.BUTTON_ARRANGEMENT_VERTICAL, \
        _("Image directory"), config['imagedir'])
    image_button.set_style(hildon.BUTTON_STYLE_PICKER)
    image_button.set_alignment(0, 0, 0, 0)
    image_button.connect('clicked', choose_directory_cb)
    general_settings_box.pack_start(image_button, expand=False, fill=False)

    font_size_button = hildon.Button(gtk.HILDON_SIZE_AUTO | \
        gtk.HILDON_SIZE_FINGER_HEIGHT, hildon.BUTTON_ARRANGEMENT_VERTICAL, \
        _("Font size"), str(int(config['font_size'])))
    font_size_button.set_style(hildon.BUTTON_STYLE_PICKER)
    font_size_button.connect('clicked', show_font_size_dialog)
    font_size_button.set_alignment(0, 0, 0, 0)
    general_settings_box.pack_start(font_size_button, expand=False, fill=False)
    
    fullscreen_button = hildon.CheckButton(gtk.HILDON_SIZE_AUTO | \
        gtk.HILDON_SIZE_FINGER_HEIGHT)
    fullscreen_button.set_label(_("Start in fullscreen mode"))
    fullscreen_button.set_active(config['fullscreen'])
    general_settings_box.pack_start(fullscreen_button, expand=False, fill=False)

    open_review_button = hildon.CheckButton(gtk.HILDON_SIZE_AUTO | \
        gtk.HILDON_SIZE_FINGER_HEIGHT)
    open_review_button.set_label(_("Open Review mode at startup"))
    open_review_button.set_active(config['startup_with_review'])
    general_settings_box.pack_start(open_review_button, expand=False, fill=False)

    general_settings_box.show_all()
    
    dialog.vbox.add(general_settings_box) 
    dialog.add_button(_("Save"), gtk.RESPONSE_OK)
    
    response = dialog.run()
    if response == gtk.RESPONSE_OK:
        config['sounddir'] = sound_button.get_value()
        config['imagedir'] = image_button.get_value()
        config['font_size'] = int(font_size_button.get_value())
        config['fullscreen'] = fullscreen_button.get_active()
        config['startup_with_review'] = open_review_button.get_active()
        config.save()
    
    dialog.destroy()
    
