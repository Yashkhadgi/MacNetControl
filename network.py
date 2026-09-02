import subprocess


WIFI_INTERFACE = "en0"


def turn_wifi_on():
    subprocess.run(
        ["networksetup", "-setairportpower", WIFI_INTERFACE, "on"],
        check=True
    )


def turn_wifi_off():
    subprocess.run(
        ["networksetup", "-setairportpower", WIFI_INTERFACE, "off"],
        check=True
    )


def get_wifi_status():
    result = subprocess.run(
        ["networksetup", "-getairportpower", WIFI_INTERFACE],
        capture_output=True,
        text=True,
        check=True
    )

    return result.stdout.strip()


if __name__ == "__main__":
    print(get_wifi_status())