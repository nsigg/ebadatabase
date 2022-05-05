# ebadatabase

Data of 2021 was extracted from https://www.eba.europa.eu/risk-analysis-and-data/eu-wide-transparency-exercise

transformed via guidelines from previous project group (UTF-8 encoded and selected worksheets only)


# Auszug aus dem ReadMe der vorherigen Gruppe bezüglich der Datentransformationen: 

Die CSV Dateien der EBA der Jahre 2015 bis 2020 sind in der Datei data.zip zu finden. Sie müssen vor Durchführung des Imports in das Root-Verzeichnis als Ordner 'data' entpackt werden. (Bsp.: banks.csv muss für das Jahr 2020 wie folgt vorliegen: data\2020\banks.csv)

Für jedes Jahr gibt es folgende Dateien:

- banks.csv Diese Datei muss manuell erstellt werden. Hierzu muss das Bankslist-Sheet der Metadata Exceltabelle in eine CSV-Datei extrahiert werden. Beachte: Die CSV-Datei muss UTF-8 codiert und durch ";" getrennt vorliegen.
- sdd.csv Diese Datei muss manuell erstellt werden. Hierzu muss das einzige Sheet der Data Dictionary Exceltabelle in eine CSV-Datei extrahiert werden. Beachte: Die CSV-Datei muss UTF-8 codiert und durch ";" getrennt vorliegen.
- tr_cre.csv Diese Datei enthält alle Daten zur Credit Risk und kann ohne Anpassung verwendet werden.
- tr_mrk.csv Diese Datei enthält alle Daten zur Market Risk und kann ohne Anpassung verwendet werden.
- tr_oth.csv Diese Datei enthält alle weiteren Daten und kann ohne Anpassung verwendet werden.
- tr_sov.csv Diese Datei enthält alle Daten zur Sovereign Debt Exposure und kann ohne Anpassung verwendet werden.
