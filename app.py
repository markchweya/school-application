# app.py
from kivy import require
require("2.3.0")

from datetime import datetime
from uuid import uuid4
from functools import partial

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import (
    ColorProperty, ListProperty, NumericProperty, StringProperty, ObjectProperty
)
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.uix.modalview import ModalView

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText


# ---------- Neumorphic circle progress ----------
class UICircleProgress(Widget):
    progress = NumericProperty(0.0)
    ring_color = ColorProperty([0.62, 0.72, 1.0, 1.0])
    bg_color = ColorProperty([1, 1, 1, 0.14])
    thickness = NumericProperty(dp(16))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self._redraw, size=self._redraw, progress=self._redraw)

    def _redraw(self, *_):
        self.canvas.clear()
        from kivy.graphics import Color, Ellipse, Line
        with self.canvas:
            # soft outer
            Color(0, 0, 0, 0.28)
            Ellipse(pos=(self.x + dp(4), self.y - dp(4)), size=(self.width, self.height))
            # plate
            Color(1, 1, 1, 0.08)
            Ellipse(pos=self.pos, size=self.size)
            # inner
            Color(0, 0, 0, 0.10)
            Ellipse(pos=(self.x + dp(4), self.y + dp(4)), size=(self.width - dp(8), self.height - dp(8)))
            # bg ring
            Color(*self.bg_color)
            Line(circle=(self.center_x, self.center_y, min(self.size)/2 - self.thickness/2, 0, 360),
                 width=self.thickness, cap="round")
            # progress
            Color(*self.ring_color)
            Line(circle=(self.center_x, self.center_y, min(self.size)/2 - self.thickness/2, -90,
                         -90 + 360 * max(0.0, min(1.0, self.progress))),
                 width=self.thickness, cap="round")


