"""Test Qt signal-slot (with PySide) as well as queue and pipe (with multiprocessing)

Based on:
https://stackoverflow.com/questions/26746379/how-to-signal-slots-in-a-gui-from-a-different-process

How it works:

- Main creates (in main process 1st thread):
  - QApplication
  - Queue and Pipe for inter-process communication
  - Mother instance for the main process and a 2nd thread
  - ChildProc for the other process
  - Form for the Qt window content
  - Qt event loop (runs until wirndow is closed)
- In Mother, the 2nd thread starts and runs an endless loop that
  - reads the data from the interprocess pipe (sent by ChildProc)
  - sends a signal with this data (received by Form)
- ChildProc runs an endless loop that gets data from the queue (put by Qt Form)
  then sends the uppercase data into the interprocess pipe (to Mother)
- Form
  - shows the Qt window
  - when a text entered, the to_child() slot receives the text (through signal)
  - receive signal (from Mother) in the updateUI() slot
  - append the received uppercase text into the multiline widget

When the window appears, user can enter a text into the input filed. Pressing
Enter fires the "returnPressed" signal. The to_child() slot is connected to
this, so it receives the entered text. It puts this text into the queue. The
2nd process (ChildProc) is waiting for data from the queue, so it gets the text
and sends it uppercase version through the pipe to the 2nd thread of the main
process (Mother). It receives the upper text from the pipe and sends it in a
signal. The updateUI() slot is connected to this signal, so it receives the
uppercase text and displays it in the upper area of the window.
"""

from multiprocessing import Pipe, Process, Queue
from multiprocessing.connection import PipeConnection
from threading import Thread

from PySide6 import QtCore, QtWidgets

class Mother(QtCore.QObject, Thread):
    """Mother process with two threads"""
    signal = QtCore.Signal((str,), name="mysignal", arguments=["uppertext"])

    def __init__(self, pipe_to_child: PipeConnection):
        QtCore.QObject.__init__(self, None)
        Thread.__init__(self)
        self.pipe_to_child = pipe_to_child

    def run(self):
        while True:
            try:
                # get text from Child through pipe
                args: str = self.pipe_to_child.recv()
            except EOFError:
                break
            else:
                # send signal (to Form)
                self.signal.emit(args)

class Form(QtWidgets.QDialog):

    def __init__(self, queue: Queue, mother: Mother, parent=None):
        super().__init__(parent)
        self.queue = queue
        self.browser = QtWidgets.QTextBrowser()
        self.lineedit = QtWidgets.QLineEdit('Type text and press <Enter>')
        self.lineedit.selectAll()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.browser)
        layout.addWidget(self.lineedit)
        self.setLayout(layout)
        self.lineedit.setFocus()
        self.setWindowTitle('Upper')
        self.lineedit.returnPressed.connect(self.to_child)
        mother.signal.connect(self.updateUI)

    def to_child(self):
        # Send text to Child through queue
        self.queue.put(self.lineedit.text())
        self.lineedit.clear()

    def updateUI(self, text):
        # Receive signal (from Mother)
        self.browser.append(text)

class ChildProc(Process):

    def __init__(self, pipe_to_mother: PipeConnection, queue: Queue, daemon=True):
        Process.__init__(self)
        self.daemon = daemon
        self.pipe_to_mother = pipe_to_mother
        self.queue = queue

    def run(self):
        while True:
            # Get text from Form through queue
            text: str = self.queue.get()
            # Send text to Mother through pipe
            self.pipe_to_mother.send(text.upper())

if __name__ == '__main__':

    app = QtWidgets.QApplication([])
    mother_pipe, child_pipe = Pipe()
    queue = Queue()

    mother = Mother(mother_pipe)
    mother.start()  # Start the 2nd tread in main process
    
    child = ChildProc(child_pipe, queue)
    child.start()  # Start the 2nd process

    form = Form(queue, mother)
    form.show()  # Display the Qt window
    
    app.exec()  # Execute the Qt application until window close
