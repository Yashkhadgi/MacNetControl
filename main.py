from network import (
    turn_wifi_on,
    turn_wifi_off,
    get_wifi_status
)


while True:

    print("\n============================")
    print("     NETWORK CONTROLLER")
    print("============================")
    print("1. Turn Wi-Fi ON")
    print("2. Turn Wi-Fi OFF")
    print("3. Check Status")
    print("4. Exit")

    choice = input("\nEnter choice: ")

    if choice == "1":
        turn_wifi_on()
        print("✅ Wi-Fi turned ON")

    elif choice == "2":
        turn_wifi_off()
        print("❌ Wi-Fi turned OFF")

    elif choice == "3":
        print(get_wifi_status())

    elif choice == "4":
        print("Exiting...")
        break

    else:
        print("Invalid choice")
        