KV = """
#:import dp kivy.metrics.dp

<GlassCard@MDCard>:
    md_bg_color: 1,1,1,.07
    elevation: 0
    radius: [22,]
    padding: dp(16)
    ripple_behavior: True
    canvas.before:
        Color:
            rgba: 1,1,1,.08
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [22,]
        Color:
            rgba: 0,0,0,.28
        RoundedRectangle:
            pos: self.x+dp(3), self.y-dp(3)
            size: self.size
            radius: [22,]

<LoginScreen>:
    name: "login"
    canvas.before:
        Color:
            rgba: 0.04, 0.05, 0.11, 1
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
                text_color: .62,.72,1,1
                font_size: "16sp"
                size_hint_y: None
                height: self.texture_size[1]

        AnchorLayout:
            anchor_x: "center"
            anchor_y: "center"
            GlassCard:
                size_hint: None, None
                width: min(root.width * .42, dp(520))
                height: dp(360)

                MDBoxLayout:
                    orientation: "vertical"
                    spacing: dp(16)

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
                    MDTextField:
                        id: email
                        hint_text: "admin@usiu.ac.ke"
                        size_hint_y: None
                        height: dp(56)
                        on_text_validate: pwd.focus = True

                    MDLabel:
                        text: "Password"
                        theme_text_color: "Custom"
                        text_color: 1,1,1,.86
                        font_size: "14sp"
                        size_hint_y: None
                        height: self.texture_size[1]
                    MDTextField:
                        id: pwd
                        hint_text: "••••"
                        password: True
                        size_hint_y: None
                        height: dp(56)
                        on_text_validate: app.sign_in(email.text, self.text)

                    MDButton:
                        style: "filled"
                        pos_hint: {"center_x": .5}
                        on_release: app.sign_in(email.text, pwd.text)
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

<AdminScreen>:
    name: "admin"
    MDBoxLayout:
        orientation: "vertical"
        spacing: 0

        # Header
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

        # Body
        MDBoxLayout:
            id: content_row
            padding: dp(16)
            spacing: dp(16)
            canvas.before:
                Color:
                    rgba: 0.04, 0.05, 0.11, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

            # Left: tasks
            MDBoxLayout:
                id: left_col
                orientation: "vertical"
                size_hint_x: None
                width: min(dp(380), root.width*.40)
                spacing: dp(12)

                MDLabel:
                    id: tasks_section_title
                    text: "My Tasks"
                    theme_text_color: "Custom"
                    text_color: 1,1,1,.98
                    size_hint_y: None
                    height: self.texture_size[1]
                    bold: True
                    font_size: "18sp"

                GlassCard:
                    id: card_tasks
                    orientation: "vertical"
                    padding: dp(18)
                    spacing: dp(10)

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
                                ring_color: .70, .78, 1, 1
                                bg_color: 1,1,1,.16
                                thickness: dp(16)

                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: dp(4)

                            MDLabel:
                                id: time_label
                                text: "Thu 06 Nov • 11:46:38"
                                theme_text_color: "Custom"
                                text_color: 1,1,1,.80
                                font_size: "12sp"
                                size_hint_y: None
                                height: self.texture_size[1]

                            MDLabel:
                                id: progress_caption
                                text: "0% complete"
                                theme_text_color: "Custom"
                                text_color: 1,1,1,.98
                                font_size: "18sp"
                                bold: True
                                size_hint_y: None
                                height: self.texture_size[1]

                # Tasks list
                GlassCard:
                    id: card_tasklist
                    padding: dp(14)
                    radius: [22,]
                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: dp(8)

                        MDBoxLayout:
                            size_hint_y: None
                            height: dp(34)
                            MDLabel:
                                text: "Tasks"
                                theme_text_color: "Custom"
                                text_color: 1,1,1,.9
                                bold: True
                                font_size: "14sp"
                                halign: "left"
                            Widget:
                            MDIconButton:
                                id: add_task_btn
                                icon: "plus"
                                theme_text_color: "Custom"
                                text_color: 1,1,1,.95
                                md_bg_color: .32,.42,.75,1
                                size_hint: None, None
                                size: dp(42), dp(42)
                                radius: [21,]
                                on_release: app.open_add_task()

                        MDScrollView:
                            MDBoxLayout:
                                id: task_list
                                orientation: "vertical"
                                adaptive_height: True
                                spacing: dp(8)

            # Right: quick actions
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

<SimpleScreen>:
    MDBoxLayout:
        orientation: "vertical"
        padding: dp(16)
        spacing: dp(12)
        MDBoxLayout:
            size_hint_y: None
            height: dp(52)
            MDLabel:
                id: title_lbl
                text: root.title
                bold: True
                font_size: "20sp"
                theme_text_color: "Custom"
                text_color: 1,1,1,.96
            Widget:
            MDButton:
                style: "text"
                on_release: app.go_home()
                MDButtonText:
                    text: "Back"
        GlassCard:
            MDBoxLayout:
                id: content_box
                padding: dp(12)
                orientation: "vertical"
                spacing: dp(8)
"""

# ---- Simple screens for actions ----
class SimpleScreen(MDScreen):
    title = StringProperty("")

class LoginScreen(MDScreen):
    pass

class AdminScreen(MDScreen):
    pass


