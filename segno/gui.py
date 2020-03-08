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
        page = notebook.nametowidget(tab_name)
        if not page.validate():
            return
        try:
            qrcode_label.qr = page.generate_qr()
            qrcode_designator.configure(text=qrcode_label.qr.designator)
            update_image()
        except Exception as ex:
            messagebox.showerror(_('Error'), str(ex) or _('Internal error'))


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
        btn.reset()
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


def notebook_tab_changed(evt):
    """

    """
    widget = evt.widget
    prev_tab = widget.tab_previous
    tab_current = widget.select()
    if prev_tab != tab_current:
        if prev_tab is not None:
            widget.nametowidget(prev_tab).lost_focus()
        if tab_current is not None:
            widget.nametowidget(tab_current).got_focus()
        widget.tab_previous = tab_current


def _grid(widget, row=0, col=0, sticky='w', padx=5, pady=5, **kw):
    widget.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky, **kw)


def _label_input(parent, label, input_, row, col=0):
    _grid(Label(parent, text=label), row=row, col=col)
    _grid(input_, row=row, col=col+1)


class NotebookPage(Frame):
    """\

    """
    def __init__(self, parent, page_name, **kw):
        Frame.__init__(self, parent, padding='2 5', **kw)
        self.page_name = page_name

    def validate(self):
        """\
        Validates the page and returns the result.

        Returns ``True`` by default, assuming that everything is okay.
        """
        return True

    def generate_qr(self):
        """\
        Creates a QRCode instance based on the information provided collected
        by this page.
        """
        raise NotImplementedError('"generate_qr" must be implemented')

    def lost_focus(self):
        """\
        Called after the page has lost the focus. Does nothing by default.
        """
        pass

    def got_focus(self):
        """\
        Called after the page got the focus. Does nothing by default.
        """
        pass


class PageText(NotebookPage):
    """\

    """
    def __init__(self, parent):
        NotebookPage.__init__(self, parent, page_name=_('Text'))
        text_widget = ScrolledText(self, height=10)
        _grid(Label(self, text=_('Text')), sticky='wn')
        text_widget.insert(END, _initial_text)
        _grid(text_widget, col=1, sticky='wens')
        self.text_widget = text_widget

    def generate_qr(self):
        return make_qr(self.text_widget.get('1.0', 'end-1c'))


class PageEPC(NotebookPage):
    """\

    """
    def __init__(self, parent):
        NotebookPage.__init__(self, parent, page_name=_('EPC'))
        self._name_var = StringVar()
        self._iban_var = StringVar()
        self._bic_var = StringVar()
        self._amount_var = StringVar()
        self._text_var = StringVar()
        self._reference_var = StringVar()
        self._purpose_var = StringVar()
        label_input = partial(_label_input, self)
        _grid(Label(self, text=_('Recipient')), row=0)
        _grid(Entry(self, textvariable=self._name_var, width=65), row=0, col=1, columnspan=4)
        label_input(_('IBAN'),
                    Entry(self, textvariable=self._iban_var, width=13), row=1)
        label_input(_('Amount'),
                    Entry(self, textvariable=self._amount_var, width=12), row=2)
        label_input(_('Text'),
                    Entry(self, textvariable=self._text_var), row=3)
        _grid(tk.Label(self, text=_('or'), fg='#585858'), row=3, col=2, sticky=None)
        label_input(_('Creditor Ref.'),
                    Entry(self, textvariable=self._reference_var), row=3, col=3)
        label_input(_('BIC'),
                    Entry(self, textvariable=self._bic_var, width=11), row=4)
        label_input(_('Purpose'),
                    Entry(self, textvariable=self._purpose_var, width=4), row=5)
        self._encoding_cb = Combobox(self, values=(_('Automatic'), 'UTF-8', 'ISO-8859-1',
                                                   'ISO-8859-2', 'ISO-8859-4', 'ISO-8859-5',
                                                   'ISO-8859-7', 'ISO-8859-10', 'ISO-8859-15'))
        self._encoding_cb.current(0)
        label_input(_('Encoding'), self._encoding_cb, row=6)

    def lost_focus(self):
        self._update_qrcode_group(enabled=True)

    def got_focus(self):
        self._update_qrcode_group(enabled=False)

    @staticmethod
    def _update_qrcode_group(enabled):
        """\

        """
        state = 'normal' if enabled else 'disabled'
        for child in qr_group.winfo_children():
            child.configure(state=state)

    def generate_qr(self):
        encoding = self._encoding_cb.get() if self._encoding_cb.current() != 0 else None
        return segno.helpers.make_epc_qr(name=self._name_var.get(),
                                         iban=self._iban_var.get(),
                                         amount=self._amount_var.get(),
                                         text=self._text_var.get(),
                                         reference=self._reference_var.get(),
                                         bic=self._bic_var.get(),
                                         purpose=self._purpose_var.get(),
                                         encoding=encoding)

    def validate(self):
        #TODO
        return True


