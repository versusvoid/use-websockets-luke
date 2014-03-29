
from gi.repository import Gtk, Pango
import re

class MainWindow(Gtk.Window):

    def __init__(self, handler):
        Gtk.Window.__init__(self, title="NCUMC")
        self.handler = handler
        self.set_size_request(200, 100)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.idEntry = Gtk.Entry()
        self.idEntry.set_text("1")
        vbox.pack_start(self.idEntry, True, True, 0)

        self.scoreEntry = Gtk.Entry()
        self.scoreEntry.set_text("0.0")
        vbox.pack_start(self.scoreEntry, True, True, 0)


        self.button = Gtk.Button("Отправить")
        self.button.connect("clicked", self.on_send_clicked)
        vbox.pack_start(self.button, True, True, 0)

    def on_send_clicked(self, button):
        id = self.idEntry.get_text()
        match = re.match('[0-9]+', id)
        if not match or match.end(0) != len(id) or not self.handler.acceptableId(int(id)):
            print('bad id')
            return

        score = self.scoreEntry.get_text()
        match = re.match('[0-9]+(\.[0-9]*)?', score)
        if not match or match.end(0) != len(score):
            print('bad score')
            return

        self.handler.handle(int(id), float(score))
        self.scoreEntry.set_text('0.0')
