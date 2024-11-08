import os
import threading
from PIL import Image
import tkinter as tk
import customtkinter as ctk

from common import *


class App(ctk.CTk):
    def __init__(self):

        super().__init__()

        self.checked = False

        # init window
        self.title("Desk-Emoji  v1.0.0")
        self.window_width = 700
        self.window_height = 450
        self.geometry(f"{self.window_width}x{self.window_height}")
        self.resizable(False, False)
        self.center_window()

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        icon_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "icons")
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(icon_path, "main_icon.png")), size=(26, 26))
        self.home_image = ctk.CTkImage(light_image=Image.open(os.path.join(icon_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(icon_path, "home_light.png")), size=(20, 20))
        self.api_icon = ctk.CTkImage(light_image=Image.open(os.path.join(icon_path, "api_dark.png")),
                                                 dark_image=Image.open(os.path.join(icon_path, "api_light.png")), size=(20, 20))
        self.usb_icon = ctk.CTkImage(light_image=Image.open(os.path.join(icon_path, "usb_dark.png")),
                                                     dark_image=Image.open(os.path.join(icon_path, "usb_light.png")), size=(20, 20))
        self.help_icon = ctk.CTkImage(light_image=Image.open(os.path.join(icon_path, "help_dark.png")),
                                                     dark_image=Image.open(os.path.join(icon_path, "help_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="  Desk-Emoji", image=self.logo_image,
                                                             compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="主页",
                                         fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                         image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.api_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="API",
                                        fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                        image=self.api_icon, anchor="w", command=self.api_button_event)
        self.api_button.grid(row=2, column=0, sticky="ew")

        self.usb_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="串口",
                                        fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                        image=self.usb_icon, anchor="w", command=self.usb_button_event)
        self.usb_button.grid(row=3, column=0, sticky="ew")

        self.help_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="帮助",
                                         fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                         image=self.help_icon, anchor="w", command=self.help_button_event)
        self.help_button.grid(row=4, column=0, sticky="ew")

        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=["System", "Light", "Dark"],
                                                      command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid_columnconfigure(1, weight=1)
        self.home_frame.grid_columnconfigure(2, weight=1)

        self.textbox = ctk.CTkTextbox(self.home_frame, height=300)
        self.textbox.grid(row=0, column=0, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.chat_msg = ctk.CTkEntry(self.home_frame)
        self.chat_msg.grid(row=1, column=0, columnspan=3, padx=20, pady=0, sticky="nsew")
        self.chat_msg.bind("<Return>", self.chat_msg_event)

        self.speaker_switch = ctk.CTkSwitch(self.home_frame, text="扬声器")
        self.speaker_switch.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        self.speaker_switch.select()

        self.speech_bar = ctk.CTkProgressBar(self.home_frame)
        self.speech_bar.grid(row=2, column=1, padx=20, pady=20, sticky="e")
        self.speech_bar.configure(mode="indeterminate")

        self.speech_button = ctk.CTkButton(self.home_frame, text="说话", height=40,
                                           command=self.speech_button_event)
        self.speech_button.grid(row=2, column=2, padx=20, pady=20, sticky='e')
        self.original_button_color = ctk.ThemeManager.theme["CTkButton"]["fg_color"]

        # create usb frame
        self.usb_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.usb_frame.grid_columnconfigure(0, weight=1)

        self.usb_combobox = ctk.CTkComboBox(self.usb_frame, values=cmd.list_ports())
        self.usb_combobox.grid(row=0, column=0, padx=20, pady=40, sticky="nsew")
        
        self.usb_connect_button = ctk.CTkButton(self.usb_frame, text="连接", command=self.usb_connect_button_event)
        self.usb_connect_button.grid(row=0, column=1, padx=20, pady=10)

        self.usb_flag_label = ctk.CTkLabel(self.usb_frame, text="")
        self.usb_flag_label.grid(row=1, column=1, padx=20, pady=20)

        # create api frame
        self.api_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.api_frame.grid_columnconfigure(0, weight=1)
        self.api_frame.grid_columnconfigure(1, weight=6)

        self.api_url_label = ctk.CTkLabel(self.api_frame, text="API URL: ")
        self.api_url_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        self.api_url = ctk.CTkEntry(self.api_frame)
        self.api_url.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.api_key_label = ctk.CTkLabel(self.api_frame, text="API Key: ")
        self.api_key_label.grid(row=1, column=0, padx=20, pady=20, sticky="w")
        self.api_key = ctk.CTkEntry(self.api_frame)
        self.api_key.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

        self.save_flag_label = ctk.CTkLabel(self.api_frame, text="")
        self.save_flag_label.grid(row=2, column=0, padx=20, pady=20)

        self.api_save_button = ctk.CTkButton(self.api_frame, text="连接", command=self.api_save_button_event)
        self.api_save_button.grid(row=2, column=1, padx=20, pady=10)

        # create help frame
        self.help_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.help_frame.grid_columnconfigure(0, weight=1)

        help_text = """
Desk-Emoji 桌面陪伴机器人

初次配置：
1. 点击“API” -> 配置 OpenAI API 网址和 Key（支持中转）
2. 连接机器人，点击“串口” -> 下拉菜单选择串口 -> 点击“连接”


杭州易问科技版权所有 2024.11.7
邮箱：mark.yang@ewen.ltd
"""
        self.help_text_lable = ctk.CTkLabel(self.help_frame, text=help_text, anchor="w", justify="left", wraplength=380)
        self.help_text_lable.grid(row=0, column=0, padx=20, pady=20)

        self.select_frame_by_name("usb")

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (self.window_width // 2)
        y = (screen_height // 2) - (self.window_height // 2)
        self.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

    def load_api_key(self):
        try:
            url, key = chatgpt.read_json()
            if not self.api_url.get():
                self.api_url.insert(0, url)
            if not self.api_key.get():
                self.api_key.insert(0, key)
        except Exception:
            pass

    def save_api_key(self):
        data = {
            'api_url': self.api_url.get(),
            'api_key': self.api_key.get()
        }
        chatgpt.write_json(data)
        logger.info(f"Saved API Key to {chatgpt.json_path}")

    def print_textbox(self, text):
        self.textbox.insert(tk.END, f"{text}\n")
        self.textbox.see(tk.END)

    def update_usb_port_list(self):
        self.usb_combobox.configure(values=cmd.list_ports())

    def select_frame_by_name(self, name):
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.api_button.configure(fg_color=("gray75", "gray25") if name == "usb" else "transparent")
        self.api_button.configure(fg_color=("gray75", "gray25") if name == "api" else "transparent")
        self.help_button.configure(fg_color=("gray75", "gray25") if name == "help" else "transparent")

        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "usb":
            self.usb_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.usb_frame.grid_forget()
        if name == "api":
            self.api_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.api_frame.grid_forget()
        if name == "help":
            self.help_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.help_frame.grid_forget()

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

    def home_button_event(self):
        self.select_frame_by_name("home")
        if not self.checked:
            self.check_all_connections()
            self.checked = True

    def usb_button_event(self):
        self.update_usb_port_list()
        self.select_frame_by_name("usb")
        self.usb_flag_label.configure(text="", fg_color="transparent")

    def usb_connect_button_event(self):
        port = self.usb_combobox.get()
        if cmd.connect(port):
            self.usb_flag_label.configure(text="连接成功", text_color="green")
        else:
            self.usb_flag_label.configure(text="连接失败", text_color="red")

    def api_button_event(self):
        self.select_frame_by_name("api")
        self.save_flag_label.configure(text="", fg_color="transparent")
        self.load_api_key()

    def api_save_button_event(self):
        self.save_api_key()
        if chatgpt.connect():
            self.save_flag_label.configure(text="连接成功", text_color="green")
        else:
            self.save_flag_label.configure(text="连接失败", text_color="red")

    def help_button_event(self):
        self.select_frame_by_name("help")

    def __chat_LLM(self, question):
            self.print_textbox(f"You:\t{question}")
            answer, emotion = chat(question)
            self.print_textbox(f"Bot:\t{answer}")
            self.print_textbox(f"Emo:\t{emotion}\n")
            if bool(self.speaker_switch.get()):
                speaker.say(answer)
            threading.Thread(target=act_emotion, args=(emotion,)).start()

    def chat_msg_event(self, event):
        question = self.chat_msg.get()
        if question:
            self.chat_msg.delete(0, tk.END)
            threading.Thread(target=self.__chat_LLM, args=(question,)).start()

    def speech_button_event(self):
        self.speech_bar.start()
        threading.Thread(target=self.__process_speech).start()

    def __process_speech(self):
        question = listener.hear()
        self.__chat_LLM(question)
        self.speech_bar.stop()

    def check_all_connections(self):
        success = True
        self.print_textbox("API 连接中...")
        if chatgpt.connect():
            self.print_textbox("API 连接成功")
        else:
            success = False
            self.print_textbox("[错误] API 连接失败，请检查 API 配置")

        self.print_textbox("串口连接中...")
        port = self.usb_combobox.get()
        if cmd.connect(port):
            self.print_textbox(f"串口 {port} 连接成功")
        else:
            success = False
            self.print_textbox(f"[错误] 串口 {port} 连接失败，请检查串口配置")
        if success:
            self.print_textbox("初始化成功\n")
        else:
            self.print_textbox("初始化失败 :(\n")


if __name__ == "__main__":
    app = App()
    app.mainloop()
