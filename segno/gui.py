#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2020 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Tkinter GUI.

"QR Code" and "Micro QR Code" are registered trademarks of DENSO WAVE INCORPORATED.
"""
from __future__ import absolute_import, unicode_literals
try:
    import tkinter as tk
    from tkinter import *
    from tkinter.ttk import *
    from tkinter import filedialog
    from tkinter import colorchooser
    from tkinter import messagebox
    from tkinter.scrolledtext import ScrolledText
except ImportError:  # Py2
    import Tkinter as tk
    from Tkinter import *
    from ttk import *
    import tkFileDialog as filedialog
    import tkColorChooser as colorchooser
    import tkMessageBox as messagebox
    from ScrolledText import ScrolledText
import locale
import base64
from functools import partial
import io
import segno
import segno.helpers

__all__ = ()

_ICON = """\
UDYgIyBDcmVhdGVkIGJ5IFNlZ25vIDxodHRwczovL3B5cGkub3JnL3Byb2plY3Qvc2Vnbm8vPgoz
MCAzMCAyNTUKFRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7////////
FRd7FRd7////////FRd7FRd7////////FRd7FRd7////////FRd7FRd7FRd7FRd7FRd7FRd7FRd7
FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7////////FRd7FRd7////////FRd7FRd7////////
FRd7FRd7////////FRd7FRd7FRd7FRd7////////////////////////////////////////FRd7
FRd7////////////////FRd7FRd7FRd7FRd7FRd7FRd7////////////////FRd7FRd7FRd7FRd7
////////////////////////////////////////FRd7FRd7////////////////FRd7FRd7FRd7
FRd7FRd7FRd7////////////////FRd7FRd7FRd7FRd7////////FRd7FRd7FRd7FRd7FRd7FRd7
////////FRd7FRd7////////////////FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7
FRd7FRd7FRd7////////FRd7FRd7FRd7FRd7FRd7FRd7////////FRd7FRd7////////////////
FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7////////FRd7FRd7FRd7
FRd7FRd7FRd7////////FRd7FRd7////////////////FRd7FRd7FRd7FRd7////////////////
FRd7FRd7FRd7FRd7FRd7FRd7////////FRd7FRd7FRd7FRd7FRd7FRd7////////FRd7FRd7////
////////////FRd7FRd7FRd7FRd7////////////////FRd7FRd7FRd7FRd7FRd7FRd7////////
FRd7FRd7FRd7FRd7FRd7FRd7////////FRd7FRd7////////////////////////FRd7FRd7////
////////////FRd7FRd7FRd7FRd7FRd7FRd7////////FRd7FRd7FRd7FRd7FRd7FRd7////////
FRd7FRd7////////////////////////FRd7FRd7////////////////FRd7FRd7FRd7FRd7FRd7
FRd7////////////////////////////////////////FRd7FRd7////////FRd7FRd7FRd7FRd7
FRd7FRd7FRd7FRd7////////FRd7FRd7////////FRd7FRd7////////////////////////////
////////////FRd7FRd7////////FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7////////FRd7FRd7
////////FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7////////FRd7
FRd7FRd7FRd7////////////////FRd7FRd7FRd7FRd7////////FRd7FRd7FRd7FRd7FRd7FRd7
FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7////////FRd7FRd7FRd7FRd7////////////////FRd7
FRd7FRd7FRd7////////////////////////////////////////////////////////////////
////////////////FRd7FRd7FRd7FRd7////////////////////////FRd7FRd7////////////
////////////////////////////////////////////////////////////FRd7FRd7FRd7FRd7
////////////////////////FRd7FRd7FRd7FRd7////////////////////////FRd7FRd7FRd7
FRd7////////////////FRd7FRd7////////////////FRd7FRd7////////////////FRd7FRd7
FRd7FRd7////////////////////////FRd7FRd7FRd7FRd7////////////////FRd7FRd7////
////////////FRd7FRd7////////////////FRd7FRd7////////FRd7FRd7FRd7FRd7////////
////////////////FRd7FRd7FRd7FRd7FRd7FRd7////////FRd7FRd7FRd7FRd7////////////
////FRd7FRd7////////FRd7FRd7FRd7FRd7////////////////////////FRd7FRd7FRd7FRd7
FRd7FRd7////////FRd7FRd7FRd7FRd7////////////////FRd7FRd7FRd7FRd7FRd7FRd7////
////////////////////FRd7FRd7////////FRd7FRd7////////FRd7FRd7////////FRd7FRd7
FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7////////////////////////FRd7FRd7////
////FRd7FRd7////////FRd7FRd7////////FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7////////
////////FRd7FRd7FRd7FRd7////////FRd7FRd7////////FRd7FRd7////////////////FRd7
FRd7FRd7FRd7FRd7FRd7FRd7FRd7////////////////////////FRd7FRd7FRd7FRd7////////
FRd7FRd7////////FRd7FRd7////////////////FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7////
////FRd7FRd7FRd7FRd7////////FRd7FRd7FRd7FRd7FRd7FRd7////////FRd7FRd7FRd7FRd7
FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7////////FRd7FRd7FRd7FRd7FRd7FRd7////////FRd7
FRd7FRd7FRd7FRd7FRd7////////FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7
////////FRd7FRd7////////FRd7FRd7FRd7FRd7FRd7FRd7FRd7FRd7////////////////////
////////////////////////////////////FRd7FRd7////////FRd7FRd7////////FRd7FRd7
FRd7FRd7FRd7FRd7FRd7FRd7////////////////////////////////////////////////////
////FRd7FRd7////////FRd7FRd7FRd7FRd7////////FRd7FRd7////////FRd7FRd7FRd7FRd7
////////FRd7FRd7////////FRd7FRd7FRd7FRd7////////FRd7FRd7FRd7FRd7FRd7FRd7FRd7
FRd7////////FRd7FRd7////////FRd7FRd7FRd7FRd7////////FRd7FRd7////////FRd7FRd7
FRd7FRd7////////FRd7FRd7FRd7FRd7FRd7FRd7"""


