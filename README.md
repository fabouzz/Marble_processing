# Traitement d'image: détection d'éléments lors de la chute d'une bille dans un liquide 

Ce repository regroupe différents outils de traitement d'images afin de traiter des mesures vidéo de chute de bille sur une surface liquide. Les outils développés comprennent la détection et l'identification de la position de la bille qui chute ainsi que la détection des bulles et de la cavité causée par la chute dans le liquide

## But du projet

L'objectif est de traiter les vidéos de mesures pour le projet bille afin de détecter les bulles, ondulations de cavité, etc. ainsi que tout autre événement pertinent. L'avancée actuelle du projet permet seulement d'obtenir l'évolution de la position de la bille ainsi que de détecter et de compter les bulles.

## Objectifs

- Arrière-plan propre sur la vidéo: isoler les bulles, la bille et les ondulations de la surface du reste
- Essais des programmes sur la zone de la cavité pour l'identifier
- Tracking de la bille: vitesse, position
- Tracking automatique des bulles: nombre, oscillation, déplacement, vitesse

## Outils développés

Pour du traitement d'image, il s'agit tout d'abord d'identifier les outils mis à disposition par la communauté sur Python 3; il existe de nombreuses librairies:
- Numpy et Scipy (traitement d'image, filtrage)
- Skimage (filtrage d'image)
- Cv2 avec OpenCv (filtrage, tracking, machine learning et autres)
- Trackpy (librairie de tracking)
- Exemple pour des bulles de mousse: http://soft-matter.github.io/trackpy/v0.3.0/tutorial/custom-feature-detection.html

## Détection sur une image fixe (exemple)

<img src="images/screen_bulles.png" width="400"/>
Image brut

<img src="images/exampleimage.png" width="400"/>
Image après le traitement: les bulles détectées sont repérées par un point rouge

## Détection de la bille avec du machine learning

TODO

## Détection des bulles

Une classe regroupant divers outils a été créée et s'intitule `BubbleDetection`. Un seul outil de détection utilise le module `cv2` avec les méthodes `findContours` et `moments` pour détecter les contours des différents éléments et calculer leur centre de gravité respectifs. Il existe plusieurs méthodes pour filtrer et binariser l'image mais la méthode `SmoothFiltering` est la plus efficace et la seule vraiment utilisable.

### Perspectives

Améliorer les outils de filtrage et de détection: obtenir les trajectoires des bulles dans un fichier pour pouvoir tracer les trajectoires et/ou le champ de vitesse des bulles. Ces données pourraient être utiles afin de pouvoir les comparer avec les paramètres d'entrée de l'étude paramétrique réalisée. Une autre possibilité pourrait être d'ajouter les outils de machine learning développés précédemment pour détecter les bulles plus finement.
