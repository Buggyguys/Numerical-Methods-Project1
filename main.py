import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QPushButton, QLabel, QStackedWidget, QHBoxLayout,
                           QGroupBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
import matplotlib
matplotlib.use('Qt5Agg')  #use Qt5Agg backend

class NumericalMethodsApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Numerical Methods Project")
        self.setMinimumSize(1000, 600)
        
        #set up the main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.create_landing_page()
    
    def create_landing_page(self):
        #clear any existing layout
        if self.central_widget.layout():
            #remove all widgets from the layout
            while self.central_widget.layout().count():
                item = self.central_widget.layout().takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            #delete the layout
            QWidget().setLayout(self.central_widget.layout())
        
        #main layout
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        #title
        title_label = QLabel("Numerical Methods Project")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Select a problem to solve:")
        subtitle_label.setStyleSheet("font-size: 16px;")
        subtitle_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle_label)
        
        #problem selection layout
        problems_layout = QHBoxLayout()
        problems_layout.setSpacing(20)
        
        #problem A5: Network Flow
        network_group = QGroupBox("Problem A5")
        network_layout = QVBoxLayout(network_group)
        
        network_title = QLabel("Transportation Network Flow")
        network_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        network_title.setAlignment(Qt.AlignCenter)
        network_layout.addWidget(network_title)
        
        network_desc = QLabel("Analyze flows in a transportation network\nusing conservation laws.")
        network_desc.setAlignment(Qt.AlignCenter)
        network_layout.addWidget(network_desc)
        
        network_btn = QPushButton("Solve Network Flow")
        network_btn.setMinimumHeight(40)
        network_btn.clicked.connect(self.open_network_flow)
        network_layout.addWidget(network_btn)
        network_layout.addStretch()
        
        problems_layout.addWidget(network_group)
        
        #problem B7: AQI
        aqi_group = QGroupBox("Problem B7")
        aqi_layout = QVBoxLayout(aqi_group)
        
        aqi_title = QLabel("Air Quality Index Trends")
        aqi_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        aqi_title.setAlignment(Qt.AlignCenter)
        aqi_layout.addWidget(aqi_title)
        
        aqi_desc = QLabel("Smooth and analyze AQI values over time\nfrom monitoring stations.")
        aqi_desc.setAlignment(Qt.AlignCenter)
        aqi_layout.addWidget(aqi_desc)
        
        aqi_btn = QPushButton("Analyze AQI Data")
        aqi_btn.setMinimumHeight(40)
        aqi_btn.clicked.connect(self.open_aqi_analysis)
        aqi_layout.addWidget(aqi_btn)
        aqi_layout.addStretch()
        
        problems_layout.addWidget(aqi_group)
        
        main_layout.addLayout(problems_layout)
        
        #footer with exit button
        exit_btn = QPushButton("Exit")
        exit_btn.clicked.connect(self.close)
        exit_btn.setMaximumWidth(100)
        
        footer_layout = QHBoxLayout()
        footer_layout.addStretch()
        footer_layout.addWidget(exit_btn)
        main_layout.addLayout(footer_layout)
    
    def open_network_flow(self):
        from network_flow_gui import NetworkFlowGUI
        
        #create a new window for the network flow analysis
        self.network_flow_window = QMainWindow()
        self.network_flow_window.setWindowTitle("Problem A5: Transportation Network Flow Analysis")
        self.network_flow_window.setMinimumSize(1000, 700)
        
        #create main widget and layout
        central_widget = QWidget()
        self.network_flow_window.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        #create the network flow GUI
        self.network_flow_widget = NetworkFlowGUI()
        layout.addWidget(self.network_flow_widget)
        
        #add a back button
        back_btn = QPushButton("Back to Main Menu")
        back_btn.clicked.connect(self.close_network_flow)
        back_btn.setMaximumWidth(200)
        back_layout = QHBoxLayout()
        back_layout.addStretch()
        back_layout.addWidget(back_btn)
        layout.addLayout(back_layout)
        
        #show the window
        self.network_flow_window.show()
    
    def close_network_flow(self):
        if hasattr(self, 'network_flow_window'):
            self.network_flow_window.close()
    
    def open_aqi_analysis(self):
        from aqi_analysis_gui import AQIAnalysisGUI
        
        #create a new window for the AQI analysis
        self.aqi_window = QMainWindow()
        self.aqi_window.setWindowTitle("Problem B7: Air Quality Index Analysis")
        self.aqi_window.setMinimumSize(1000, 700)
        
        #create main widget and layout
        central_widget = QWidget()
        self.aqi_window.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        #create the AQI analysis GUI
        self.aqi_widget = AQIAnalysisGUI()
        layout.addWidget(self.aqi_widget)
        
        #add a back button
        back_btn = QPushButton("Back to Main Menu")
        back_btn.clicked.connect(self.close_aqi_analysis)
        back_btn.setMaximumWidth(200)
        back_layout = QHBoxLayout()
        back_layout.addStretch()
        back_layout.addWidget(back_btn)
        layout.addLayout(back_layout)
        
        #show the window
        self.aqi_window.show()
    
    def close_aqi_analysis(self):
        if hasattr(self, 'aqi_window'):
            self.aqi_window.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NumericalMethodsApp()
    window.show()
    sys.exit(app.exec_())
