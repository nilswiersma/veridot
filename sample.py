#!/usr/bin/env python3
#
# Copyright 2008 Jose Fonseca
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

DOTFILE = '/home/nils/.yosys_show.dot'
VERILOGROOT = ''
XDOT = 'submod/xdot/'
EDITOR = 'subl'

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

import sys, os
sys.path.insert(0, XDOT)
from xdot import DotWindow
from xdot.ui.elements import TextShape

import re
from pathlib import Path


def on_click(*args, **kwargs):
    # print('hello world')
    el, event = args
    # print(args)
    # print(kwargs)
    ret = False
    regex = r"\$flatten\\([^.]*).\$[^\$]*\$([^:]*):(\d*)"
    # test_str = "$flatten\\picorv32.$logic_not$picorv32.v:1944$1523_Y"


    if el and el.shapes:
        for shape in el.shapes:
            if isinstance(shape, TextShape):
                m = re.match(regex, shape.t)
                if m:
                    print(m.groups())
                    loc = f'{Path(VERILOGROOT) / m.group(2)}:{m.group(3)}'
                    print(loc)
                    os.system(f'{EDITOR} {loc}')

                    ret = True



    # print(f'click, el={el}, {el.shapes}')
    # for shape in el.shapes:
    #     print(f'type(shape): {type(shape)}')
    #     if isinstance(shape, TextShape):
    #         print(f'shape: {shape}')
    #         print(f'.t: {shape.t}')

    # dialog = Gtk.MessageDialog(
    #     parent=self,
    #     buttons=Gtk.ButtonsType.OK,
    #     message_format="%s clicked" % url)
    # dialog.connect('response', lambda dialog, response: dialog.destroy())
    # dialog.run()
    
    # True means don't do anything else with the click
    return ret 




class MyDotWindow(DotWindow):

    def __init__(self, *args, **kwargs):
        super(MyDotWindow, self).__init__(*args, **kwargs)
        self.dotwidget.on_click = on_click

dotcode = b"""
digraph G {
  Hello [shape=diamond, label="$flatten\\picorv32.$0\\reg_pc[31:0]"]
  World [URL="http://en.wikipedia.org/wiki/World"]
    Hello -> World
}
"""

dotcode = b"""
digraph "top" {
label="top";
rankdir="LR";
remincross=true;
v0 [ label="picorv32.mem_done" ];
v1 [ label="$flatten\\picorv32.$logic_not$picorv32.v:1944$1523_Y", URL="file://file" ];
c5 [ shape=record, label="{{<p2> A|<p3> B}|$flatten\\picorv32.$logic_or$picorv32.v:1944$1524\n$logic_or|{<p4> Y}}" ];
n1 [ shape=diamond, label="$flatten\\picorv32.$logic_or$picorv32.v:1944$1524_Y" ];
c5:p4:e -> n1:w [color="black", label=""];
v0:e -> c5:p3:w [color="black", label=""];
v1:e -> c5:p2:w [color="black", label=""];
}

"""


def main():
    window = MyDotWindow(width=800, height=1000)
    if sys.platform != 'win32':
        # Reset KeyboardInterrupt SIGINT handler, so that glib loop can be stopped by it
        import signal
        signal.signal(signal.SIGINT, signal.SIG_DFL)
    # window.set_dotcode(dotcode)
    filename = DOTFILE
    fp = open(filename, 'rb')
    window.set_dotcode(fp.read(), filename)
    fp.close()
    window.connect('delete-event', Gtk.main_quit)
    Gtk.main()


if __name__ == '__main__':
    main()
