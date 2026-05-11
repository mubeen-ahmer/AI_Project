VALID_VEHICLE_TYPES = ["ambulance", "fire_truck", "police", "car", "bus", "truck"]

EMERGENCY_VEHICLES = ["ambulance", "fire_truck", "police"]
CIVILIAN_VEHICLES  = ["car", "bus", "truck"]

HOSPITALS       = ["City_Hospital"]

VALID_CATEGORIES = [
    "route_request",
    "policy_check",
    "control_allocation_request",
    "emergency_response_request",
    "integrated_city_service_request"
]

VALID_SEVERITY = ["low", "medium", "high"]
VALID_ZONES = ["s1", "s2", "s3", "s4", "s5"]

UNWEIGHTED_CITY_GRAPH = {
    "Police_HQ": ["Traffic_Control_Center", "River_Bridge"],
    "Traffic_Control_Center": ["Police_HQ", "North_Station"],
    "River_Bridge": ["Police_HQ", "North_Station", "Stadium"],
    "North_Station": ["Traffic_Control_Center", "River_Bridge", "Central_Junction"],
    "Stadium": ["River_Bridge", "East_Market", "Airport_Road"],
    "Airport_Road": ["Stadium", "South_Residential"],
    "South_Residential": ["Airport_Road", "Central_Junction", "City_Hospital"],
    "City_Hospital": ["South_Residential", "East_Market"],
    "East_Market": ["City_Hospital", "Stadium", "Central_Junction"],
    "Central_Junction": ["East_Market", "North_Station", "South_Residential", "West_Terminal"],
    "West_Terminal": ["Central_Junction", "Fire_Station", "Industrial_Zone"],
    "Fire_Station": ["West_Terminal"],
    "Industrial_Zone": ["West_Terminal"]
}

WEIGHTED_CITY_GRAPH = {
    "Traffic_Control_Center": {"Police_HQ": 2, "North_Station": 2},
    "Police_HQ": {"Traffic_Control_Center": 2, "River_Bridge": 2},
    "North_Station": {"Traffic_Control_Center": 2, "River_Bridge": 4, "Central_Junction": 3},
    "River_Bridge": {"Police_HQ": 2, "North_Station": 4},
    "Airport_Road": {"Stadium": 5, "South_Residential": 2},
    "Stadium": {"Airport_Road": 5, "East_Market": 2},
    "South_Residential": {"Airport_Road": 2, "Central_Junction": 4, "City_Hospital": 8},
    "Central_Junction": {"North_Station": 3, "South_Residential": 4, "East_Market": 3, "West_Terminal": 4},
    "East_Market": {"Stadium": 2, "Central_Junction": 3, "City_Hospital": 3},
    "City_Hospital": {"East_Market": 3, "South_Residential": 8},
    "West_Terminal": {"Central_Junction": 4, "Fire_Station": 2, "Industrial_Zone": 4},
    "Fire_Station": {"West_Terminal": 2},
    "Industrial_Zone": {"West_Terminal": 4}
}

CSP_VARIABLES = ["S1","S2","S3","S4","S5"]

CSP_DOMAINS = {
    "S1" : ["PhaseA","PhaseB"],
    "S2" : ["PhaseA","PhaseB","PhaseC"],
    "S3" : ["PhaseB" , "PhaseC"],
    "S4" : ["PhaseA","PhaseC"],
    "S5" : ["PhaseB","PhaseC"]
}

CSP_CONSTRAINTS = [("S1", "S2"),("S1", "S3")]
CSP_COORDINATION = [("S2", "S4")]
EMERGENCY_PRIORITY = [("S4", "S5")]
PRECEDENCE_CORRIDOR = [("S1", "S5")]

INTERSECTION_LOCATIONS = {
    "S1": "Central_Junction",
    "S2": "North_Station",
    "S3": "East_Market",
    "S4": "River_Bridge",
    "S5": "City_Hospital"
}