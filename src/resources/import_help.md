# Guide d'importation CSV

Pour importer correctement vos données, votre fichier CSV doit :

## 1. Format du fichier
- Être encodé en UTF-8
- Utiliser la virgule (,) comme séparateur
- Contenir une ligne d'en-tête

## 2. Structure des colonnes
L'ordre des colonnes doit être :
1. Nom (obligatoire)
2. Numéro de Série
3. Adresse MAC
4. Marque/Modèle
5. Catégorie
6. Localisation
7. Utilisateur Assigné
8. Date d'Assignement (format: YYYY-MM-DD)
9. Commentaires

## 3. Exemple de ligne
Nom,N°Serie,MAC,Marque/Modele,Categorie,Lieu,User,Date,Commentaires
PC-001,ABC123,00:11:22:33:44:55,Dell XPS,PC,Bureau A,Jean,2024-01-15,RAS

## Notes importantes
- Seul le nom est obligatoire, les autres champs peuvent être vides
- Les dates doivent être au format YYYY-MM-DD
- Les champs vides doivent être représentés par rien entre les virgules