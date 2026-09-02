import subprocess


def get_running_apps():
    script = '''
    tell application "System Events"
        set appNames to name of every application process whose background only is false
        set appPids to unix id of every application process whose background only is false
    end tell

    set output to ""
    repeat with i from 1 to count of appNames
        set output to output & (item i of appNames) & "|" & (item i of appPids) & linefeed
    end repeat

    return output
    '''

    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("Error:", result.stderr)
        return []

    apps = []

    for line in result.stdout.strip().splitlines():
        if "|" in line:
            name, pid = line.rsplit("|", 1)

            apps.append({
                "name": name,
                "pid": int(pid)
            })

    return apps


if __name__ == "__main__":
    apps = get_running_apps()

    for app in apps:
        print(f'{app["name"]:<40} PID: {app["pid"]}')