def _(s):
    return s

_initial_text = _('Welcome to Segno')

generate_config = dict(boost_error=True)
output_config = dict(scale=3, dark='#000', light='#fff', border=None)
qrcode = segno.make(_initial_text)


def make_image(qr, config):
    out = io.BytesIO()
    try:
        qr.save(out, kind='ppm', **config)
    except ValueError as ex:
        messagebox.showerror(_('Error'), str(ex))
    return out.getvalue()


def generate_qr():
    tab_name = notebook.select()
    if tab_name:
        qrcode_label.qr = notebook.nametowidget(tab_name).generate_qr()
        qrcode_designator.configure(text=qrcode_label.qr.designator)
        update_image()


def save(qrcode, config):
    files = [(_('PNG image'), '*.png'),
             (_('SVG document'), '*.svg'),
             (_('PPM image'), '*.ppm'),
             ]
    f = filedialog.asksaveasfile(filetypes=files)
    if f is None:
        return
    fn = f.name
    f.close()
    qrcode.save(fn, **config)


def choose_color(btn):
    rgb, name = colorchooser.askcolor(color=btn.color)
    if name is not None:
        btn['bg'] = name
        btn.color = name
        btn.use_color = False
        output_config[btn.label] = name
        update_image()


def reset_colors():
    for btn in color_buttons:
        output_config.pop(btn.label, None)
        btn['bg'] = btn.bg_default
        btn.color = '#000' if btn.type == 'dark' else '#fff'
        if btn.label in ('dark', 'light'):
            btn['bg'] = btn.color
        output_config.pop(btn.label, None)
    output_config['dark'] = '#000'
    output_config['light'] = '#fff'
    update_image()


def update_output_config(evt=None):
    border = None
    try:
        border = int(border_val.get())
    except ValueError:
        pass
    output_config['border'] = border
    scale = 1
    if scale_val.get().strip():
        try:
            scale = int(scale_val.get())
        except ValueError:
            scale_val.set(1)
        if scale > 80:
            messagebox.showerror(_('Scale too large'), 'Please choose another scaling value')
            scale_val.set(80)
        output_config['scale'] = scale


def update_generate_config(evt=None):
    generate_config['version'] = version_cb.get() if version_cb.current() != 0 else None
    generate_config['error'] = error_cb.get()[:1] if error_cb.current() != 0 else None
    generate_config['boost_error'] = boost_error_val.get()
    micro = not qrcode_only_val.get()
    if micro:
        micro = None
    generate_config['micro'] = micro


def update_image():
    qrcode_label.image = PhotoImage(data=make_image(qrcode_label.qr, output_config))
    qrcode_label.configure(image=qrcode_label.image)


def make_qr(content):
    try:
        return segno.make(content, **generate_config)
    except segno.DataOverflowError:
        messagebox.showerror(_('Too much data'), _('Too much data for the (Micro) QR Code. Try to set the version to "Automatic"'))
        return qrcode_label.qr
    except ValueError as ex:
        messagebox.showerror(_('Error'), str(ex))
        return qrcode_label.qr


def page_text_generate_qr():
    return make_qr(text_widget.get('1.0', 'end-1c'))


