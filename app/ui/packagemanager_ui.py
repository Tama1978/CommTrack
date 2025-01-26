import sys
import json
import os
import shutil
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import zipfile

class PackageManagerUi(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_active_packages()  # Load active packages from JSON

    def initUI(self):
        self.setWindowTitle('CommTrack Package Manager')
        self.setWindowIcon(QIcon('app/assets/HamLog-Logo.png'))
        self.setGeometry(500, 500, 1000, 500)
        layout = QVBoxLayout()
        self.package_list = QListWidget()
        self.load_packages()  # Load all packages
        layout.addWidget(self.package_list)
        self.activate_button = QPushButton('Activate')
        self.activate_button.clicked.connect(self.activate_package)
        layout.addWidget(self.activate_button)
        self.deactivate_button = QPushButton('Deactivate')
        self.deactivate_button.clicked.connect(self.deactivate_package)
        layout.addWidget(self.deactivate_button)
        self.setLayout(layout)

    def load_packages(self):
        packages_dir = 'app/packages'
        self.package_list.clear()

        # Load non-active packages
        for filename in os.listdir(packages_dir):
            if filename.endswith('.zip'):
                zip_path = os.path.join(packages_dir, filename)
                print(f"Checking {zip_path}")  # Debugging output
                with zipfile.ZipFile(zip_path, 'r') as zip_file:
                    if 'manifest.json' in zip_file.namelist():
                        with zip_file.open('manifest.json') as f:
                            package_data = json.load(f)
                            item_text = f"{package_data['name']}, {package_data['Type']}, {package_data['Version']}, {package_data['Description']}, {package_data['Package Developer']}"
                            item = QListWidgetItem(item_text)
                            item.setData(Qt.UserRole, filename)
                            self.package_list.addItem(item)
                    else:
                        print(f"Manifest not found in {filename}")  # Debugging output

        # Load active packages from the JSON file
        self.load_active_packages()

    def load_active_packages(self):
        try:
            with open('packages.json', 'r') as f:
                data = json.load(f)
                active_packages = data.get("active_packages", [])
                for package_name in active_packages:
                    item = QListWidgetItem(package_name)
                    item.setBackground(QColor(144, 238, 144))  # Light green for active packages
                    self.package_list.addItem(item)
        except FileNotFoundError:
            # If the file doesn't exist, create it with an empty active list
            with open('packages.json', 'w') as f:
                json.dump({"active_packages": []}, f)

    def activate_package(self):
        selected_package = self.package_list.currentItem()
        if selected_package:
            package_name = selected_package.data(Qt.UserRole)
            with open('packages.json', 'r') as f:
                data = json.load(f)
                active_packages = data.get("active_packages", [])
            if package_name not in active_packages:
                active_packages.append(package_name)
                data["active_packages"] = active_packages
                with open('packages.json', 'w') as f:
                    json.dump(data, f)
                self.load_packages()  # Refresh the list
                
                # Store the text of the selected package before refreshing the list
                package_text = selected_package.text()
                QMessageBox.information(self, 'Activate', f'Activated {package_text}...')
            else:
                QMessageBox.warning(self, 'Warning', f'{selected_package.text()} is already activated.')
        else:
            QMessageBox.warning(self, 'Warning', 'Please select a package to activate.')

    def deactivate_package(self):
        selected_package = self.package_list.currentItem()
        if selected_package:
            package_name = selected_package.text()  # Get the text of the item
            with open('packages.json', 'r') as f:
                data = json.load(f)
                active_packages = data.get("active_packages", [])
            if package_name in active_packages:
                active_packages.remove(package_name)
                data["active_packages"] = active_packages
                with open('packages.json', 'w') as f :
                    json.dump(data, f)
                self.load_packages()  # Refresh the list
                QMessageBox.information(self, 'Deactivate', f'Deactivated {package_name}...')
            else:
                QMessageBox.warning(self, 'Warning', f'{package_name} is not activated.')
        else:
            QMessageBox.warning(self, 'Warning', 'Please select a package to deactivate.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PackageManagerUi()
    window.show()
    sys.exit(app.exec_())