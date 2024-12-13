from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5.QtCore import Qt
from datetime import datetime
import csv
from src.database.models import Material

class MaterialManager:
    def __init__(self, session, table_widget):
        self.session = session
        self.table_widget = table_widget
        self.materials_dict = {}
        self.all_materials = []

    def load_materials(self):
        query = self.session.query(Material).order_by(Material.name)
        materials = query.all()
        self.materials_dict = {m.id: m for m in materials}
        self.all_materials = materials
        self.display_materials(self.all_materials)

    def display_materials(self, materials):
        self.table_widget.blockSignals(True)
        
        self.table_widget.setRowCount(len(materials))
        self.table_widget.setColumnCount(9)
        
        self.table_widget.setHorizontalHeaderLabels([
            "Nom", "Numéro de Série", "Catégorie", "Adresse MAC", 
            "Marque/Modèle", "Localisation", "Utilisateur Assigné", 
            "Date d'Assignement", "Commentaires"
        ])
        
        for i, material in enumerate(materials):
            name_item = QTableWidgetItem(material.name)
            name_item.setData(Qt.UserRole, material.id)
            
            items = [
                name_item,
                QTableWidgetItem(str(material.serial_number or "")),
                QTableWidgetItem(material.category or ""),
                QTableWidgetItem(material.mac_address or ""),
                QTableWidgetItem(material.brand_model or ""),
                QTableWidgetItem(material.location or ""),
                QTableWidgetItem(material.assigned_user or ""),
                QTableWidgetItem(material.assignment_date.strftime("%Y-%m-%d") if material.assignment_date else ""),
                QTableWidgetItem(material.comments or "")
            ]
            
            for j, item in enumerate(items):
                self.table_widget.setItem(i, j, item)
        
        self.table_widget.blockSignals(False)
        
        # Ajuster les colonnes après avoir rempli la table
        self.adjust_columns()

    def filter_materials(self, search_text):
        if not search_text:
            self.display_materials(self.all_materials)
            return
        
        search_text = search_text.lower()
        filtered_materials = [
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
        ]
        
        self.display_materials(filtered_materials)

    def delete_materials(self, material_ids):
        try:
            self.session.query(Material).filter(
                Material.id.in_(material_ids)
            ).delete(synchronize_session='fetch')
            self.session.commit()
            
            # Mettre à jour le cache local
            for material_id in material_ids:
                self.materials_dict.pop(material_id, None)
            self.all_materials = list(self.materials_dict.values())
            self.display_materials(self.all_materials)
            
            return True
        except Exception as e:
            self.session.rollback()
            QMessageBox.critical(None, "Erreur", f"Erreur lors de la suppression: {str(e)}")
            return False

    def import_materials(self, file_name):
        try:
            materials_to_add = []
            with open(file_name, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                
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
            
            self.session.bulk_save_objects(materials_to_add)
            self.session.commit()
            self.load_materials()
            return True
            
        except Exception as e:
            self.session.rollback()
            QMessageBox.critical(None, "Erreur", f"Erreur lors de l'import: {str(e)}")
            return False

    def export_materials(self, file_name):
        try:
            with open(file_name, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "Nom", "Numéro de Série", "Adresse MAC", "Marque/Modèle",
                    "Catégorie", "Localisation", "Utilisateur Assigné",
                    "Date d'Assignement", "Commentaires"
                ])
                
                for material in self.all_materials:
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
                return True
                
        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Erreur lors de l'export: {str(e)}")
            return False

    def adjust_columns(self):
        """Ajuste les colonnes à la taille de la fenêtre"""
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