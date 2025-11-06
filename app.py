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
from kivy.uix.modalview import ModalView  # <-- use ModalView instead of MDDialog

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
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
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.selectioncontrol import MDCheckbox


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
                            MDList:
                                id: task_list

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
    # use ModalView instead of MDDialog for max compatibility
    _add_view: ModalView | None = None
    new_task_field: MDTextField | None = None

    # task model: {"title": str, "status": "todo"|"almost"|"done"}
    tasks = ListProperty([])

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
        self.sm = ScreenManager(transition=FadeTransition(duration=0.32))
        self.sm.add_widget(LoginScreen())
        self.sm.add_widget(AdminScreen())
        return self.sm

    # --- helpers ---
    def notify(self, text: str):
        try:
            MDSnackbar(MDSnackbarText(text=text), duration=1.6).open()
        except Exception as e:
            print(f"[Snackbar] {text} ({e})")

    def forgot_password(self):
        self.notify("Ask IT Helpdesk to reset password")

    # --- login ---
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

    # --- profile menu ---
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

    # --- admin build ---
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
            tile = self._action_tile(icon, label, fn)
            tile.opacity = 0
            grid.add_widget(tile)
            Animation(opacity=1, d=0.26, t="out_cubic").start(tile)

        self._refresh_progress_labels()
        Clock.schedule_once(lambda *_: self._rebuild_task_list(), 0.05)

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

        def _press(*_):
            Animation(md_bg_color=(1, 1, 1, 0.10), elevation=2, d=.10).start(tile)

        def _release(*_):
            Animation(md_bg_color=(1, 1, 1, 0.06), elevation=0, d=.18).start(tile)
            callback()

        box = MDBoxLayout(orientation="vertical", spacing=dp(10))
        ic = MDIcon(icon=icon_name, theme_text_color="Custom", text_color=(.85, .89, 1, 1))
        ic.font_size = "40sp"
        lbl = MDLabel(text=label, theme_text_color="Custom", text_color=(1, 1, 1, .96),
                      halign="center", font_size="15sp")
        box.add_widget(ic); box.add_widget(lbl)
        tile.add_widget(box)
        tile.bind(on_press=_press, on_release=_release)
        return tile

    # --- lightweight "dialog" built with ModalView ---
    def open_add_task(self):
        if self._add_view:
            try:
                self._add_view.dismiss()
            except Exception:
                pass
            self._add_view = None

        self.new_task_field = MDTextField(
            hint_text="Task title",
            mode="outlined",
            size_hint_y=None,
            height=dp(56),
        )

        # Build the modal content
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
            text="Add Task",
            theme_text_color="Custom",
            text_color=(1, 1, 1, .96),
            bold=True,
            font_size="18sp",
            size_hint_y=None,
            height=dp(26),
        )
        btn_row = MDBoxLayout(spacing=dp(8), size_hint_y=None, height=dp(44))
        btn_cancel = MDButton(style="text", on_release=lambda *_: self._dismiss_add_view())
        btn_cancel.add_widget(MDButtonText(text="Cancel"))
        btn_add = MDButton(style="filled", on_release=lambda *_: self._add_task_confirm())
        btn_add.add_widget(MDButtonText(text="Add"))
        btn_row.add_widget(Widget())
        btn_row.add_widget(btn_cancel)
        btn_row.add_widget(btn_add)

        card.add_widget(title)
        card.add_widget(self.new_task_field)
        card.add_widget(btn_row)

        mv = ModalView(size_hint=(1, 1), background_color=(0, 0, 0, 0.45), auto_dismiss=True)
        mv.add_widget(card)
        self._add_view = mv
        mv.open()

    def _dismiss_add_view(self):
        if self._add_view:
            try:
                self._add_view.dismiss()
            finally:
                self._add_view = None

    def _add_task_confirm(self):
        title = (self.new_task_field.text or "").strip()
        if not title:
            self.notify("Enter a task title"); return
        self.tasks.append({"title": title, "status": "todo"})
        self._rebuild_task_list()
        self._dismiss_add_view()
        self.notify("Task added")

    # --- task helpers ---
    def _status_icon(self, status: str) -> str:
        return {
            "todo": "checkbox-blank-circle-outline",
            "almost": "progress-check",
            "done": "check-circle",
        }.get(status, "checkbox-blank-circle-outline")

    def _status_color(self, status: str):
        return {
            "todo": (.70, .76, .95, 1),
            "almost": (1.00, .86, .45, 1),
            "done": (.54, .90, .62, 1),
        }[status]

    def _status_weight(self, status: str) -> float:
        return {"todo": 0.0, "almost": 0.5, "done": 1.0}[status]

    def _cycle_status(self, idx: int):
        order = ["todo", "almost", "done"]
        cur = self.tasks[idx]["status"]
        nxt = order[(order.index(cur) + 1) % len(order)]
        self.tasks[idx]["status"] = nxt
        self._rebuild_task_list()
        self.notify(f"Task marked {nxt.replace('almost','almost done')}")

    def _remove_task(self, idx: int):
        if 0 <= idx < len(self.tasks):
            title = self.tasks[idx]["title"]
            self.tasks.pop(idx)
            self._rebuild_task_list()
            self.notify(f"Removed: {title}")

    def _rebuild_task_list(self, *_):
        scr = self.sm.get_screen("admin")
        lst = scr.ids.get("task_list", None)
        if lst is None:
            Clock.schedule_once(self._rebuild_task_list, 0.05)
            return

        lst.clear_widgets()

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
            row_card.opacity = 0
            Animation(opacity=1, d=.28).start(row_card)
            lst.add_widget(row_card)

            Clock.schedule_once(self._animate_progress_to_current, 0.05)
            return

        for idx, task in enumerate(self.tasks):
            item = MDListItem()
            lead = MDListItemLeadingIcon(
                icon=self._status_icon(task["status"]),
                theme_text_color="Custom",
                text_color=self._status_color(task["status"]),
            )
            lead.bind(on_release=lambda _btn, _idx=idx: self._cycle_status(_idx))
            item.add_widget(lead)

            item.add_widget(MDListItemHeadlineText(text=task["title"]))

            trash = MDListItemTrailingIcon(
                icon="trash-can-outline",
                theme_text_color="Custom",
                text_color=(1,1,1,.80),
                on_release=lambda _btn, _idx=idx: self._remove_task(_idx),
            )
            item.add_widget(trash)

            item.opacity = 0
            lst.add_widget(item)
            Animation(opacity=1, d=.20).start(item)

        Clock.schedule_once(self._animate_progress_to_current, 0.05)

    # --- progress math & UI ---
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

    # --- entrance choreography ---
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

    # --- live clock ---
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

    # --- action stubs ---
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
