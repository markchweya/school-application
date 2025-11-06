# app.py
from kivy import require
require("2.3.0")

from datetime import datetime
from uuid import uuid4

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import (
    ColorProperty, ListProperty, NumericProperty,
    StringProperty, ObjectProperty
)
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.uix.modalview import ModalView

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivymd.uix.card import MDCard
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.menu import MDDropdownMenu


# ---------- Circle progress ----------
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
            Color(0, 0, 0, 0.28)
            Ellipse(pos=(self.x + dp(4), self.y - dp(4)), size=(self.width, self.height))
            Color(1, 1, 1, 0.08)
            Ellipse(pos=self.pos, size=self.size)
            Color(0, 0, 0, 0.10)
            Ellipse(pos=(self.x + dp(4), self.y + dp(4)), size=(self.width - dp(8), self.height - dp(8)))
            Color(*self.bg_color)
            Line(circle=(self.center_x, self.center_y, min(self.size)/2 - self.thickness/2, 0, 360),
                 width=self.thickness, cap="round")
            Color(*self.ring_color)
            Line(circle=(self.center_x, self.center_y, min(self.size)/2 - self.thickness/2, -90,
                         -90 + 360 * max(0.0, min(1.0, self.progress))),
                 width=self.thickness, cap="round")


# ---------- One task row ----------
class TaskRow(MDCard):
    """Custom row for a task with status toggle, title label, edit and delete."""
    task_id = StringProperty("")
    title = StringProperty("")
    status = StringProperty("todo")  # "todo" | "progress" | "done"
    app_ref = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.elevation = 0
        self.radius = [14]
        self.padding = (dp(10), dp(10))
        self.size_hint_y = None
        self.height = dp(52)
        self.md_bg_color = (1, 1, 1, 0.06)

        row = MDBoxLayout(orientation="horizontal", spacing=dp(10))

        # Left: status icon button
        self.btn_status = MDIconButton(
            theme_text_color="Custom",
            text_color=self._status_color(self.status),
            icon=self._status_icon(self.status),
            on_release=lambda *_: self._cycle_status()
        )
        self.btn_status.size_hint = (None, None)
        self.btn_status.size = (dp(36), dp(36))
        row.add_widget(self.btn_status)

        # Title label (stretch)
        self.lbl = MDLabel(
            text=self.title,
            theme_text_color="Custom",
            text_color=(1, 1, 1, .95),
            halign="left",
            valign="middle"
        )
        row.add_widget(self.lbl)
        row.add_widget(Widget())

        # Edit
        self.btn_edit = MDIconButton(
            icon="pencil-outline",
            theme_text_color="Custom",
            text_color=(.85, .90, 1, 1),
            on_release=lambda *_: self._edit_title()
        )
        self.btn_edit.size_hint = (None, None)
        self.btn_edit.size = (dp(32), dp(32))
        row.add_widget(self.btn_edit)

        # Delete
        self.btn_del = MDIconButton(
            icon="trash-can-outline",
            theme_text_color="Custom",
            text_color=(1, .80, .80, 1),
            on_release=lambda *_: self._delete_me()
        )
        self.btn_del.size_hint = (None, None)
        self.btn_del.size = (dp(32), dp(32))
        row.add_widget(self.btn_del)

        self.add_widget(row)

    # helpers
    def _status_icon(self, st: str) -> str:
        return {"todo": "checkbox-blank-circle-outline",
                "progress": "progress-check",
                "done": "check-circle"}[st]

    def _status_color(self, st: str):
        return {"todo": (.70, .76, .95, 1),
                "progress": (1.00, .86, .45, 1),
                "done": (.54, .90, .62, 1)}[st]

    def _cycle_status(self):
        order = ["todo", "progress", "done"]
        nxt = order[(order.index(self.status) + 1) % len(order)]
        self.status = nxt
        # update visuals
        self.btn_status.icon = self._status_icon(nxt)
        self.btn_status.text_color = self._status_color(nxt)
        # notify app
        if self.app_ref:
            self.app_ref.update_task_status(self.task_id, nxt)
            label = {"todo": "Not started", "progress": "In progress", "done": "Complete"}[nxt]
            self.app_ref.notify(f"Status: {label}")

    def _delete_me(self):
        if self.app_ref:
            self.app_ref.delete_task(self.task_id)

    def _edit_title(self):
        if self.app_ref:
            self.app_ref.open_rename_task(self.task_id, self.title)