class PageWiFi(NotebookPage):
    """\

    """
    def __init__(self, parent):
        NotebookPage.__init__(self, parent, _('Wi-Fi'))
        self._ssid_var = StringVar()
        self._password_var = StringVar()
        self._hidden_var = BooleanVar()
        label_input = partial(_label_input, self)
        label_input(_('SSID'), Entry(self, textvariable=self._ssid_var), row=0)
        label_input(_('Password'), Entry(self, show='*', textvariable=self._password_var), row=1)
        self._wifi_security = Combobox(self, values=('-', 'WEP', 'WPA'))
        label_input(_('Security'), self._wifi_security, row=2)
        _grid(Checkbutton(self, text=_('Hidden'), variable=self._hidden_var, onvalue=True, offvalue=False), row=3, columnspan=2)

    def generate_qr(self):
        security = self._wifi_security.get()
        if security in ('-', ''):
            security = None
        return make_qr(segno.helpers.make_wifi_data(ssid=self._ssid_var.get(),
                                                    password=self._password_var.get(),
                                                    security=security,
                                                    hidden=self._hidden_var.get()))


class ColorPickerWidget(Frame):
    """\

    """
    def __init__(self, parent, type, color, label, **kw):
        Frame.__init__(self, parent, **kw)
        self._hex_var = StringVar()
        self._entry = Entry(self, textvariable=self._hex_var, width=7)
        self._btn = tk.Button(self, width=1, height=1, command=self._pick_color)
        self._btn_color_default = self._btn.cget('background')
        self.type = type
        self._type_color = color
        self.label = label
        self._entry.grid(sticky='w')
        self._btn.grid(row=0, column=1, sticky='w')
        self._hex_var.trace('w', lambda name, index, mode: self._update_btn())

    def _update_btn(self):
        try:
            self._btn['bg'] = self._hex_var.get()
            output_config[self.label] = self._hex_var.get()
        except:
            output_config[self.label] = self._type_color
            self._btn['bg'] = self._btn_color_default
        update_image()

    def reset(self):
        """\

        """
        self._hex_var.set('')
        output_config.pop(self.label, None)
        btn = self._btn
        btn['bg'] = self._btn_color_default
        if self.label in ('dark', 'light'):
            self._hex_var.set(self._type_color)

    def _pick_color(self):
        rgb, name = colorchooser.askcolor(color=self._hex_var.get() or self._type_color)
        self._hex_var.set(name)


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
notebook.tab_previous = None
notebook.grid(row=0, column=0, columnspan=2, sticky='wens')
notebook.bind('<<NotebookTabChanged>>', notebook_tab_changed)
for page_cls in (PageText, PageWiFi, PageEPC):
    page = page_cls(notebook)
    notebook.add(page, text=page.page_name)
#-- QR options
qr_group = LabelFrame(left_frame, text=_('QR Code options'))
qr_group.grid(row=1, column=0, padx=5, pady=5, sticky='wens')
version_cb = Combobox(qr_group, values=[_('Automatic'), 'M1', 'M2', 'M3', 'M4'] + [str(i) for i in range(1, 41)])
version_cb.current(0)
_label_input(qr_group, _('Version'), version_cb, row=0)
version_cb.bind("<<ComboboxSelected>>", update_generate_config)
qrcode_only_val = BooleanVar()
_grid(Checkbutton(qr_group, text=_('Only QR Codes (no Micro QR Codes)'),
                  onvalue=True, offvalue=False, variable=qrcode_only_val,
                  command=update_generate_config),
      row=1, columnspan=2)