# ---- Basic input dialog (ModalView) ----
class InputDialog(ModalView):
    title = StringProperty("Title")
    text = StringProperty("")
    on_submit = ObjectProperty(allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.auto_dismiss = False
        self.background = ""
        self.width = min(Window.width * .45, dp(520))
        self.height = dp(220)

        card = MDCard(
            orientation="vertical",
            padding=dp(16),
            radius=[20],
            size_hint=(1, 1),
            md_bg_color=(0.1, 0.12, 0.18, 1),
        )

        self._title_lbl = MDLabel(
            text=self.title, bold=True, font_size="18sp",
            theme_text_color="Custom", text_color=(1, 1, 1, .96),
            size_hint_y=None, height=dp(28)
        )
        self._field = MDTextField(
            hint_text="Enter text",
            text=self.text,
            size_hint_y=None, height=dp(56)
        )

        btn_row = MDBoxLayout(size_hint_y=None, height=dp(48), spacing=dp(8))
        btn_row.add_widget(Widget())
        btn_row.add_widget(MDButton(
            MDButtonText(text="Cancel"),
            style="text",
            on_release=lambda *_: self.dismiss(),
        ))
        btn_row.add_widget(MDButton(
            MDButtonText(text="Save"),
            style="filled",
            on_release=lambda *_: self._fire_submit(),
        ))

        card.add_widget(self._title_lbl)
        card.add_widget(self._field)
        card.add_widget(Widget())
        card.add_widget(btn_row)
        self.add_widget(card)

    def open_with(self, title: str, preset: str):
        self._title_lbl.text = title
        self._field.text = preset or ""
        super().open()

    def _fire_submit(self):
        txt = (self._field.text or "").strip()
        if not txt:
            return
        if self.on_submit:
            try:
                self.on_submit(txt)
            finally:
                self.on_submit = None
        self.dismiss()


# ---- App ----
class AppUSIU(MDApp):
    dialog: InputDialog | None = None
    tasks = ListProperty([])  # each: {"id": str, "title": str, "status": "todo"|"progress"|"done"}

    _profile_menu: MDDropdownMenu | None = None
    _clock_ev = None
    sm: ScreenManager

    students = ListProperty([])  # {"id": str, "name": str, "program": str}

    def build(self):
        if not Window.fullscreen:
            Window.size = (1100, 720)

        self.title = "USIU – App"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.accent_palette = "Amber"

        Builder.load_string(KV)
        self.sm = ScreenManager(transition=FadeTransition(duration=0.32))
        self.sm.add_widget(LoginScreen())
        self.sm.add_widget(AdminScreen())

        # action screens
        self._add_simple_screen("students", "Manage Students")
        self._add_simple_screen("lecturers", "Manage Lecturers")
        self._add_simple_screen("courses", "Manage Courses")
        self._add_simple_screen("announce", "Make Announcement")
        self._add_simple_screen("adverts", "Create Advert")
        self._add_simple_screen("timetable", "Timetable")
        self._add_simple_screen("reports", "Reports")
        self._add_simple_screen("settings", "Settings")

        return self.sm

    def _add_simple_screen(self, name: str, title: str):
        scr = SimpleScreen(name=name, title=title)
        box = scr.ids.content_box

        if name == "students":
            top = MDBoxLayout(size_hint_y=None, height=dp(44), spacing=dp(8))
            top.add_widget(MDLabel(text="Students", bold=True,
                                   theme_text_color="Custom", text_color=(1,1,1,.96)))
            top.add_widget(Widget())
            top.add_widget(MDButton(MDButtonText(text="Add Student"),
                                    style="filled", on_release=lambda *_: self._open_add_student()))
            box.add_widget(top)

            self._students_scroll = MDScrollView()
            self._students_list = MDBoxLayout(orientation="vertical", adaptive_height=True, spacing=dp(6))
            self._students_scroll.add_widget(self._students_list)
            box.add_widget(self._students_scroll)

        elif name == "settings":
            row = MDBoxLayout(size_hint_y=None, height=dp(50), spacing=dp(12))
            row.add_widget(MDLabel(text="Theme", theme_text_color="Custom", text_color=(1,1,1,.9)))
            row.add_widget(Widget())
            row.add_widget(MDButton(MDButtonText(text="Light"), style="text",
                                    on_release=lambda *_: self._set_theme("Light")))
            row.add_widget(MDButton(MDButtonText(text="Dark"), style="filled",
                                    on_release=lambda *_: self._set_theme("Dark")))
            box.add_widget(row)
        else:
            info = MDLabel(text=f"{title} – placeholder screen.",
                           theme_text_color="Custom", text_color=(1,1,1,.8))
            box.add_widget(info)

        self.sm.add_widget(scr)

    def _set_theme(self, mode: str):
        self.theme_cls.theme_style = mode
        self.notify(f"Theme: {mode}")

    def go_home(self):
        self.sm.current = "admin"

    # ---- helpers ----
    def notify(self, text: str):
        try:
            MDSnackbar(MDSnackbarText(text=text), duration=1.6).open()
        except Exception as e:
            print(f"[Snackbar] {text} ({e})")

    # ---- login ----
    def sign_in(self, email: str, password: str):
        e, p = email.strip(), password.strip()
        if not e or not p:
            self.notify("Enter email and password"); return
        if (e.lower() in ("admin", "admin@usiu.ac.ke")) and p == "1245":
            self.notify("Welcome, Admin")
            self.to_admin()
            return
        self.notify("Invalid credentials (use admin@usiu.ac.ke / 1245)")

    def to_admin(self):
        self.sm.current = "admin"
        Clock.schedule_once(lambda *_: self._prepare_admin_screen(), 0.05)
        Clock.schedule_once(lambda *_: self._animate_admin_intro(), 0.10)
        Clock.schedule_once(lambda *_: self._start_live_clock(), 0.12)
        Clock.schedule_once(self._animate_progress_to_current, 0.22)

    def logout(self, *_):
        self._stop_live_clock()
        self.sm.current = "login"
        self.notify("Signed out")

    # ---- profile menu ----
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
            self.notify("Profile (coming soon)")

    # ---- admin build ----
    def _prepare_admin_screen(self):
        scr = self.sm.get_screen("admin")
        grid: MDGridLayout = scr.ids.action_grid
        grid.clear_widgets()
        actions = [
            ("account-tie", "Manage Lecturers", lambda: self._open("lecturers")),
            ("book-open-variant", "Manage Courses", lambda: self._open("courses")),
            ("account-multiple", "Manage Students", lambda: self._open("students")),
            ("bullhorn-variant", "Make Announcement", lambda: self._open("announce")),
            ("billboard", "Create Advert", lambda: self._open("adverts")),
            ("calendar-month", "Timetable", lambda: self._open("timetable")),
            ("file-chart", "Reports", lambda: self._open("reports")),
            ("cog", "Settings", lambda: self._open("settings")),
        ]
        for icon, label, fn in actions:
            grid.add_widget(self._action_tile(icon, label, fn))

        Clock.schedule_once(lambda *_: self._rebuild_task_list(), 0.05)
        self._refresh_progress_labels()

    def _open(self, screen_name: str):
        self.sm.current = screen_name

    def _action_tile(self, icon_name: str, label: str, callback):
        tile = MDCard(
            md_bg_color=(1, 1, 1, 0.06),
            elevation=0,
            radius=[20],
            padding=(dp(16), dp(18)),
            ripple_behavior=True,
            size_hint_y=None,
            height=dp(150),
        )
        box = MDBoxLayout(orientation="vertical", spacing=dp(10))
        ic = MDIcon(icon=icon_name, theme_text_color="Custom", text_color=(.85, .89, 1, 1))
        ic.font_size = "40sp"
        lbl = MDLabel(text=label, theme_text_color="Custom", text_color=(1, 1, 1, .96),
                      halign="center", font_size="15sp")
        box.add_widget(ic); box.add_widget(lbl)
        tile.add_widget(box)
        tile.bind(on_release=lambda *_: callback())
        return tile

    # ---- tasks ops ----
    def open_add_task(self):
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = InputDialog(on_submit=self._add_task_confirm)
        self.dialog.open_with("Add Task", "")

    def _add_task_confirm(self, title: str):
        self.tasks.append({"id": str(uuid4()), "title": title, "status": "todo"})
        self._rebuild_task_list()
        self.notify("Task added")

    def _edit_task_title(self, task_id: str, *_):
        task = next((t for t in self.tasks if t["id"] == task_id), None)
        if not task:
            return
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = InputDialog(on_submit=partial(self._confirm_edit_title, task_id))
        self.dialog.open_with("Edit Task", task["title"])

    def _confirm_edit_title(self, task_id: str, new_title: str):
        for t in self.tasks:
            if t["id"] == task_id:
                t["title"] = new_title
                break
        self._rebuild_task_list()
        self.notify("Task updated")

    def _remove_task(self, task_id: str, *_):
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        self._rebuild_task_list()
        self.notify("Task deleted")

    def _set_status(self, task_id: str, status: str, *_):
        for t in self.tasks:
            if t["id"] == task_id:
                t["status"] = status
                break
        self._rebuild_task_list()
        self.notify({"todo":"Not started","progress":"In progress","done":"Done"}[status])

    def _status_color(self, status: str):
        return {
            "todo": (.70, .76, .95, 1),
            "progress": (1.00, .86, .45, 1),
            "done": (.54, .90, .62, 1),
        }[status]

    def _status_weight(self, status: str) -> float:
        return {"todo": 0.0, "progress": 0.5, "done": 1.0}[status]

    def _rebuild_task_list(self, *_):
        scr = self.sm.get_screen("admin")
        container: MDBoxLayout = scr.ids.task_list
        container.clear_widgets()

        if not self.tasks:
            row_card = MDCard(
                md_bg_color=(1, 1, 1, 0.06),
                elevation=0,
                radius=[14],
                padding=(dp(12), dp(10)),
                size_hint_y=None,
                height=dp(56),
            )
            line = MDBoxLayout(spacing=dp(8))
            line.add_widget(MDIcon(icon="information-outline",
                                   theme_text_color="Custom",
                                   text_color=(.75, .82, 1, 1)))
            line.add_widget(MDLabel(text="You have zero tasks",
                                    theme_text_color="Custom",
                                    text_color=(1, 1, 1, .90)))
            row_card.add_widget(line)
            container.add_widget(row_card)
            self._animate_progress_to_current()
            return

        for task in self.tasks:
            row = MDCard(md_bg_color=(1,1,1,.06), elevation=0, radius=[12],
                         padding=(dp(12), dp(8)), size_hint_y=None, height=dp(54))

            line = MDBoxLayout(spacing=dp(10))
            # status button + menu
            status_btn = MDIconButton(
                icon=("check-circle" if task["status"] == "done"
                      else ("progress-clock" if task["status"] == "progress"
                            else "checkbox-blank-circle-outline")),
                theme_text_color="Custom",
                text_color=self._status_color(task["status"]),
            )
            menu_items = [
                {"text": "Not started", "on_release": partial(self._menu_pick_status, status_btn, task["id"], "todo")},
                {"text": "In progress", "on_release": partial(self._menu_pick_status, status_btn, task["id"], "progress")},
                {"text": "Done",        "on_release": partial(self._menu_pick_status, status_btn, task["id"], "done")},
            ]
            menu = MDDropdownMenu(caller=status_btn, items=menu_items, width_mult=3)
            status_btn.bind(on_release=lambda *_: menu.open())

            line.add_widget(status_btn)
            line.add_widget(MDLabel(text=task["title"],
                                    theme_text_color="Custom",
                                    text_color=(1,1,1,.96)))
            line.add_widget(Widget())

            edit_btn = MDIconButton(icon="pencil", theme_text_color="Custom", text_color=(1,1,1,.85),
                                    on_release=partial(self._edit_task_title, task["id"]))
            del_btn = MDIconButton(icon="trash-can-outline", theme_text_color="Custom", text_color=(1,1,1,.85),
                                   on_release=partial(self._remove_task, task["id"]))
            line.add_widget(edit_btn)
            line.add_widget(del_btn)

            row.add_widget(line)
            container.add_widget(row)

        self._animate_progress_to_current()

    def _menu_pick_status(self, caller_btn, task_id: str, status: str, *_):
        self._set_status(task_id, status)
        # update button instantly
        caller_btn.text_color = self._status_color(status)
        caller_btn.icon = ("check-circle" if status == "done"
                           else ("progress-clock" if status == "progress"
                                 else "checkbox-blank-circle-outline"))
        # close any open menu safely
        try:
            MDDropdownMenu.dismiss(caller_btn)  # no-op if unsupported
        except Exception:
            pass

    # ---- progress math & UI ----
    def _calc_progress(self) -> float:
        if not self.tasks:
            return 0.0
        score = sum(self._status_weight(t["status"]) for t in self.tasks)
        return score / float(len(self.tasks))

    def _refresh_progress_labels(self, *_):
        try:
            scr = self.sm.get_screen("admin")
            ring: UICircleProgress = scr.ids.get("progress_ring", None)
            cap: MDLabel = scr.ids.get("progress_caption", None)
            if not (ring and cap): 
                return
            pct = int(round((ring.progress or 0) * 100))
            cap.text = f"{pct}% complete"
        except Exception:
            pass

    def _animate_progress_to_current(self, *_):
        try:
            scr = self.sm.get_screen("admin")
        except Exception:
            Clock.schedule_once(self._animate_progress_to_current, 0.05)
            return

        ring = scr.ids.get("progress_ring", None)
        if ring is None:
            Clock.schedule_once(self._animate_progress_to_current, 0.05)
            return

        target = self._calc_progress()
        try:
            Animation.cancel_all(ring, "progress")
            anim = Animation(progress=target, d=.35, t="out_cubic")
            anim.bind(on_progress=self._refresh_progress_labels, on_complete=self._refresh_progress_labels)
            anim.start(ring)
        except Exception:
            ring.progress = target
            self._refresh_progress_labels()

    # ---- entrance choreography ----
    def _animate_admin_intro(self):
        scr = self.sm.get_screen("admin")
        header = scr.ids.header_bar
        left = scr.ids.left_col
        right = scr.ids.right_col
        actions_card = scr.ids.actions_card
        tasks_card = scr.ids.card_tasks
        tasklist_card = scr.ids.card_tasklist
        tasks_title = scr.ids.tasks_section_title

        for w in (header, left, right, tasks_card, tasklist_card, actions_card, tasks_title):
            w.opacity = 0
        header.y += dp(18); left.x -= dp(22); right.y -= dp(22)

        Animation(opacity=1, y=header.y - dp(18), d=.28, t="out_cubic").start(header)
        Clock.schedule_once(lambda *_: Animation(opacity=1, x=left.x + dp(22), d=.30, t="out_cubic").start(left), .06)
        Clock.schedule_once(lambda *_: Animation(opacity=1, y=right.y + dp(22), d=.32, t="out_cubic").start(right), .10)
        Clock.schedule_once(lambda *_: Animation(opacity=1, d=.25).start(tasks_title), .12)
        Clock.schedule_once(lambda *_: Animation(opacity=1, d=.25).start(tasks_card), .16)
        Clock.schedule_once(lambda *_: Animation(opacity=1, d=.25).start(tasklist_card), .22)
        Clock.schedule_once(lambda *_: Animation(opacity=1, d=.25).start(actions_card), .22)

    # ---- live clock ----
    def _format_now(self) -> str:
        return datetime.now().strftime("%a %d %b • %H:%M:%S")

    def _tick_clock(self, *_):
        try:
            scr = self.sm.get_screen("admin")
            lbl = scr.ids.get("time_label", None)
            if lbl:
                lbl.text = self._format_now()
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

    # ---- Students helpers ----
    def _open_add_student(self):
        if self.dialog:
            self.dialog.dismiss()
        dlg = InputDialog(on_submit=self._add_student_row)
        dlg.open_with("New Student (Name – Program)", "")
        self.dialog = dlg

    def _add_student_row(self, text: str):
        parts = [p.strip() for p in text.split("–", 1)]
        name = parts[0]
        program = parts[1] if len(parts) > 1 else "Unknown Program"
        self.students.append({"id": str(uuid4())[:8], "name": name, "program": program})
        self._refresh_students_list()
        self.notify("Student added")

    def _refresh_students_list(self):
        scr = self.sm.get_screen("students")
        lst: MDBoxLayout = self._students_list
        lst.clear_widgets()
        if not self.students:
            lst.add_widget(MDLabel(text="No students yet.",
                                   theme_text_color="Custom", text_color=(1,1,1,.8)))
            return
        for s in self.students:
            row = MDCard(md_bg_color=(1,1,1,.06), elevation=0, radius=[12],
                         padding=(dp(12), dp(8)), size_hint_y=None, height=dp(54))
            line = MDBoxLayout(spacing=dp(10))
            line.add_widget(MDIcon(icon="account", theme_text_color="Custom", text_color=(.85,.89,1,1)))
            line.add_widget(MDLabel(text=f"{s['name']}  •  {s['program']}",
                                    theme_text_color="Custom", text_color=(1,1,1,.96)))
            line.add_widget(Widget())
            del_btn = MDIconButton(icon="trash-can-outline", theme_text_color="Custom", text_color=(1,1,1,.85),
                                   on_release=partial(self._delete_student, s["id"]))
            line.add_widget(del_btn)
            row.add_widget(line)
            lst.add_widget(row)

    def _delete_student(self, sid: str, *_):
        self.students = [x for x in self.students if x["id"] != sid]
        self._refresh_students_list()
        self.notify("Student removed")


if __name__ == "__main__":
    AppUSIU().run()
