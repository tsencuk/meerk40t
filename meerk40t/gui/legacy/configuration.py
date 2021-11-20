# -*- coding: ISO-8859-1 -*-

import wx

from meerk40t.gui.icons import icons8_administrative_tools_50, icons8_computer_support_50
from meerk40t.gui.mwindow import MWindow

_ = wx.GetTranslation


class ConfigurationDefaultPanel(wx.Panel):
    def __init__(self, *args, context=None, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.context = context
        self.text_controller_message = wx.TextCtrl(
            self,
            wx.ID_ANY,
            _(
                "The input/driver properties of the selected device provides no graphical user interface."
            ),
            style=wx.TE_CENTRE | wx.TE_MULTILINE | wx.TE_READONLY,
        )

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):

        self.text_controller_message.SetFont(
            wx.Font(
                14,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                0,
                "Segoe UI",
            )
        )
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: Properties.__do_layout
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(self.text_controller_message, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def pane_show(self):
        self.context.listen("active", self.on_active_change)

    def pane_hide(self):
        self.context.unlisten("active", self.on_active_change)

    def on_active_change(self, origin, active):
        if origin == self.context.path:
            return
        try:
            self.GetParent().Close()
        except (TypeError, AttributeError):
            pass


class Configuration(MWindow):
    def __init__(self, *args, **kwds):
        super().__init__(423, 110, *args, **kwds)

        self.panel = ConfigurationDefaultPanel(self, wx.ID_ANY, context=self.context)
        # begin wxGlade: Properties.__set_properties
        self.SetTitle(_("Configuration"))
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(icons8_administrative_tools_50.GetBitmap())
        self.SetIcon(_icon)

    @staticmethod
    def sub_register(kernel):
        kernel.register(
            "button/config/Configuration",
            {
                "label": _("Config"),
                "icon": icons8_computer_support_50,
                "tip": _("Opens device-specfic configuration window"),
                "action": lambda v: kernel.console("window toggle Configuration\n"),
            },
        )
        
    def window_open(self):
        self.panel.pane_show()

    def window_close(self):
        self.panel.pane_hide()

    def window_preserve(self):
        return False
