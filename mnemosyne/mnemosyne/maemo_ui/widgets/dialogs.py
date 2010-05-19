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
import mnemosyne.maemo_ui.widgets.common as widgets

_ = gettext.gettext

MIN_FONT_SIZE = 10
MAX_FONT_SIZE = 60


def show_about_dialog():
    """SHows About dialog."""
    
    dialog = hildon.Dialog()
    dialog.set_title(_('About'))
    
    program_name_label = gtk.Label()
    program_name_label.set_justify(gtk.JUSTIFY_CENTER)
    program_name_label.set_use_markup(True)
    program_name_label.set_markup("<span foreground='white' size='medium'><b>" \
        "Mnemosyne for Maemo</b></span>\n<span foreground='white' size=" \
        "'small'>version 2.0.0~beta11</span>\n")
    
    pannable_area = hildon.PannableArea()
    pannable_area.set_size_request_policy(hildon.SIZE_REQUEST_CHILDREN)
    developers_label = gtk.Label()
    developers_label.set_use_markup(True)
    developers_label.set_markup("<span foreground='white' size='small'><b>" \
        "Developers:</b></span>\n<span foreground='white' size='small'>" \
        "Max Usachev |</span> <span foreground='#299BFC' size='small'>" \
        "maxusachev@gmail.com</span>\n<span foreground='white' size=" \
        "'small'>Ed Bartosh |</span> <span foreground='#299BFC' size=" \
        "'small'>bartosh@gmail.com</span>\n<span foreground='white' " \
        "size='small'>Vlad Vasiliev |</span> <span foreground='#299BFC' " \
        "size='small'>vlad@gas.by</span>\n\n<span foreground='white' " \
        "size='small'><b>Designer:</b>\n</span><span foreground='white' " \
        "size='small'>Andrew Zhilin |</span> <span foreground='#299BFC' " \
        "size='small'>drew.zhilin@gmail.com</span>\n\n<span foreground=" \
        "'white' size='small'><b>Development team:</b></span>\n<span " \
        "foreground='#299BFC' size='small'>pomni@googlegroups.com</span>"
        "<span foreground='white' size='small'><b>" \
        "\n\nSpecial Thanks To:</b></span>\n<span foreground='white' size=" \
        "'small'>Peter Bienstman</span>\n<span foreground='#299BFC' size=" \
        "'small'>Peter.Bienstman@ugent.be</span>\n<span foreground=" \
        "'#299BFC' size='small'>http://www.mnemosyne-proj.org/</span>" \
        "\n<span size='x-large'></span><span foreground='white' size=" \
        "'small'>\nGSoC 2009</span>\n<span foreground='#299BFC' size='"\
        "small'>http://socghop.appspot.com/</span>\n<span size='x-large'>" \
        "</span><span foreground='white' size='small'>\nMaemo community" \
        "</span>\n<span foreground='#299BFC' size='small'>" \
        "http://maemo.org/</span>")
    pannable_area.add_with_viewport(developers_label)
    
    dialog.vbox.pack_start(program_name_label, expand=False, fill=True)
    dialog.vbox.pack_start(pannable_area)
    dialog.vbox.set_spacing(10)
    dialog.vbox.show_all()
    dialog.add_button(_('Visit website'), gtk.RESPONSE_OK)
    dialog.add_button(_('Report bug'), gtk.RESPONSE_OK)
    dialog.run()
    dialog.destroy()


def show_items_dialog(window, widget, items, caption):
    """Shows custom PickerDialog with TouchSelector widget."""

    dialog = hildon.PickerDialog(window)
    dialog.set_title(caption)
    selector = hildon.TouchSelector(text=True)
    dialog.set_selector(selector)
    selector.set_column_selection_mode( \
        hildon.TOUCH_SELECTOR_SELECTION_MODE_SINGLE)
        
    # fill items list
    current_item = widget.get_value()
    items_dict = dict([(index, item) for index, item in enumerate(items)])
    for item in items_dict.values():
        selector.append_text(item)
    for key in items_dict:
        if items_dict[key] == current_item:
            selector.set_active(0, key)
            break

    dialog.run()
    selected_item = items_dict[selector.get_active(0)]
    dialog.destroy()
    return selected_item


def show_general_settings_dialog(config):
    """Shows General settings dialog."""

    dialog = hildon.Dialog()
    dialog.set_title(_('General settings'))
    
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

        widget.set_value(show_items_dialog(args, widget, [str(size) for \
            size in range(MIN_FONT_SIZE, MAX_FONT_SIZE)], _('Font size')))


    # create widgets
    widgets_box = gtk.VBox()
    widgets_box.set_spacing(4)
    
    sound_button = hildon.Button(gtk.HILDON_SIZE_AUTO | \
        gtk.HILDON_SIZE_FINGER_HEIGHT, hildon.BUTTON_ARRANGEMENT_VERTICAL, \
        _('Sound directory'), config['sounddir']) 
    sound_button.set_style(hildon.BUTTON_STYLE_PICKER)
    sound_button.set_alignment(0, 0, 0, 0)
    sound_button.connect('clicked', choose_directory_cb)
    widgets_box.pack_start(sound_button, expand=False, fill=False)
    
    image_button = hildon.Button(gtk.HILDON_SIZE_AUTO | \
        gtk.HILDON_SIZE_FINGER_HEIGHT, hildon.BUTTON_ARRANGEMENT_VERTICAL, \
        _('Image directory'), config['imagedir'])
    image_button.set_style(hildon.BUTTON_STYLE_PICKER)
    image_button.set_alignment(0, 0, 0, 0)
    image_button.connect('clicked', choose_directory_cb)
    widgets_box.pack_start(image_button, expand=False, fill=False)

    font_size_button = hildon.Button(gtk.HILDON_SIZE_AUTO | \
        gtk.HILDON_SIZE_FINGER_HEIGHT, hildon.BUTTON_ARRANGEMENT_VERTICAL, \
        _('Font size'), str(int(config['font_size'])))
    font_size_button.set_style(hildon.BUTTON_STYLE_PICKER)
    font_size_button.connect('clicked', show_font_size_dialog)
    font_size_button.set_alignment(0, 0, 0, 0)
    widgets_box.pack_start(font_size_button, expand=False, fill=False)
    
    open_review_button = hildon.CheckButton(gtk.HILDON_SIZE_AUTO | \
        gtk.HILDON_SIZE_FINGER_HEIGHT)
    open_review_button.set_label(_('Open Review mode at startup'))
    open_review_button.set_active(config['startup_with_review'])
    widgets_box.pack_start(open_review_button, expand=False, fill=False)

    widgets_box.show_all()
    
    dialog.vbox.add(widgets_box) 
    dialog.add_button(_('Save'), gtk.RESPONSE_OK)
    
    response = dialog.run()
    if response == gtk.RESPONSE_OK:
        config['sounddir'] = sound_button.get_value()
        config['imagedir'] = image_button.get_value()
        config['font_size'] = int(font_size_button.get_value())
        config['startup_with_review'] = open_review_button.get_active()
        config.save()
    
    dialog.destroy()
   

