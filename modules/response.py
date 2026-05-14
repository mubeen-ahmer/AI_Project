def build_response(request, pipeline, ann_result=None, kb_result=None, csp_result=None, route_result=None):
    """
    Builds the final response by combining outputs from
    all modules that were used in the pipeline.
    Only includes fields from modules that were actually used.
    Returns a formatted response dictionary.
    """
    response = {}

    response["request_id"]      = request["request_id"]
    response["vehicle_type"]    = request["vehicle_type"]
    response["category"]        = request["request_category"]
    response["from"]            = request["current_location"]
    response["to"]              = request["destination"]

    if "ann" in pipeline and ann_result:
        response["predicted_priority"] = ann_result

    if "knowledge_base" in pipeline and kb_result:
        response["policy_status"]   = "APPROVED" if kb_result["approved"] else "REJECTED"
        response["priority"]        = kb_result["priority"]
        response["allowed_actions"] = kb_result["allowed_actions"]
        response["reason"]          = kb_result["reason"]

    if "csp" in pipeline and csp_result:
        response["signal_plan"] = csp_result

    if "search" in pipeline and route_result:
        response["route"]      = route_result[0]
        response["route_cost"] = route_result[1]

    if kb_result and not kb_result["approved"]:
        response["message"] = "❌ Request REJECTED — unauthorized action"
    elif "search" in pipeline and route_result[0]:
        response["message"] = "✅ Route successfully generated"
    else:
        response["message"] = "✅ Request processed successfully"

    return response


def print_response(response):
    """
    Prints the final response in a clean readable format.
    Only displays fields that are present in the response.
    """
    print("\n" + "="*50)
    print("         FINAL RESPONSE")
    print("="*50)
    print(f"  Request ID  : {response['request_id']}")
    print(f"  Vehicle     : {response['vehicle_type']}")
    print(f"  Category    : {response['category']}")
    print(f"  From        : {response['from']}")
    print(f"  To          : {response['to']}")

    if "predicted_priority" in response:
        print(f"  ANN Priority: {response['predicted_priority']}")

    if "policy_status" in response:
        print(f"  Policy      : {response['policy_status']}")
        print(f"  Priority    : {response['priority']}")
        print(f"  Actions     : {response['allowed_actions']}")
        print(f"  Reason      : {response['reason']}")

    if "signal_plan" in response:
        print(f"  Signal Plan : {response['signal_plan']}")

    if "route" in response:
        print(f"  Route       : {' → '.join(response['route'])}")
        print(f"  Route Cost  : {response['route_cost']}")

    print(f"  Message     : {response['message']}")
    print("="*50 + "\n")