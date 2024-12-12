from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QWidget, QLabel, QGridLayout
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QBarSeries, QBarSet, QValueAxis, QBarCategoryAxis
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from sqlalchemy import func
from src.database.models import Material

class DashboardDialog(QDialog):
    def __init__(self, session, parent=None):
        super().__init__(parent)
        self.session = session
        self.setWindowTitle("Tableau de Bord")
        self.setMinimumSize(800, 600)
        
        # Layout principal
        layout = QVBoxLayout(self)
        
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
        
        # Statistiques générales
        stats = self.get_general_stats()
        stats_label = QLabel(
            f"<h3>Statistiques générales</h3>"
            f"<p><b>Total matériels:</b> {stats['total']}</p>"
            f"<p><b>Matériels assignés:</b> {stats['assigned']}</p>"
            f"<p><b>Matériels non assignés:</b> {stats['unassigned']}</p>"
        )
        stats_label.setStyleSheet("QLabel { padding: 10px; }")
        layout.addWidget(stats_label, 0, 0)
        
        # Graphique par catégorie
        category_chart = self.create_category_chart()
        layout.addWidget(category_chart, 1, 0)
        
        return tab

    def create_location_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        chart_view = self.create_location_chart()
        layout.addWidget(chart_view)
        return tab

    def create_users_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        chart_view = self.create_users_chart()
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
            
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Répartition par catégorie")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.legend().setVisible(True)
        
        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)
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
        
        axisX = QBarCategoryAxis()
        axisX.append(categories)
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)
        
        axisY = QValueAxis()
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)
        
        chart.legend().setVisible(True)
        
        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)
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
        
        axisX = QBarCategoryAxis()
        axisX.append(categories)
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)
        
        axisY = QValueAxis()
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)
        
        chart.legend().setVisible(True)
        
        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)
        return chartview 