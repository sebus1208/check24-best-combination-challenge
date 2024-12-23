import pandas as pd
import pulp
import time

def ILP_set_cover(game_ids, anbieter, abdeckung, preis):
    """
    Greedy-Algorithmus für das Set Cover Problem.
    
    :param game_ids: Liste der Spiele, die abgedeckt werden müssen
    :param anbieter: Liste der Anbieter
    :param abdeckung: Dictionary mit Anbieter als Schlüssel und Liste der abgedeckten Spiele als Wert
    :param preis: Dictionary mit Anbieter als Schlüssel und den Kosten als Wert
    :return: Liste der ausgewählten Anbieter, Preis und ungedeckte Spiele
    """
    covered_games = [g for g in game_ids if any(g in abdeckung[k] for k in abdeckung)]
    uncovered_games = [g for g in game_ids if not any(g in abdeckung[k] for k in abdeckung)]

    # Das Set-Cover Problem wird als Lineares Programmierungsproblem definiert
    problem = pulp.LpProblem("MinimalCostPackages", pulp.LpMinimize)

    #Entscheidungsvariablen: Alle Anbieter ob diese gekauft werden oder nicht
    x = pulp.LpVariable.dicts('Anbieter', anbieter, cat='Binary')

    #Zielminimierung: Möglichst geringe kosten, 0/1 ob anbieter ausgewählt wird * preis
    problem += pulp.lpSum(preis[k]*x[k] for k in anbieter)

    #Einschränkungen: Jedes Spiel muss ansehbar sein wenn es auch angeboten wird
    for g in covered_games:
        problem += pulp.lpSum([
            x[k] for k in anbieter if k in abdeckung and g in abdeckung[k]
        ]) >= 1, f"Deckung_{g}"

    problem.solve() # Hier wird Branch-and-Cut verwendet

    selected_provider = []

    for a in anbieter:
        if pulp.value(x[a]) == 1:
            selected_provider.append(a)

    # Kosten minimieren
    price = pulp.value(problem.objective)

    return {"ausgewählte_anbieter": selected_provider, "preis": price, "ungedeckte_spiele": uncovered_games}


def greedy_set_cover(game_ids, anbieter, abdeckung, preis):
    """
    Greedy-Algorithmus für das Set Cover Problem.
    
    :param game_ids: Liste der Spiele, die abgedeckt werden müssen
    :param anbieter: Liste der Anbieter
    :param abdeckung: Dictionary mit Anbieter als Schlüssel und Liste der abgedeckten Spiele als Wert
    :param preis: Dictionary mit Anbieter als Schlüssel und den Kosten als Wert
    :return: Liste der ausgewählten Anbieter
    """
    covered_games = [g for g in game_ids if any(g in abdeckung[k] for k in abdeckung)]
    uncovered_games = [g for g in game_ids if not any(g in abdeckung[k] for k in abdeckung)]

    open_games = set(covered_games)  # Noch nicht abgedeckte Spiele
    selected_providers = []          # Ausgewählte Anbieter
    
    while open_games:
        # Finde den Anbieter mit dem besten Preis-Leistungs-Verhältnis
        best_provider = max(
            anbieter,
            key=lambda a: (
                len(open_games & set(abdeckung.get(a, []))) / preis[a] if preis[a] > 0 else 0
            )
        )
        
        # Füge den Anbieter zur Lösung hinzu
        selected_providers.append(best_provider)
        
        # Entferne die von diesem Anbieter abgedeckten Spiele aus der Liste
        open_games -= set(abdeckung.get(best_provider, []))

    price = 0
    for p in selected_providers:
        price += preis[p]

    return {'ausgewählte_anbieter': selected_providers, 'preis': price,'ungedeckte_spiele': uncovered_games}
