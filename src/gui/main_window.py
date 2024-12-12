from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QTableWidget, QTableWidgetItem, QMenu, QMessageBox, QToolBar, QFileDialog, QLineEdit, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QPalette, QColor
from src.gui.add_item import AddItemDialog
from src.database.db_setup import get_session
from src.database.queries import add_material, update_material, delete_material
from src.database.models import Material
import csv
from datetime import datetime
from src.gui.dashboard import DashboardDialog  # Ajouter cet import

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GestCharge - Gestion de Matériel")
        self.setGeometry(100, 100, 1000, 600)
        self.setMinimumSize(800, 400)  # Taille minimale pour l'utilisabilité
        self.session = get_session()
        
        # Initialiser les variables de cache
        self._cached_materials = None
        self._last_update = None
        
        # Widget central pour contenir la barre de recherche et le tableau
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Initialiser le thème
        self.settings = QSettings('GestCharge', 'MainWindow')
        self.dark_mode = self.settings.value('dark_mode', False, type=bool)
        self.init_theme()
        
        # Toolbar
        self.create_toolbar()
        
        # Barre de recherche
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Rechercher un matériel...")
        self.search_bar.textChanged.connect(self.filter_materials)
        layout.addWidget(self.search_bar)
        
        # Table pour afficher les matériels
        self.table_widget = QTableWidget()
        self.table_widget.itemChanged.connect(self.on_item_changed)
        self.table_widget.setSelectionMode(QTableWidget.MultiSelection)
        layout.addWidget(self.table_widget)
        
        # Stocker les matériels en mémoire avec un dictionnaire pour un accès plus rapide
        self.materials_dict = {}  # id -> material
        self.load_materials()
        
        # Activer le menu contextuel
        self.table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(self.show_context_menu)
        
        # Appliquer le thème si nécessaire (après création de tous les widgets)
        if self.dark_mode:
            self.toggle_theme()

    def create_toolbar(self):
        toolbar = QToolBar()
        toolbar.setMovable(False)  # Empêcher le déplacement de la toolbar
        self.addToolBar(toolbar)
        
        # Rendre la toolbar responsive
        toolbar.setStyleSheet("""
            QToolBar {
                spacing: 5px;
                padding: 3px;
            }
            QToolButton {
                padding: 5px;
                border-radius: 3px;
                min-width: 30px;  # Largeur minimale pour les boutons
            }
        """)
        
        # Groupe Gestion des matériels
        add_action = QAction("➕ Ajouter", self)
        add_action.triggered.connect(self.add_material)
        toolbar.addAction(add_action)
        
        delete_action = QAction("🗑️ Supprimer", self)
        delete_action.triggered.connect(self.delete_selected_materials)
        toolbar.addAction(delete_action)
        
        # Premier séparateur
        toolbar.addSeparator()
        
        # Groupe Import/Export
        import_action = QAction("📥 Importer", self)
        import_action.triggered.connect(self.import_materials)
        toolbar.addAction(import_action)
        
        # Bouton d'aide pour l'import
        import_help_action = QAction("❓ Aide Import", self)
        import_help_action.triggered.connect(self.show_import_help)
        toolbar.addAction(import_help_action)
        
        export_action = QAction("📤 Exporter", self)
        export_action.triggered.connect(self.export_materials)
        toolbar.addAction(export_action)
        
        # Deuxième séparateur
        toolbar.addSeparator()
        
        # Groupe PDF
        pdf_action = QAction("📄 Générer PDF", self)
        pdf_action.triggered.connect(self.generate_pdf)
        toolbar.addAction(pdf_action)
        
        # Troisième séparateur
        toolbar.addSeparator()
        
        # Groupe Apparence
        self.theme_action = QAction("☼", self)
        self.theme_action.setToolTip("Changer le thème")
        self.theme_action.triggered.connect(self.toggle_theme)
        toolbar.addAction(self.theme_action)
        
        # Après le bouton PDF
        stats_action = QAction("📊 Statistiques", self)
        stats_action.triggered.connect(self.show_dashboard)
        toolbar.addAction(stats_action)

    def init_theme(self):
        self.light_palette = QPalette()
        
        # Créer la palette sombre
        self.dark_palette = QPalette()
        self.dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        self.dark_palette.setColor(QPalette.WindowText, Qt.white)
        self.dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
        self.dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        self.dark_palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
        self.dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        self.dark_palette.setColor(QPalette.Text, Qt.white)
        self.dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        self.dark_palette.setColor(QPalette.ButtonText, Qt.white)
        self.dark_palette.setColor(QPalette.BrightText, Qt.red)
        self.dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        self.dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        self.dark_palette.setColor(QPalette.HighlightedText, QColor(35, 35, 35))
        
        # Appliquer le thème clair par défaut
        QApplication.setPalette(self.light_palette)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        
        if self.dark_mode:
            QApplication.setPalette(self.dark_palette)
            self.theme_action.setText("☼")  # Symbole soleil Unicode
            
            # Style spécifique pour le mode sombre
            self.setStyleSheet("""
                QToolBar {
                    background: #2b2b2b;
                    spacing: 5px;
                    padding: 3px;
                    border: none;
                }
                QToolButton {
                    background: #3b3b3b;
                    color: white;
                    padding: 5px;
                    border-radius: 3px;
                }
                QToolButton:hover {
                    background: #4b4b4b;
                }
                QLineEdit {
                    background: #3b3b3b;
                    color: white;
                    padding: 5px;
                    border: 1px solid #4b4b4b;
                    border-radius: 3px;
                }
            """)
            
            self.table_widget.setStyleSheet("""
                QTableWidget {
                    gridline-color: #1e1e1e;
                    selection-background-color: #404040;
                    background: #2b2b2b;
                    color: white;
                }
                QHeaderView::section {
                    background-color: #3b3b3b;
                    color: white;
                    border: 1px solid #1e1e1e;
                    padding: 5px;
                }
                QTableWidget::item:selected {
                    background: #404040;
                }
            """)
        else:
            QApplication.setPalette(self.light_palette)
            self.theme_action.setText("☾")  # Symbole lune Unicode
            
            # Style pour le mode clair avec effet de survol
            self.setStyleSheet("""
                QToolBar {
                    spacing: 5px;
                    padding: 3px;
                    background: #f0f0f0;
                }
                QToolButton {
                    padding: 5px;
                    border-radius: 3px;
                    background: #f8f8f8;
                }
                QToolButton:hover {
                    background: #e0e0e0;
                }
                QLineEdit {
                    padding: 5px;
                    border: 1px solid #d0d0d0;
                    border-radius: 3px;
                    background: white;
                }
            """)
            self.table_widget.setStyleSheet("""
                QTableWidget {
                    gridline-color: #d0d0d0;
                }
                QHeaderView::section {
                    background-color: #f0f0f0;
                    padding: 5px;
                    border: 1px solid #d0d0d0;
                }
            """)
        
        self.settings.setValue('dark_mode', self.dark_mode)

    def load_materials(self):
        # Utiliser une seule requête avec jointure si nécessaire
        query = self.session.query(Material).order_by(Material.name)
        materials = query.all()
        
        # Mise en cache optimisée
        self.materials_dict = {m.id: m for m in materials}
        self.all_materials = materials  # Pas besoin de convertir en liste
        self.display_materials(self.all_materials)

    def display_materials(self, materials):
        # Bloquer les signaux pendant la mise à jour
        self.table_widget.blockSignals(True)
        
        # Préparer toutes les données avant de les insérer
        self.table_widget.setRowCount(len(materials))
        self.table_widget.setColumnCount(9)  # Ajout du nombre de colonnes
        
        # Définir les en-têtes
        self.table_widget.setHorizontalHeaderLabels([
            "Nom", "Numéro de Série", "Catégorie", "Adresse MAC", 
            "Marque/Modèle", "Localisation", "Utilisateur Assigné", 
            "Date d'Assignement", "Commentaires"
        ])
        
        # Créer tous les items en une fois
        items = []
        for i, material in enumerate(materials):
            row_items = []
            name_item = QTableWidgetItem(material.name)
            name_item.setData(Qt.UserRole, material.id)
            row_items.append(name_item)
            row_items.extend([
                QTableWidgetItem(str(value) if value is not None else "")
                for value in [
                    material.serial_number,
                    material.category,
                    material.mac_address,
                    material.brand_model,
                    material.location,
                    material.assigned_user,
                    material.assignment_date.strftime("%Y-%m-%d") if material.assignment_date else "",
                    material.comments
                ]
            ])
            items.append(row_items)
        
        # Insérer tous les items d'un coup
        for i, row_items in enumerate(items):
            for j, item in enumerate(row_items):
                self.table_widget.setItem(i, j, item)
        
        # Ajuster les colonnes à la taille de la fenêtre
        header = self.table_widget.horizontalHeader()
        available_width = self.table_widget.viewport().width()
        
        # Définir les largeurs relatives des colonnes
        column_ratios = {
            0: 0.12,  # Nom (12%)
            1: 0.12,  # N° Série (12%)
            2: 0.10,  # Catégorie (10%)
            3: 0.15,  # Adresse MAC (15%)
            4: 0.13,  # Marque/Modèle (13%)
            5: 0.12,  # Localisation (12%)
            6: 0.12,  # Utilisateur (12%)
            7: 0.10,  # Date (10%)
            8: 0.04   # Commentaires (4%)
        }
        
        # Appliquer les largeurs
        for column, ratio in column_ratios.items():
            width = int(available_width * ratio)
            header.setSectionResizeMode(column, header.Interactive)
            self.table_widget.setColumnWidth(column, width)
        
        # Permettre l'étirement de la dernière colonne
        header.setStretchLastSection(True)
        
        self.table_widget.blockSignals(False)

    def filter_materials(self, search_text):
        if not search_text:
            self.display_materials(self.all_materials)
            return
        
        search_text = search_text.lower()
        
        # Utiliser un set pour une recherche plus rapide
        filtered_materials = {
            material for material in self.all_materials
            if any(
                search_text in (str(value) or "").lower()
                for value in (
                    material.name,
                    material.serial_number,
                    material.mac_address,
                    material.brand_model,
                    material.category,
                    material.location,
                    material.assigned_user,
                    material.comments
                )
            )
        }
        
        self.display_materials(list(filtered_materials))

    def add_material(self):
        dialog = AddItemDialog(self.session)
        if dialog.exec_():
            self.load_materials()

    def closeEvent(self, event):
        self.session.close()  # Fermer la session lors de la fermeture de la fenêtre
        super().closeEvent(event)

    def on_item_changed(self, item):
        row = item.row()
        col = item.column()
        new_value = item.text()
        
        material_id = self.table_widget.item(row, 0).data(Qt.UserRole)
        
        field_map = {
            0: "name",
            1: "serial_number",
            2: "category",
            3: "mac_address",
            4: "brand_model",
            5: "location",
            6: "assigned_user",
            8: "comments"
        }
        
        if col in field_map:
            field_name = field_map[col]
            update_material(self.session, material_id, **{field_name: new_value or None})

    def show_context_menu(self, position):
        menu = QMenu()
        delete_action = menu.addAction("Supprimer")
        
        # Obtenir l'élément sélectionné
        row = self.table_widget.rowAt(position.y())
        if row >= 0:
            action = menu.exec_(self.table_widget.viewport().mapToGlobal(position))
            if action == delete_action:
                self.delete_material(row)

    def delete_material(self, row):
        material_id = self.table_widget.item(row, 0).data(Qt.UserRole)
        
        reply = QMessageBox.question(self, 'Confirmation', 
                                   'Voulez-vous vraiment supprimer ce matériel ?',
                                   QMessageBox.Yes | QMessageBox.No, 
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                # S'assurer qu'il n'y a pas de transaction active
                self.session.rollback()
                
                # Commencer une nouvelle transaction
                with self.session.begin():
                    material = self.session.query(Material).get(material_id)
                    if material:
                        self.session.delete(material)
                
                # Mettre à jour le cache local
                self.materials_dict.pop(material_id, None)
                self.all_materials = list(self.materials_dict.values())
                self.display_materials(self.all_materials)
                
                # Nettoyer explicitement les références
                self.materials_dict.clear()
                self.all_materials = []
                self.load_materials()
                
            except Exception as e:
                self.session.rollback()
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression: {str(e)}")

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
            try:
                # S'assurer qu'il n'y a pas de transaction active
                self.session.rollback()
                
                # Récupérer tous les IDs
                ids_to_delete = [
                    self.table_widget.item(row, 0).data(Qt.UserRole)
                    for row in selected_rows
                ]
                
                # Supprimer en une seule transaction
                with self.session.begin():
                    self.session.query(Material).filter(
                        Material.id.in_(ids_to_delete)
                    ).delete(synchronize_session='fetch')
                
                # Mettre à jour le cache local
                self.materials_dict = {
                    k: v for k, v in self.materials_dict.items()
                    if k not in ids_to_delete
                }
                self.all_materials = list(self.materials_dict.values())
                self.display_materials(self.all_materials)
                
            except Exception as e:
                self.session.rollback()
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression: {str(e)}")

    def import_materials(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Sélectionner le fichier CSV",
            "",
            "CSV Files (*.csv)"
        )
        
        if file_name:
            try:
                materials_to_add = []
                with open(file_name, 'r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    next(reader)
                    
                    # Préparer tous les matériels avant l'insertion
                    for row in reader:
                        if len(row) >= 9:
                            material_data = {
                                'name': row[0],
                                'serial_number': row[1] or None,
                                'mac_address': row[2] or None,
                                'brand_model': row[3] or None,
                                'category': row[4] or None,
                                'location': row[5] or None,
                                'assigned_user': row[6] or None,
                                'assignment_date': datetime.strptime(row[7], '%Y-%m-%d') if row[7] else None,
                                'comments': row[8] or None
                            }
                            materials_to_add.append(Material(**material_data))
                
                # Insérer tous les matériels en une seule transaction
                with self.session.begin():
                    self.session.bulk_save_objects(materials_to_add)
                
                self.load_materials()
                QMessageBox.information(self, "Succès", "Import terminé avec succès!")
                
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de l'import: {str(e)}")

    def export_materials(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter en CSV",
            "",
            "CSV Files (*.csv)"
        )
        
        if file_name:
            try:
                with open(file_name, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    # Écrire l'en-tête
                    writer.writerow([
                        "Nom", "Numéro de Série", "Adresse MAC", "Marque/Modèle",
                        "Catégorie", "Localisation", "Utilisateur Assigné",
                        "Date d'Assignement", "Commentaires"
                    ])
                    
                    # Écrire les données
                    materials = self.session.query(Material).all()
                    for material in materials:
                        writer.writerow([
                            material.name,
                            material.serial_number or "",
                            material.mac_address or "",
                            material.brand_model or "",
                            material.category or "",
                            material.location or "",
                            material.assigned_user or "",
                            material.assignment_date.strftime("%Y-%m-%d") if material.assignment_date else "",
                            material.comments or ""
                        ])
                
                QMessageBox.information(
                    self,
                    "Succès",
                    "Export terminé avec succès!"
                )
                
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Erreur",
                    f"Erreur lors de l'export: {str(e)}"
                )

    def generate_pdf(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Enregistrer le PDF",
            "",
            "PDF Files (*.pdf)"
        )
        
        if file_name:
            try:
                from src.utils.pdf_generator import generate_inventory_pdf
                generate_inventory_pdf(self.all_materials, file_name)
                QMessageBox.information(
                    self,
                    "Succès",
                    "PDF généré avec succès!"
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Erreur",
                    f"Erreur lors de la génération du PDF: {str(e)}"
                )

    def show_import_help(self):
        try:
            # Lire le fichier markdown
            with open('src/resources/import_help.md', 'r', encoding='utf-8') as file:
                md_content = file.read()
            
            # Convertir le markdown en HTML
            from markdown import markdown
            html_content = markdown(md_content, extensions=['fenced_code'])
            
            # Afficher l'aide
            msg = QMessageBox(self)
            msg.setWindowTitle("Aide - Import CSV")
            msg.setTextFormat(Qt.RichText)
            msg.setText(html_content)
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erreur",
                f"Erreur lors du chargement de l'aide : {str(e)}"
            )

    def resizeEvent(self, event):
        """Gérer le redimensionnement de la fenêtre"""
        super().resizeEvent(event)
        
        # Réajuster les colonnes quand la fenêtre est redimensionnée
        if hasattr(self, 'table_widget'):
            header = self.table_widget.horizontalHeader()
            available_width = self.table_widget.viewport().width()
            
            # Recalculer les largeurs des colonnes
            for column, ratio in {
                0: 0.12,  # Nom
                1: 0.12,  # N° Série
                2: 0.10,  # Catégorie
                3: 0.15,  # Adresse MAC
                4: 0.13,  # Marque/Modèle
                5: 0.12,  # Localisation
                6: 0.12,  # Utilisateur
                7: 0.10,  # Date
                8: 0.04   # Commentaires
            }.items():
                width = int(available_width * ratio)
                self.table_widget.setColumnWidth(column, width)

    def show_dashboard(self):
        dashboard = DashboardDialog(self.session, self)
        dashboard.exec_()