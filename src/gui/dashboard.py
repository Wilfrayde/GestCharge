from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QWidget, QLabel, QGridLayout
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QBarSeries, QBarSet, QValueAxis, QBarCategoryAxis
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QBrush, QColor
from sqlalchemy import func
from src.database.models import Material

class DashboardDialog(QDialog):
    def __init__(self, session, parent=None):
        super().__init__(parent)
        self.session = session
        self.setWindowTitle("Tableau de Bord")
        self.setMinimumSize(800, 600)
        
        # Appliquer un style moderne à l'ensemble du dashboard
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff; /* Arrière-plan blanc pour un meilleur contraste */
            }
            QLabel {
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                color: #333333;
            }
            QTabWidget::pane {
                border-top: 2px solid #C2C7CB;
            }
            QTabBar::tab {
                background: #d9d9d9; /* Fond des onglets modifié pour une meilleure lisibilité */
                color: #333333;      /* Couleur de texte explicitement définie */
                border: 1px solid #C4C4C4;
                padding: 10px;
                margin: 2px;
            }
            QTabBar::tab:selected {
                background: #ffffff;
                color: #333333;
                border-bottom-color: #ffffff;
                font-weight: bold;
            }
        """)

        # Layout principal avec marges et espacement améliorés
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Widget à onglets
        tab_widget = QTabWidget()
        
        # Onglet Vue d'ensemble
        overview_tab = self.create_overview_tab()
        tab_widget.addTab(overview_tab, "Vue d'ensemble")
        
        # Onglet Localisation
        location_tab = self.create_location_tab()
        tab_widget.addTab(location_tab, "Par localisation")
        
        # Onglet Utilisateurs
        users_tab = self.create_users_tab()
        tab_widget.addTab(users_tab, "Par utilisateur")
        
        layout.addWidget(tab_widget)

    def create_overview_tab(self):
        tab = QWidget()
        layout = QGridLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setHorizontalSpacing(20)
        layout.setVerticalSpacing(20)
        
        # Ajout d'un en-tête pour la vue d'ensemble
        header_label = QLabel("<h2>Tableau de Bord - Vue d'ensemble</h2>")
        header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(header_label, 0, 0, 1, 2)
        
        # Statistiques générales
        stats = self.get_general_stats()
        stats_label = QLabel(
            f"<p style='font-size: 16px;'><b>Total matériels :</b> {stats['total']}</p>"
            f"<p style='font-size: 16px;'><b>Matériels assignés :</b> {stats['assigned']}</p>"
            f"<p style='font-size: 16px;'><b>Matériels non assignés :</b> {stats['unassigned']}</p>"
        )
        stats_label.setStyleSheet(
            "padding: 10px; background-color: #ffffff; border-radius: 5px;"
        )
        layout.addWidget(stats_label, 1, 0)
        
        # Graphique par catégorie
        category_chart = self.create_category_chart()
        layout.addWidget(category_chart, 2, 0)
        
        return tab

    def create_location_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        chart_view = self.create_location_chart()
        chart_view.setMinimumSize(400, 300)
        layout.addWidget(chart_view)
        return tab

    def create_users_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        chart_view = self.create_users_chart()
        chart_view.setMinimumSize(400, 300)
        layout.addWidget(chart_view)
        return tab

    def get_general_stats(self):
        total = self.session.query(Material).count()
        assigned = self.session.query(Material).filter(
            Material.assigned_user.isnot(None)
        ).count()
        
        return {
            'total': total,
            'assigned': assigned,
            'unassigned': total - assigned
        }

    def create_category_chart(self):
        series = QPieSeries()
        
        categories = self.session.query(
            Material.category, 
            func.count(Material.id)
        ).group_by(Material.category).all()
        
        for category, count in categories:
            series.append(category or "Non catégorisé", count)
        
        # Rendre les étiquettes de chaque tranche visibles uniquement au survol
        for slice in series.slices():
            slice.setLabelVisible(False)  # Masquer les étiquettes par défaut
            slice.setLabelBrush(QBrush(QColor("#333333")))
            # Afficher l'étiquette lors du survol et la masquer lorsqu'on ne survole plus
            slice.hovered.connect(lambda state, s=slice: s.setLabelVisible(state))
            
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Répartition par catégorie")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.legend().setVisible(True)
        chart.setBackgroundVisible(True)
        chart.setBackgroundBrush(QBrush(QColor("#ffffff")))
        chart.setPlotAreaBackgroundVisible(True)
        chart.setPlotAreaBackgroundBrush(QBrush(QColor("#ffffff")))
        chart.setTitleBrush(QBrush(QColor("#333333")))
        chart.legend().setLabelBrush(QBrush(QColor("#333333")))
        
        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)
        chartview.setMinimumSize(400, 300)
        return chartview

    def create_location_chart(self):
        series = QBarSeries()
        
        locations = self.session.query(
            Material.location, 
            func.count(Material.id)
        ).group_by(Material.location).all()
        
        barset = QBarSet("Nombre d'équipements")
        categories = []
        
        for location, count in locations:
            barset.append(count)
            categories.append(location or "Non défini")
        
        series.append(barset)
        
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Répartition par localisation")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setBackgroundVisible(True)
        chart.setBackgroundBrush(QBrush(QColor("#ffffff")))
        chart.setPlotAreaBackgroundVisible(True)
        chart.setPlotAreaBackgroundBrush(QBrush(QColor("#ffffff")))
        chart.setTitleBrush(QBrush(QColor("#333333")))
        chart.legend().setLabelBrush(QBrush(QColor("#333333")))
        
        axisX = QBarCategoryAxis()
        axisX.append(categories)
        axisX.setLabelsBrush(QBrush(QColor("#333333")))
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)
        
        axisY = QValueAxis()
        axisY.setLabelsBrush(QBrush(QColor("#333333")))
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)
        
        chart.legend().setVisible(True)
        
        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)
        chartview.setMinimumSize(400, 300)
        return chartview

    def create_users_chart(self):
        series = QBarSeries()
        
        users = self.session.query(
            Material.assigned_user, 
            func.count(Material.id)
        ).filter(
            Material.assigned_user.isnot(None)
        ).group_by(Material.assigned_user).all()
        
        barset = QBarSet("Équipements assignés")
        categories = []
        
        for user, count in users:
            barset.append(count)
            categories.append(user)
        
        series.append(barset)
        
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Équipements par utilisateur")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setBackgroundVisible(True)
        chart.setBackgroundBrush(QBrush(QColor("#ffffff")))
        chart.setPlotAreaBackgroundVisible(True)
        chart.setPlotAreaBackgroundBrush(QBrush(QColor("#ffffff")))
        chart.setTitleBrush(QBrush(QColor("#333333")))
        chart.legend().setLabelBrush(QBrush(QColor("#333333")))
        
        axisX = QBarCategoryAxis()
        axisX.append(categories)
        axisX.setLabelsBrush(QBrush(QColor("#333333")))
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)
        
        axisY = QValueAxis()
        axisY.setLabelsBrush(QBrush(QColor("#333333")))
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)
        
        chart.legend().setVisible(True)
        
        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)
        chartview.setMinimumSize(400, 300)
        return chartview 