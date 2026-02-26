import tkinter as tk
from tkinter import ttk, scrolledtext
import customtkinter as ctk

class PasteBlockerTestApp:
    def __init__(self):
        # 初始化CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("粘贴阻止测试软件")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        self.setup_ui()
    
    def setup_ui(self):
        # 主框架
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)








































































        # 标题
        title_label = ctk.CTkLabel(main_frame, text="粘贴阻止测试软件", 
                                  font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=(10, 20))
        
        # 说明文本
        instruction_text = """本软件用于测试粘贴阻止功能：
• 下方的文本框已禁用粘贴功能
• 只能通过逐字符输入方式输入文本
• 支持中英文输入
• 可以正常复制内容"""
        
        instruction_label = ctk.CTkLabel(main_frame, text=instruction_text, 
                                       font=ctk.CTkFont(size=12),
                                       justify="left")
        instruction_label.pack(pady=(0, 20))
        
        # 测试文本框框架
        text_frame = ctk.CTkFrame(main_frame)
        text_frame.pack(fill="both", expand=True, padx=10, pady=(0, 20))
        
        # 文本框标题
        ctk.CTkLabel(text_frame, text="测试文本框 (粘贴已禁用):", 
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        # 创建禁用粘贴的文本框
        self.test_textbox = DisabledPasteTextWidget(text_frame)
        self.test_textbox.pack(padx=10, pady=(0, 10), fill="both", expand=True)
        
        # 控制按钮框架
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # 清空按钮
        clear_button = ctk.CTkButton(button_frame, text="清空文本", 
                                   command=self.clear_text,
                                   width=100, height=30)
        clear_button.pack(side="left", padx=(0, 10))
        
        # 获取文本按钮
        get_text_button = ctk.CTkButton(button_frame, text="获取文本", 
                                      command=self.get_text,
                                      width=100, height=30)
        get_text_button.pack(side="left", padx=(0, 10))
        
        # 状态标签
        self.status_label = ctk.CTkLabel(main_frame, text="就绪 - 可以开始测试", 
                                       text_color="gray")
        self.status_label.pack(pady=(0, 10))
        
        # 快捷键提示
        shortcut_label = ctk.CTkLabel(main_frame, 
                                    text="快捷键: Ctrl+C 复制 | Ctrl+A 全选 | Delete 删除",
                                    font=ctk.CTkFont(size=10),
                                    text_color="gray")
        shortcut_label.pack()
    
    def clear_text(self):
        """清空文本框内容"""
        self.test_textbox.delete("1.0", "end")
        self.status_label.configure(text="文本已清空")
    
    def get_text(self):
        """获取并显示文本框内容"""
        content = self.test_textbox.get("1.0", "end-1c")
        if content:
            print(f"文本框内容: {repr(content)}")
            self.status_label.configure(text=f"获取到 {len(content)} 个字符")
        else:
            self.status_label.configure(text="文本框为空")

class DisabledPasteTextWidget(ctk.CTkTextbox):
    """禁用粘贴功能的文本框"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.setup_bindings()
    
    def setup_bindings(self):
        """设置键盘绑定以禁用粘贴"""
        # 禁用Ctrl+V粘贴
        self.bind("<Control-v>", self.block_paste)
        self.bind("<Control-V>", self.block_paste)
        
        # 禁用Shift+Insert粘贴
        self.bind("<Shift-Insert>", self.block_paste)
        
        # 禁用右键菜单中的粘贴
        self.bind("<Button-3>", self.block_right_click)
        
        # 允许其他正常的编辑操作
        # Ctrl+C 复制 - 保持默认行为
        # Ctrl+X 剪切 - 保持默认行为
        # Ctrl+A 全选 - 保持默认行为
        # Delete 删除 - 保持默认行为
        
        # 可以添加自定义的输入监控
        self.bind("<Key>", self.on_key_press)
    
    def block_paste(self, event=None):
        """阻止粘贴操作"""
        print("粘贴操作已被阻止")
        return "break"  # 阻止事件继续传播
    
    def block_right_click(self, event=None):
        """阻止右键菜单显示"""
        print("右键菜单已被阻止")
        return "break"
    
    def on_key_press(self, event):
        """监控按键输入"""
        # 记录输入的字符（用于调试）
        char = event.char
        if char and char.isprintable():
            print(f"输入字符: {repr(char)}")
        elif event.keysym in ['BackSpace', 'Delete', 'Return']:
            print(f"编辑操作: {event.keysym}")
        
        # 允许正常处理
        return None

def main():
    app = PasteBlockerTestApp()
    app.root.mainloop()

if __name__ == "__main__":
    main()