from PyQt5.QtWidgets import QListView
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt
from src.file import File
from src.notification import NotificationCenter, NotificationName

class PlayList(QListView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.file = File('../PlayList.txt')
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.clicked.connect(self.did_clicked)
        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.refresh()

        NotificationCenter.subscribe(NotificationName.end_video, self.next_video)
        NotificationCenter.subscribe(NotificationName.add_video, self.add_video)

        # 첫 번째 인덱스로 영상 시작
        self.play_video(0)

    def add_video(self, kv_tuple):
        current_index = self.currentIndex()
        self.file.save_text("{0}','{1}".format(kv_tuple[0], kv_tuple[1]), "../PlayList.txt")
        self.refresh()
        self.setCurrentIndex(current_index)

    def remove_video(self, key):
        self.file.remove(key)
        self.refresh()
        if self.model.rowCount() > 0:
            self.next_video(2)

    def refresh(self):
        self.model.removeRows(0, self.model.rowCount())
        for i, value in enumerate(self.file.result.items()):
            item = QStandardItem(value[0])
            self.model.appendRow(item)

    def did_clicked(self, sender):
        value = self.file.result[sender.data()]
        self.setCurrentIndex(sender)
        NotificationCenter.notification(NotificationName.play, value)
        NotificationCenter.notification(NotificationName.update, sender.data())

    def play_video(self, index):
        if self.model.rowCount() <= 0:
            return

        index = self.model.index(index, 0)
        self.did_clicked(index)

    def next_video(self, amount=1):
        next_index = self.currentIndex().row() + amount

        if next_index >= self.model.rowCount():
            next_index = 0

        index = self.model.index(next_index, 0)
        self.did_clicked(index)