KV = """
#:import dp kivy.metrics.dp
#:import Animation kivy.animation.Animation

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
                height: dp(440)

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
                        mode: "outlined"
                        hint_text: "admin@usiu.ac.ke"
                        icon_right: "email-outline"
                        size_hint_y: None
                        height: dp(56)
                        text_color_normal: 1,1,1,1
                        text_color_focus: 1,1,1,1
                        line_color_normal: 1,1,1,.25
                        line_color_focus: .62,.72,1,1
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
                        mode: "outlined"
                        hint_text: "••••"
                        password: True
                        icon_right: "lock-outline"
                        size_hint_y: None
                        height: dp(56)
                        text_color_normal: 1,1,1,1
                        text_color_focus: 1,1,1,1
                        line_color_normal: 1,1,1,.25
                        line_color_focus: .62,.72,1,1
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
                                text: "Thu 06 Nov • 12:38:32"
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
                                id: fab_plus
                                icon: "plus"
                                theme_text_color: "Custom"
                                text_color: 0.12,0.16,0.32,1
                                md_bg_color: .82,.88,1,1
                                size_hint: None, None
                                size: dp(40), dp(40)
                                radius: [20,]
                                on_release: app.open_add_task()
                                canvas.before:
                                    Color:
                                        rgba: 1,1,1,.85
                                    RoundedRectangle:
                                        pos: self.pos
                                        size: self.size
                                        radius: [20,]
                                    Color:
                                        rgba: 1,1,1,.25
                                    RoundedRectangle:
                                        pos: self.x, self.y
                                        size: self.size
                                        radius: [20,]
                                canvas.after:
                                    Color:
                                        rgba: 0,0,0,.28
                                    RoundedRectangle:
                                        pos: self.x+dp(2), self.y-dp(2)
                                        size: self.size
                                        radius: [20,]

                        MDScrollView:
                            MDBoxLayout:
                                id: task_list
                                orientation: "vertical"
                                spacing: dp(8)
                                size_hint_y: None
                                height: self.minimum_height

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
"""


class LoginScreen(MDScreen):
    pass


class AdminScreen(MDScreen):
    pass


