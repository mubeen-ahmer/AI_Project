from modules.preprocessing  import preprocess
from modules.router          import route_request
from modules.ann             import run_ann
from modules.knowledge_base  import run_knowledge_base
from modules.csp             import run_csp
from modules.search          import find_route
from modules.response        import build_response, print_response


def get_input(prompt, valid_options=None):
    """
    Helper function to get input from user.
    Keeps asking until a valid option is entered.
    """
    while True:
        value = input(prompt).strip()
        if valid_options:
            if value.lower() in [v.lower() for v in valid_options]:
                return value.lower()
            else:
                print(f"  Invalid option. Choose from: {valid_options}")
        else:
            if value:
                return value
            print("  Input cannot be empty.")


def collect_request():
    """
    Collects request details from user input.
    Returns a structured request dictionary.
    """
    print("\n--- Enter Request Details ---")

    request_id = get_input("  Request ID       : ")

    vehicle_type = get_input(
        "  Vehicle Type     : (ambulance/fire_truck/police/car/bus/truck): ",
        ["ambulance", "fire_truck", "police", "car", "bus", "truck"]
    )

    category = get_input(
        "  Request Category : (route_request / policy_check / control_allocation_request / emergency_response_request / integrated_city_service_request): ",
        ["route_request", "policy_check", "control_allocation_request",
         "emergency_response_request", "integrated_city_service_request"]
    )

    print("  Locations: Police_HQ, Traffic_Control_Center, North_Station, River_Bridge,")
    print("             Stadium, Airport_Road, South_Residential, City_Hospital,")
    print("             East_Market, Central_Junction, West_Terminal, Fire_Station, Industrial_Zone")

    current_location = get_input("  Current Location : ")
    destination      = get_input("  Destination      : ")

    severity = get_input(
        "  Incident Severity: (low/medium/high): ",
        ["low", "medium", "high"]
    )

    time_sensitivity = get_input(
        "  Time Sensitive   : (true/false): ",
        ["true", "false"]
    )
    time_sensitivity = True if time_sensitivity == "true" else False

    traffic_density = float(get_input("  Traffic Density  : (0.0 to 1.0): "))

    priority_claim = get_input(
        "  Priority Claim   : (true/false): ",
        ["true", "false"]
    )
    priority_claim = True if priority_claim == "true" else False

    control_zone = get_input(
        "  Control Zone     : (s1/s2/s3/s4/s5): ",
        ["s1", "s2", "s3", "s4", "s5"]
    )

    description = get_input("  Description      : ")

    return {
        "request_id"       : request_id,
        "vehicle_type"     : vehicle_type,
        "request_category" : category,
        "current_location" : current_location,
        "destination"      : destination,
        "incident_severity": severity,
        "time_sensitivity" : time_sensitivity,
        "traffic_density"  : traffic_density,
        "priority_claim"   : priority_claim,
        "control_zone"     : control_zone,
        "description_note" : description
    }


def process_request(request):
    """
    Runs the full pipeline for a given request.
    Calls modules in order based on router decision.
    Builds and prints the final response.
    """
    try:
        # Step 1 — Preprocess
        request = preprocess(request)

        # Step 2 — Route
        pipeline = route_request(request)

        # Step 3 — Run modules based on pipeline
        ann_result   = None
        kb_result    = None
        csp_result   = None
        route_result = None

        if "ann" in pipeline:
            ann_result = run_ann(request)

        if "knowledge_base" in pipeline:
            kb_result = run_knowledge_base(request)

            # stop if rejected
            if not kb_result["approved"]:
                response = build_response(request, pipeline, ann_result, kb_result)
                print_response(response)
                return

        if "csp" in pipeline and kb_result:
            csp_result = run_csp(request, kb_result["allowed_actions"], kb_result["priority"])

        if "search" in pipeline:
            # pick algorithm based on category
            if request["request_category"] == "route_request":
                algorithm = "bfs"
            else:
                algorithm = "astar"

            route_result = find_route(
                request["current_location"],
                request["destination"],
                algorithm
            )

        # Step 4 — Build and print response
        response = build_response(request, pipeline, ann_result, kb_result, csp_result, route_result)
        print_response(response)

    except ValueError as e:
        print(f"\n  ❌ Error: {e}\n")


def show_menu():
    """
    Displays the main menu and returns user choice.
    """
    print("\n" + "="*50)
    print("   Smart City Traffic & Emergency Response")
    print("="*50)
    print("  1. Submit Route Request")
    print("  2. Submit Policy Check")
    print("  3. Submit Control Allocation Request")
    print("  4. Submit Emergency Response Request")
    print("  5. Submit Integrated City Service Request")
    print("  6. Exit")
    print("="*50)
    return input("  Enter choice (1-6): ").strip()


# ── Main Loop ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("\nWelcome to Smart City Traffic AI System")

    while True:
        choice = show_menu()

        if choice == "6":
            print("\nGoodbye!\n")
            break

        elif choice in ["1", "2", "3", "4", "5"]:
            request = collect_request()
            process_request(request)

        else:
            print("  Invalid choice. Enter 1-6.")