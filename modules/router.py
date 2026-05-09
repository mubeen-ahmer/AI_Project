def route_request(request):
    """
    Examines the request category and determines which
    modules to activate. Returns a list of module names
    in the order they should be executed.
    """
    category = request["request_category"]

    if category == "route_request":
        pipeline = ["search"]

    elif category == "policy_check":
        pipeline = ["knowledge_base"]

    elif category == "control_allocation_request":
        pipeline = ["knowledge_base", "csp"]

    elif category == "emergency_response_request":
        pipeline = ["ann", "knowledge_base", "csp", "search"]

    elif category == "integrated_city_service_request":
        pipeline = ["ann", "knowledge_base", "csp", "search"]

    else:
        raise ValueError(f"Unknown request category: {category}")

    print(f"[Router] Category: {category}")
    print(f"[Router] Pipeline: {pipeline}")
    return pipeline