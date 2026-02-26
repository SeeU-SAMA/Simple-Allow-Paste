import tkinter as tk
import time
import ctypes
import threading
import random
import customtkinter as ctk

user32 = ctypes.windll.user32


class SimpleAllowPaste:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Simple-Allow-Paste v1.1 LTS")
        self.root.geometry("400x500")
        self.root.minsize(200, 200)
        self.root.attributes("-topmost", True)

        self.delay = 0.05
        self.input_mode = "整段输入"
        self.is_random_enabled = tk.BooleanVar(value=True)
        self.settings_window = None
        self.stop_event = threading.Event()
        self.default_text = "就绪 | 使用Q键终止输入"

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.setup_ui()
        threading.Thread(target=self.keyboard_watcher, daemon=True).start()

    def setup_ui(self):
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(3, weight=1)

        # 工具栏
        toolbar = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        toolbar.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        self.settings_btn = ctk.CTkButton(toolbar, text="⚙️ 设置", command=self.open_unified_settings, width=70)
        self.settings_btn.pack(side="left")
        self.title_label = ctk.CTkLabel(toolbar, text="Simple-Allow-Paste", font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.pack(side="right", padx=5)

        # 模式切换
        mode_frame = ctk.CTkFrame(self.main_frame)
        mode_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(10, 0))
        self.mode_selector = ctk.CTkSegmentedButton(mode_frame, values=["整段输入", "逐字输入"],
                                                    command=self.mode_changed)
        self.mode_selector.set("整段输入")
        self.mode_selector.pack(side="left", padx=10, pady=10, fill="x", expand=True)

        self.mode_desc = ctk.CTkLabel(self.main_frame, text="采用消息灌送，不占剪贴板，稳定不丢字", font=("", 11),
                                      text_color="gray")
        self.mode_desc.grid(row=2, column=0, sticky="w", padx=20, pady=(2, 10))

        # 文本框
        self.text_box = ctk.CTkTextbox(self.main_frame, font=("Consolas", 13), border_width=2)
        self.text_box.grid(row=3, column=0, padx=10, pady=(5, 0), sticky="nsew")
        self.text_box.bind("<KeyRelease>", self.update_char_count)

        self.count_label = ctk.CTkLabel(self.main_frame, text="0 字", font=("", 11), text_color=("black", "white"))
        self.count_label.grid(row=4, column=0, sticky="w", padx=15, pady=2)

        # 按钮
        btn_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_container.grid(row=5, column=0, pady=10)
        self.start_btn = ctk.CTkButton(btn_container, text="开始输入", command=self.start_typing, width=160, height=45)
        self.start_btn.pack(side="left", padx=10)
        self.clear_btn = ctk.CTkButton(btn_container, text="清空", command=self.clear_all, border_width=2,
                                       border_color=("#E74C3C", "#C0392B"), text_color=("#E74C3C", "#E74C3C"),
                                       fg_color="transparent", width=80, height=45)
        self.clear_btn.pack(side="left", padx=10)

        self.status_bar = ctk.CTkLabel(self.main_frame, text=self.default_text, text_color="gray")
        self.status_bar.grid(row=6, column=0, pady=(0, 5))

    def mode_changed(self, value):
        self.input_mode = value
        desc = "采用消息灌送，不占剪贴板，稳定不丢字" if value == "整段输入" else "模拟真实打字，支持随机延迟波动"
        self.mode_desc.configure(text=desc)

    def update_char_count(self, event=None):
        count = len(self.text_box.get("1.0", "end-1c"))
        self.count_label.configure(text=f"{count} 字")

    def clear_all(self):
        self.text_box.delete("1.0", "end")
        self.update_char_count()

    def start_typing(self):
        text = self.text_box.get("1.0", tk.END).rstrip("\n")
        if not text:
            self.status_bar.configure(text="我做了非空检测，就先不发了哈", text_color="white")
            self.root.after(1500, lambda: self.status_bar.configure(text=self.default_text, text_color="gray"))
            return

        self.stop_event.clear()
        self.set_ui_lock(True)
        self.status_bar.configure(text="2秒内切换窗口...", text_color="#E67E22")
        threading.Thread(target=self._background_send, args=(text,), daemon=True).start()

    def _background_send(self, text):
        time.sleep(2)
        chunk_reset = 0
        hwnd = user32.GetForegroundWindow()

        # 决定使用哪种延迟逻辑
        is_burst = (self.input_mode == "整段输入")

        for ch in text:
            if self.stop_event.is_set():
                break

            if ch == '\n':
                # 回车
                user32.PostMessageW(hwnd, 0x0100, 0x0D, 0)
                time.sleep(0.001)
                user32.PostMessageW(hwnd, 0x0101, 0x0D, 0)
                time.sleep(0.001)
            else:
                user32.PostMessageW(hwnd, 0x0102, ord(ch), 0)

            # 延迟逻辑
            if is_burst:
                chunk_delay = 0.001 if 10 >= chunk_reset >= 2 else 0
                chunk_reset += -10 if chunk_reset == 10 else 1
                time.sleep(chunk_delay)
            else:
                actual_delay = random.uniform(self.delay * 0.8,
                                              self.delay * 1.2) if self.is_random_enabled.get() else self.delay
                time.sleep(actual_delay)

        self.root.after(0, self.finish_typing)

    def finish_typing(self):
        was_stopped = self.stop_event.is_set()
        self.set_ui_lock(False)
        if was_stopped:
            self.status_bar.configure(text="× 已手动终止", text_color="#E74C3C")
        else:
            self.status_bar.configure(text="√ 发送完毕", text_color="#2ECC71")

    def open_unified_settings(self):
        if self.settings_window is not None and self.settings_window.winfo_exists():
            self.settings_window.focus_force()
            return
        self.settings_window = ctk.CTkToplevel(self.root)
        self.settings_window.title("设置")
        sw, sh = 400, 480
        px, py = self.root.winfo_x(), self.root.winfo_y()
        pw, ph = self.root.winfo_width(), self.root.winfo_height()
        self.settings_window.geometry(f"{sw}x{sh}+{px + (pw - sw) // 2}+{py + (ph - sh) // 2}")
        self.settings_window.attributes("-topmost", True)
        self.settings_window.grab_set()

        ctk.CTkLabel(self.settings_window, text="逐字输入延迟 (ms):", font=("", 13, "bold")).pack(pady=(20, 5))
        sync_frame = ctk.CTkFrame(self.settings_window, fg_color="transparent")
        sync_frame.pack(pady=5)

        delay_entry = ctk.CTkEntry(sync_frame, width=60)
        delay_entry.insert(0, str(int(self.delay * 1000)))
        delay_entry.pack(side="left", padx=5)

        d_slider = ctk.CTkSlider(self.settings_window, from_=1, to=1000,
                                 command=lambda v: [delay_entry.delete(0, "end"), delay_entry.insert(0, str(int(v)))])
        d_slider.set(self.delay * 1000)
        d_slider.pack(padx=30, pady=10)

        delay_entry.bind("<KeyRelease>",
                         lambda e: [d_slider.set(int(delay_entry.get())) if delay_entry.get().isdigit() else None])
        ctk.CTkLabel(self.settings_window, text="随机延迟模拟:", font=("", 13, "bold")).pack(pady=(20, 5))
        ctk.CTkSwitch(self.settings_window, text="启用波动", variable=self.is_random_enabled).pack()

        info_frame = ctk.CTkFrame(self.settings_window, fg_color="transparent", border_width=1)
        info_frame.pack(fill="x", padx=30, pady=25)
        ctk.CTkLabel(info_frame, text="作者：SeeU_SAMA\n版本：v1.1 LTS\n新年快乐！🧧", font=("", 11)).pack(pady=10)

        def save():
            self.delay = d_slider.get() / 1000.0
            self.settings_window.destroy()

        ctk.CTkButton(self.settings_window, text="保存", command=save, width=120).pack(pady=10)

    def set_ui_lock(self, locked):
        state = "disabled" if locked else "normal"
        self.start_btn.configure(state=state)
        self.clear_btn.configure(state=state)
        self.settings_btn.configure(state=state)
        self.mode_selector.configure(state=state)
        self.text_box.configure(state=state)
        if not locked: self.start_btn.configure(text="开始输入")

    def keyboard_watcher(self):
        while True:
            if user32.GetAsyncKeyState(ord('Q')) & 0x8000:
                self.stop_event.set()
            time.sleep(0.05)


if __name__ == "__main__":
    app = SimpleAllowPaste()
    app.root.mainloop()