qrcode_only_val.set(False)
error_cb = Combobox(qr_group, values=[_('Automatic'), 'L (7%)', 'M (15%)', 'Q (25%)', 'H (30%)'])
error_cb.current(0)
error_cb.bind("<<ComboboxSelected>>", update_generate_config)
_label_input(qr_group, _('Error-Level'), error_cb, row=2)
boost_error_val = BooleanVar()
boost_error_val.set(generate_config['boost_error'])
_grid(Checkbutton(qr_group, text=_('Boost error correction level'), onvalue=True, offvalue=False,
                  variable=boost_error_val, command=update_generate_config),
      row=3, columnspan=2)
#-- Output options
output_group = LabelFrame(left_frame, text=_('Output options'))
output_group.grid(row=2, column=0, padx=5, pady=5, sticky='wens')
border_val = StringVar()
_label_input(output_group, _('Border'),
             Spinbox(output_group, textvariable=border_val, values=[_('Automatic')] + [str(i) for i in range(0, 21)],), row=0)
scale_val = StringVar()
_label_input(output_group, _('Scale'), Spinbox(output_group, values=[str(i) for i in range(1, 81)], textvariable=scale_val), row=1)
border_val.set(_('Automatic'))
scale_val.set(output_config['scale'])
border_val.trace('w', lambda name, index, mode: update_output_config())
scale_val.trace('w', lambda name, index, mode: update_output_config())
#-- Color options
color_group = LabelFrame(left_frame, text=_('Colors'))
_grid(color_group, row=1, col=1, rowspan=2, sticky='wens')
_grid(Label(color_group, text=_('Dark')), col=1, sticky='wn')
_grid(Label(color_group, text=_('Light')), col=2, sticky='wn')
_module_types = ('General', 'Alignment', 'Dark module', 'Data', 'Finder',
                 'Format', 'Quiet zone', 'Separator', 'Timing', 'Version')
color_buttons = []
for idx, name in enumerate(_module_types, start=1):
    label = Label(color_group, text=_(name))
    _grid(label, row=idx, sticky='wn')
    lbl = name.lower().replace('general', '').replace(' ', '_')
    for typ, clr in (('dark', '#000'), ('light', '#fff')):
        if typ == 'dark' and lbl in ('quiet_zone', 'separator'):
            continue
        if typ == 'light' and lbl == 'dark_module':
            continue
        label = lbl + '_{0}'.format(typ) if lbl else typ
        if label.count('_') > 1 or lbl == 'separator':
            label = label[:label.rfind('_')]
        wg = ColorPickerWidget(color_group, type=typ, color=clr, label=label)
        col, padx = (1, 0) if typ == 'dark' else (2, 5)
        wg.grid(row=idx, column=col, padx=padx)
        color_buttons.append(wg)
_grid(Button(color_group, text=_('Reset'), command=reset_colors), row=idx+1, sticky='wn')
tk.Label(left_frame, text='"QR Code" and "Micro QR Code" are registered trademarks of DENSO WAVE INCORPORATED.', fg='#585858')\
    .grid(row=3, columnspan=2, sticky='w')
#-- Right frame
# Buttons
btn_frame = Frame(right_frame)
btn_frame.grid(sticky='wn')
Label(btn_frame, text='').grid(row=0, columnspan=3)  # Extra space to align the btns to the notebook
generate_btn = Button(btn_frame, text=_('Generate'), command=generate_qr)
_grid(generate_btn, row=1)
master.bind('<Control-g>', lambda evt: generate_qr())
save_fn = lambda evt=None: save(qrcode_label.qr, output_config)
save_btn = Button(btn_frame, text=_('Save'), command=save_fn)
_grid(save_btn, row=1, col=1)
master.bind('<Control-s>', save_fn)
# Image
qrcode_image = PhotoImage(data=make_image(qrcode, output_config))
qrcode_label = Label(right_frame, image=qrcode_image)
qrcode_label.image = qrcode_image
qrcode_label.qr = qrcode
_grid(qrcode_label, row=2, columnspan=2, sticky='n')
qrcode_designator = Label(right_frame, text=qrcode.designator)
_grid(qrcode_designator, row=3, columnspan=2, sticky='n')

reset_colors()


def main():
    master.mainloop()


if __name__ == '__main__':
    main()

