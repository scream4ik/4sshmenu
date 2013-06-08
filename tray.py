# -*- coding: utf-8 -*-
import pygtk
pygtk.require('2.0')
import gtk

from settings import Settings, WinStatus


class SystemTrayIcon:

    def __init__(self):
        self.tray = gtk.StatusIcon()
        self.tray.set_from_file('images/tray.png')
        self.tray.connect('popup-menu', self.on_right_click)
        self.tray.connect('activate', self.on_left_click)
        self.tray.set_tooltip('4sshmenu')

        self.bridge = WinStatus()
        self.bridge.set_status(False)

    def on_right_click(self, widget, event_button, event_time):
        menu = gtk.Menu()

        settings = gtk.MenuItem('Servers list')
        settings.show()
        menu.append(settings)
        settings.connect('activate', self.show_settings)

        quit = gtk.MenuItem('Quit')
        quit.show()
        menu.append(quit)
        quit.connect('activate', gtk.main_quit)

        menu.popup(None, None, gtk.status_icon_position_menu,
                event_button, event_time, self.tray)

    def on_left_click(self, widget):
        self.show_settings(widget)

    def show_settings(self, widget):
        Settings(self.bridge).show_me()
