# Sample requests for testing — you'll build a menu later in Phase 8
from modules.preprocessing import check_required_fields
emergency_request = {
    "request_id"       : "REQ-001",
    "vehicle_type"     : "ambulance",
    "request_category" : "Emergency_Response_Request",
    "current_location" : "Central_Junction",
    "destination"      : "City_Hospital",
    "incident_severity": "High",
    "time_sensitivity" : True,
    "traffic_density"  : 0.85,
    "priority_claim"   : True,
    "control_zone"     : "S1",
    "description_note" : "Cardiac emergency"
}

route_request = {
    "request_id"       : "REQ-002",
    "vehicle_type"     : "car",
    "request_category" : "Route_Request",
    "current_location" : "Stadium",
    "destination"      : "Fire_Station",
    "incident_severity": "Low",
    "time_sensitivity" : False,
    "traffic_density"  : 0.3,
    "priority_claim"   : False,
    "control_zone"     : "S2",
    "description_note" : "Normal commute"
}

check_required_fields(route_request)
