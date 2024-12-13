# GestCharge - Gestionnaire de Matériel

GestCharge est une application de bureau permettant de gérer efficacement l'inventaire du matériel informatique d'une entreprise. Elle offre une interface intuitive pour suivre les équipements, leur attribution et leur localisation.

## Dernières mises à jour (v1.1.0)

- **Amélioration de l'interface utilisateur**
  - Persistance du thème choisi (clair/sombre) entre les sessions
  - Redimensionnement automatique et intelligent des colonnes
  - Meilleure réactivité de l'interface

- **Refactoring majeur**
  - Séparation des responsabilités (Material, Theme, Toolbar Managers)
  - Styles externalisés dans un fichier QSS dédié
  - Code plus maintenable et modulaire

- **Optimisations**
  - Amélioration des performances de chargement
  - Gestion optimisée de la mémoire
  - Réduction de la duplication de code

## Fonctionnalités

### 1. Gestion du Matériel
- **Ajout de matériel** : Formulaire complet pour ajouter un nouvel équipement
- **Modification** : Édition directe dans le tableau
- **Suppression** : Individuelle ou multiple avec confirmation
- **Recherche** : Recherche instantanée dans tous les champs

### 2. Import/Export
- **Import CSV** : Import en masse de données via fichier CSV
- **Export CSV** : Export des données pour sauvegarde ou analyse
- **Génération PDF** : Création de rapports PDF professionnels
- **Guide d'importation** : Assistant détaillé pour le format CSV

### 3. Visualisation
- **Tableau de bord** : Statistiques et graphiques
  - Répartition par catégorie
  - Distribution par localisation
  - Attribution par utilisateur
  - Statistiques générales

### 4. Interface
- **Mode sombre/clair** : Interface adaptable
- **Responsive** : S'adapte à la taille de la fenêtre
- **Colonnes ajustables** : Personnalisation de l'affichage

## Installation

### Prérequis
- Python 3.8 ou supérieur
- Gestionnaire de paquets pip
- Base de données SQLite (incluse avec Python)

### Sur Linux

1. Cloner le dépôt :
```bash
git clone https://github.com/Wilfrayde/GestCharge.git
cd GestCharge
```

2. Installation des dépendances système :
```bash
sudo apt update
sudo apt install python3-pip python3-venv python3-qt5
```

3. Création et activation de l'environnement virtuel :
```bash
python3 -m venv .venv
source .venv/bin/activate
```

4. Installation des dépendances Python :
```bash
pip install -r requirements.txt
```

### Sur Windows

1. Télécharger et installer Python depuis [python.org](https://www.python.org/downloads/)

2. Cloner le dépôt :
```powershell
git clone https://github.com/Wilfrayde/GestCharge.git
cd GestCharge
```

3. Créer et activer l'environnement virtuel :
```powershell
python -m venv .venv
.venv\Scripts\activate
```

4. Installer les dépendances :
```powershell
pip install -r requirements.txt
```

### Sur macOS

1. Installer Homebrew si non installé :
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Installer Python et Qt :
```bash
brew install python@3.8 pyqt@5
```

3. Cloner et configurer :
```bash
git clone https://github.com/Wilfrayde/GestCharge.git
cd GestCharge
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Utilisation

### Démarrage
```bash
# Activer l'environnement virtuel
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Lancer l'application
python src/main.py
```

### Guide Détaillé des Fonctionnalités

#### 1. Gestion du Matériel

##### Ajouter un équipement
1. Cliquer sur "➕ Ajouter"
2. Remplir les champs :
   - Nom (obligatoire)
   - Numéro de série
   - Adresse MAC
   - Marque/Modèle
   - Catégorie
   - Localisation
   - Utilisateur
   - Date d'attribution
   - Commentaires
3. Valider avec "OK"

##### Modifier un équipement
- Double-cliquer sur la cellule à modifier
- Modifier la valeur
- Appuyer sur Entrée pour valider

##### Supprimer des équipements
- **Suppression individuelle** : Clic droit → Supprimer
- **Suppression multiple** : 
  1. Ctrl+Clic pour sélectionner plusieurs lignes
  2. Cliquer sur "🗑️ Supprimer"
  3. Confirmer la suppression

#### 2. Import/Export

##### Import CSV
1. Cliquer sur "📥 Importer"
2. Sélectionner un fichier CSV
3. Format requis :
```csv
Nom,N°Serie,MAC,Marque/Modele,Categorie,Lieu,User,Date,Commentaires
PC-001,ABC123,00:11:22:33:44:55,Dell XPS,PC,Bureau A,Jean,2024-01-15,RAS
```

##### Export CSV
1. Cliquer sur "📤 Exporter"
2. Choisir l'emplacement du fichier
3. Le fichier contiendra toutes les données au même format que l'import

##### Génération PDF
1. Cliquer sur "📄 Générer PDF"
2. Choisir l'emplacement du rapport
3. Le PDF généré inclut :
   - En-tête avec date de génération
   - Tableau formaté des équipements
   - Pied de page

#### 3. Tableau de Bord

##### Accès aux statistiques
1. Cliquer sur "📊 Statistiques"
2. Trois onglets disponibles :
   - **Vue d'ensemble** : Statistiques générales et répartition par catégorie
   - **Par localisation** : Distribution des équipements par site
   - **Par utilisateur** : Attribution du matériel par utilisateur

##### Fonctionnalités des graphiques
- Interactifs : survol pour plus de détails
- Animations fluides
- Légendes détaillées

#### 4. Interface

##### Mode sombre/clair
- Cliquer sur l'icône "☼/☾" pour basculer
- Le choix est sauvegardé entre les sessions

##### Recherche
- Saisie instantanée dans la barre de recherche
- Recherche dans tous les champs
- Mise à jour en temps réel des résultats

## Structure du Projet

```
GestCharge/
├── src/
│   ├── database/
│   │   ├── models.py      # Modèles de données
│   │   ├── queries.py     # Requêtes SQL
│   │   └── db_setup.py    # Configuration BD
│   ├── gui/
│   │   ├── main_window.py # Fenêtre principale
│   │   ├── add_item.py    # Dialogue d'ajout
│   │   ├── dashboard.py   # Tableau de bord
│   │   └── toolbar_manager.py # Gestionnaire de la barre d'outils
│   ├── utils/
│   │   ├── material_manager.py # Gestionnaire des matériels
│   │   ├── theme_manager.py    # Gestionnaire des thèmes
│   │   └── pdf_generator.py    # Générateur PDF
│   ├── resources/
│   │   └── styles.qss     # Styles de l'interface
│   └── main.py            # Point d'entrée
├── requirements.txt       # Dépendances
└── README.md             # Documentation
```

## Contribution

1. Fork du projet
2. Créer une branche (`git checkout -b feature/NouvelleFeature`)
3. Commit des changements (`git commit -m 'Ajout de NouvelleFeature'`)
4. Push vers la branche (`git push origin feature/NouvelleFeature`)
5. Ouvrir une Pull Request