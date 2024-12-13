from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QDateEdit, QMessageBox, QComboBox
from PyQt5.QtCore import QDate
from src.database.db_setup import get_session
from src.database.models import Material
from src.database.queries import add_material
from datetime import datetime

class AddItemDialog(QDialog):
    def __init__(self, session):
        super().__init__()
        self.setWindowTitle("Ajouter un Matériel")
        self.setGeometry(100, 100, 400, 500)
        self.session = session
        
        layout = QVBoxLayout()
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nom du Matériel")
        layout.addWidget(QLabel("Nom:"))
        layout.addWidget(self.name_input)
        
        self.serial_number_input = QLineEdit()
        self.serial_number_input.setPlaceholderText("Numéro de Série")
        layout.addWidget(QLabel("Numéro de Série:"))
        layout.addWidget(self.serial_number_input)
        
        self.mac_address_input = QLineEdit()
        self.mac_address_input.setPlaceholderText("Adresse MAC")
        layout.addWidget(QLabel("Adresse MAC:"))
        layout.addWidget(self.mac_address_input)
        
        self.brand_model_input = QLineEdit()
        self.brand_model_input.setPlaceholderText("Marque/Modèle")
        layout.addWidget(QLabel("Marque/Modèle:"))
        layout.addWidget(self.brand_model_input)
        
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("Localisation")
        layout.addWidget(QLabel("Localisation:"))
        layout.addWidget(self.location_input)
        
        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Catégorie")
        layout.addWidget(QLabel("Catégorie:"))
        layout.addWidget(self.category_input)
        
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Utilisateur Assigné")
        layout.addWidget(QLabel("Utilisateur Assigné:"))
        layout.addWidget(self.user_input)
        
        self.assignment_date_input = QDateEdit()
        self.assignment_date_input.setDate(QDate.currentDate())
        self.assignment_date_input.setDisplayFormat("dd/MM/yyyy")  # Format français
        layout.addWidget(QLabel("Date d'Assignement:"))
        layout.addWidget(self.assignment_date_input)
        
        self.comments_input = QLineEdit()
        self.comments_input.setPlaceholderText("Commentaires")
        layout.addWidget(QLabel("Commentaires:"))
        layout.addWidget(self.comments_input)
        
        self.submit_button = QPushButton("Ajouter")
        self.submit_button.clicked.connect(self.submit)
        layout.addWidget(self.submit_button)
        
        self.setLayout(layout)

    def submit(self):
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Erreur", "Le nom du matériel est obligatoire.")
            return
        
        try:
            material_data = self.get_material_data()
            add_material(self.session, **material_data)
            self.session.commit()
            super().accept()
        except Exception as e:
            self.session.rollback()
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'ajout: {str(e)}")

    def get_material_data(self):
        # Récupérer la date au format français
        date = self.assignment_date_input.date().toPyDate()
        return {
            "name": self.name_input.text().strip(),
            "serial_number": self.serial_number_input.text().strip() or None,
            "mac_address": self.mac_address_input.text().strip() or None,
            "brand_model": self.brand_model_input.text().strip() or None,
            "location": self.location_input.text().strip() or None,
            "category": self.category_input.text().strip() or None,
            "assigned_user": self.user_input.text().strip() or None,
            "assignment_date": date,
            "comments": self.comments_input.text().strip() or None,
        }
