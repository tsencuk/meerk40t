# -*- coding: ISO-8859-1 -*-
#
# generated by wxGlade 0.9.3 on Thu Jun 27 21:45:40 2019
#
import platform

import wx

from .icons import icons8_administrative_tools_50
from .mwindow import MWindow
from .propertiespanel import PropertiesPanel

_ = wx.GetTranslation

MILS_IN_MM = 39.3701


class PreferencesPanel(wx.Panel):
    def __init__(self, *args, context=None, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.context = context

        self.radio_units = wx.RadioBox(
            self,
            wx.ID_ANY,
            _("Units:"),
            choices=["mm", "cm", "inch", "steps"],
            majorDimension=1,
            style=wx.RA_SPECIFY_ROWS,
        )
        self.combo_svg_ppi = wx.ComboBox(
            self,
            wx.ID_ANY,
            choices=[
                _("96 px/in Inkscape"),
                _("72 px/in Illustrator"),
                _("90 px/in Old Inkscape"),
                _("Custom"),
            ],
            style=wx.CB_READONLY,
        )
        # self.text_svg_ppi = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        self.text_svg_ppi = wx.TextCtrl(self, wx.ID_ANY, "")

        self.text_scale_x = wx.TextCtrl(self, wx.ID_ANY, "1.000")
        self.text_scale_y = wx.TextCtrl(self, wx.ID_ANY, "1.000")
        self.checklist_options = PropertiesPanel(
            self, wx.ID_ANY, context=context, choices="preferences"
        )
        from .wxmeerk40t import supported_languages

        choices = [
            language_name
            for language_code, language_name, language_index in supported_languages
        ]
        self.combo_language = wx.ComboBox(
            self, wx.ID_ANY, choices=choices, style=wx.CB_READONLY
        )
        self.spin_bedwidth = wx.SpinCtrlDouble(
            self, wx.ID_ANY, str(self.context.device.bedwidth), min=1.0, max=80000.0, inc=MILS_IN_MM
        )
        self.spin_bedheight = wx.SpinCtrlDouble(
            self, wx.ID_ANY, str(self.context.device.bedheight), min=1.0, max=80000.0, inc=MILS_IN_MM
        )
        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.spin_on_bedwidth, self.spin_bedwidth)
        self.Bind(wx.EVT_TEXT, self.spin_on_bedwidth, self.spin_bedwidth)
        self.Bind(wx.EVT_TEXT_ENTER, self.spin_on_bedwidth, self.spin_bedwidth)
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.spin_on_bedheight, self.spin_bedheight)
        self.Bind(wx.EVT_TEXT, self.spin_on_bedheight, self.spin_bedheight)
        self.Bind(wx.EVT_TEXT_ENTER, self.spin_on_bedheight, self.spin_bedheight)
        self.Bind(wx.EVT_RADIOBOX, self.on_radio_units, self.radio_units)
        self.Bind(wx.EVT_COMBOBOX, self.on_combo_language, self.combo_language)
        self.Bind(wx.EVT_COMBOBOX, self.on_combo_svg_ppi, self.combo_svg_ppi)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_text_svg_ppi, self.text_svg_ppi)
        self.Bind(wx.EVT_TEXT, self.on_text_svg_ppi, self.text_svg_ppi)
        self.Bind(wx.EVT_TEXT, self.on_text_x_scale, self.text_scale_x)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_text_x_scale, self.text_scale_x)
        self.Bind(wx.EVT_TEXT, self.on_text_y_scale, self.text_scale_y)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_text_y_scale, self.text_scale_y)

    def pane_show(self):
        context_root = self.context.root

        context_root.setting(float, "svg_ppi", 96.0)
        self.text_svg_ppi.SetValue(str(context_root.elements.svg_ppi))

        self.context.setting(int, "language", 0)
        self.context.setting(str, "units_name", "mm")
        self.context.setting(int, "units_marks", 10)
        self.context.setting(int, "units_index", 0)
        self.context.setting(float, "units_convert", MILS_IN_MM)
        self.radio_units.SetSelection(self.context.units_index)
        self.combo_language.SetSelection(self.context.language)
        self.spin_bedwidth.SetValue(self.context.device.bedwidth)
        self.spin_bedheight.SetValue(self.context.device.bedheight)
        self.text_scale_x.SetValue("%.3f" % self.context.device.scale_x)
        self.text_scale_y.SetValue("%.3f" % self.context.device.scale_y)
        self.Children[0].SetFocus()

    def pane_hide(self):
        pass

    def __set_properties(self):
        self.radio_units.SetToolTip(_("Set default units for guides"))
        self.radio_units.SetSelection(0)
        self.combo_language.SetToolTip(_("Select the desired language to use."))
        self.combo_svg_ppi.SetToolTip(
            _("Select the Pixels Per Inch to use when loading an SVG file")
        )
        self.text_svg_ppi.SetMinSize((60, 23))
        self.text_svg_ppi.SetToolTip(
            _("Custom Pixels Per Inch to use when loading an SVG file")
        )
        self.spin_bedwidth.SetMinSize((80, 23))
        self.spin_bedwidth.SetToolTip(_("Width of the laser bed."))
        self.spin_bedheight.SetMinSize((80, 23))
        self.spin_bedheight.SetToolTip(_("Height of the laser bed."))
        self.text_scale_x.SetToolTip(
            _(
                "Scale factor for the X-axis. This defines the ratio of mils to steps. This is usually at 1:1 steps/mils but due to functional issues it can deviate and needs to be accounted for"
            )
        )
        self.text_scale_y.SetToolTip(
            _(
                "Scale factor for the Y-axis. This defines the ratio of mils to steps. This is usually at 1:1 steps/mils but due to functional issues it can deviate and needs to be accounted for"
            )
        )
        self.text_scale_x.Enable(False)
        self.text_scale_y.Enable(False)
        # end wxGlade

    def __do_layout(self):
        sizer_preferences = wx.BoxSizer(wx.HORIZONTAL)
        sizer_gui_options = wx.BoxSizer(wx.VERTICAL)
        sizer_bed = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Bed Dimensions:")), wx.HORIZONTAL
        )
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7 = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Y Scale Factor:")), wx.HORIZONTAL
        )
        sizer_4 = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("X Scale Factor:")), wx.HORIZONTAL
        )
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("SVG Pixels Per Inch:")), wx.HORIZONTAL
        )
        sizer_2 = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Language:")), wx.HORIZONTAL
        )
        sizer_gui_options.Add(self.radio_units, 0, wx.EXPAND, 0)
        sizer_2.Add(self.combo_language, 0, 0, 0)
        sizer_gui_options.Add(sizer_2, 0, wx.EXPAND, 0)
        sizer_3.Add(self.combo_svg_ppi, 0, 0, 0)
        sizer_3.Add((20, 20), 0, 0, 0)
        sizer_3.Add(self.text_svg_ppi, 1, 0, 0)
        sizer_gui_options.Add(sizer_3, 0, wx.EXPAND, 0)
        label_2 = wx.StaticText(self, wx.ID_ANY, _("Width"))
        sizer_5.Add(label_2, 0, 0, 0)
        sizer_5.Add(self.spin_bedwidth, 0, 0, 0)
        label_17 = wx.StaticText(self, wx.ID_ANY, _("steps"))
        sizer_5.Add(label_17, 0, 0, 0)
        sizer_bed.Add(sizer_5, 1, 0, 0)
        label_3 = wx.StaticText(self, wx.ID_ANY, _("Height"))
        sizer_6.Add(label_3, 0, 0, 0)
        sizer_6.Add(self.spin_bedheight, 0, 0, 0)
        label_18 = wx.StaticText(self, wx.ID_ANY, _("steps"))
        sizer_6.Add(label_18, 0, 0, 0)
        sizer_bed.Add(sizer_6, 1, 0, 0)
        sizer_gui_options.Add(sizer_bed, 0, 0, 0)
        sizer_4.Add(self.text_scale_x, 1, 0, 0)
        sizer_1.Add(sizer_4, 1, wx.EXPAND, 0)
        sizer_7.Add(self.text_scale_y, 1, 0, 0)
        sizer_1.Add(sizer_7, 1, wx.EXPAND, 0)
        sizer_gui_options.Add(sizer_1, 0, wx.EXPAND, 0)
        sizer_preferences.Add(sizer_gui_options, 0, wx.EXPAND, 0)
        sizer_preferences.Add(self.checklist_options, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_preferences)
        self.Layout()
        # end wxGlade

    def on_combo_svg_ppi(self, event=None):
        elements = self.context.elements
        ppi = self.combo_svg_ppi.GetSelection()
        if ppi == 0:
            elements.svg_ppi = 96.0
        elif ppi == 1:
            elements.svg_ppi = 72.0
        elif ppi == 2:
            elements.svg_ppi = 90.0
        else:
            elements.svg_ppi = 96.0
        self.text_svg_ppi.SetValue(str(elements.svg_ppi))

    def on_text_svg_ppi(self, event=None):
        elements = self.context.elements
        try:
            svg_ppi = float(self.text_svg_ppi.GetValue())
        except ValueError:
            return
        if svg_ppi == 96:
            if self.combo_svg_ppi.GetSelection() != 0:
                self.combo_svg_ppi.SetSelection(0)
        elif svg_ppi == 72:
            if self.combo_svg_ppi.GetSelection() != 1:
                self.combo_svg_ppi.SetSelection(1)
        elif svg_ppi == 90:
            if self.combo_svg_ppi.GetSelection() != 2:
                self.combo_svg_ppi.SetSelection(2)
        else:
            if self.combo_svg_ppi.GetSelection() != 3:
                self.combo_svg_ppi.SetSelection(3)
        elements.svg_ppi = svg_ppi

    def on_combo_language(self, event=None):
        lang = self.combo_language.GetSelection()
        if lang != -1 and self.context.app is not None:
            self.context.app.update_language(lang)

    def on_radio_units(self, event):
        if event.Int == 0:
            self.set_mm()
        elif event.Int == 1:
            self.set_cm()
        elif event.Int == 2:
            self.set_inch()
        elif event.Int == 3:
            self.set_mil()

    def set_inch(self):
        context_root = self.context.root
        p = context_root
        p.units_convert, p.units_name, p.units_marks, p.units_index = (
            1000.0,
            "inch",
            1,
            2,
        )
        p.signal("units")

    def set_mil(self):
        context_root = self.context.root
        p = context_root
        p.units_convert, p.units_name, p.units_marks, p.units_index = (
            1.0,
            "mil",
            1000,
            3,
        )
        p.signal("units")

    def set_cm(self):
        context_root = self.context.root
        p = context_root
        p.units_convert, p.units_name, p.units_marks, p.units_index = (
            393.7,
            "cm",
            1,
            1,
        )
        p.signal("units")

    def set_mm(self):
        context_root = self.context.root
        p = context_root
        p.units_convert, p.units_name, p.units_marks, p.units_index = (
            39.37,
            "mm",
            10,
            0,
        )
        p.signal("units")

    def spin_on_bedwidth(self, event=None):
        self.context.device.bedwidth = float(self.spin_bedwidth.GetValue())
        self.context.device.bedheight = float(self.spin_bedheight.GetValue())
        self.context.signal(
            "bed_size", (self.context.device.bedwidth, self.context.device.bedheight)
        )

    def spin_on_bedheight(self, event=None):
        self.context.device.bedwidth = float(self.spin_bedwidth.GetValue())
        self.context.device.bedheight = float(self.spin_bedheight.GetValue())
        self.context.signal(
            "bed_size", (self.context.device.bedwidth, self.context.device.bedheight)
        )

    def on_text_x_scale(self, event=None):
        try:
            self.context.device.scale_x = float(self.text_scale_x.GetValue())
            self.context.device.scale_y = float(self.text_scale_y.GetValue())
            self.context.signal(
                "scale_step", (self.context.device.scale_x, self.context.device.scale_y)
            )
        except ValueError:
            pass

    def on_text_y_scale(self, event=None):
        try:
            self.context.device.scale_x = float(self.text_scale_x.GetValue())
            self.context.device.scale_y = float(self.text_scale_y.GetValue())
            self.context.signal(
                "scale_step", (self.context.device.scale_x, self.context.device.scale_y)
            )
        except ValueError:
            pass


class Preferences(MWindow):
    def __init__(self, *args, **kwds):
        from sys import platform as _platform
        super().__init__(
            565,
            327,
            *args,
            style=wx.CAPTION
            | wx.CLOSE_BOX
            | wx.FRAME_FLOAT_ON_PARENT
            | wx.TAB_TRAVERSAL
            | (wx.RESIZE_BORDER if _platform != "darwin" else 0),
            **kwds
        )

        self.panel = PreferencesPanel(self, wx.ID_ANY, context=self.context)
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(icons8_administrative_tools_50.GetBitmap())
        self.SetIcon(_icon)
        self.SetTitle(_("Preferences"))

    @staticmethod
    def sub_register(kernel):
        from sys import platform
        if platform != "darwin":
            kernel.register(
                "button/config/Preferences",
                {
                    "label": _("Preferences"),
                    "icon": icons8_administrative_tools_50,
                    "tip": _("Opens Preferences Window"),
                    "action": lambda v: kernel.console("window toggle Preferences\n"),
                },
            )

    def window_open(self):
        self.panel.pane_show()

    def window_close(self):
        self.panel.pane_hide()
