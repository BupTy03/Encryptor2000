from PyQt5.QtCore import QObject
from PyQt5.Qt import pyqtSignal, pyqtSlot


def empty_task(args):
    return 0


class PackagedTask(QObject):
    def __init__(self):
        super(PackagedTask, self).__init__()
        self.task = empty_task
        self.args = ()
        self.results = ()
        self.stored_exception = Exception()

    def set_task(self, task, args: tuple):
        self.task = task
        self.args = args

    def get_result(self):
        return self.results

    def get_stored_exception(self):
        return self.stored_exception

# slots:
    @pyqtSlot()
    def start_task(self):
        try:
            self.results = self.task(*self.args)
            self.task_done.emit(True)

        except Exception as exc:
            self.stored_exception = exc
            self.task_done.emit(False)

# signals:
    task_done = pyqtSignal(bool)

