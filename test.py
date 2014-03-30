#!/usr/bin/env python

import json

class Handler(object):

    def __init__(self):
        self.loadTable()
        self.loadScores()
        self.connections = []

    def loadTable(self):
        f = open('table.csv', 'r')
        self.table = []
        for l in f:
            id, name = l.strip().split(',')
            self.table.append({'id': int(id.strip()), 'name': name.strip()})
        f.close()
        self.ids = {}
        for record in self.table:
            assert record['id'] not in self.ids
            self.ids[record['id']] = record
            record['score'] = 0.0

    def loadScores(self):
        self.scoresFile = open('scores.csv', 'a')

        f = open('scores.csv', 'r')
        for l in f:
            id, score = l.strip().split(',')
            id = int(id)
            score = float(score)
            self.ids[id]['score'] += score
        f.close()


    def acceptableId(self, id):
        return id in self.ids


    def addConnection(self, webSocket):
        webSocket.send(json.dumps({'type':'table', 'data': self.table}), False)
        self.connections.append(webSocket)

    def __call__(self, id, score):
        print(id, 'got', score, 'scores')
        print('{},{}'.format(id, round(score, 3)), file=self.scoresFile)
        self.scoresFile.flush()

        self.ids[id]['score'] += score
        message = json.dumps({
            'type': 'score', 
            'data': {
                'id': id,
                'score': score
            }
        }, indent=4)

        activeConnections = []
        for connection in self.connections:
            if connection.terminated: continue
            connection.send(message, False)
            activeConnections.append(connection)

        self.connections = activeConnections
    
    handle = __call__

handler = Handler()
import ws
ws.handler = handler

import window
from gi.repository import Gtk

win = window.MainWindow(handler)
win.connect("delete-event", Gtk.main_quit)
win.connect("destroy-event", Gtk.main_quit)
win.show_all()
Gtk.main()
