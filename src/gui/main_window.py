from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QMessageBox, QFileDialog, QLineEdit, QWidget, QVBoxLayout, QMenu
from PyQt5.QtCore import Qt, QSettings
from src.gui.add_item import AddItemDialog
from src.database.db_setup import get_session
from src.gui.dashboard import DashboardDialog
from src.utils.theme_manager import ThemeManager
from src.utils.material_manager import MaterialManager
from src.gui.toolbar_manager import ToolbarManager
from markdown import markdown

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.init_managers()
        self.setup_ui()
        self.setup_connections()
        self.load_data()

    def setup_window(self):
        self.setWindowTitle("GestCharge - Gestion de Matériel")
        self.setGeometry(100, 100, 1000, 600)
        self.setMinimumSize(800, 400)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

    def init_managers(self):
        # Base de données
        self.session = get_session()
        
        # Gestionnaire de thème
        self.settings = QSettings('GestCharge', 'MainWindow')
        self.dark_mode = self.settings.value('dark_mode', False, type=bool)
        self.theme_manager = ThemeManager()
        
        # Toolbar (doit être créé avant d'appliquer le thème)
        self.toolbar_manager = ToolbarManager(self)
        self.addToolBar(self.toolbar_manager.toolbar)
        
        # Table et recherche
        self.table_widget = QTableWidget()
        self.search_bar = QLineEdit()
        self.material_manager = MaterialManager(self.session, self.table_widget)
        
        # Appliquer le thème sauvegardé
        if self.dark_mode:
            self.theme_manager.apply_theme(self, True)

    def setup_ui(self):
        # Configuration de la barre de recherche
        self.search_bar.setPlaceholderText("Rechercher un matériel...")
        self.layout.addWidget(self.search_bar)
        
        # Configuration de la table
        self.table_widget.setSelectionMode(QTableWidget.MultiSelection)
        self.table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.layout.addWidget(self.table_widget)

    def setup_connections(self):
        self.search_bar.textChanged.connect(self.material_manager.filter_materials)
        self.table_widget.customContextMenuRequested.connect(self.show_context_menu)
        self.table_widget.itemChanged.connect(self.on_item_changed)

    def load_data(self):
        self.material_manager.load_materials()

    # Méthodes de gestion des matériels
    def add_material(self):
        dialog = AddItemDialog(self.session)
        if dialog.exec_():
            self.material_manager.load_materials()

    def delete_selected_materials(self):
        selected_rows = set(item.row() for item in self.table_widget.selectedItems())
        if not selected_rows:
            return
        
        reply = QMessageBox.question(
            self, 
            'Confirmation', 
            f'Voulez-vous vraiment supprimer {len(selected_rows)} matériel(s) ?',
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            ids_to_delete = [
                self.table_widget.item(row, 0).data(Qt.UserRole)
                for row in selected_rows
            ]
            self.material_manager.delete_materials(ids_to_delete)

    def on_item_changed(self, item):
        row = item.row()
        col = item.column()
        new_value = item.text()
        material_id = self.table_widget.item(row, 0).data(Qt.UserRole)
        
        field_map = {
            0: "name", 1: "serial_number", 2: "category",
            3: "mac_address", 4: "brand_model", 5: "location",
            6: "assigned_user", 8: "comments"
        }
        
        if col in field_map:
            self.material_manager.update_material(material_id, field_map[col], new_value)

    # Import/Export
    def import_materials(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Sélectionner le fichier CSV", "", "CSV Files (*.csv)")
        if file_name and self.material_manager.import_materials(file_name):
            QMessageBox.information(self, "Succès", "Import terminé avec succès!")

    def export_materials(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Exporter en CSV", "", "CSV Files (*.csv)")
        if file_name and self.material_manager.export_materials(file_name):
            QMessageBox.information(self, "Succès", "Export terminé avec succès!")

    def show_import_help(self):
        try:
            with open('src/resources/import_help.md', 'r', encoding='utf-8') as file:
                md_content = file.read()
            html_content = markdown(md_content, extensions=['fenced_code'])
            
            msg = QMessageBox(self)
            msg.setWindowTitle("Aide - Import CSV")
            msg.setTextFormat(Qt.RichText)
            msg.setText(html_content)
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du chargement de l'aide : {str(e)}")

    # Autres fonctionnalités
    def generate_pdf(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Enregistrer le PDF", "", "PDF Files (*.pdf)")
        if file_name:
            try:
                from src.utils.pdf_generator import generate_inventory_pdf
                generate_inventory_pdf(self.material_manager.all_materials, file_name)
                QMessageBox.information(self, "Succès", "PDF généré avec succès!")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la génération du PDF: {str(e)}")

    def show_dashboard(self):
        dashboard = DashboardDialog(self.session, self)
        dashboard.exec_()

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.theme_manager.apply_theme(self, self.dark_mode)
        self.settings.setValue('dark_mode', self.dark_mode)

    def closeEvent(self, event):
        self.session.close()
        super().closeEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'table_widget'):
            self.material_manager.adjust_columns()

    def show_context_menu(self, position):
        menu = QMenu()
        delete_action = menu.addAction("Supprimer")
        
        # Obtenir l'élément sélectionné
        row = self.table_widget.rowAt(position.y())
        if row >= 0:
            action = menu.exec_(self.table_widget.viewport().mapToGlobal(position))
            if action == delete_action:
                # Utiliser delete_materials avec une liste d'un seul ID
                material_id = self.table_widget.item(row, 0).data(Qt.UserRole)
                if QMessageBox.question(
                    self, 
                    'Confirmation', 
                    'Voulez-vous vraiment supprimer ce matériel ?',
                    QMessageBox.Yes | QMessageBox.No, 
                    QMessageBox.No
                ) == QMessageBox.Yes:
                    self.material_manager.delete_materials([material_id])