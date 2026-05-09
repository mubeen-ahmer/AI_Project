from data.city_graph import (
    VALID_VEHICLE_TYPES,
    VALID_CATEGORIES,
    VALID_SEVERITY,
    VALID_ZONES,
    EMERGENCY_VEHICLES,
    CIVILIAN_VEHICLES,
)
REQUIRED_FIELDS = [
    "request_id",
    "vehicle_type",
    "request_category",
    "current_location",
    "destination",
    "incident_severity",
    "time_sensitivity",
    "traffic_density",
    "priority_claim",
    "control_zone",
    "description_note",
]

def check_required_fields(request):
    """checks all feilds are present"""

    for val in REQUIRED_FIELDS:
        if val not in request:
            raise ValueError("missing required field",val)
        
def validate_fields(request):
    """make sure all fields are valid """

    if request["vehicle_type"] not in VALID_VEHICLE_TYPES:
        raise ValueError(f"Vehicle type {request["vehicle_type"]} is invalid")
    
    if request["request_category"] not in VALID_CATEGORIES:
        raise ValueError(f"request category {request["request_category"]} is invalid")
    
    if request["incident_severity"] not in VALID_SEVERITY:
        raise ValueError(f"incident severity {request["incident_severity"]} is invalid")
    
    if request["control_zone"] not in VALID_ZONES:
        raise ValueError(f"control zone type {request["control_zone"]} is invalid")
    
    if request["traffic_density"] < 0.0 or request["traffic_density"] > 1.0 :
        raise ValueError("Traffic density must be in between 0.0 to 1.0 ") 
    
    if request["time_sensitivity"] != True and  request["time_sensitivity"] != False:
        raise ValueError("time sensivity must be a bool value(True/False)") 
    
    if request["priority_claim"] != True and  request["priority_claim"] != False:
        raise ValueError("priority claim must be a bool value(True/False)") 
    
    if not request["current_location"]:
        raise ValueError("current location must be non empty")
    
    if not request["destination"]:
        raise ValueError("destination must be non empty")
    
def normalize_request(request):
    """
    Normalizes string fields and maps vehicle_type to
    EmergencyVehicle or CivilianVehicle class.
    Returns the updated request dictionary.
    """
    string_fields = ["current_location", "destination","description_note", "vehicle_type", "request_category","incident_severity", "control_zone"]

    for val in string_fields:
        request[val] = request[val].strip()

    request["vehicle_type"]      = request["vehicle_type"].lower()
    request["request_category"]  = request["request_category"].lower()
    request["incident_severity"] = request["incident_severity"].lower()
    request["control_zone"]      = request["control_zone"].lower()

    if request["vehicle_type"] in EMERGENCY_VEHICLES:
        request["vehicle_class"]="EmergencyVehicle"
    else:
        request["vehicle_class"]="CivilianVehicle"
    return request
  
def build_feature_vector(request):
    """
    Converts request fields into a numeric feature vector for ANN input.
    Returns a list of numbers.
    """
    mylist = []
    if request["vehicle_class"] == "EmergencyVehicle":
        mylist.append(1)
    else:
        mylist.append(0)
    
    if request["incident_severity"] == "low" :
        mylist.append(0)
    elif request["incident_severity"] == "medium" :
        mylist.append(1)
    else:
        mylist.append(2)
    
    if request["time_sensitivity"] :
        mylist.append(1)
    else:
        mylist.append(0)
    
    mylist.append(request["traffic_density"])

    if request["priority_claim"]:
        mylist.append(1)
    else:
        mylist.append(0)
    
    mylist.append(1.0) #hardcore for distance for now will update later in search

    return mylist
    # vehicle_class  → EmergencyVehicle=1, CivilianVehicle=0
    # incident_severity → Low=0, Medium=1, High=2
    # time_sensitivity → True=1, False=0
    # traffic_density → already a float, use as-is
    # priority_claim → True=1, False=0
    # distance → hardcode 1.0 for now (we'll update after Search module is done)

def preprocess(request):
    """
    Master preprocessing function. Validates, normalizes, and prepares
    the request. Returns cleaned request with feature vector attached.
    """
    check_required_fields(request)
    validate_fields(request)
    request = normalize_request(request)
    request["feature_vector"] = build_feature_vector(request)
    print(f"[Preprocessing] Request {request['request_id']} passed validation.")
    return request