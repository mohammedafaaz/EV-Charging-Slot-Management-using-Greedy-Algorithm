"""
EV CHARGING SLOT ALLOCATION USING GREEDY ALGORITHM
------------------------------------

Features:
✔ Greedy Slot Allocation
✔ Waiting Queue
✔ Duplicate Booking Prevention
✔ Vehicle Number Normalization
✔ Lowest Battery Priority
✔ Activity Logs
✔ Edge Case Handling
✔ Input Validation

Algorithm Used:
1. Greedy Algorithm

"""

import time


# ──────────────────────────────────────────────
#   CONSTANTS
# ──────────────────────────────────────────────
TOTAL_SLOTS = 5
MAX_QUEUE_SIZE = 10


# ──────────────────────────────────────────────
#   SLOT DATA
# ──────────────────────────────────────────────

# True = Free
# False = Occupied
slot_status = [True] * TOTAL_SLOTS

# Stores vehicle number
slot_owner = [None] * TOTAL_SLOTS

# Stores battery %
slot_battery = [None] * TOTAL_SLOTS

# Waiting queue (Greedy selection based on lowest battery)
waiting_queue = []

# Activity logs
activity_log = []


# ──────────────────────────────────────────────
#   PRINT DIVIDER
# ──────────────────────────────────────────────
def print_line():
    print("-" * 60)


# ──────────────────────────────────────────────
#   LOG EVENTS
# ──────────────────────────────────────────────
def log_event(message):

    current_time = time.strftime("%H:%M:%S")

    activity_log.append(
        f"[{current_time}] {message}"
    )


# ──────────────────────────────────────────────
#   NORMALIZE VEHICLE NUMBER
# ──────────────────────────────────────────────
def normalize_vehicle_number(vehicle_number):

    vehicle_number = vehicle_number.upper()
    vehicle_number = vehicle_number.replace(" ", "")

    return vehicle_number


# ──────────────────────────────────────────────
#   GREEDY SLOT SEARCH
#   Time Complexity : O(n)
# ──────────────────────────────────────────────
def find_first_free_slot():

    for i in range(TOTAL_SLOTS):

        if slot_status[i]:
            return i

    return -1


# ──────────────────────────────────────────────
#   FIND PRIORITY VEHICLE
#   Lowest battery gets highest priority
#
#   Time Complexity : O(k)
# ──────────────────────────────────────────────

# ──────────────────────────────────────────────
#   BOOK SLOT
# ──────────────────────────────────────────────
def book_slot(vehicle_number, battery_level):

    print_line()

    # Normalize vehicle number
    vehicle_number = normalize_vehicle_number(
        vehicle_number
    )

    # Battery validation
    if battery_level < 0 or battery_level > 100:

        print(" Invalid battery percentage.")
        print_line()
        return

    # Duplicate booking prevention
    if vehicle_number in slot_owner:

        print(
            f" Vehicle {vehicle_number} "
            f"already has a slot."
        )

        print_line()
        return

    # Duplicate queue prevention
    if any(
        vehicle["vehicle"] == vehicle_number
        for vehicle in waiting_queue
    ):

        print(
            f" Vehicle {vehicle_number} "
            f"already exists in waiting queue."
        )

        print_line()
        return

    # Queue full condition
    if len(waiting_queue) >= MAX_QUEUE_SIZE:

        print(" Waiting queue is full.")
        print_line()
        return

    # Greedy slot assignment
    chosen_slot = find_first_free_slot()

    # Slot available
    if chosen_slot != -1:

        slot_status[chosen_slot] = False

        slot_owner[chosen_slot] = vehicle_number

        slot_battery[chosen_slot] = battery_level

        print(
            f" Slot {chosen_slot + 1} "
            f"assigned to vehicle "
            f"{vehicle_number}"
        )

        print(
            f" Battery Level : "
            f"{battery_level}%"
        )

        log_event(
            f"Vehicle {vehicle_number} "
            f"assigned Slot {chosen_slot + 1}"
        )

    # No slots available
    else:

        waiting_queue.append({

            "vehicle": vehicle_number,
            "battery": battery_level

        })

        print(" All slots are occupied.")

        print(
            f" Vehicle {vehicle_number} "
            f"added to waiting queue."
        )

        print(f" Current Queue Size : {len(waiting_queue)}")

        log_event(
            f"Vehicle {vehicle_number} "
            f"added to waiting queue"
        )

    print_line()


# ──────────────────────────────────────────────
#   CANCEL SLOT
# ──────────────────────────────────────────────
def cancel_slot(vehicle_number):

    print_line()

    # Normalize vehicle number
    vehicle_number = normalize_vehicle_number(
        vehicle_number
    )

    # Vehicle not found
    if vehicle_number not in slot_owner:

        print(
            f" Vehicle {vehicle_number} "
            f"does not have any booking."
        )

        print_line()
        return

    # Find slot
    slot_index = slot_owner.index(vehicle_number)

    # Free slot
    slot_status[slot_index] = True

    slot_owner[slot_index] = None

    slot_battery[slot_index] = None

    print(
        f" Slot {slot_index + 1} "
        f"released successfully."
    )

    log_event(
        f"Vehicle {vehicle_number} "
        f"left Slot {slot_index + 1}"
    )

    # Assign priority vehicle
    assign_next_vehicle(slot_index)

    print_line()


