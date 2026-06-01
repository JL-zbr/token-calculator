import tkinter as tk
from tkinter import ttk, scrolledtext
import tiktoken

MODELS = {
    "DeepSeek V4 Flash":  {"enc": "o200k_base", "in": 1/1e6, "out": 2/1e6},
    "DeepSeek V4 Pro 优惠价": {"enc": "o200k_base", "in": 3/1e6, "out": 6/1e6},
    "DeepSeek V4 Pro 原价":  {"enc": "o200k_base", "in": 12/1e6, "out": 24/1e6},
    "DeepSeek V3/R1":     {"enc": "o200k_base", "in": 2/1e6, "out": 8/1e6},
    "DeepSeek V2":        {"enc": "cl100k_base", "in": 1/1e6, "out": 2/1e6},
    "GPT-4o":             {"enc": "o200k_base", "in": 2.5/1e6, "out": 10/1e6},
    "GPT-4o-mini":        {"enc": "o200k_base", "in": 0.15/1e6, "out": 0.6/1e6},
    "Claude 3.5 Sonnet":  {"enc": "cl100k_base", "in": 3/1e6, "out": 15/1e6},
}

class TokenCounter:
    def __init__(self, root):
        self.root = root
        root.title("Token 计算器")
        root.geometry("520x520")
        root.resizable(False, False)
        root.configure(bg="#f0f0f0")

        tk.Label(root, text="输入文本：", font=("Microsoft YaHei", 10), bg="#f0f0f0").pack(anchor="w", padx=10, pady=(10,0))
        self.text = scrolledtext.ScrolledText(root, height=10, font=("Microsoft YaHei", 10), wrap="word", relief="solid", borderwidth=1)
        self.text.pack(padx=10, pady=5, fill="both", expand=True)

        frame = tk.Frame(root, bg="#f0f0f0")
        frame.pack(pady=5)
        tk.Label(frame, text="模型：", font=("Microsoft YaHei", 10), bg="#f0f0f0").pack(side="left")
        self.model_var = tk.StringVar(value="DeepSeek V3/R1")
        self.model_menu = ttk.Combobox(frame, textvariable=self.model_var, values=list(MODELS.keys()), state="readonly", width=18, font=("Microsoft YaHei", 9))
        self.model_menu.pack(side="left", padx=5)

        self.btn = tk.Button(frame, text="计算 Token", command=self.calc, bg="#4a90d9", fg="white", font=("Microsoft YaHei", 10), padx=15, pady=3, relief="flat", cursor="hand2")
        self.btn.pack(side="left", padx=10)

        self.result = tk.Text(root, height=7, font=("Microsoft YaHei", 10), state="disabled", relief="solid", borderwidth=1, bg="white")
        self.result.pack(padx=10, pady=5, fill="x")

        tk.Label(root, text="提示：粘贴文本后点「计算 Token」即可  |  Ctrl+Enter 快速计算", font=("Microsoft YaHei", 8), fg="gray", bg="#f0f0f0").pack()
        root.bind("<Control-Return>", lambda e: self.calc())

    def calc(self):
        text = self.text.get("1.0", "end-1c")
        if not text.strip():
            self._show("⚠️ 请先输入文本")
            return
        model = MODELS[self.model_var.get()]
        enc = tiktoken.get_encoding(model["enc"])
        tokens = len(enc.encode(text))
        chars = len(text)
        in_cost = tokens * model["in"]
        out_cost = tokens * model["out"]
        total = in_cost + out_cost
        self._show(f"""📊 Token 统计
━━━━━━━━━━━━━━━━━━
字符数    : {chars:,}
Token数   : {tokens:,}

💰 费用估算（{self.model_var.get()}）
━━━━━━━━━━━━━━━━━━
输入: ¥{in_cost:.6f}
输出: ¥{out_cost:.6f}（按同量估）
合计: ¥{total:.6f}

💡 约 {int(1/total) if total>0 else 0} 次/元
""")

    def _show(self, msg):
        self.result.configure(state="normal")
        self.result.delete("1.0", "end")
        self.result.insert("1.0", msg)
        self.result.configure(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    TokenCounter(root)
    root.mainloop()
