# # Sample requests for testing — you'll build a menu later in Phase 8
# # from modules.preprocessing import validate_fields
from modules.preprocessing import preprocess
emergency_request = {
    "request_id"       : "REQ-001",
    "vehicle_type"     : "ambulance",
    "request_category" : "emergency_response_request",
    "current_location" : "Central_Junction",
    "destination"      : "City_Hospital",
    "incident_severity": "high",
    "time_sensitivity" : True,
    "traffic_density"  : 0.85,
    "priority_claim"   : True,
    "control_zone"     : "S1",
    "description_note" : "Cardiac emergency"
}

# route_request = {
#     "request_id"       : "REQ-002",
#     "vehicle_type"     : "car",
#     "request_category" : "Route_Request",
#     "current_location" : "Stadium",
#     "destination"      : "Fire_Station",
#     "incident_severity": "Low",
#     "time_sensitivity" : False,
#     "traffic_density"  : 0.3,
#     "priority_claim"   : False,
#     "control_zone"     : "S2",
#     "description_note" : "Normal commute"
# }


# try:
cleaned = preprocess(emergency_request)
#     print("Cleaned request:", cleaned)
#     print("Feature vector:", cleaned["feature_vector"])
# except ValueError as e:
#     print("Validation error:", e)

from modules.router import route_request

pipeline = route_request(cleaned)
print("Pipeline:", pipeline)