def show_tts_settings_dialog(config):
    """Shows TTS settings dialog."""

    import mnemosyne.maemo_ui.tts as tts
    
    dialog = hildon.Dialog()
    dialog.set_title(_('TTS settings'))
    
    if not tts.is_available():
        label = gtk.Label(_("TTS is not available on your system!\n" \
            "Install eSpeak first."))
        label.set_justify(gtk.JUSTIFY_CENTER)
        dialog.vbox.pack_start(label)
        dialog.vbox.show_all()
        dialog.run()
        dialog.destroy()
        return

        
    def show_language_dialog(widget, args=dialog):
        """Shows Languages dialog."""

        widget.set_value(show_items_dialog(args, widget, tts.get_languages(), \
            _('Language')))
        

    def show_voice_dialog(widget, args=dialog):
        """Shows Voices dialog."""
        
        widget.set_value(show_items_dialog(args, widget, \
            [_('Male'), _('Female')], _('Voice')))
        

    def show_speed_dialog(widget, args=dialog):
        """Shows PronunciationSpeed dialog."""

        widget.set_value(show_items_dialog(args, widget, [str(speed) for speed \
            in range(tts.MIN_SPEED_VALUE, tts.MAX_SPEED_VALUE)], \
            _('Pronunciation speed')))

        
    def show_pitch_dialog(widget, args=dialog):
        """Shows VoicePitch dialog."""

        widget.set_value(show_items_dialog(args, widget, [str(pitch) for pitch \
            in range(tts.MIN_SPEED_VALUE, tts.MAX_SPEED_VALUE)], \
            _('Voice pitch')))


    # create widgets
    widgets_box = gtk.VBox()
    widgets_box.set_spacing(4)

    language_button = hildon.Button(gtk.HILDON_SIZE_AUTO | \
        gtk.HILDON_SIZE_FINGER_HEIGHT, hildon.BUTTON_ARRANGEMENT_VERTICAL, \
        _('Language'), config['tts_language']) 
    language_button.set_style(hildon.BUTTON_STYLE_PICKER)
    language_button.set_alignment(0, 0, 0, 0)
    language_button.connect('clicked', show_language_dialog)
    widgets_box.pack_start(language_button, expand=False, fill=False)

    voice_button = hildon.Button(gtk.HILDON_SIZE_AUTO | \
        gtk.HILDON_SIZE_FINGER_HEIGHT, hildon.BUTTON_ARRANGEMENT_VERTICAL, \
        _('Voice'), config['tts_voice']) 
    voice_button.set_style(hildon.BUTTON_STYLE_PICKER)
    voice_button.set_alignment(0, 0, 0, 0)
    voice_button.connect('clicked', show_voice_dialog)
    widgets_box.pack_start(voice_button, expand=False, fill=False)

    speed_button = hildon.Button(gtk.HILDON_SIZE_AUTO | \
        gtk.HILDON_SIZE_FINGER_HEIGHT, hildon.BUTTON_ARRANGEMENT_VERTICAL, \
        _('Pronunciation speed'), str(config['tts_speed'])) 
    speed_button.set_style(hildon.BUTTON_STYLE_PICKER)
    speed_button.set_alignment(0, 0, 0, 0)
    speed_button.connect('clicked', show_speed_dialog)
    widgets_box.pack_start(speed_button, expand=False, fill=False)
    
    pitch_button = hildon.Button(gtk.HILDON_SIZE_AUTO | \
        gtk.HILDON_SIZE_FINGER_HEIGHT, hildon.BUTTON_ARRANGEMENT_VERTICAL, \
        _('Voice pitch'), str(config['tts_pitch'])) 
    pitch_button.set_style(hildon.BUTTON_STYLE_PICKER)
    pitch_button.set_alignment(0, 0, 0, 0)
    pitch_button.connect('clicked', show_pitch_dialog)
    widgets_box.pack_start(pitch_button, expand=False, fill=False)
    
    widgets_box.show_all()

    dialog.vbox.add(widgets_box) 
    dialog.add_button(_('Save'), gtk.RESPONSE_OK)
    
    response = dialog.run()
    if response == gtk.RESPONSE_OK:
        config['tts_language'] = language_button.get_value()
        config['tts_voice'] = voice_button.get_value()
        config['tts_speed'] = int(speed_button.get_value())
        config['tts_pitch'] = int(pitch_button.get_value())
    dialog.destroy()
