from PyQt5.QtWidgets import (QMainWindow, QWidget, QPushButton, QVBoxLayout, QTableWidget, 
                             QTableWidgetItem, QLabel, QLineEdit, QFileDialog, QMessageBox, QComboBox, QTabWidget, 
                             QHeaderView, QGridLayout, QHBoxLayout)
from PyQt5.QtGui import QPixmap
import requests
from presenter.interface import ITravelAgencyGUI
from presenter.presenter import Presenter
from PyQt5.QtWidgets import QDateEdit
from PyQt5.QtCore import QDate
from threading import Thread

class View(QMainWindow, ITravelAgencyGUI):
    def __init__(self):
        super().__init__()
        self.presenter = Presenter(self)
        self.setWindowTitle("Travel Agency Manager")
        self.setGeometry(100, 150, 1000, 800)
        self.form_inputs = {}
        self._initUI()
    
    def _initUI(self):
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        
        # Tab widget to switch between tables
        self.tab_widget = QTabWidget()
        
        # Create tables
        self.package_headers = ["ID", "Destination", "Period", "Price", "Image 1", "Image 2", "Image 3"]
        self.client_headers = ["ID", "Name", "Email", "Phone"]
        self.bought_package_headers = ["ID", "Package ID", "Client ID", "Bought Date", "Departure", "Arrival"]
        
        self.package_table = self._create_table(self.package_headers, "package")
        self.client_table = self._create_table(self.client_headers, "client")
        self.bought_package_table = self._create_table(self.bought_package_headers, "bought_package")

        layout.addWidget(self.tab_widget)
        
        # Search and Filter Inputs
        self.search_client_input = QLineEdit()
        self.search_client_input.setPlaceholderText("Search bought packages by client name")
        self.search_client_btn = QPushButton("Search")
        
        # Filtering options
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Destination", "Period", "Price"])
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Enter filter value")
        self.filter_btn = QPushButton("Apply Filter")
        
        # Sorting options
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Destination", "Period", "Price"])
        self.sort_btn = QPushButton("Sort Packages")
        
        # Add widgets to the appropriate tabs in a grid layout
        package_tab_layout = self.tab_widget.widget(0).layout()
        package_tab_layout.insertWidget(0, self.package_table)
        package_filter_sort_layout = QGridLayout()
        package_filter_sort_layout.addWidget(QLabel("Filter by:"), 0, 0)
        package_filter_sort_layout.addWidget(self.filter_combo, 0, 1)
        package_filter_sort_layout.addWidget(self.filter_input, 0, 2)
        package_filter_sort_layout.addWidget(self.filter_btn, 0, 3)
        package_filter_sort_layout.addWidget(QLabel("Sort by:"), 1, 0)
        package_filter_sort_layout.addWidget(self.sort_combo, 1, 1)
        package_filter_sort_layout.addWidget(self.sort_btn, 1, 3)
        package_tab_layout.addLayout(package_filter_sort_layout)

        client_tab_layout = self.tab_widget.widget(1).layout()
        client_tab_layout.insertWidget(0, self.client_table)
        
        bought_package_tab_layout = self.tab_widget.widget(2).layout()
        bought_package_tab_layout.insertWidget(0, self.bought_package_table)
        bought_package_search_layout = QGridLayout()
        bought_package_search_layout.addWidget(QLabel("Search by client name:"), 0, 0)
        bought_package_search_layout.addWidget(self.search_client_input, 0, 1)
        bought_package_search_layout.addWidget(self.search_client_btn, 0, 2)
        bought_package_tab_layout.addLayout(bought_package_search_layout)
        
        central_widget.setLayout(layout)
        
        # Connect buttons to presenter methods
        self.search_client_btn.clicked.connect(self.presenter.search_bought_packages)
        self.filter_btn.clicked.connect(self.presenter.filter_packages)
        self.sort_btn.clicked.connect(self.presenter.sort_packages)

        self.presenter.UI_initialized()
    
        
    def _create_table(self, headers, table_type):
        table = QTableWidget()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.itemSelectionChanged.connect(lambda: self.presenter.row_selected(table_type, table.currentRow()))
        
        tab = QWidget()
        layout = QVBoxLayout()
        form = self._create_form(headers, table_type)
        layout.addLayout(form)
        buttons = self._create_buttons(table_type, table_type.capitalize())
        layout.addLayout(buttons)
        tab.setLayout(layout)
        self.tab_widget.addTab(tab, table_type.capitalize() + "s")
        
        return table

    def _create_form(self, headers, table_type):

        self.form_inputs[table_type] = {}
        form_layout = QGridLayout()  # Arrange in a grid with 2 columns
        for i, header in enumerate(headers):
            label = QLabel(header.capitalize().replace("_", " "))
            if "date" in header.lower() or "arrival" in header.lower() or "departure" in header.lower():
                input_field = QDateEdit()
                #can you set the date to look like this: 01-01-2021
                input_field.setDisplayFormat("dd-MM-yyyy")
                input_field.setCalendarPopup(True)
                input_field.setDate(QDate.currentDate())
            else:
                input_field = QLineEdit()
                if header == "ID":
                    input_field.setReadOnly(True)

            form_layout.addWidget(label, i // 2, (i % 2) * 2)
            form_layout.addWidget(input_field, i // 2, (i % 2) * 2 + 1)
            self.form_inputs[table_type][header] = input_field
        return form_layout
    
    def _create_buttons(self, table_type, label):
        button_layout = QHBoxLayout()
        label = label.capitalize().replace("_", " ")
        add_button = QPushButton(f"Add {label}")
        update_button = QPushButton(f"Update {label}")
        delete_button = QPushButton(f"Delete {label}")
        export_csv_button = QPushButton(f"Export {label}s to CSV")
        export_doc_button = QPushButton(f"Export {label}s to DOC")
        
        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(export_csv_button)
        button_layout.addWidget(export_doc_button)
        
        add_button.clicked.connect(lambda: self.presenter.add_item())
        update_button.clicked.connect(lambda: self.presenter.update_item())
        delete_button.clicked.connect(lambda: self.presenter.delete_item())
        export_csv_button.clicked.connect(lambda: self.presenter.export_to_csv())
        export_doc_button.clicked.connect(lambda: self.presenter.export_to_doc())
        
        return button_layout
        
    #implementation of ITravelAgencyGUI interface
    
    def display_packages(self, packages_id, packages_dest, packages_period, packages_price, packages_image1, packages_image2, packages_image3):
        self.package_table.setRowCount(len(packages_id))
        for row, package in enumerate(zip(packages_id, packages_dest, packages_period, packages_price, packages_image1, packages_image2, packages_image3)):
            for col, header in enumerate(self.package_headers):
                self.package_table.setItem(row, col, QTableWidgetItem(str(package[col])))

    def display_clients(self, clients_id, clients_name, clients_email, clients_phone):
        self.client_table.setRowCount(len(clients_id))
        for row, client in enumerate(zip(clients_id, clients_name, clients_email, clients_phone)):
            for col, header in enumerate(self.client_headers):
                self.client_table.setItem(row, col, QTableWidgetItem(str(client[col])))

    def display_bought_packages(self, bought_packages_id, bought_packages_package_id, bought_packages_client_id, bought_packages_bought_date, bought_packages_departure, bought_packages_arrival):
        self.bought_package_table.setRowCount(len(bought_packages_id))
        for row, bought_package in enumerate(zip(bought_packages_id, bought_packages_package_id, bought_packages_client_id, bought_packages_bought_date, bought_packages_departure, bought_packages_arrival)):
            for col, header in enumerate(self.bought_package_headers):
                self.bought_package_table.setItem(row, col, QTableWidgetItem(str(bought_package[col])))
    
    def display_bought_package_form_data(self, bought_package):
        for header in self.bought_package_headers:
            if "date" in header.lower() or "arrival" in header.lower() or "departure" in header.lower():
                self.form_inputs["bought_package"][header].setDate(QDate.fromString(str(getattr(bought_package, header.lower().replace(" ", "_"))), "dd-MM-yyyy-hh-mm-ss"))
            else:
                self.form_inputs["bought_package"][header].setText(str(getattr(bought_package, header.lower().replace(" ", "_"))))
    
    def display_package_form_data(self, package):
        for header in self.package_headers:
            self.form_inputs["package"][header].setText(str(getattr(package, header.lower().replace(" ", "_"))))
    
    def display_client_form_data(self, client):
        for header in self.client_headers:
            self.form_inputs["client"][header].setText(str(getattr(client, header.lower().replace(" ", "_"))))
    
    def get_table_type(self):
        current_tab = self.tab_widget.currentIndex()
        if current_tab == 0:
            return "package"
        elif current_tab == 1:
            return "client"
        else:
            return "bought_package"

    def get_package_form_data(self):
        data = {header.lower().replace(" ", "_"): self.form_inputs["package"][header].text() for header in self.package_headers}
        return data

    def get_client_form_data(self):
        data = {header.lower().replace(" ", "_"): self.form_inputs["client"][header].text() for header in self.client_headers}
        return data

    def get_bought_package_form_data(self) :
        data = {header.lower().replace(" ", "_"): self.form_inputs["bought_package"][header].text() for header in self.bought_package_headers}
        return data

    def get_filter_input_combo(self):
        return (self.filter_combo.currentText(), self.filter_input.text())

    def get_sort_combo(self):
        return self.sort_combo.currentText()
    
    def get_search_client_input(self):
        return self.search_client_input.text()
    
    def show_message(self, message):
        QMessageBox.information(self, "Information", message)
    
    def get_row_selected_data(self, table_type):
        row = self.tab_widget.widget(self.tab_widget.currentIndex()).layout().itemAt(0).widget().currentRow()
        data = {}
        headers = self.package_headers if table_type == "package" else self.client_headers if table_type == "client" else self.bought_package_headers
        for header in self.form_inputs[table_type]:
            data[header.lower().replace(" ", "_")] = self.tab_widget.widget(self.tab_widget.currentIndex()).layout().itemAt(0).widget().item(row, headers.index(header)).text()
        return data
    
    def display_images(self,package_image1, package_image2, package_image3):
        package_tab_layout = self.tab_widget.widget(0).layout()
        image_grid_layout = QGridLayout()
        if hasattr(self, 'image_grid_layout'):
            for i in reversed(range(self.image_grid_layout.count())):
                widget = self.image_grid_layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)
        else:
            self.image_grid_layout = QGridLayout()
            package_tab_layout.insertLayout(1, self.image_grid_layout)

        images = [package_image1, package_image2, package_image3]
        for i, image_url in enumerate(images):
            image_label = QLabel()
            if image_url:
                image_label.setFixedSize(200, 200)
                image_label.setText("Loading image...")
                def load_image(image_label=image_label, image_url=image_url):
                    pixmap = QPixmap()
                    pixmap.loadFromData(requests.get(image_url).content)
                    image_label.setPixmap(pixmap)
                    image_label.setScaledContents(True)
                
                thread = Thread(target=load_image)
                thread.start()
            else:
                image_label.setText("No image")
            self.image_grid_layout.addWidget(image_label, 0, i)

    
    