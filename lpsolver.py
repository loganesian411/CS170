import numpy as np
import pulp

def cycleCost(cycle):
    """Calculate the cost of a particular cycle"""
    return cycle[1]

def lpsetpack(cycle_cost_pairs):
    """Expects a list of ([cycle], cost) tuple pairs."""
    # extract cycles and costs from the given information
    cycles, costs = zip(*cycle_cost_pairs)

    # create a set of all individuals
    patients = set()
    [patients.update(cycle) for cycle in cycles]

    x = pulp.LpVariable.dicts('surgery_group', cycle_cost_pairs,
                              lowBound = 0,
                              upBound = 1,
                              cat = pulp.LpInteger)

   

    #create a binary variable to state that a table setting is used
    surgery_model = pulp.LpProblem("Kidney Donor/Patient Model", pulp.LpMaximize)

    # objective function
    surgery_model += sum([cycleCost(cycle) * x[cycle] for cycle in cycle_cost_pairs])

    # constraint that patient must appear no more than once
    for patient in patients:
        surgery_model += sum([x[cycle] for cycle in cycle_cost_pairs
                                    if patient in cycle[0]]) <= 1

    # solve the linear program
    surgery_model.solve()

    cycles_selected = []
    for cycle in cycle_cost_pairs:
        if x[cycle].value() == 1.0:
            print(cycle[0])
            cycles_selected.append(cycle[0])

    return cycles_selected

