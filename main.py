# -*- coding: utf-8 -*-
import pygtk
pygtk.require('2.0')
import gtk

from tray import SystemTrayIcon
from xml_all import check_settings


if __name__ == '__main__':
    check_settings()
    SystemTrayIcon()
    gtk.main()
