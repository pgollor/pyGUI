# pyGUI
python3 modular GUI based on PyQt4

Hier möchte ich ein Projekt vorstellen, dass im [Fachgebiet Messtechnik](http://www.uni-kassel.de/eecs/fachgebiete/messtechnik/) der [Universität Kassel](http://www.uni-kassel.de/) entstanden ist.<br>
Im Rahmen einer Dissertation entstand als Nebenprodukt eine Software-Umgebung um schnell und einfach Python Programme in eine GUI einzubetten und Messungen oder Auswertungen der Messdaten durchführen zu können. Die Wahl der Programmiersprache fiel auf Python aus mehreren Gründen:
* große Anzahl an Bibliotheken zur Signalverarbeitung und gute Darstellungsmöglichkeiten
* hervorragende Unterstützung von QT als GUI Backend
* Möglichkeiten der Einbindung externer Bibliotheken und der Wegfall der teueren Lizenzkosten, wie es bei MATLAB (wurde hauptsächlich früher im Fachgebiet eingesetzt) der Fall ist.

<br>Ich möchte aber ausdrücklich betonen, dass die Veröffentlichung der pyGUI als Opensource-Lizenz von mir und Stanislav Tereschenko ausschließlich privat erfolgt. **Das heißt, dass die Veröffentlichung vom Fachgebiet Messtechnik gestattet wurde, aber das Fachgebiet Messtechnik keinerlei Support oder Haftung übernimmt!**<br><br>
Darüber hinaus möchte ich um Verständnis werben, dass aus verständlichen Gründen nur die GUI an sich und keinerlei Messabläufe, Algorithmen oder Hardwareschnittstellen in der pyGUI enthalten sind.

## Grundidee
Im Fachgebiet sollten verschiedene Messabläufe insbesondere für hochauflösende Interferometer aber auch anschließende Auswertung und Darstellung der Messergebnisse in Python realisiert werden. Das kann man entweder mit X verschiedenen Messprogramm realisieren, oder man entwickelt ein modulares Konstrukt, das man mit den verschiedensten Modulen füttern kann, um Messungen durchführen zu können und eine grafische Ausgabe daraus zu generieren. Daraus entstand die Grundidee zur pyGUI.<br><br>

Aus dieser Grundidee ist eine kleine Eierlegendewollmilchsau geworden, die wir gerne der Opensourcegemeinschaft zur Verfügung stellen möchten. Leider ist aus Zeitgründen die Dokumentation noch sehr rudimentär bzw. schnell zusammen geschrieben. Das werde ich aber so schnell wie möglich versuchen nachzubessern. Aktuell wird mit doxygen eine pdf und eine Windows-Hilfe erstellt. Die Windows-Hilfe soll unter Windows auch noch Zeitnah in die pyGUI direkt eingebunden werden.

## Grobes Konstrukt

Da das Programm modular aufgebaut ist, ist es nicht auf Messabläufe beschränkt. Jeder erdenklicher Programmablauf lässt sich in verschiedenen Modulen nachbilden, mit der die pyGUI gefüttert werden kann.<br>
Das heißt, dass die pyGUI eine grafische Benutzeroberfläche zur Verfügung stellt die mit Qt realisiert wurde und die Module auf einige Standardelemente (Logging, GUI Elemente automatisch speichern, …) zurückgreifen können.<br>
Dazu gibt es drei verschiedene arten von Modulen die man in der pyGUI hinzufügen kann:
* *hidden* Module
* *settings* Module
* *application* Module

Das *hidden* Modul eignet sich perfekt um eine Schnittstelle zu einer DLL, Hardware oder sonst etwas für andere Module herzustellen. Auf diese Schnittstelle kann dann zum Beispiel ein *settings* Modul oder ein *applikation* Modul zugreifen. Das *hidden* Modul hat dabei keine grafische Ausgabe.<br>
Das *settings* und das *application* Modul sind im Grunde genommen gleichwertige Module mit der Ausnahme, dass die *apllication* Module in der GUI direkt angezeigt werden und die *settings* Module nur über das Menü „Module Settings“ zu erreichen sind. Dies soll die bekannt Struktur von Programmen widerspiegeln.<br><br>

Ein paar Testmodule sind in der GUI unter „sampleModules“ enthalten und können bei bedarf in den Ordner „modules“ eingefügt werden. Zum aktivieren des Moduls muss dieses unter dem Menüreiter „Main->Modules“ ausgewählt werden. Nach einem Neustart des Programms wird es automatisch geladen.

## Voraussetzung
Um pyGUI benutzen zu können wird eine python3 Umgebung mit qt und ein paar anderen Bibliotheken benötigt. Am einfachsten Benutzt man unter Windows das winPython Paket und unter Linux die python3-spyderlib. Dann einfach die main.py starten und los geht es.<br><br>

pyGUI kann sowohl unter Windows 7 und 8 als auch unter Linux verwendet werden. Bisher ist der Einsatz aber nur unter Windows getestet worden. Bei anderen Oberflächen wie Gnome oder KDE kann es zu einer anderen Darstellung kommen. Da würden wir uns über zahlreiche Rückmeldungen freuen. Dazu und zu allen anderen Themen der pyGUI kann gerne auf meiner Homepage diskutiert werden.


# License

Dieses Projekt ist lizensiert als Inhalt der
Creative Commons Namensnennung - Weitergabe unter gleichen Bedingungen 3.0 Unported-Lizenz.<br>
Um eine Kopie der Lizenz zu sehen, besuchen Sie http://creativecommons.org/licenses/by-sa/3.0/.<br>
-- englisch version --<br>
This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Germany License.<br>
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a letter to<br>
Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.
