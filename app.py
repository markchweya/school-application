# app.py
from kivy import require
require("2.3.0")

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFillRoundFlatButton, MDTextButton
from kivy.metrics import dp
from kivymd.uix.behaviors import HoverBehavior

KV = """
#:import dp kivy.metrics.dp

<GlassCard@MDCard>:
    md_bg_color: 1, 1, 1, .09
    radius: [20,]
    elevation: 3
    padding: dp(24)
    spacing: dp(16)

<HoverLink@MDTextButton+HoverBehavior>:
    theme_text_color: "Custom"
    text_color: .72, .78, 1, 1
    on_enter: self.text_color = (1, 1, 1, 1)
    on_leave: self.text_color = (.72, .78, 1, 1)

<PressablePill@MDFillRoundFlatButton>:
    md_bg_color: 1, 1, 1, 1
    text_color: 0.10, 0.12, 0.25, 1
    on_press: self.md_bg_color = (1.00, 0.80, 0.20, 1)
    on_release: self.md_bg_color = (1, 1, 1, 1)

MDScreen:
    md_bg_color: 0.05, 0.06, 0.12, 1

    ScreenManager:
        id: router
        # NOTE: don't set current here; children aren't added yet

        # ============ LOGIN ============
        MDScreen:
            name: "login"

            MDBoxLayout:
                orientation: "vertical"
                padding: dp(0), dp(40), dp(0), dp(28)
                spacing: dp(12)

                MDBoxLayout:
                    orientation: "vertical"
                    size_hint_y: None
                    height: self.minimum_height
                    spacing: dp(3)

                    MDLabel:
                        text: "USIU"
                        halign: "center"
                        font_style: "H4"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, .97
                        bold: True
                        size_hint_y: None
                        height: self.texture_size[1]

                    MDLabel:
                        text: "AFRICA"
                        halign: "center"
                        font_style: "Subtitle1"
                        theme_text_color: "Custom"
                        text_color: .58, .66, 1, 1
                        size_hint_y: None
                        height: self.texture_size[1]

                AnchorLayout:
                    anchor_x: "center"
                    anchor_y: "center"

                    GlassCard:
                        size_hint: None, None
                        width: min(root.width * .42, dp(500))
                        height: dp(380)

                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: dp(14)
                            padding: 0, dp(6), 0, 0

                            MDLabel:
                                text: "Login"
                                halign: "center"
                                font_style: "H5"
                                theme_text_color: "Custom"
                                text_color: 1,1,1,.97
                                bold: True
                                size_hint_y: None
                                height: self.texture_size[1] + dp(8)

                            MDTextField:
                                id: email
                                hint_text: "Email"
                                icon_right: "email-outline"
                                size_hint_y: None
                                height: dp(56)
                                text_color_normal: 1,1,1,1
                                text_color_focus: 1,1,1,1
                                line_color_normal: 1,1,1,.25
                                line_color_focus: .58, .66, 1, 1
                                font_size: "17sp"
                                on_text_validate: pwd.focus = True

                            MDTextField:
                                id: pwd
                                hint_text: "Password"
                                password: True
                                icon_right: "lock-outline"
                                size_hint_y: None
                                height: dp(56)
                                text_color_normal: 1,1,1,1
                                text_color_focus: 1,1,1,1
                                line_color_normal: 1,1,1,.25
                                line_color_focus: .58, .66, 1, 1
                                font_size: "17sp"
                                on_text_validate: app.sign_in(email.text, self.text, remember.active)

                            MDBoxLayout:
                                spacing: dp(8)
                                adaptive_height: True

                                MDBoxLayout:
                                    adaptive_height: True
                                    spacing: dp(8)
                                    size_hint_x: .7
                                    MDCheckbox:
                                        id: remember
                                        size_hint: None, None
                                        size: dp(22), dp(22)
                                        pos_hint: {"center_y": .5}
                                    MDLabel:
                                        text: "Remember Me"
                                        theme_text_color: "Custom"
                                        text_color: 1,1,1,.82
                                        halign: "left"
                                        valign: "middle"

                                HoverLink:
                                    text: "FORGOT PASSWORD"
                                    on_release: app.forgot_password()

                            PressablePill:
                                text: "LOG IN"
                                pos_hint: {"center_x": .5}
                                height: dp(46)
                                on_release: app.sign_in(email.text, pwd.text, remember.active)

                MDLabel:
                    text: "Education to take you places"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: 1,1,1,.7
                    size_hint_y: None
                    height: self.texture_size[1] + dp(8)

        # ============ ADMIN ============
        MDScreen:
            name: "admin"
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(24)
                spacing: dp(16)
                MDBoxLayout:
                    adaptive_height: True
                    MDLabel:
                        text: "Admin Dashboard"
                        font_style: "H5"
                        halign: "left"
                    MDLabel:
                        text: "USIU • Admin"
                        halign: "right"
                        theme_text_color: "Custom"
                        text_color: .75, .79, 1, 1
                MDGridLayout:
                    cols: 3
                    spacing: dp(12)
                    adaptive_height: True
                    size_hint_y: None
                    height: dp(120)
                    MDRaisedButton:
                        text: "Manage Lecturers"
                        icon: "account-tie"
                        on_release: toast("Open: Lecturers")
                    MDRaisedButton:
                        text: "Manage Courses"
                        icon: "book-multiple"
                        on_release: toast("Open: Courses")
                    MDRaisedButton:
                        text: "Manage Students"
                        icon: "account-group"
                        on_release: toast("Open: Students")
                Widget:
                MDRaisedButton:
                    text: "Log out"
                    icon: "logout"
                    pos_hint: {"center_x": .5}
                    on_release: app.go("login")

        # ============ LECTURER ============
        MDScreen:
            name: "lecturer"
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(24)
                spacing: dp(16)
                MDBoxLayout:
                    adaptive_height: True
                    MDLabel:
                        text: "Lecturer Home"
                        font_style: "H5"
                        halign: "left"
                    MDLabel:
                        text: "USIU • Lecturer"
                        halign: "right"
                        theme_text_color: "Custom"
                        text_color: .75, .79, 1, 1
                MDGridLayout:
                    cols: 3
                    spacing: dp(12)
                    adaptive_height: True
                    size_hint_y: None
                    height: dp(120)
                    MDRaisedButton:
                        text: "My Courses"
                        icon: "book-open-page-variant"
                        on_release: toast("Open: My Courses")
                    MDRaisedButton:
                        text: "Attendance"
                        icon: "clipboard-check"
                        on_release: toast("Open: Attendance")
                    MDRaisedButton:
                        text: "Upload Materials"
                        icon: "cloud-upload"
                        on_release: toast("Open: Materials")
                Widget:
                MDRaisedButton:
                    text: "Log out"
                    icon: "logout"
                    pos_hint: {"center_x": .5}
                    on_release: app.go("login")
"""

class AppUSIU(MDApp):
    dialog = None

    def build(self):
        if not Window.fullscreen:
            Window.size = (1040, 680)
        self.title = "USIU – Login"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        root = Builder.load_string(KV)
        # Set initial screen after children are created
        Clock.schedule_once(lambda *_: self.go("login"), 0)
        return root

    def go(self, dest: str):
        sm = self.root.ids.get("router")
        if sm and dest in [s.name for s in sm.screens]:
            sm.current = dest

    def sign_in(self, email: str, password: str, remember: bool):
        e, p = (email or "").strip(), (password or "").strip()
        if not e and not p:
            toast("Enter email and password"); return
        if not e:
            toast("Enter your email"); return
        if not p:
            toast("Enter your password"); return

        if e.lower() == "admin" and p == "1245":
            self.go("admin")
            toast("Welcome, Admin")
            return

        self.go("lecturer")
        toast(f"Welcome, {e}  • Remember: {'Yes' if remember else 'No'}")

    def forgot_password(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Forgot password",
                text="(Demo) Launch your password reset flow here.",
                buttons=[MDTextButton(text="Close", on_release=lambda *_: self.dialog.dismiss())],
            )
        self.dialog.open()


if __name__ == "__main__":
    AppUSIU().run()
