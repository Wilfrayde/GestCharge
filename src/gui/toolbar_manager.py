from PyQt5.QtWidgets import QToolBar, QAction

class ToolbarManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.toolbar = QToolBar()
        self.setup_toolbar()

    def setup_toolbar(self):
        self.toolbar.setMovable(False)
        
        # Groupe Gestion des matériels
        add_action = QAction("➕ Ajouter", self.main_window)
        add_action.triggered.connect(self.main_window.add_material)
        self.toolbar.addAction(add_action)
        
        delete_action = QAction("🗑️ Supprimer", self.main_window)
        delete_action.triggered.connect(self.main_window.delete_selected_materials)
        self.toolbar.addAction(delete_action)
        
        self.toolbar.addSeparator()
        
        # Groupe Import/Export
        import_action = QAction("📥 Importer", self.main_window)
        import_action.triggered.connect(self.main_window.import_materials)
        self.toolbar.addAction(import_action)
        
        import_help_action = QAction("❓ Aide Import", self.main_window)
        import_help_action.triggered.connect(self.main_window.show_import_help)
        self.toolbar.addAction(import_help_action)
        
        export_action = QAction("📤 Exporter", self.main_window)
        export_action.triggered.connect(self.main_window.export_materials)
        self.toolbar.addAction(export_action)
        
        self.toolbar.addSeparator()
        
        # Groupe PDF et Stats
        pdf_action = QAction("📄 Générer PDF", self.main_window)
        pdf_action.triggered.connect(self.main_window.generate_pdf)
        self.toolbar.addAction(pdf_action)
        
        stats_action = QAction("📊 Statistiques", self.main_window)
        stats_action.triggered.connect(self.main_window.show_dashboard)
        self.toolbar.addAction(stats_action)
        
        self.toolbar.addSeparator()
        
        # Thème
        self.main_window.theme_action = QAction("☼", self.main_window)
        self.main_window.theme_action.setToolTip("Changer le thème")
        self.main_window.theme_action.triggered.connect(self.main_window.toggle_theme)
        self.toolbar.addAction(self.main_window.theme_action)
        
        return self.toolbar 