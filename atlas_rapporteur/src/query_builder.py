from itertools import product

TRADES=["plomberie","chauffage","pompe à chaleur","chaudière","climatisation","électricité","serrurerie","vitrerie","toiture","rénovation complète","isolation","maçonnerie","terrassement","piscine","salle de bain","cuisine","dégâts des eaux"]
CITIES={"france":["Paris","Lyon","Marseille"],"belgique":["Bruxelles","Namur","Liège"],"suisse":["Genève","Lausanne"],"luxembourg":["Luxembourg"],"quebec":["Montréal","Québec"]}
INTENTS=["cherche {trade} urgence {city}","besoin devis {trade} {city}","recherche artisan {trade} {city}","{trade} panne urgent {city}","chantier {trade} à faire {city}"]


def build_queries(limit=80,country=None,trade=None,city=None):
    countries=[country] if country else list(CITIES.keys())
    trades=[trade] if trade else TRADES
    queries=[]
    for c in countries:
        for t,ci,pat in product(trades,CITIES.get(c,[]),INTENTS):
            if city and ci.lower()!=city.lower():
                continue
            queries.append({"query":pat.format(trade=t,city=ci),"country":c,"trade":t,"city":ci})
            if len(queries)>=limit:
                return queries
    return queries
