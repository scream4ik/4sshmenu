# -*- coding: utf-8 -*-
import pygtk
pygtk.require('2.0')
import gtk
import sys
import subprocess

from xml_all import add_settings, get_name_settings, get_by_name_settings, remove_settings


class WinStatus:

    def get_status(self):
        if hasattr(self, 'show'):
            pass
        else:
            setattr(self, 'show', False)
        return self.show

    def set_status(self, status):
        if hasattr(self, 'show'):
            self.show = status
        else:
            setattr(self, 'show', status)


class Settings(gtk.Window):

    def __init__(self, bridge):
        super(Settings, self).__init__()

        self.set_title('4sshmenu')
        self.set_size_request(200, 300)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_resizable(False)
        self.connect('delete-event', self.hide_window)

        self.bridge = bridge

        try:
            self.set_icon_from_file('images/tray.png')
        except Exception, e:
            print e.message
            sys.exit(1)

        vbox = gtk.VBox()
        hbox = gtk.HBox()

        # create a scrollable window and integrate it into the vbox
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        vbox.pack_start(sw)

        # create a TreeView object which will work with our model (ListStore)
        store = self.create_model()
        self.treeView = gtk.TreeView(store)
        self.treeView.set_rules_hint(True)

        sw.add(self.treeView)
        self.create_columns(self.treeView)

        vbox.pack_start(hbox, False, False)

        btn_add = gtk.Button('Add')
        btn_add.connect('clicked', self.add_ssh)
        hbox.pack_start(btn_add)

        btn_edit = gtk.Button('Edit')
        btn_edit.connect('clicked', self.edit_ssh)
        hbox.pack_start(btn_edit)

        btn_remove = gtk.Button('Remove')
        btn_remove.connect('clicked', self.remove_ssh)
        hbox.pack_start(btn_remove)

        self.add(vbox)

    def show_me(self):
        if not self.bridge.get_status():
            self.show_all()
            self.bridge.set_status(True)

    def hide_window(self, window, event):
        window.hide()
        self.bridge.set_status(False)
        return True

    def hide_me(self):
        self.hide()
        self.bridge.set_status(False)

    def create_model(self):

        store = gtk.ListStore(str)
        for item in get_name_settings():
            store.append([item])

        return store

    def update_model(self):
        self.treeView.set_model(self.create_model())

    def create_columns(self, treeView):

        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Servers', rendererText, text=0)
        column.set_sort_column_id(0)
        treeView.append_column(column)
        treeView.connect('row-activated', self.row_activated_cb)

    def add_ssh(self, widget, data=None):
        AddSsh(self).show_all()

    def edit_ssh(self, widget, data=None):
        tree_sel = self.treeView.get_selection()
        (tm, ti) = tree_sel.get_selected()
        try:
            EditSsh(tm.get_value(ti, 0), self).show_all()
        except TypeError:
            pass

    def remove_ssh(self, widget, data=None):
        tree_sel = self.treeView.get_selection()
        (tm, ti) = tree_sel.get_selected()
        try:
            remove_settings(tm.get_value(ti, 0))
            self.update_model()
        except TypeError:
            pass

    def row_activated_cb(self, treeview, path, column):
        tree_sel = self.treeView.get_selection()
        (tm, ti) = tree_sel.get_selected()
        try:
            username, host, port = get_by_name_settings(tm.get_value(ti, 0))
            self.hide_me()
            cmd = '%s@%s -p %s' % (username, host, port)
            subprocess.Popen(args=["mate-terminal", "--command=ssh %s" % cmd])
        except TypeError:
            pass


class AddSsh(gtk.Window):

    def __init__(self, settings):
        super(AddSsh, self).__init__()
        self.settings = settings

        self.set_title('Add / edit server')
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_resizable(False)
        self.edit = False

        try:
            self.set_icon_from_file('images/tray.png')
        except Exception, e:
            print e.message
            sys.exit(1)

        vbox = gtk.VBox()
        hbox = gtk.HBox()

        vbox.pack_start(hbox, False, False)

        label = gtk.Label('Name:       ')
        hbox.pack_start(label)

        self.server_name = gtk.Entry()
        hbox.pack_start(self.server_name)

        hbox = gtk.HBox()
        vbox.pack_start(hbox, False, False)

        label = gtk.Label('Username:')
        hbox.pack_start(label)

        self.username = gtk.Entry()
        hbox.pack_start(self.username)

        hbox = gtk.HBox()
        vbox.pack_start(hbox, False, False)

        label = gtk.Label('Host:         ')
        hbox.pack_start(label)

        self.host = gtk.Entry()
        hbox.pack_start(self.host)

        hbox = gtk.HBox()
        vbox.pack_start(hbox, False, False)

        label = gtk.Label('Port:          ')
        hbox.pack_start(label)

        self.port = gtk.Entry()
        self.port.set_text('22')
        hbox.pack_start(self.port)

        hbox = gtk.HBox()
        vbox.pack_start(hbox, False, False)

        btn_ok = gtk.Button('Ok')
        btn_ok.connect('clicked', self.btn_save)
        hbox.pack_start(btn_ok)

        btn_cancel = gtk.Button('Cancel')
        btn_cancel.connect('clicked', self.btn_cancel)
        hbox.pack_start(btn_cancel)

        self.add(vbox)

    def btn_save(self, widget, data=None):

        server_name = self.server_name.get_text().strip()
        username = self.username.get_text().strip()
        host = self.host.get_text().strip()
        port = self.port.get_text().strip()

        if server_name and username and host and port:

            try:
                int(self.port.get_text().strip())
            except ValueError:
                return

            if self.edit:
                remove_settings(self.oldname)
            add_settings(server_name, username, host, port)
            self.hide()
            self.settings.update_model()

    def btn_cancel(self, widget, data=None):
        self.hide()


class EditSsh(AddSsh):

    def __init__(self, name, settings):
        super(EditSsh, self).__init__(settings)
        self.settings = settings
        self.oldname = name
        self.edit = True

        username, host, port = get_by_name_settings(name)
        self.server_name.set_text(name)
        self.username.set_text(username)
        self.host.set_text(host)
        self.port.set_text(port)
