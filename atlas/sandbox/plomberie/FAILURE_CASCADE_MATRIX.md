# FAILURE CASCADE MATRIX

| # | Scénario | Ce qui casse | Stable | Gravité | Action secours | Next best action | Test |
|---|---|---|---|---|---|---|---|
|1|appel incomplet|B,D|C|élevée|rappel structuré|collecter 5 champs critiques|scenario_01|
|2|adresse absente|D,E|B|élevée|bloquer dispatch|valider adresse|scenario_02|
|3|urgence mal classée|C,D|H|critique|retriage|escalade planning|scenario_03|
|4|sécurité gaz ignorée|C,E|A|critique|arrêt immédiat|validation sécurité|scenario_04|
|5|technicien sans packet|D,H|B|élevée|packet express|checklist pré-départ|scenario_05|
|6|devis trop tôt|E|C|moyenne|devis provisoire|collecter mesures|scenario_06|
|7|facture oubliée|E,G|D|moyenne|génération facture|relance J+2|scenario_07|
|8|relance non faite|G|C|moyenne|cadence relance|assigner owner|scenario_08|
|9|assurance non documentée|F|D|élevée|dossier incident|collecte pièces|scenario_09|
|10|photos manquantes|H,J|A|moyenne|demande photos|standard preuve|scenario_10|
|11|propriétaire non informé|I|D|moyenne|message officiel|coordination parties|scenario_11|
|12|syndic non coordonné|D,F|B|élevée|point syndic|calendrier validé|scenario_12|
|13|matériel oublié|D,E|A|élevée|réappro rapide|kit minimum|scenario_13|
|14|client pro non relancé|G,I|C|moyenne|contact compte|plan fidélisation|scenario_14|
|15|litige sans preuve|F,I|G|critique|gel dossier|collecte preuves|scenario_15|
|16|intervention sans compte rendu|H,J|E|élevée|CR rétroactif|obligation clôture|scenario_16|
|17|retour terrain absent|J|I|moyenne|debrief|rituel fin mission|scenario_17|
|18|planning saturé|D,I|F|élevée|priorisation urgence|sous-traitance validée|scenario_18|
|19|technicien indisponible|D|B|élevée|dispatch alternatif|mise à jour capacité|scenario_19|
|20|données non anonymisées|conformité|A|critique|anonymiser|audit conformité|scenario_20|