def page_wifi_generate_qr():
    security = wifi_security.get()
    if security in ('-', ''):
        security = None
    return make_qr(segno.helpers.make_wifi_data(ssid=wifi_ssid.get(),
                                                password=wifi_password.get(),
                                                security=security,
                                                hidden=wifi_hidden.get()))

master = Tk()
master.title('Segno v{}'.format(segno.__version__))
master.tk.call('wm', 'iconphoto', master._w, PhotoImage(data=base64.b64decode(_ICON)))

frame = Frame(master, padding='5 5')
frame.grid()

left_frame = Frame(frame)
left_frame.grid(row=0, column=0, sticky='n')
right_frame = Frame(frame)
right_frame.grid(row=0, column=1, sticky='n')

#-- Left frame
# Notebook
notebook = Notebook(left_frame)
notebook.grid(row=0, column=0, columnspan=2, sticky='wens')
# Page text
page_text = Frame(notebook)
Label(page_text, text=_('Text')).grid(row=0, padx=5, pady=5, sticky='wn')
text_widget = ScrolledText(page_text, height=10)
text_widget.insert(END, _initial_text)
text_widget.grid(row=0, column=1, padx=5, pady=5, sticky='wens')
page_text.generate_qr = page_text_generate_qr
notebook.add(page_text, text=_('Text'))
# Page wifi
page_wifi = Frame(notebook)
Label(page_wifi, text=_('SSID')).grid(row=0, column=0, padx=5, pady=5, sticky='w')
wifi_ssid = StringVar()
wifi_password = StringVar()
wifi_hidden = BooleanVar()
Entry(page_wifi, textvariable=wifi_ssid).grid(row=0, column=1, padx=5, pady=5, sticky='w')
Label(page_wifi, text=_('Password')).grid(row=1, column=0, padx=5, pady=5, sticky='w')
Entry(page_wifi, show='*', textvariable=wifi_password).grid(row=1, column=1, padx=5, pady=5, sticky='w')
Label(page_wifi, text=_('Security')).grid(row=2, column=0, padx=5, pady=5, sticky='w')
wifi_security = Combobox(page_wifi, values=('-', 'WEP', 'WPA'))
wifi_security.grid(row=2, column=1, padx=5, pady=5, sticky='w')
Checkbutton(page_wifi, text=_('Hidden'), variable=wifi_hidden, onvalue=True, offvalue=False).grid(row=3, padx=5, pady=5)
page_wifi.generate_qr = page_wifi_generate_qr
notebook.add(page_wifi, text=_('Wi-Fi'))
# Page EPC
page_epc = Frame(notebook)
epc_name = StringVar()
epc_iban = StringVar()
Label(page_epc, text=_('Recipient')).grid(row=0, column=0, padx=5, pady=5, sticky='w')
Entry(page_epc, textvariable=epc_name).grid(row=0, column=1, padx=5, pady=5, sticky='w')
Label(page_epc, text=_('IBAN')).grid(row=1, column=0, padx=5, pady=5, sticky='w')
Entry(page_epc, textvariable=epc_iban).grid(row=1, column=1, padx=5, pady=5, sticky='w')
notebook.add(page_epc, text=_('EPC'))
#-- QR options
qr_group = LabelFrame(left_frame, text=_('QR Code options'))
qr_group.grid(row=1, column=0, padx=5, pady=5, sticky='wens')
Label(qr_group, text=_('Version')).grid(row=0, padx=5, pady=5, sticky='wn')
version_cb = Combobox(qr_group, values=[_('Automatic'), 'M1', 'M2', 'M3', 'M4'] + [str(i) for i in range(1, 41)])
version_cb.grid(row=0, column=1, padx=5, pady=5, sticky='wn')
version_cb.current(0)
version_cb.bind("<<ComboboxSelected>>", update_generate_config)
qrcode_only_val = BooleanVar()
Checkbutton(qr_group, text=_('Only QR Codes (no Micro QR Codes)'), onvalue=True, offvalue=False, variable=qrcode_only_val,
            command=update_generate_config).grid(row=1, columnspan=2, padx=5, pady=5, sticky='w')
qrcode_only_val.set(False)
Label(qr_group, text=_('Error-Level')).grid(row=2, padx=5, pady=5, sticky='wn')
error_cb = Combobox(qr_group, values=[_('Automatic'), 'L (7%)', 'M (15%)', 'Q (25%)', 'H (30%)'])
error_cb.grid(row=2, column=1, padx=5, pady=5, sticky='wn')
error_cb.current(0)
error_cb.bind("<<ComboboxSelected>>", update_generate_config)
boost_error_val = BooleanVar()
boost_error_val.set(generate_config['boost_error'])
Checkbutton(qr_group, text=_('Boost error correction level'), onvalue=True, offvalue=False, variable=boost_error_val,
            command=update_generate_config).grid(row=3, columnspan=2, padx=5, pady=5, sticky='w')
