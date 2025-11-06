# app.py
from kivy import require
require("2.3.0")

from datetime import datetime
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ColorProperty, ListProperty, NumericProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.factory import Factory

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivymd.uix.card import MDCard
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.list import (
    MDListItem,
    MDListItemHeadlineText,
    MDListItemTrailingIcon,
    MDListItemLeadingIcon,
)
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.menu import MDDropdownMenu


# ----------------------------
# Custom 3D Circular Progress
# ----------------------------
class UICircleProgress(Widget):
    progress = NumericProperty(0.0)
    ring_color = ColorProperty([0.54, 0.64, 1.0, 1.0])
    bg_color = ColorProperty([1, 1, 1, 0.10])
    thickness = NumericProperty(dp(16))  # thicker for visibility

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self._redraw, size=self._redraw, progress=self._redraw)

    def _redraw(self, *_):
        self.canvas.clear()
        from kivy.graphics import Color, Ellipse, Line

        with self.canvas:
            # soft drop shadow
            Color(0, 0, 0, 0.25)
            Ellipse(pos=(self.x + dp(3), self.y - dp(3)), size=(self.width, self.height))
            # outer plate
            Color(1, 1, 1, 0.10)
            Ellipse(pos=self.pos, size=self.size)
            # inner bevel
            Color(0, 0, 0, 0.12)
            Ellipse(pos=(self.x + dp(3), self.y + dp(3)), size=(self.width - dp(6), self.height - dp(6)))
            # background ring
            Color(*self.bg_color)
            Line(circle=(self.center_x, self.center_y, min(self.size)/2 - self.thickness/2, 0, 360),
                 width=self.thickness, cap="round")
            # foreground progress
            Color(*self.ring_color)
            Line(circle=(self.center_x, self.center_y, min(self.size)/2 - self.thickness/2, -90,
                         -90 + 360 * max(0.0, min(1.0, self.progress))),
                 width=self.thickness, cap="round")


