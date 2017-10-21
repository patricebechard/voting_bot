# Robot pour le combat des mots

Ce robot permet de voter un grand nombre de fois à un sondage retrouvé en ligne. Il cherche dans la page source HTML d'un url donné pour un module ou voter de type 'Radio' et coche la case voulue selon une cible. Il soumet ensuite le formulaire répète cette étape pour un nombre de fois voulu.

Le code est appelé directement du terminal de la façon suivante:

`python3 voting_bot.py`

Il est possible d'ajouter l'argument `-d` (ou `--default` de façon équivalente) pour appeler directement la tâche pour laquelle le robot a été conçu, soit voter pour un gagnant au 'Combat des mots' de l'émission de radio 'Plus on est de fous, plus on lit'. 
