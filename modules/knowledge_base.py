from data.city_graph import HOSPITALS, INTERSECTION_LOCATIONS

def determine_priority(request):
    """
    Determines the priority level of the vehicle based on
    vehicle class, incident severity and time sensitivity.
    Returns priority as a string: Low, Normal, High or Critical.
    """
    vehicle_class = request["vehicle_class"]
    severity      = request["incident_severity"]
    time_sensitive = request["time_sensitivity"]

    # From PDF rules:
    # EmergencyVehicle + High severity → Critical
    # EmergencyVehicle + time sensitive → High
    # CivilianVehicle → Normal

    if vehicle_class == "EmergencyVehicle" and severity == "high":
        return "Critical"
    elif vehicle_class == "EmergencyVehicle" and time_sensitive:
        return "High"
    elif vehicle_class == "EmergencyVehicle":
        return "High"
    else:
        return "Normal"
    
def check_authorization(request, priority):
    """
    Checks whether the vehicle is authorized to perform
    actions based on its class, destination and priority.
    Returns a dictionary of allowed actions.
    """
    vehicle_class = request["vehicle_class"]
    destination   = request["destination"]
    allowed       = []

    # From PDF rules:
    # EmergencyVehicle + SignalZone → Authorized for SignalOverride
    # CivilianVehicle + SignalZone → NOT authorized for SignalOverride
    # EmergencyVehicle + destination is Hospital → EmergencyCorridor
    # EmergencyCorridor → Authorized for EmergencyRoute

    if vehicle_class == "EmergencyVehicle":
        allowed.append("SignalOverride")

        if destination in HOSPITALS:
            allowed.append("EmergencyCorridor")
            allowed.append("EmergencyRoute")

    # if priority == "Critical" and "EmergencyRoute" in allowed:
    #     allowed.append("SignalOverride")  # already there but confirms critical path

    return allowed

def validate_request(request, priority, allowed_actions):
    """
    Validates the request against traffic policy rules based on
    request category, priority level and allowed actions.
    Returns (approved: bool, reason: str).
    """
    category = request["request_category"]

    if category == "route_request":
        return True, "Route requests are always approved"

    elif category == "policy_check":
        if allowed_actions:
            return True, "Vehicle is authorized for requested action"
        else:
            return False, "Vehicle is not authorized for any action"

    elif category == "control_allocation_request":
        if "SignalOverride" in allowed_actions or "EmergencyRoute" in allowed_actions:
            return True, "Control action authorized"
        else:
            return False, "No control actions authorized for this vehicle"

    elif category == "emergency_response_request":
        if "EmergencyRoute" in allowed_actions:
            return True, "Emergency route authorized"
        else:
            return False, "Emergency route not authorized"

    elif category == "integrated_city_service_request":
        if priority == "Critical" and "EmergencyRoute" in allowed_actions:
            return True, "Critical priority with full emergency authorization"
        else:
            return False, "Integrated service requires critical priority and emergency route"

    else:
        return False, "Unknown request category"
    

def run_knowledge_base(request):
    """
    Master function for knowledge base module.
    Runs priority determination, authorization check,
    and request validation in sequence.
    Returns result dictionary.
    """
    priority        = determine_priority(request)
    allowed_actions = check_authorization(request, priority)
    approved, reason = validate_request(request, priority, allowed_actions)

    print(f"[Knowledge Base] Priority      : {priority}")
    print(f"[Knowledge Base] Allowed Actions: {allowed_actions}")
    print(f"[Knowledge Base] Status        : {'APPROVED' if approved else 'REJECTED'}")
    print(f"[Knowledge Base] Reason        : {reason}")

    return {
        "priority"       : priority,
        "allowed_actions": allowed_actions,
        "approved"       : approved,
        "reason"         : reason
    }