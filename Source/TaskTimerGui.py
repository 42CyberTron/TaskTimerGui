import sys
import time
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import QTimer

class TaskTimerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.tasks = []  # Store tasks
        self.current_task = -1  # No task is active initially
        self.running = False  # Timer state
        self.start_time = None
        self.lap_start_time = None
        self.total_elapsed_time = 0  # Store cumulative time
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Task Timer")
        self.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Task", "Time", "Lap Time"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)
        
        self.start_pause_button = QPushButton("Start")
        self.start_pause_button.clicked.connect(self.toggle_timer)
        layout.addWidget(self.start_pause_button)
        
        self.lap_button = QPushButton("Lap")
        self.lap_button.clicked.connect(self.lap_time)
        layout.addWidget(self.lap_button)
        
        self.add_task_button = QPushButton("Add Task")
        self.add_task_button.clicked.connect(self.add_task)
        layout.addWidget(self.add_task_button)
        
        self.setLayout(layout)
        
        self.timer.timeout.connect(self.update_time)
        self.timer.setInterval(10)  # Update every 10 milliseconds
    
    def add_task(self):
        task_name = f"Task {len(self.tasks) + 1}"
        self.tasks.append({'name': task_name, 'time': self.total_elapsed_time})
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        self.table.setItem(row, 0, QTableWidgetItem(task_name))
        self.table.setItem(row, 1, QTableWidgetItem("00:00:00.000"))
        self.table.setItem(row, 2, QTableWidgetItem("-"))
    
    def toggle_timer(self):
        if self.running:
            self.timer.stop()
            self.start_pause_button.setText("Start")
        else:
            if self.current_task == -1 and self.tasks:
                self.current_task = 0  # Start first task if none are active
                self.start_time = time.time() - self.total_elapsed_time / 1000
                self.lap_start_time = self.start_time
            self.timer.start()
            self.start_pause_button.setText("Pause")
        self.running = not self.running
    
    def update_time(self):
        if self.current_task != -1 and self.current_task < len(self.tasks):
            elapsed = int((time.time() - self.start_time) * 1000)
            formatted_time = time.strftime('%H:%M:%S', time.gmtime(elapsed // 1000)) + f".{elapsed % 1000:03d}"
            self.table.setItem(self.current_task, 1, QTableWidgetItem(formatted_time))
    
    def lap_time(self):
        if self.current_task != -1 and self.current_task < len(self.tasks):
            lap_elapsed = int((time.time() - self.lap_start_time) * 1000)
            formatted_lap_time = time.strftime('%H:%M:%S', time.gmtime(lap_elapsed // 1000)) + f".{lap_elapsed % 1000:03d}"
            self.table.setItem(self.current_task, 2, QTableWidgetItem(formatted_lap_time))
            
            # Move to next task
            self.total_elapsed_time += lap_elapsed  # Accumulate time correctly
            self.current_task += 1
            
            if self.current_task >= len(self.tasks):
                self.timer.stop()
                self.running = False
                self.start_pause_button.setText("Start")
                self.current_task = -1
            else:
                self.lap_start_time = time.time()  # Reset lap timer for new task
                self.start_time = time.time() - self.total_elapsed_time / 1000  # Ensure correct total time continuation

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TaskTimerApp()
    window.show()
    sys.exit(app.exec())
