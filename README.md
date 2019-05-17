# Marble_processing

Video processing for objects detection. Bubble detection at the impact of a marble on a water surface.  Programs developped for data science analysis purposes.

## But du projet

L'objectif est de traiter les vidéos de mesures pour le projet bille afin de détecter les bulles, ondulations de cavité, etc. ainsi que tout autre événement pertinent.

## Objectifs

- Arrière-plan propre sur la vidéo: isoler les bulles, la bille et les ondulations de la surface
- Essai sur la mesure de la cavité
- Tracking de la bille: vitesse, position
- Tracking automatique des bulles: nombre et oscillation

## semaine du 13 au 17 mai

Début du projet: soustraction et filtrage de l'arrière-plan, plusieurs méthodes mises en place.
Premier algorithme de détection des bulles: isolation sur une section d'image et comptage avec le module `cv2`
Travail avec du machine learning pour la détection de la bille. Potentielle application pour la détection des bulles mais l'utilité pour la bille est d'éviter de la compter comme une bulle: après le filtrage c'est un simple rond noir sur l'image comme toutes les bulles.