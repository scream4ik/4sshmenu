# -*- coding: utf-8 -*-
import os
from xml.dom.minidom import *


SETTINGS_FILE = os.path.expanduser('~/.pysshmenu/config.xml')


def check_settings():

    if not os.path.exists('/'.join(SETTINGS_FILE.split('/')[:-1])):
        os.mkdir('/'.join(SETTINGS_FILE.split('/')[:-1]))

    if not os.path.exists(SETTINGS_FILE):
        doc = Document()
        wml = doc.createElement("root")
        doc.appendChild(wml)
        doc.writexml(open(SETTINGS_FILE, 'w'))


def add_settings(con_name, con_username, con_host, con_port):
    doc = xml.dom.minidom.parse(SETTINGS_FILE)
    root = doc.getElementsByTagName("root")[0]

    if doc.getElementsByTagName(con_name):
        root.removeChild(doc.getElementsByTagName(con_name)[0])

    node = doc.createElement(con_name)
    node.setAttribute("username", con_username)
    node.setAttribute("host", con_host)
    node.setAttribute("port", con_port)

    root.appendChild(node)
    doc.writexml(open(SETTINGS_FILE, 'w'))


def get_name_settings():
    doc = xml.dom.minidom.parse(SETTINGS_FILE)
    name = doc.getElementsByTagName('root')[0].childNodes
    results = []

    for node in name:
        results.append(node.localName)

    return results


def get_by_name_settings(name):
    doc = xml.dom.minidom.parse(SETTINGS_FILE)
    node = doc.getElementsByTagName(name)[0]
    return node.getAttributeNode('username').nodeValue, node.getAttributeNode('host').nodeValue, node.getAttributeNode('port').nodeValue


def remove_settings(name):
    doc = xml.dom.minidom.parse(SETTINGS_FILE)
    root = doc.getElementsByTagName("root")[0]

    if doc.getElementsByTagName(name):
        root.removeChild(doc.getElementsByTagName(name)[0])

    doc.writexml(open(SETTINGS_FILE, 'w'))
