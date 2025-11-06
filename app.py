# app.py
from kivy import require
require("2.3.0")

from kivy.core.window import Window
from kivy.lang import Builder
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

    # Arrange header -> middle (card) -> footer in a column
    MDBoxLayout:
        orientation: "vertical"
        padding: dp(0), dp(40), dp(0), dp(28)   # top/bottom padding creates breathing room
        spacing: dp(12)

        # ===== Header =====
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

        # ===== Middle (takes the remaining space) =====
        AnchorLayout:
            anchor_x: "center"
            anchor_y: "center"
            # this zone expands/shrinks so the card stays centered between header and footer

            GlassCard:
                size_hint: None, None
                width: min(root.width * .42, dp(500))
                height: dp(380)  # keep fixed for consistency; no more overlap thanks to layout
                canvas.before:
                    Color:
                        rgba: 1,1,1,.12
                    RoundedRectangle:
                        size: self.size
                        pos: self.pos
                        radius: self.radius

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

        # ===== Footer =====
        MDLabel:
            text: "Education to take you places"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 1,1,1,.7
            size_hint_y: None
            height: self.texture_size[1] + dp(8)
"""

class AppUSIU(MDApp):
    dialog = None

    def build(self):
        if not Window.fullscreen:
            Window.size = (1040, 680)
        self.title = "USIU – Login"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.accent_palette = "Amber"
        return Builder.load_string(KV)

    def sign_in(self, email: str, password: str, remember: bool):
        e, p = email.strip(), password.strip()
        if not e and not p:
            toast("Enter email and password"); return
        if not e:
            toast("Enter your email"); return
        if not p:
            toast("Enter your password"); return
        toast(f"Signing in…  Remember: {'Yes' if remember else 'No'}")

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