KV = """
#:import dp kivy.metrics.dp

<GlassCard@MDCard>:
    md_bg_color: 1,1,1,.08
    elevation: 3
    radius: [20,]
    padding: dp(16)
    ripple_behavior: True

<LoginScreen@MDScreen>:
    name: "login"
    canvas.before:
        Color:
            rgba: 0.05, 0.06, 0.12, 1
        Rectangle:
            pos: self.pos
            size: self.size

    MDBoxLayout:
        orientation: "vertical"
        padding: dp(0), dp(36), dp(0), dp(24)
        spacing: dp(10)

        MDBoxLayout:
            orientation: "vertical"
            adaptive_height: True
            MDLabel:
                text: "USIU"
                halign: "center"
                theme_text_color: "Custom"
                text_color: 1,1,1,.98
                bold: True
                font_size: "28sp"
                size_hint_y: None
                height: self.texture_size[1]
            MDLabel:
                text: "AFRICA"
                halign: "center"
                theme_text_color: "Custom"
                text_color: .58,.66,1,1
                font_size: "16sp"
                size_hint_y: None
                height: self.texture_size[1]

        AnchorLayout:
            anchor_x: "center"
            anchor_y: "center"

            GlassCard:
                size_hint: None, None
                width: min(root.width * .42, dp(520))
                height: dp(440)

                MDBoxLayout:
                    orientation: "vertical"
                    spacing: dp(14)

                    MDLabel:
                        text: "Login"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: 1,1,1,.98
                        bold: True
                        font_size: "22sp"
                        size_hint_y: None
                        height: self.texture_size[1]+dp(4)

                    MDLabel:
                        text: "Email"
                        theme_text_color: "Custom"
                        text_color: 1,1,1,.86
                        font_size: "14sp"
                        size_hint_y: None
                        height: self.texture_size[1]
                        padding_x: dp(4)
                    MDTextField:
                        id: email
                        mode: "outlined"
                        hint_text: "name@usiu.ac.ke"
                        icon_right: "email-outline"
                        size_hint_y: None
                        height: dp(56)
                        text_color_normal: 1,1,1,1
                        text_color_focus: 1,1,1,1
                        line_color_normal: 1,1,1,.25
                        line_color_focus: .58,.66,1,1
                        on_text_validate: pwd.focus = True

                    MDLabel:
                        text: "Password"
                        theme_text_color: "Custom"
                        text_color: 1,1,1,.86
                        font_size: "14sp"
                        size_hint_y: None
                        height: self.texture_size[1]
                        padding_x: dp(4)
                    MDTextField:
                        id: pwd
                        mode: "outlined"
                        hint_text: "••••"
                        password: True
                        icon_right: "lock-outline"
                        size_hint_y: None
                        height: dp(56)
                        text_color_normal: 1,1,1,1
                        text_color_focus: 1,1,1,1
                        line_color_normal: 1,1,1,.25
                        line_color_focus: .58,.66,1,1
                        on_text_validate: app.sign_in(email.text, self.text, remember.active)

                    MDBoxLayout:
                        adaptive_height: True
                        spacing: dp(8)
                        MDBoxLayout:
                            size_hint_x: .7
                            adaptive_height: True
                            spacing: dp(8)
                            MDCheckbox:
                                id: remember
                                size_hint: None, None
                                size: dp(22), dp(22)
                                pos_hint: {"center_y": .5}
                            MDLabel:
                                text: "Remember Me"
                                theme_text_color: "Custom"
                                text_color: 1,1,1,.85
                                valign: "middle"
                                halign: "left"
                                font_size: "14sp"
                        MDButton:
                            style: "text"
                            on_release: app.forgot_password()
                            MDButtonText:
                                text: "FORGOT PASSWORD"

                    MDButton:
                        style: "filled"
                        pos_hint: {"center_x": .5}
                        on_release: app.sign_in(email.text, pwd.text, remember.active)
                        MDButtonText:
                            text: "LOG IN"

        MDLabel:
            text: "Education to take you places"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 1,1,1,.7
            font_size: "13sp"
            size_hint_y: None
            height: self.texture_size[1] + dp(6)

<AdminScreen@MDScreen>:
    name: "admin"

    MDBoxLayout:
        orientation: "vertical"
        spacing: 0

        # ---- Header ----
        MDBoxLayout:
            id: header_bar
            size_hint_y: None
            height: dp(58)
            padding: dp(16), 0
            md_bg_color: 1,1,1,.06
            MDLabel:
                id: header_title
                text: "USIU · Admin"
                theme_text_color: "Custom"
                text_color: 1,1,1,.95
                halign: "left"
                bold: True
                font_size: "20sp"
            Widget:
            MDIconButton:
                id: profile_btn
                icon: "account-circle"
                theme_text_color: "Custom"
                text_color: 1,1,1,.95
                on_release: app.open_profile_menu(self)

        # ---- Content ----
        MDBoxLayout:
            id: content_row
            padding: dp(16)
            spacing: dp(16)
            canvas.before:
                Color:
                    rgba: 0.05, 0.06, 0.12, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

            # Left column: Tasks
            MDBoxLayout:
                id: left_col
                orientation: "vertical"
                size_hint_x: None
                width: min(dp(380), root.width*.40)
                spacing: dp(12)

                # ----- Tasks Summary Card -----
                GlassCard:
                    id: card_tasks
                    orientation: "vertical"
                    padding: dp(18)
                    spacing: dp(10)

                    # HEADER pinned to top
                    MDBoxLayout:
                        id: tasks_header
                        size_hint_y: None
                        height: dp(34)
                        spacing: dp(8)

                        MDLabel:
                            text: "My Tasks"
                            theme_text_color: "Custom"
                            text_color: 1,1,1,.98
                            bold: True
                            font_size: "18sp"
                            halign: "left"

                        MDCard:
                            id: time_pill
                            size_hint: None, None
                            height: dp(26)
                            radius: [13,]
                            padding: dp(12), 0
                            md_bg_color: 1,1,1,.10
                            elevation: 0
                            MDLabel:
                                id: time_label
                                text: "Thu 06 Nov • 09:44:12"
                                theme_text_color: "Custom"
                                text_color: 1,1,1,.92
                                font_size: "12sp"
                                halign: "center"
                                valign: "middle"
                                size_hint: None, 1
                                text_size: None, self.height
                                on_texture_size: self.parent.width = self.texture_size[0] + dp(24)

                    # Spacer ensures no overlap with the ring
                    Widget:
                        size_hint_y: None
                        height: dp(26)

                    # CONTENT: bigger ring + stats
                    MDBoxLayout:
                        adaptive_height: True
                        spacing: dp(16)

                        MDBoxLayout:
                            size_hint_x: None
                            width: dp(168)
                            padding: dp(2)
                            UICircleProgress:
                                id: progress_ring
                                size_hint: None, None
                                size: dp(128), dp(128)
                                ring_color: .62, .72, 1, 1
                                bg_color: 1,1,1,.18
                                thickness: dp(16)

                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: dp(6)
                            MDLabel:
                                id: progress_caption
                                text: "0% complete"
                                theme_text_color: "Custom"
                                text_color: 1,1,1,.98
                                font_size: "18sp"
                                bold: True
                            MDLabel:
                                id: progress_sub
                                text: "0 / 0 tasks"
                                theme_text_color: "Custom"
                                text_color: 1,1,1,.75
                                font_size: "13sp"

                # ----- Task List Card -----
                GlassCard:
                    id: card_tasklist
                    padding: 0
                    radius: [16,]
                    MDScrollView:
                        MDList:
                            id: task_list

                MDButton:
                    id: add_task_btn
                    style: "filled"
                    on_release: app.open_add_task()
                    MDButtonText:
                        text: "Add Task"

            # Right column: Actions grid
            MDBoxLayout:
                id: right_col
                orientation: "vertical"
                spacing: dp(12)

                MDLabel:
                    id: quick_actions_title
                    text: "Quick Actions"
                    theme_text_color: "Custom"
                    text_color: 1,1,1,.98
                    size_hint_y: None
                    height: self.texture_size[1]
                    bold: True
                    font_size: "18sp"

                GlassCard:
                    id: actions_card
                    padding: dp(14)
                    MDGridLayout:
                        id: action_grid
                        cols: 2 if root.width < dp(980) else 3
                        adaptive_height: True
                        spacing: dp(12)
"""


