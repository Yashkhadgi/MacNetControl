import subprocess


PHONE_VENDOR_ID = "0x04e8"


def is_phone_connected():
    result = subprocess.run(
        ["system_profiler", "SPUSBHostDataType"],
        capture_output=True,
        text=True
    )

    return PHONE_VENDOR_ID in result.stdout


def is_charger_connected():
    result = subprocess.run(
        ["pmset", "-g", "batt"],
        capture_output=True,
        text=True
    )

    return "AC Power" in result.stdout


if __name__ == "__main__":

    print("📱 Phone:",
          "Connected" if is_phone_connected() else "Not Connected")

    print("🔌 Charger:",
          "Connected" if is_charger_connected() else "Disconnected")