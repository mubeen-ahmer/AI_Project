from modules.preprocessing  import preprocess
from modules.router          import route_request
from modules.ann             import run_ann
from modules.knowledge_base  import run_knowledge_base
from modules.csp             import run_csp
from modules.search          import find_route
from modules.response        import build_response, print_response



def get_input(prompt, valid_options=None, input_type=None):
    """
    Repeatedly prompts user until a valid input is received.
    Supports option validation, float, and bool input types.
    """
    while True:
        try:
            value = input(f"  {prompt}").strip()

            if input_type == "float":
                value = float(value)
                if not (0.0 <= value <= 1.0):
                    print("  Must be between 0.0 and 1.0")
                    continue
                return value

            if valid_options:
                if value.lower() in [v.lower() for v in valid_options]:
                    return value.lower()
                print(f"  Invalid. Choose from: {', '.join(valid_options)}")
                continue

            if value == "":
                print("  Cannot be empty.")
                continue

            return value

        except ValueError:
            print("  Invalid input. Try again.")



def show_locations():
    """Prints all valid city locations for user reference."""
    print()
    print("  Available Locations:")
    print("  Police_HQ            Traffic_Control_Center")
    print("  North_Station        River_Bridge")
    print("  Stadium              Airport_Road")
    print("  South_Residential    City_Hospital")
    print("  East_Market          Central_Junction")
    print("  West_Terminal        Fire_Station")
    print("  Industrial_Zone")
    print()


def collect_route_request():
    """
    Collects only the fields needed for a basic route request.
    Only requires start and destination — no other fields needed
    since pipeline is Search only.
    """
    print("\n  [Route Request — finds shortest path between two locations]")
    show_locations()

    req_id = get_input("Request ID          : ")
    start  = get_input("Current Location    : ")
    dest   = get_input("Destination         : ")

    return {
        "request_id"       : req_id,
        "request_category" : "route_request",
        "vehicle_type"     : "car",
        "vehicle_class"    : "CivilianVehicle",
        "current_location" : start,
        "destination"      : dest,
        "incident_severity": "low",
        "time_sensitivity" : False,
        "traffic_density"  : 0.0,
        "priority_claim"   : False,
        "control_zone"     : "s1",
        "description_note" : "route only"
    }


def collect_policy_check():
    """
    Collects fields needed for policy validation.
    Requires vehicle type, destination and control zone since
    KB checks authorization based on these three fields.
    """
    print("\n  [Policy Check — validates if vehicle is authorized for an action]")
    show_locations()

    req_id  = get_input("Request ID          : ")
    vehicle = get_input(
        "Vehicle Type        : (ambulance/fire_truck/police/car/bus/truck): ",
        ["ambulance", "fire_truck", "police", "car", "bus", "truck"]
    )
    start   = get_input("Current Location    : ")
    dest    = get_input("Destination         : ")
    zone    = get_input(
        "Control Zone        : (s1/s2/s3/s4/s5): ",
        ["s1", "s2", "s3", "s4", "s5"]
    )

    return {
        "request_id"       : req_id,
        "request_category" : "policy_check",
        "vehicle_type"     : vehicle,
        "current_location" : start,
        "destination"      : dest,
        "incident_severity": "low",
        "time_sensitivity" : False,
        "traffic_density"  : 0.0,
        "priority_claim"   : False,
        "control_zone"     : zone,
        "description_note" : "policy check"
    }


def collect_control_allocation():
    """
    Collects fields needed for signal control allocation.
    Requires vehicle type, severity and time sensitivity since
    KB uses these for authorization before CSP runs.
    """
    print("\n  [Control Allocation — assigns signal phases to intersections]")
    show_locations()

    req_id   = get_input("Request ID          : ")
    vehicle  = get_input(
        "Vehicle Type        : (ambulance/fire_truck/police/car/bus/truck): ",
        ["ambulance", "fire_truck", "police", "car", "bus", "truck"]
    )
    start    = get_input("Current Location    : ")
    dest     = get_input("Destination         : ")
    severity = get_input(
        "Incident Severity   : (low/medium/high): ",
        ["low", "medium", "high"]
    )
    time_s   = get_input(
        "Time Sensitive      : (true/false): ",
        ["true", "false"]
    )
    zone     = get_input(
        "Control Zone        : (s1/s2/s3/s4/s5): ",
        ["s1", "s2", "s3", "s4", "s5"]
    )

    return {
        "request_id"       : req_id,
        "request_category" : "control_allocation_request",
        "vehicle_type"     : vehicle,
        "current_location" : start,
        "destination"      : dest,
        "incident_severity": severity,
        "time_sensitivity" : True if time_s == "true" else False,
        "traffic_density"  : 0.0,
        "priority_claim"   : False,
        "control_zone"     : zone,
        "description_note" : "control allocation"
    }


