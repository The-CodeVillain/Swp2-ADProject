#-*- coding: utf-8 -*-
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import pyqtSlot
from src.notification import NotificationCenter, NotificationName
import os

class WebPlayer(QWebEngineView):

    def __init__(self, parent=None):
        super().__init__(parent)
        # 클래스 기본 설정
        path = os.getcwd() + '/support/webplayer.html'
        file = open(path, 'r', encoding="UTF8")
        self.html = file.read()
        file.close()

        NotificationCenter.subscribe(NotificationName.play, self.play)
        QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)

        # UI 설정
        self.setHtml(self.html)
        self.web_channel = QWebChannel(self)
        self.web_channel.registerObject('handler', self)
        self.page().setWebChannel(self.web_channel)

    # 재생
    def play(self, token):
        html = self.html.replace('{0}', token)
        self.setHtml(html)

    @pyqtSlot()
    def endVideo(self):
        NotificationCenter.notification(NotificationName.end_video)