class AppUSIU(MDApp):
    dialog: MDDialog | None = None
    new_task_field: MDTextField | None = None
    tasks = ListProperty([])  # {"title": str, "done": bool}
    _profile_menu: MDDropdownMenu | None = None
    _clock_ev = None

    def build(self):
        if not Window.fullscreen:
            Window.size = (1100, 720)

        self.title = "USIU – App"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.accent_palette = "Amber"

        Builder.load_string(KV)
        self.sm = ScreenManager(transition=FadeTransition(duration=0.22))
        self.sm.add_widget(Factory.LoginScreen())
        self.sm.add_widget(Factory.AdminScreen())
        return self.sm

    # -------- Helpers --------
    def notify(self, text: str):
        try:
            MDSnackbar(MDSnackbarText(text=text), duration=1.6).open()
        except Exception as e:
            print(f"[Snackbar fallback] {text} (reason: {e})")

    def forgot_password(self):
        self.notify("Forgot password tapped")

    # -------- Login --------
    def sign_in(self, email: str, password: str, remember: bool):
        e, p = email.strip(), password.strip()
        if not e or not p:
            self.notify("Enter email and password")
            return
        if (e.lower() in ("admin", "admin@usiu.ac.ke")) and p == "1245":
            self.notify("Welcome, Admin")
            Clock.schedule_once(lambda *_: self.to_admin(), 0.1)
            return
        self.notify("Invalid credentials (try admin@usiu.ac.ke / 1245)")

    def to_admin(self):
        self.sm.current = "admin"
        Clock.schedule_once(lambda *_: self._prepare_admin_screen(), 0.05)
        Clock.schedule_once(lambda *_: self._animate_admin_intro(), 0.10)
        Clock.schedule_once(lambda *_: self._start_live_clock(), 0.12)

    def logout(self):
        self._stop_live_clock()
        self.sm.current = "login"
        self.notify("Signed out")

    # -------- Profile menu --------
    def open_profile_menu(self, caller_btn: MDIconButton):
        items = [
            {"text": "Profile", "on_release": lambda: self._profile_selected("profile")},
            {"text": "Logout", "on_release": lambda: self._profile_selected("logout")},
        ]
        if self._profile_menu:
            self._profile_menu.dismiss()
        self._profile_menu = MDDropdownMenu(caller=caller_btn, items=items, width_mult=3)
        self._profile_menu.open()

    def _profile_selected(self, which: str):
        if self._profile_menu:
            self._profile_menu.dismiss()
        if which == "logout":
            self.logout()
        else:
            self.notify("Profile (stub)")

    # -------- Admin build --------
    def _prepare_admin_screen(self):
        scr = self.sm.get_screen("admin")
        grid: MDGridLayout = scr.ids.action_grid
        grid.clear_widgets()

        actions = [
            ("account-tie", "Manage Lecturers", self.action_manage_lecturers),
            ("book-open-variant", "Manage Courses", self.action_manage_courses),
            ("account-multiple", "Manage Students", self.action_manage_students),
            ("bullhorn-variant", "Make Announcement", self.action_make_announcement),
            ("billboard", "Create Advert", self.action_make_advert),
            ("calendar-month", "Timetable", self.action_timetable),
            ("file-chart", "Reports", self.action_reports),
            ("cog", "Settings", self.action_settings),
        ]
        for icon, label, fn in actions:
            tile = self._action_tile(icon, label, fn)
            tile.opacity = 0
            tile.scale = 0.95
            grid.add_widget(tile)
            Animation(opacity=1, scale=1, d=0.28, t="out_cubic").start(tile)

        self._refresh_progress_labels()

    def _action_tile(self, icon_name: str, label: str, callback):
        tile = MDCard(
            md_bg_color=(1, 1, 1, 0.06),
            elevation=2,
            radius=[18],
            padding=(dp(16), dp(18)),
            ripple_behavior=True,
            size_hint_y=None,
            height=dp(150),
        )
        box = MDBoxLayout(orientation="vertical", spacing=dp(10))
        ic = MDIcon(icon=icon_name, theme_text_color="Custom", text_color=(.82, .86, 1, 1))
        ic.font_size = "38sp"
        lbl = MDLabel(text=label, theme_text_color="Custom", text_color=(1, 1, 1, .96),
                      halign="center", font_size="15sp")
        box.add_widget(ic); box.add_widget(lbl)
        tile.add_widget(box)
        tile.bind(on_release=lambda *_: callback())
        tile.bind(on_press=lambda *_: Animation(scale=0.98, d=0.08).start(tile),
                  on_release=lambda *_: Animation(scale=1.0, d=0.12).start(tile))
        return tile

    # -------- Tasks --------
    def open_add_task(self):
        self.new_task_field = MDTextField(hint_text="Task title", helper_text="e.g., Verify new course submissions")
        self.dialog = MDDialog(
            title="Add Task",
            type="custom",
            content_cls=self.new_task_field,
            buttons=[
                MDButton(MDButtonText(text="Cancel"), style="text", on_release=lambda *_: self.dialog.dismiss()),
                MDButton(MDButtonText(text="Add"), style="filled", on_release=lambda *_: self._add_task_confirm()),
            ],
        )
        self.dialog.open()

    def _add_task_confirm(self):
        title = (self.new_task_field.text or "").strip()
        if not title:
            self.notify("Enter a task title"); return
        self.tasks.append({"title": title, "done": False})
        self._rebuild_task_list()
        self.dialog.dismiss()
        self.notify("Task added")

    def _rebuild_task_list(self):
        scr = self.sm.get_screen("admin")
        lst = scr.ids.task_list
        lst.clear_widgets()
        for idx, task in enumerate(self.tasks):
            item = MDListItem(
                ripple_behavior=True,
                on_release=lambda _i, _idx=idx: self._toggle_task(_idx)
            )
            item.add_widget(MDListItemLeadingIcon(
                icon="check-circle" if task["done"] else "checkbox-blank-circle-outline",
                theme_text_color="Custom", text_color=(.58, .78, 1, 1)))
            item.add_widget(MDListItemHeadlineText(text=task["title"]))
            item.add_widget(MDListItemTrailingIcon(
                icon="close", on_release=lambda _b, _idx=idx: self._remove_task(_idx)))
            lst.add_widget(item)
        self._animate_progress_to_current()

    def _toggle_task(self, idx: int):
        self.tasks[idx]["done"] = not self.tasks[idx]["done"]
        self._rebuild_task_list()
        self.notify("Task updated")

    def _remove_task(self, idx: int):
        if 0 <= idx < len(self.tasks):
            self.tasks.pop(idx)
            self._rebuild_task_list()
            self.notify("Task removed")

    def _calc_progress(self) -> float:
        if not self.tasks:
            return 0.0
        return sum(1 for t in self.tasks if t["done"]) / float(len(self.tasks))

    def _refresh_progress_labels(self):
        scr = self.sm.get_screen("admin")
        ring: UICircleProgress = scr.ids.progress_ring
        cap: MDLabel = scr.ids.progress_caption
        sub: MDLabel = scr.ids.progress_sub
        pct = int(round((ring.progress or 0) * 100))
        cap.text = f"{pct}% complete"
        sub.text = f"{sum(1 for t in self.tasks if t.get('done'))} / {len(self.tasks)} tasks"

    def _animate_progress_to_current(self):
        scr = self.sm.get_screen("admin")
        ring: UICircleProgress = scr.ids.progress_ring
        target = self._calc_progress()
        Animation.cancel_all(ring, "progress")
        Animation(progress=target, d=.35, t="out_cubic").bind(
            on_progress=lambda *_: self._refresh_progress_labels()
        ).start(ring)

    # -------- Entrance animations --------
    def _animate_admin_intro(self):
        scr = self.sm.get_screen("admin")
        header = scr.ids.header_bar
        left = scr.ids.left_col
        right = scr.ids.right_col
        actions_card = scr.ids.actions_card
        tasks_card = scr.ids.card_tasks
        tasklist_card = scr.ids.card_tasklist
        add_btn = scr.ids.add_task_btn

        for w in (header, left, right, tasks_card, tasklist_card, actions_card, add_btn):
            w.opacity = 0
        header.y += dp(18); left.x -= dp(22); right.y -= dp(22)

        Animation(opacity=1, y=header.y - dp(18), d=.28, t="out_cubic").start(header)
        Clock.schedule_once(lambda *_: Animation(opacity=1, x=left.x + dp(22), d=.30, t="out_cubic").start(left), .06)
        Clock.schedule_once(lambda *_: Animation(opacity=1, y=right.y + dp(22), d=.32, t="out_cubic").start(right), .10)
        Clock.schedule_once(lambda *_: Animation(opacity=1, d=.25).start(tasks_card), .16)
        Clock.schedule_once(lambda *_: Animation(opacity=1, d=.25).start(tasklist_card), .22)
        Clock.schedule_once(lambda *_: Animation(opacity=1, d=.25).start(actions_card), .22)
        Clock.schedule_once(lambda *_: Animation(opacity=1, d=.25).start(add_btn), .28)

    # -------- Live date/time --------
    def _format_now(self) -> str:
        return datetime.now().strftime("%a %d %b • %H:%M:%S")

    def _tick_clock(self, *_):
        try:
            scr = self.sm.get_screen("admin")
            scr.ids.time_label.text = self._format_now()
        except Exception:
            pass

    def _start_live_clock(self):
        self._stop_live_clock()
        self._tick_clock()
        self._clock_ev = Clock.schedule_interval(self._tick_clock, 1.0)

    def _stop_live_clock(self):
        if self._clock_ev is not None:
            self._clock_ev.cancel()
            self._clock_ev = None

    # -------- Action stubs --------
    def action_manage_lecturers(self): self.notify("Open: Manage Lecturers")
    def action_manage_courses(self): self.notify("Open: Manage Courses")
    def action_manage_students(self): self.notify("Open: Manage Students")
    def action_make_announcement(self): self.notify("Open: Make Announcement")
    def action_make_advert(self): self.notify("Open: Create Advert")
    def action_timetable(self): self.notify("Open: Timetable")
    def action_reports(self): self.notify("Open: Reports")
    def action_settings(self): self.notify("Open: Settings")


if __name__ == "__main__":
    AppUSIU().run()