def collect_emergency_request(category):
    """
    Collects all fields needed for emergency or integrated request.
    All fields required since full pipeline runs:
    ANN needs density and priority_claim,
    KB needs severity and time_sensitivity,
    CSP needs control_zone,
    Search needs start and destination.
    """
    label = "Emergency Response" if category == "emergency_response_request" else "Integrated City Service"
    print(f"\n  [{label} — runs full AI pipeline: ANN → KB → CSP → Search]")
    show_locations()

    req_id   = get_input("Request ID          : ")
    vehicle  = get_input(
        "Vehicle Type        : (ambulance/fire_truck/police/car/bus/truck): ",
        ["ambulance", "fire_truck", "police", "car", "bus", "truck"]
    )
    start    = get_input("Current Location    : ")
    dest     = get_input("Destination         : ")
    severity = get_input(
        "Incident Severity   : (low/medium/high): ",
        ["low", "medium", "high"]
    )
    time_s   = get_input(
        "Time Sensitive      : (true/false): ",
        ["true", "false"]
    )
    density  = get_input(
        "Traffic Density     : (0.0 to 1.0): ",
        input_type="float"
    )
    claim    = get_input(
        "Priority Claim      : (true/false): ",
        ["true", "false"]
    )
    zone     = get_input(
        "Control Zone        : (s1/s2/s3/s4/s5): ",
        ["s1", "s2", "s3", "s4", "s5"]
    )
    desc     = get_input("Description         : ")

    return {
        "request_id"       : req_id,
        "request_category" : category,
        "vehicle_type"     : vehicle,
        "current_location" : start,
        "destination"      : dest,
        "incident_severity": severity,
        "time_sensitivity" : True if time_s == "true" else False,
        "traffic_density"  : density,
        "priority_claim"   : True if claim == "true" else False,
        "control_zone"     : zone,
        "description_note" : desc
    }



def process_request(request):
    """
    Runs the full pipeline for a given request.
    Calls only the modules selected by the router.
    Stops early if knowledge base rejects the request.
    """
    try:
        request = preprocess(request)

        pipeline = route_request(request)

        ann_result   = None
        kb_result    = None
        csp_result   = None
        route_result = None

        if "ann" in pipeline:
            ann_result = run_ann(request)

        if "knowledge_base" in pipeline:
            kb_result = run_knowledge_base(request)
            if not kb_result["approved"]:
                response = build_response(
                    request, pipeline, ann_result, kb_result
                )
                print_response(response)
                return

        if "csp" in pipeline and kb_result:
            csp_result = run_csp(
                request,
                kb_result["allowed_actions"],
                kb_result["priority"]
            )

        if "search" in pipeline:
            algorithm = "bfs" if request["request_category"] == "route_request" else "astar"
            route_result = find_route(
                request["current_location"],
                request["destination"],
                algorithm
            )

        response = build_response(
            request, pipeline,
            ann_result, kb_result,
            csp_result, route_result
        )
        print_response(response)

    except ValueError as e:
        print(f"\n  Error: {e}\n")


def show_menu():
    """
    Displays the main menu with descriptions of each option.
    Returns the user's choice as a string.
    """
    print("\n" + "="*55)
    print("   Smart City Traffic & Emergency Response System")
    print("="*55)
    print("  1. Route Request          → Search only (BFS)")
    print("  2. Policy Check           → Knowledge Base only")
    print("  3. Control Allocation     → KB + CSP")
    print("  4. Emergency Response     → ANN + KB + CSP + Search")
    print("  5. Integrated Service     → ANN + KB + CSP + Search")
    print("  6. Exit")
    print("="*55)
    return input("  Choice (1-6): ").strip()



if __name__ == "__main__":
    print("\n  Welcome to Smart City Traffic AI System")

    while True:
        choice = show_menu()

        if choice == "1":
            request = collect_route_request()
            process_request(request)

        elif choice == "2":
            request = collect_policy_check()
            process_request(request)

        elif choice == "3":
            request = collect_control_allocation()
            process_request(request)

        elif choice == "4":
            request = collect_emergency_request("emergency_response_request")
            process_request(request)

        elif choice == "5":
            request = collect_emergency_request("integrated_city_service_request")
            process_request(request)

        elif choice == "6":
            print("\n  Goodbye!\n")
            break

        else:
            print("  Invalid choice. Enter 1-6.")