# ──────────────────────────────────────────────
#   ASSIGN NEXT PRIORITY VEHICLE
# ──────────────────────────────────────────────
def assign_next_vehicle(slot_index):

    if not waiting_queue:

        print(" No vehicles waiting.")
        return

    # Greedy selection: choose the waiting vehicle with the lowest battery level
    min_index = min(range(len(waiting_queue)), key=lambda i: waiting_queue[i]['battery'])
    selected_vehicle = waiting_queue.pop(min_index)

    slot_status[slot_index] = False

    slot_owner[slot_index] = (
        selected_vehicle["vehicle"]
    )

    slot_battery[slot_index] = (
        selected_vehicle["battery"]
    )

    print(
        f" Vehicle "
        f"{selected_vehicle['vehicle']} "
        f"assigned Slot {slot_index + 1}"
    )

    print(
        f" Battery Level : "
        f"{selected_vehicle['battery']}%"
    )

    log_event(
        f"Vehicle "
        f"{selected_vehicle['vehicle']} "
        f"assigned Slot {slot_index + 1}"
    )


# ──────────────────────────────────────────────
#   SHOW STATUS
# ──────────────────────────────────────────────
def show_status():

    print_line()

    print(" EV CHARGING STATION STATUS")

    print_line()

    free_slots = 0

    for i in range(TOTAL_SLOTS):

        if slot_status[i]:

            print(
                f" Slot {i + 1} : [ FREE ]"
            )

            free_slots += 1

        else:

            print(
                f" Slot {i + 1} : [ BUSY ] "
                f"Vehicle: {slot_owner[i]} "
                f"| Battery: {slot_battery[i]}%"
            )

    print_line()

    print(
        f" Total Slots : {TOTAL_SLOTS}"
    )

    print(
        f" Free Slots  : {free_slots}"
    )

    print(
        f" Busy Slots  : "
        f"{TOTAL_SLOTS - free_slots}"
    )

    print_line()

    # Waiting queue display
    if waiting_queue:

        print(" WAITING QUEUE")
        print()

        print(f"{'Vehicle':<18}{'Battery'}")
        print("-" * 28)

        for vehicle in sorted(waiting_queue, key=lambda x: x["battery"]):
            print(f"{vehicle['vehicle']:<18}{vehicle['battery']}%")

    else:

        print(" Waiting Queue Empty")

    print_line()


# ──────────────────────────────────────────────
#   SHOW LOG
# ──────────────────────────────────────────────
def show_log():

    print_line()

    print(" ACTIVITY LOG")

    print_line()

    if not activity_log:

        print(" No activity recorded.")

    else:

        for entry in activity_log:
            print(entry)

    print_line()


# ──────────────────────────────────────────────
#   COMPLEXITY ANALYSIS
# ──────────────────────────────────────────────
def show_complexity():

    print_line()

    print(" COMPLEXITY ANALYSIS")

    print_line()

    print(" Greedy Slot Search        : O(n)")
    print(" Slot Booking              : O(n)")

    print()

    print(" n = total charging slots")
    print(" k = vehicles in queue")

    print()

    print(" Why Greedy Works?")
    print("Whenever a charging slot becomes available,")
    print("the waiting vehicle with the")
    print("lowest battery percentage is selected.")
    print()
    print("If two vehicles have the same battery,")
    print("the one that entered the queue first is selected.")

    print_line()


# ──────────────────────────────────────────────
#   MAIN MENU
# ──────────────────────────────────────────────
def main():

    print("\n" + "=" * 60)

    print(" EV CHARGING SLOT ALLOCATION USING GREEDY ALGORITHM")

    print(" ADA PROJECT — 2026")

    print("=" * 60)

    while True:

        print("\n MENU")

        print(" 1. Book Charging Slot")
        print(" 2. Cancel Charging Slot")
        print(" 3. View Slot Status")
        print(" 4. View Activity Log")
        print(" 5. Complexity Analysis")
        print(" 6. Exit")

        choice = input(
            "\n Enter choice (1-6): "
        ).strip()

        # Empty menu input
        if choice == "":

            print(" Please enter a valid choice.")
            continue

        # BOOK SLOT
        if choice == "1":

            vehicle = input(
                " Enter Vehicle Number: "
            ).strip()

            vehicle = normalize_vehicle_number(
                vehicle
            )

            try:

                battery = int(

                    input(
                        " Enter Battery Percentage: "
                    )

                )

            except:

                print(" Invalid battery percentage.")
                continue

            book_slot(vehicle, battery)

        # CANCEL SLOT
        elif choice == "2":

            vehicle = input(
                " Enter Vehicle Number: "
            ).strip()

            vehicle = normalize_vehicle_number(
                vehicle
            )

            cancel_slot(vehicle)

        # STATUS
        elif choice == "3":

            show_status()

        # LOG
        elif choice == "4":

            show_log()

        # COMPLEXITY
        elif choice == "5":

            show_complexity()

        # EXIT
        elif choice == "6":

            print("\n Session Ended Successfully.")

            show_log()

            break

        else:

            print(
                " Invalid choice. "
                "Please enter between 1 and 6."
            )


# ──────────────────────────────────────────────
#   PROGRAM START
# ──────────────────────────────────────────────
if __name__ == "__main__":

    main()