class AppUSIU(MDApp):
    # lightweight modals instead of MDDialog
    _add_view: ModalView | None = None
    _rename_view: ModalView | None = None
    new_task_field: MDTextField | None = None
    rename_field: MDTextField | None = None

    # task model list of dicts with stable IDs
    tasks = ListProperty([])  # [{"id": str, "title": str, "status": str}, ...]

    _profile_menu: MDDropdownMenu | None = None
    _clock_ev = None

    STATUS_LABELS = {"todo": "Not started", "progress": "In progress", "done": "Complete"}
    STATUS_WEIGHTS = {"todo": 0.0, "progress": 0.5, "done": 1.0}

    def build(self):
        if not Window.fullscreen:
            Window.size = (1100, 720)
        self.title = "USIU – App"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.accent_palette = "Amber"

        # register TaskRow rule so kivy can instantiate it
        Builder.load_string("""
<TaskRow>:
""")
        Builder.load_string(KV)
        self.sm = ScreenManager(transition=FadeTransition(duration=0.32))
        self.sm.add_widget(LoginScreen())
        self.sm.add_widget(AdminScreen())
        return self.sm

    # ---- helpers ----
    def notify(self, text: str):
        try:
            MDSnackbar(MDSnackbarText(text=text), duration=1.4).open()
        except Exception as e:
            print(f"[Snackbar] {text} ({e})")

    def forgot_password(self):
        self.notify("Ask IT Helpdesk to reset password")

    # ---- login ----
    def sign_in(self, email: str, password: str, remember: bool):
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
        if grid is None:
            Clock.schedule_once(lambda *_: self._prepare_admin_screen(), 0.05)
            return

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
            tile = MDCard(
                md_bg_color=(1, 1, 1, 0.06),
                elevation=0,
                radius=[20],
                padding=(dp(16), dp(18)),
                ripple_behavior=True,
                size_hint_y=None,
                height=dp(150),
            )

            def _press(*_):
                Animation(md_bg_color=(1, 1, 1, 0.10), elevation=2, d=.10).start(tile)

            # FIXED: capture fn via default arg on a normal named parameter
            def _release(*_, cb=fn):
                Animation(md_bg_color=(1, 1, 1, 0.06), elevation=0, d=.18).start(tile)
                cb()

            box = MDBoxLayout(orientation="vertical", spacing=dp(10))
            ic = MDIcon(icon=icon, theme_text_color="Custom", text_color=(.85, .89, 1, 1))
            ic.font_size = "40sp"
            lbl = MDLabel(text=label, theme_text_color="Custom", text_color=(1, 1, 1, .96),
                          halign="center", font_size="15sp")
            box.add_widget(ic); box.add_widget(lbl)
            tile.add_widget(box)
            tile.bind(on_press=_press, on_release=_release)

            tile.opacity = 0
            grid.add_widget(tile)
            Animation(opacity=1, d=0.26, t="out_cubic").start(tile)

        self._refresh_progress_labels()
        Clock.schedule_once(lambda *_: self._rebuild_task_list(), 0.05)

    # ---- add / rename modals (ModalView) ----
    def _build_modal(self, title_text: str, field: MDTextField, on_confirm):
        card = MDCard(
            orientation="vertical",
            padding=(dp(16), dp(16), dp(16), dp(12)),
            spacing=dp(12),
            radius=[18],
            size_hint=(None, None),
            size=(dp(420), dp(200)),
            md_bg_color=(0.10, 0.11, 0.16, 1),
        )
        title = MDLabel(
            text=title_text,
            theme_text_color="Custom",
            text_color=(1, 1, 1, .96),
            bold=True,
            font_size="18sp",
            size_hint_y=None,
            height=dp(26),
        )
        btn_row = MDBoxLayout(spacing=dp(8), size_hint_y=None, height=dp(44))
        btn_cancel = MDButton(style="text", on_release=lambda *_: mv.dismiss())
        btn_cancel.add_widget(MDButtonText(text="Cancel"))
        btn_ok = MDButton(style="filled", on_release=lambda *_: on_confirm() or mv.dismiss())
        btn_ok.add_widget(MDButtonText(text="Save"))
        btn_row.add_widget(Widget())
        btn_row.add_widget(btn_cancel)
        btn_row.add_widget(btn_ok)

        card.add_widget(title)
        card.add_widget(field)
        card.add_widget(btn_row)

        mv = ModalView(size_hint=(1, 1), background_color=(0, 0, 0, 0.45), auto_dismiss=True)
        mv.add_widget(card)
        return mv

    def open_add_task(self):
        self.new_task_field = MDTextField(
            hint_text="Task title",
            mode="outlined",
            size_hint_y=None,
            height=dp(56),
        )
        mv = self._build_modal("Add Task", self.new_task_field, self._add_task_confirm)
        self._add_view = mv
        mv.open()

    def _add_task_confirm(self):
        title = (self.new_task_field.text or "").strip()
        if not title:
            self.notify("Enter a task title"); return
        self.tasks.append({"id": str(uuid4()), "title": title, "status": "todo"})
        self._rebuild_task_list()
        self.notify("Task added")

    def open_rename_task(self, task_id: str, current_title: str):
        self.rename_field = MDTextField(
            text=current_title,
            mode="outlined",
            size_hint_y=None,
            height=dp(56),
        )
        def _do():
            new_t = (self.rename_field.text or "").strip()
            if not new_t:
                self.notify("Title cannot be empty"); return
            for t in self.tasks:
                if t["id"] == task_id:
                    t["title"] = new_t
                    break
            self._rebuild_task_list()
            self.notify("Task updated")
        mv = self._build_modal("Rename Task", self.rename_field, _do)
        self._rename_view = mv
        mv.open()

    # ---- task ops called from TaskRow ----
    def update_task_status(self, task_id: str, status: str):
        for t in self.tasks:
            if t["id"] == task_id:
                t["status"] = status
                break
        self._animate_progress_to_current()

    def delete_task(self, task_id: str):
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        self._rebuild_task_list()
        self.notify("Task deleted")

    def _rebuild_task_list(self, *_):
        scr = self.sm.get_screen("admin")
        container: MDBoxLayout = scr.ids.get("task_list", None)
        if container is None:
            Clock.schedule_once(self._rebuild_task_list, 0.05)
            return

        container.clear_widgets()

        if not self.tasks:
            empty = MDCard(
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
            empty.add_widget(line)
            empty.opacity = 0
            Animation(opacity=1, d=.28).start(empty)
            container.add_widget(empty)
            self._animate_progress_to_current()
            return

        for t in self.tasks:
            row = TaskRow(task_id=t["id"], title=t["title"], status=t["status"], app_ref=self)
            row.opacity = 0
            container.add_widget(row)
            Animation(opacity=1, d=.18).start(row)

        self._animate_progress_to_current()

    # ---- progress math & UI ----
    def _calc_progress(self) -> float:
        n = len(self.tasks)
        if n == 0:
            return 0.0
        score = sum(self.STATUS_WEIGHTS[t["status"]] for t in self.tasks)
        return score / float(n)

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
            ring = scr.ids.get("progress_ring", None)
        except Exception:
            Clock.schedule_once(self._animate_progress_to_current, 0.05)
            return

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

    # ---- action stubs ----
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
