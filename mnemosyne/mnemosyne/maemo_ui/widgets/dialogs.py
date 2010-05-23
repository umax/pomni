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
    program_name_label.set_markup("<span foreground='white' size='large'><b>" \
        "Mnemosyne for Maemo</b></span>\n<span foreground='white' size=" \
        "'medium'>version 2.0.0~beta11~rc1</span>\n")
    
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

        import gobject
        chooser = gobject.new(hildon.FileChooserDialog, \
            action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
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


def show_import_dialog(file_formats, current_format, database):
    """Shows ImportCards dialog."""
    
    from mnemosyne.libmnemosyne.file_formats.mnemosyne_XML import MnemosyneXML

    def update_tags(current_format_description, tags_button, selected_tags):
        """Updates tags UI."""

        if current_format_description == MnemosyneXML.description:
            tags_button.set_sensitive(False)
            tags_button.set_value(_('Using XML tags'))
        else:
            tags_button.set_sensitive(True)
            tags_button.set_value(', '.join(selected_tags))

            
    # callbacks
    def change_format_cb(widget, window, formats, tags_button, \
        selected_tags, update_tags):
        """Changes current file format and updates UI."""
    
        selected_format = show_items_dialog(window, widget, formats, \
            _('File format'))
        widget.set_value(selected_format)
        update_tags(selected_format, tags_button, selected_tags)
       

    def add_new_tag_cb(widget, tags_button, tags):
        """Creates new tag and updates UI."""

        dialog = hildon.Dialog()
        dialog.set_title(_('New tag'))
        entry = hildon.Entry(gtk.HILDON_SIZE_AUTO)
        entry.show()
        dialog.vbox.pack_start(entry)
        dialog.add_button(_('Add'), gtk.RESPONSE_OK)
        dialog.run()
        tag_name = entry.get_text()
        dialog.destroy()
        if tag_name:
            tags.append(tag_name)


    def set_file_cb(widget):
        """Shows FileChooser dialog to open file."""
          
        import gobject
        dialog = gobject.new(hildon.FileChooserDialog, \
            action=gtk.FILE_CHOOSER_ACTION_OPEN)
        dialog.run()
        fname = dialog.get_filename()
        dialog.destroy()
        if fname:
            widget.set_value(fname)
                                  
                                            
    def select_tags_cb(widget, window, tags, selected_tags, tags_button):
        """Creates TagsSelection dialog UI."""

        selector = hildon.TouchSelector(text=True) 
    
        # fill tags list
        for tag in selected_tags:
            if not tag in tags:
                tags.append(tag)
                
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
        dialog.set_title(_('Tags for new cards'))
        dialog.set_selector(selector)
        dialog.run()
        indexes_of_selected_tags = [item[0] for item in \
            selector.get_selected_rows(0)]
        model = selector.get_model(0)
        selected_tags[:] = []
        for index in indexes_of_selected_tags:
            selected_tags.append(unicode(model[index][0]))
        dialog.destroy()
        tags_button.set_value(', '.join(selected_tags))


    formats = {}
    fname = None  
    tags = [tag.name for tag in database.get_tags()]
    selected_tags = [_(u'<default>')]
    

    for _format in file_formats:
        formats[_format.description] = _format.filename_filter

    dialog = hildon.Dialog()
    dialog.set_title(_('Import cards'))
  
    # create widgets
    format_button = hildon.Button(gtk.HILDON_SIZE_AUTO | \
        gtk.HILDON_SIZE_FINGER_HEIGHT, hildon.BUTTON_ARRANGEMENT_VERTICAL, \
        _('File format'), current_format.description) 
    format_button.set_style(hildon.BUTTON_STYLE_PICKER)
    format_button.set_alignment(0, 0, 0, 0)
    
    file_button = hildon.Button(gtk.HILDON_SIZE_AUTO | \
        gtk.HILDON_SIZE_FINGER_HEIGHT, hildon.BUTTON_ARRANGEMENT_VERTICAL, \
        _('File to import from'), _('Select file')) 
    file_button.set_style(hildon.BUTTON_STYLE_PICKER)
    file_button.set_alignment(0, 0, 0, 0)
   
    tags_button = hildon.Button(gtk.HILDON_SIZE_AUTO | \
        gtk.HILDON_SIZE_FINGER_HEIGHT, hildon.BUTTON_ARRANGEMENT_VERTICAL, \
        _('Tags for new cards'), ', '.join(selected_tags)) 
    tags_button.set_style(hildon.BUTTON_STYLE_PICKER)
    tags_button.set_alignment(0, 0, 0, 0)
  
    new_tag_button = hildon.Button(gtk.HILDON_SIZE_AUTO | \
        gtk.HILDON_SIZE_FINGER_HEIGHT, hildon.BUTTON_ARRANGEMENT_VERTICAL, \
        _('New tag'), '') 
    new_tag_button.set_style(hildon.BUTTON_STYLE_NORMAL)
    new_tag_button.set_alignment(0.5, 0.5, 0, 0)
    new_tag_button.show()
    
    # connect signals
    format_button.connect('clicked', change_format_cb, dialog, formats.keys(), \
        tags_button, selected_tags, update_tags)
    new_tag_button.connect('clicked', add_new_tag_cb, tags_button, tags)
    file_button.connect('clicked', set_file_cb)
    tags_button.connect('clicked', select_tags_cb, dialog, tags, \
        selected_tags, tags_button)

    # packing widgets
    dialog.vbox.pack_start(format_button)
    dialog.vbox.pack_start(file_button)
    dialog.vbox.pack_start(tags_button)
    dialog.action_area.pack_start(new_tag_button)
    dialog.add_button(_('Import'), gtk.RESPONSE_OK)
    dialog.vbox.show_all()

    # updates ui
    update_tags(current_format.description, tags_button, selected_tags)

    response = dialog.run()
    dialog.destroy()
    if response == gtk.RESPONSE_OK:
        print fname
        print 'import'
    
    
def show_sync_dialog():
    """Shows Sync dialog."""

    dialog = hildon.Dialog()
    dialog.set_title(_('Sync'))
      
    label = gtk.Label("\nSync feature is not implemented yet :(\n" \
        "It will be available soon!\n")
    label.set_justify(gtk.JUSTIFY_CENTER)
    dialog.vbox.pack_start(label)
    dialog.vbox.show_all()

    dialog.run()
    dialog.destroy()
    
