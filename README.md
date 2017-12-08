# Heuristieken case RailNL

In dit project wordt de optimale lijnvoering voor het Nederlandse spoornetwerk bepaald. De lijnvoering bestaat uit een vast aantal trajecten, waarbij over elk traject één trein rijdt. Er wordt gebruikgemaakt van de algoritmen Breadth-First, Hillclimber en Greedy om de oplossing voor dit probleem te optimaliseren. Daarnaast wordt een zelf geïmplementeerde random-search toegepast, die willekeurige opties als resultaat geeft. De algoritmen worden met elkaar vergeleken, en op basis van een scorefunctie en de runtime wordt bepaald welk algoritme het meest geschikt is en wordt de beste oplossing voor dit probleem benaderd.

## Gebruikte software
- Python 3.6, gebruikt om de code te runnen
- numpy, gebruikt om als hoofdstructuur om de belangrijkste data op te slaan binnen de python bestanden
- matplotlib, gebruikt om de berekende trajecten in een kaartje van Holland te plotten. Zowel numpy als matplotlib kunnen worden geinstalleerd met behulp van pip

## Structuur
De repository is opgedeeld in een aantal mapjes. 'Algorithms' bevat uiteindelijk de individuele python algoritme bestanden die met behulp van dezelfde algemene inputs hun eigen output kunnen creëren. 'Classes' bevat alle python class bestanden. 'csv' bevat de benodigde data bestanden om een datastructuur in python op te kunnen zetten. 'Functions' bevat de functies om de score te berekenen van trajecten, evenals om deze trajecten te visualiseren.

## Werking van het programma
Wanneer de gehele datastructuur goed verbonden is en de algoritmes volledig werken, zal alles via één hoofdbestand aangeroepen kunnen worden. Op dit moment is het hoofdbestand 'RailNL.py', waarin het 'random' algoritme al kan worden aangeroepen. Wanneer 'py railnl.py' wordt gerund in de terminal zal het algoritme dus automatisch werken.

## Authors

* **Jesse Emmelot** - *Initial work* - [jemmelot](https://github.com/jemmelot)
* **Siwa Sardjoemissier** - *Initial work* - [swcloud1](https://github.com/swcloud1)
* **Bas Zwanenburg** - *Initial work* - [baszwanenburg](https://github.com/baszwanenburg)

See also the list of [contributors](https://github.com/jemmelot/Heuristieken/graphs/contributors) who participated in this project.

## Acknowledgments
Begeleiding:
- Bas Terwijn
- Maarten van der Sande