#-- Output options
output_group = LabelFrame(left_frame, text=_('Output options'))
output_group.grid(row=2, column=0, padx=5, pady=5, sticky='wens')
Label(output_group, text=_('Border')).grid(row=0, column=0, padx=5, pady=5, sticky='w')
border_val = StringVar()
Spinbox(output_group, textvariable=border_val, values=[_('Automatic')] + [str(i) for i in range(0, 21)],)\
    .grid(row=0, column=1, padx=5, pady=5, sticky='w')
Label(output_group, text=_('Scale')).grid(row=1, column=0, padx=5, pady=5, sticky='w')
scale_val = StringVar()
Spinbox(output_group, values=[str(i) for i in range(1, 81)], textvariable=scale_val).grid(row=1, column=1, padx=5, pady=5, sticky='w')
border_val.set(_('Automatic'))
scale_val.set(output_config['scale'])
border_val.trace('w', lambda name, index, mode: update_output_config())
scale_val.trace('w', lambda name, index, mode: update_output_config())
#-- Color options
color_group = LabelFrame(left_frame, text=_('Colors'))
color_group.grid(row=1, column=1, rowspan=2, padx=5, pady=5, sticky='wens')
Label(color_group, text=_('Dark')).grid(row=0, column=1, padx=5, pady=5, sticky='wn')
Label(color_group, text=_('Light')).grid(row=0, column=2, padx=5, pady=5, sticky='wn')
_module_types = ('General', 'Alignment', 'Dark module', 'Data', 'Finder',
                 'Format', 'Quiet zone', 'Separator', 'Timing', 'Version')
color_buttons = []
for idx, name in enumerate(_module_types, start=1):
    Label(color_group, text=_(name)).grid(row=idx, padx=5, pady=5, sticky='wn')
    lbl = name.lower().replace('general', '').replace(' ', '_')
    if name not in ('Quiet zone', 'Separator'):
        bg = '#000'
        btn = tk.Button(color_group, width=1, height=1)
        btn.type = 'dark'
        btn.bg_default = btn.cget('background')
        btn.label = lbl + '_dark' if lbl else 'dark'
        btn.color = bg
        if btn.label.count('_') > 1:
            btn.label = btn.label[:btn.label.rfind('_')]
        btn.grid(row=idx, column=1, padx=2, pady=2)
        btn.configure(command=partial(choose_color, btn))
        if btn.label == 'dark':
            btn['bg'] = bg
        color_buttons.append(btn)
    if name != 'Dark module':
        bg = '#fff'
        btn = tk.Button(color_group, width=1, height=1)
        btn.type = 'light'
        btn.bg_default = btn.cget('background')
        btn.color = bg
        btn.label = lbl + '_light' if lbl else 'light'
        if btn.label == 'separator_light' or btn.label.count('_') > 1:
            btn.label = btn.label[:btn.label.rfind('_')]
        btn.grid(row=idx, column=2, padx=2, pady=2)
        btn.configure(command=partial(choose_color, btn))
        if btn.label == 'light':
            btn['bg'] = bg
        color_buttons.append(btn)
Button(color_group, text=_('Reset'), command=reset_colors).grid(row=idx+1, padx=5, pady=5, sticky='wn')
tk.Label(left_frame, text='"QR Code" and "Micro QR Code" are registered trademarks of DENSO WAVE INCORPORATED.', fg='#585858').grid(row=3, columnspan=2, sticky='w')
#-- Right frame
# Buttons
Label(right_frame, text='').grid(row=0)  # Extra space to align the btns to the notebook
generate_btn = Button(right_frame, text=_('Generate'), command=generate_qr)
generate_btn.grid(row=1, padx=5, pady=5, sticky='w')
master.bind('<Control-g>', lambda evt: generate_qr())
save_fn = lambda evt=None: save(qrcode_label.qr, output_config)
save_btn = Button(right_frame, text=_('Save'), command=save_fn)
save_btn.grid(row=1, column=1, padx=5, pady=5, sticky='w')
master.bind('<Control-s>', save_fn)
# Image
qrcode_image = PhotoImage(data=make_image(qrcode, output_config))
qrcode_label = Label(right_frame, image=qrcode_image)
qrcode_label.image = qrcode_image
qrcode_label.qr = qrcode
qrcode_label.grid(row=2, columnspan=3, padx=5, pady=5, sticky='n')
qrcode_designator = Label(right_frame, text=qrcode.designator)
qrcode_designator.grid(row=3, columnspan=3)


def main():
    master.mainloop()


if __name__ == '__main__':
    main()

