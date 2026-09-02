import tkinter as tk
from tkinter import messagebox

from network import (
    turn_wifi_on,
    turn_wifi_off,
    get_wifi_status
)

from apps import get_running_apps

from device import (
    is_phone_connected,
    is_charger_connected
)

from app_rules import (
    set_app_blocked,
    is_app_blocked
)


class NetworkController:

    def __init__(self, root):

        self.root = root

        self.root.title("Network Controller")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)

        self.setup_ui()

        self.update_dashboard()

    # --------------------------------------------------
    # MAIN UI
    # --------------------------------------------------

    def setup_ui(self):

        # Background
        self.root.configure(bg="#f5f5f7")

        # ================= HEADER =================

        header = tk.Frame(
            self.root,
            bg="#f5f5f7"
        )
        header.pack(
            fill="x",
            padx=30,
            pady=(25, 15)
        )

        tk.Label(
            header,
            text="Network Controller",
            font=("Arial", 26, "bold"),
            bg="#f5f5f7",
            fg="#111111"
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Control your network and connected devices",
            font=("Arial", 11),
            bg="#f5f5f7",
            fg="#666666"
        ).pack(anchor="w", pady=(5, 0))

        # ================= STATUS CARDS =================

        cards = tk.Frame(
            self.root,
            bg="#f5f5f7"
        )
        cards.pack(
            fill="x",
            padx=30,
            pady=10
        )

        self.wifi_card = self.create_status_card(
            cards,
            "Wi-Fi",
            "Checking..."
        )

        self.phone_card = self.create_status_card(
            cards,
            "Phone",
            "Checking..."
        )

        self.charger_card = self.create_status_card(
            cards,
            "Charger",
            "Checking..."
        )

        self.wifi_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 8)
        )

        self.phone_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=8
        )

        self.charger_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(8, 0)
        )

        # ================= WIFI CONTROL =================

        wifi_control = tk.Frame(
            self.root,
            bg="white",
            bd=1,
            relief="solid"
        )

        wifi_control.pack(
            fill="x",
            padx=30,
            pady=15
        )

        left = tk.Frame(
            wifi_control,
            bg="white"
        )

        left.pack(
            side="left",
            padx=20,
            pady=15
        )

        tk.Label(
            left,
            text="Internet Connection",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#111111"
        ).pack(anchor="w")

        tk.Label(
            left,
            text="Control system-wide Wi-Fi connectivity",
            font=("Arial", 10),
            bg="white",
            fg="#777777"
        ).pack(anchor="w", pady=(3, 0))

        self.wifi_button = tk.Button(
            wifi_control,
            text="",
            font=("Arial", 11, "bold"),
            width=16,
            height=2,
            command=self.toggle_wifi
        )

        self.wifi_button.pack(
            side="right",
            padx=20,
            pady=15
        )

        # ================= APPS SECTION =================

        apps_container = tk.Frame(
            self.root,
            bg="white",
            bd=1,
            relief="solid"
        )

        apps_container.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 20)
        )

        # Apps header
        apps_header = tk.Frame(
            apps_container,
            bg="white"
        )

        apps_header.pack(
            fill="x",
            padx=20,
            pady=15
        )

        tk.Label(
            apps_header,
            text="Application Network Control",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#111111"
        ).pack(side="left")

        self.refresh_button = tk.Button(
            apps_header,
            text="↻ Refresh",
            font=("Arial", 10),
            command=self.update_dashboard
        )

        self.refresh_button.pack(side="right")

        # Column headers
        columns = tk.Frame(
            apps_container,
            bg="#eeeeee"
        )

        columns.pack(
            fill="x",
            padx=15
        )

        tk.Label(
            columns,
            text="APPLICATION",
            font=("Arial", 10, "bold"),
            bg="#eeeeee",
            fg="#555555",
            anchor="w"
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=10,
            pady=8
        )

        tk.Label(
            columns,
            text="PID",
            font=("Arial", 10, "bold"),
            bg="#eeeeee",
            fg="#555555",
            width=15
        ).pack(side="left")

        tk.Label(
            columns,
            text="NETWORK",
            font=("Arial", 10, "bold"),
            bg="#eeeeee",
            fg="#555555",
            width=15
        ).pack(side="left")

        # Scrollable application area
        self.canvas = tk.Canvas(
            apps_container,
            bg="white",
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            apps_container,
            orient="vertical",
            command=self.canvas.yview
        )

        self.apps_frame = tk.Frame(
            self.canvas,
            bg="white"
        )

        self.apps_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window(
            (0, 0),
            window=self.apps_frame,
            anchor="nw"
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(15, 0),
            pady=10
        )

    # --------------------------------------------------
    # STATUS CARD
    # --------------------------------------------------

    def create_status_card(self, parent, title, status):

        card = tk.Frame(
            parent,
            bg="white",
            bd=1,
            relief="solid"
        )

        tk.Label(
            card,
            text=title,
            font=("Arial", 11),
            bg="white",
            fg="#777777"
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 3)
        )

        label = tk.Label(
            card,
            text=status,
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#111111"
        )

        label.pack(
            anchor="w",
            padx=15,
            pady=(0, 12)
        )

        card.status_label = label

        return card

    # --------------------------------------------------
    # DASHBOARD UPDATE
    # --------------------------------------------------

    def update_dashboard(self):

        self.update_wifi()

        self.update_devices()

        self.update_apps()

    # --------------------------------------------------
    # WIFI
    # --------------------------------------------------

    def update_wifi(self):

        try:

            status = get_wifi_status()

            if "On" in status:

                self.wifi_card.status_label.config(
                    text="● ON",
                    fg="#16803c"
                )

                self.wifi_button.config(
                    text="Turn Wi-Fi OFF"
                )

            else:

                self.wifi_card.status_label.config(
                    text="● OFF",
                    fg="#d93025"
                )

                self.wifi_button.config(
                    text="Turn Wi-Fi ON"
                )

        except Exception as e:

            print("Wi-Fi error:", e)

    def toggle_wifi(self):

        try:

            status = get_wifi_status()

            if "On" in status:

                turn_wifi_off()

            else:

                turn_wifi_on()

            self.update_wifi()

        except Exception as e:

            messagebox.showerror(
                "Wi-Fi Error",
                str(e)
            )

    # --------------------------------------------------
    # DEVICES
    # --------------------------------------------------

    def update_devices(self):

        try:

            phone = is_phone_connected()

            charger = is_charger_connected()

            if phone:

                self.phone_card.status_label.config(
                    text="● Connected",
                    fg="#16803c"
                )

            else:

                self.phone_card.status_label.config(
                    text="● Disconnected",
                    fg="#777777"
                )

            if charger:

                self.charger_card.status_label.config(
                    text="● Connected",
                    fg="#16803c"
                )

            else:

                self.charger_card.status_label.config(
                    text="● Disconnected",
                    fg="#777777"
                )

        except Exception as e:

            print("Device error:", e)

    # --------------------------------------------------
    # APPLICATIONS
    # --------------------------------------------------

    def update_apps(self):

        for widget in self.apps_frame.winfo_children():

            widget.destroy()

        try:

            running_apps = get_running_apps()

        except Exception as e:

            print("Application error:", e)
            return

        for app in running_apps:

            name = app["name"]
            pid = app["pid"]

            blocked = is_app_blocked(name)

            row = tk.Frame(
                self.apps_frame,
                bg="white"
            )

            row.pack(
                fill="x",
                pady=3
            )

            # Application name
            tk.Label(
                row,
                text=name,
                font=("Arial", 11),
                bg="white",
                fg="#222222",
                anchor="w"
            ).pack(
                side="left",
                fill="x",
                expand=True,
                padx=10,
                pady=8
            )

            # PID
            tk.Label(
                row,
                text=str(pid),
                font=("Arial", 10),
                bg="white",
                fg="#777777",
                width=15
            ).pack(side="left")

            # Status button
            button = tk.Button(
                row,
                text="BLOCKED" if blocked else "ALLOWED",
                font=("Arial", 9, "bold"),
                width=12,
                command=lambda n=name: self.toggle_app(n)
            )

            button.pack(
                side="left",
                padx=10
            )

    # --------------------------------------------------
    # APP RULE
    # --------------------------------------------------

    def toggle_app(self, app_name):

        current = is_app_blocked(app_name)

        set_app_blocked(
            app_name,
            not current
        )

        self.update_apps()


# --------------------------------------------------
# START APPLICATION
# --------------------------------------------------

root = tk.Tk()

app = NetworkController(root)

root.mainloop()