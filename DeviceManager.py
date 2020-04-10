#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.3 on Sat Feb  1 06:42:01 2020
#

import wx
from icons import icons8_administrative_tools_50, icons8_down, icons8up, icons8_plus_50, icons8_trash_50

_ = wx.GetTranslation


class DeviceManager(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: DeviceManager.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE | wx.FRAME_TOOL_WINDOW
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((707, 337))
        self.devices_list = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
        self.new_device_button = wx.BitmapButton(self, wx.ID_ANY, icons8_plus_50.GetBitmap())
        self.remove_device_button = wx.BitmapButton(self, wx.ID_ANY, icons8_trash_50.GetBitmap())
        self.device_properties_button = wx.BitmapButton(self, wx.ID_ANY, icons8_administrative_tools_50.GetBitmap())
        self.move_item_up_button = wx.BitmapButton(self, wx.ID_ANY, icons8up.GetBitmap())
        self.move_item_down_button = wx.BitmapButton(self, wx.ID_ANY, icons8_down.GetBitmap())

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.on_list_drag, self.devices_list)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_list_item_activated, self.devices_list)
        self.Bind(wx.EVT_BUTTON, self.on_button_new, self.new_device_button)
        self.Bind(wx.EVT_BUTTON, self.on_button_remove, self.remove_device_button)
        self.Bind(wx.EVT_BUTTON, self.on_button_properties, self.device_properties_button)
        self.Bind(wx.EVT_BUTTON, self.on_button_up, self.move_item_up_button)
        self.Bind(wx.EVT_BUTTON, self.on_button_down, self.move_item_down_button)
        # end wxGlade

        self.Bind(wx.EVT_CLOSE, self.on_close, self)
        self.kernel = None

    def on_close(self, event):
        item = self.devices_list.GetFirstSelected()
        if item != -1:
            uid = self.devices_list.GetItem(item).Text
            self.kernel.device_primary = uid
        self.kernel.device_list = ";".join([d for d in self.kernel.devices])

        self.kernel.mark_window_closed("DeviceManager")
        self.kernel = None
        event.Skip()  # Call destroy as regular.

    def set_kernel(self, kernel):
        self.kernel = kernel
        self.kernel.setting(str, 'device_list', '')
        self.kernel.setting(str, 'device_primary', '')
        self.refresh_device_list()

    def __set_properties(self):
        # begin wxGlade: DeviceManager.__set_properties
        self.SetTitle(_("Device Manager"))
        self.devices_list.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Segoe UI"))
        self.devices_list.AppendColumn(_("Name"), format=wx.LIST_FORMAT_LEFT, width=117)
        self.devices_list.AppendColumn(_("Driver"), format=wx.LIST_FORMAT_LEFT, width=146)
        self.devices_list.AppendColumn(_("State"), format=wx.LIST_FORMAT_LEFT, width=105)
        self.devices_list.AppendColumn(_("Location"), format=wx.LIST_FORMAT_LEFT, width=254)
        self.new_device_button.SetSize(self.new_device_button.GetBestSize())
        self.remove_device_button.SetSize(self.remove_device_button.GetBestSize())
        self.device_properties_button.SetSize(self.device_properties_button.GetBestSize())
        self.move_item_up_button.SetSize(self.move_item_up_button.GetBestSize())
        self.move_item_down_button.SetSize(self.move_item_down_button.GetBestSize())
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: DeviceManager.__do_layout
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.devices_list, 1, wx.EXPAND, 0)
        sizer_2.Add(self.new_device_button, 0, 0, 0)
        sizer_2.Add(self.remove_device_button, 0, 0, 0)
        sizer_2.Add(self.device_properties_button, 0, 0, 0)
        sizer_2.Add(self.move_item_up_button, 0, 0, 0)
        sizer_2.Add(self.move_item_down_button, 0, 0, 0)
        sizer_1.Add(sizer_2, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def refresh_device_list(self):
        self.devices_list.DeleteAllItems()
        if len(self.kernel.devices) <= 0:
            return
        i = 0
        for key, value in self.kernel.devices.items():
            m = self.devices_list.InsertItem(i, str(key))
            if m != -1:
                self.devices_list.SetItem(m, 1, "Lhystudios")
                self.devices_list.SetItem(m, 2, str(value.state))
                self.devices_list.SetItem(m, 3, str(value.location))
            if value is self.kernel.device:
                self.devices_list.Select(m)
            i += 1

    def on_list_drag(self, event):  # wxGlade: DeviceManager.<event_handler>
        pass

    def on_list_item_activated(self, event):  # wxGlade: DeviceManager.<event_handler>
        uid = event.GetLabel()
        self.kernel.activate_device(uid)
        self.Close()

    def on_button_new(self, event):  # wxGlade: DeviceManager.<event_handler>
        for name, backend in self.kernel.backends.items():
            dlg = wx.TextEntryDialog(None, _('Enter name of the %s device') % name, _('Device Name'))
            dlg.SetValue("")
            if dlg.ShowModal() == wx.ID_OK:
                name = dlg.GetValue()
                if name not in self.kernel.devices:
                    backend.create_device(dlg.GetValue())
            dlg.Destroy()
        self.refresh_device_list()

    def on_button_remove(self, event):  # wxGlade: DeviceManager.<event_handler>
        item = self.devices_list.GetFirstSelected()
        uid = self.devices_list.GetItem(item).Text
        device = self.kernel.devices[uid]
        del self.kernel.devices[uid]
        if device is self.kernel.device:
            self.kernel.activate_device(None)
        self.refresh_device_list()

    def on_button_properties(self, event):  # wxGlade: DeviceManager.<event_handler>
        old = self.kernel.device
        item = self.devices_list.GetFirstSelected()
        uid = self.devices_list.GetItem(item).Text
        data = self.kernel.devices[uid]
        self.kernel.device = data
        self.kernel.open_window("Preferences")
        self.kernel.device = old

    def on_button_up(self, event):  # wxGlade: DeviceManager.<event_handler>
        print("Event handler 'on_button_up' not implemented!")
        event.Skip()

    def on_button_down(self, event):  # wxGlade: DeviceManager.<event_handler>
        print("Event handler 'on_button_down' not implemented!")
        event.Skip()
