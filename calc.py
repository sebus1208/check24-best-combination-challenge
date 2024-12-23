import pandas as pd
import pulp
import time

def ILP_set_cover(game_ids, providers, coverage, cost):
    """
    Integer Linear Programming (ILP) solution for the Set Cover Problem.

    :param game_ids: List of games to be covered
    :param providers: List of providers
    :param coverage: Dictionary with provider as key and list of covered games as value
    :param cost: Dictionary with provider as key and their cost as value
    :return: List of selected providers, total cost, and uncovered games
    """
    covered_games = [g for g in game_ids if any(g in coverage[k] for k in coverage)]
    uncovered_games = [g for g in game_ids if not any(g in coverage[k] for k in coverage)]

    # Define the Set Cover problem as a Linear Programming problem
    problem = pulp.LpProblem("MinimalCostPackages", pulp.LpMinimize)

    # Decision variables: Whether to select a provider or not
    x = pulp.LpVariable.dicts('Provider', providers, cat='Binary')

    # Objective function: Minimize cost, 0/1 if provider is selected * cost
    problem += pulp.lpSum(cost[k] * x[k] for k in providers)

    # Constraints: Every game must be covered if offered by any provider
    for g in covered_games:
        problem += pulp.lpSum([
            x[k] for k in providers if k in coverage and g in coverage[k]
        ]) >= 1, f"Coverage_{g}"

    problem.solve()  # Uses Branch-and-Cut algorithm

    selected_providers = []

    for p in providers:
        if pulp.value(x[p]) == 1:
            selected_providers.append(p)

    # Minimize total cost
    total_cost = pulp.value(problem.objective)

    return {"selected_providers": selected_providers, "cost": total_cost, "uncovered_games": uncovered_games}


def greedy_set_cover(game_ids, providers, coverage, cost):
    """
    Greedy algorithm for the Set Cover Problem.

    :param game_ids: List of games to be covered
    :param providers: List of providers
    :param coverage: Dictionary with provider as key and list of covered games as value
    :param cost: Dictionary with provider as key and their cost as value
    :return: List of selected providers, total cost, and uncovered games
    """
    covered_games = [g for g in game_ids if any(g in coverage[k] for k in coverage)]
    uncovered_games = [g for g in game_ids if not any(g in coverage[k] for k in coverage)]

    open_games = set(covered_games)  # Games not yet covered
    selected_providers = []          # Selected providers

    while open_games:
        # Find the provider with the best price-performance ratio
        best_provider = max(
            providers,
            key=lambda p: (
                len(open_games & set(coverage.get(p, []))) / cost[p] if cost[p] > 0 else 0
            )
        )

        # Add the provider to the solution
        selected_providers.append(best_provider)

        # Remove games covered by this provider from the list
        open_games -= set(coverage.get(best_provider, []))

    total_cost = sum(cost[p] for p in selected_providers)

    return {'selected_providers': selected_providers, 'cost': total_cost, 'uncovered_games': uncovered_games}
