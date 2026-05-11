from data.city_graph import (
    CSP_VARIABLES,
    CSP_DOMAINS,
    CSP_CONSTRAINTS,
    CSP_COORDINATION,
    EMERGENCY_PRIORITY,
    PRECEDENCE_CORRIDOR,
    INTERSECTION_LOCATIONS
)


def is_consistent(variable, value, assignment):
    """
    Checks if assigning 'value' to 'variable' violates
    any constraint with already assigned variables.
    Returns True if consistent, False if conflict found.
    """
    for (v1, v2) in CSP_CONSTRAINTS:
        if variable == v1 and v2 in assignment:
            if assignment[v2] == value:
                return False
        if variable == v2 and v1 in assignment:
            if assignment[v1] == value:
                return False
    return True


def backtrack(assignment):
    """
    Recursively assigns phases to intersections using
    backtracking. Returns complete assignment or None
    if no solution exists.
    """
    # base case — all variables assigned
    if len(assignment) == len(CSP_VARIABLES):
        return assignment

    # pick next unassigned variable
    for var in CSP_VARIABLES:
        if var not in assignment:
            unassigned = var
            break

    # try each value in domain
    for value in CSP_DOMAINS[unassigned]:
        if is_consistent(unassigned, value, assignment):
            assignment[unassigned] = value
            result = backtrack(assignment)
            if result is not None:
                return result
            del assignment[unassigned]  # backtrack

    return None


def run_csp(request, allowed_actions, priority):
    """
    Master CSP function. Runs backtracking to find valid
    signal phase assignments for all intersections.
    Applies emergency overrides if priority is Critical.
    Returns final assignment dictionary.
    """
    print("[CSP] Running signal assignment...")

    # run backtracking to get base assignment
    assignment = backtrack({})

    if assignment is None:
        print("[CSP] No valid assignment found!")
        return None

    # apply coordination preference — S2 and S4 should match if possible
    for (v1, v2) in CSP_COORDINATION:
        if v1 in assignment and v2 in assignment:
            # try to make them match
            for phase in CSP_DOMAINS[v2]:
                if phase == assignment[v1]:
                    assignment[v2] = phase
                    break

    # apply emergency overrides if critical priority
    if priority == "Critical" and "EmergencyRoute" in allowed_actions:
        print("[CSP] Emergency corridor active — overriding signal priorities")
        assignment["S4"] = "PhaseC"  # emergency priority link S4 → S5
        assignment["S5"] = "PhaseB"  # City_Hospital emergency phase
        assignment["S1"] = "PhaseA"  # precedence corridor start

    # print final assignments
    for var in CSP_VARIABLES:
        location = INTERSECTION_LOCATIONS[var]
        print(f"[CSP] {var} ({location}) → {assignment[var]}")

    print("[CSP] Assignment complete.")
    return assignment