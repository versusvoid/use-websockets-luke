
from gi.repository import Gtk, Gdk
import re

class MainWindow(Gtk.Window):

    def __init__(self, handler):
        Gtk.Window.__init__(self, title="NCUMC")
        self.set_border_width(20)
        self.handler = handler

        grid = Gtk.Grid()
        self.grid = grid
        grid.set_row_spacing(15)
        grid.set_column_spacing(15)
        self.add(grid)

        idLabel = Gtk.Label('Идентификатор участника:')
        grid.attach(idLabel, 0, 0, 1, 1)

        self.idEntry = Gtk.Entry()
        self.idEntry.set_text("0")
        self.idEntry.connect("changed", self.clear_warning)
        grid.attach_next_to(self.idEntry, idLabel, Gtk.PositionType.RIGHT, 1, 1)

        scoreLabel = Gtk.Label('Количество баллов:')
        grid.attach_next_to(scoreLabel, idLabel, Gtk.PositionType.BOTTOM, 1, 1)

        self.scoreEntry = Gtk.Entry()
        self.scoreEntry.set_text("0.0")
        self.idEntry.connect("changed", self.clear_warning)
        self.idEntry.connect("activate", self.score_focus)
        self.scoreEntry.connect("activate", self.on_send_clicked)
        grid.attach_next_to(self.scoreEntry, scoreLabel, Gtk.PositionType.RIGHT, 1, 1)

        self.button = Gtk.Button("Отправить")
        self.button.connect("clicked", self.on_send_clicked)
        grid.attach_next_to(self.button, scoreLabel, Gtk.PositionType.BOTTOM, 2, 1)

        self.warningLabel = Gtk.Label('')
        self.warningLabel.hide()
        self.warningLabel.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse("red"))
        grid.attach_next_to(self.warningLabel, idLabel, Gtk.PositionType.TOP, 2, 1)

    def clear_warning(self, *args):
        self.warningLabel.set_text('')

    def score_focus(self, *args):
        self.scoreEntry.grab_focus()

    def id_warning(self):
        self.warningLabel.set_text('Проверьте идентификатор')
        self.idEntry.grab_focus()

    def score_warning(self):
        self.warningLabel.set_text('Проверьте введённые баллы')
        self.scoreEntry.grab_focus()

    def on_send_clicked(self, button):
        id = self.idEntry.get_text()
        match = re.match('[0-9]+', id)
        if not match or match.end(0) != len(id) or not self.handler.acceptableId(int(id)):
            print('bad id', id)
            self.id_warning()
            return

        score = self.scoreEntry.get_text()
        match = re.match('[0-9]+(\.[0-9]*)?', score)
        if not match or match.end(0) != len(score):
            print('bad score', score)
            self.score_warning()
            return

        self.handler.handle(int(id), float(score))
        self.scoreEntry.set_text('0.0')
        self.idEntry.grab_focus()
