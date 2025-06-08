import tkinter as tk
from tkinter import ttk, messagebox

class HammingSimulator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hamming SEC-DED Simülatörü")
        self.geometry("600x400")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        # Bit uzunluğu seçimi
        frame_top = ttk.Frame(self)
        frame_top.pack(pady=10)
        ttk.Label(frame_top, text="Bit Uzunluğu:").pack(side=tk.LEFT, padx=5)
        self.bit_length = tk.IntVar(value=8)
        ttk.Combobox(frame_top, textvariable=self.bit_length, values=[8, 16, 32], width=5, state="readonly").pack(side=tk.LEFT)

        # Veri girişi
        frame_data = ttk.Frame(self)
        frame_data.pack(pady=10)
        ttk.Label(frame_data, text="Veri (binary):").pack(side=tk.LEFT, padx=5)
        self.data_entry = ttk.Entry(frame_data, width=40)
        self.data_entry.pack(side=tk.LEFT)

        # Butonlar
        frame_buttons = ttk.Frame(self)
        frame_buttons.pack(pady=10)
        ttk.Button(frame_buttons, text="Kodla", command=self.encode_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Belleğe Yaz", command=self.write_memory).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Bellekten Oku", command=self.read_memory).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Hata Ekle", command=self.add_error).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Düzelt", command=self.correct_error).pack(side=tk.LEFT, padx=5)

        # Sonuç alanı
        frame_result = ttk.Frame(self)
        frame_result.pack(pady=10, fill=tk.BOTH, expand=True)
        ttk.Label(frame_result, text="Sonuçlar:").pack(anchor=tk.W)
        self.result_text = tk.Text(frame_result, height=6, width=70, state=tk.DISABLED)
        self.result_text.pack()
        # Bit kutucukları için panel
        self.bits_frame = ttk.Frame(self)
        self.bits_frame.pack(pady=5)

    def show_bits(self, bits, error_index=None):
        # Önce eski kutucukları temizle
        for widget in self.bits_frame.winfo_children():
            widget.destroy()
        for i, bit in enumerate(bits):
            bg = "#ffcccc" if error_index is not None and i == error_index else "#e0e0e0"
            fg = "red" if error_index is not None and i == error_index else "black"
            lbl = tk.Label(self.bits_frame, text=bit, width=2, height=1, relief=tk.RIDGE, borderwidth=2, bg=bg, fg=fg, font=("Consolas", 14, "bold"))
            lbl.pack(side=tk.LEFT, padx=2)

    def show_result(self, text, bits=None, error_index=None):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state=tk.DISABLED)
        if bits:
            self.show_bits(bits, error_index)
        else:
            self.show_bits("")

    def encode_data(self):
        data = self.data_entry.get().strip()
        n = self.bit_length.get()
        if not all(c in '01' for c in data) or len(data) != n:
            messagebox.showerror("Hata", f"Lütfen {n} bitlik binary veri giriniz.")
            return
        hamming_code = self.hamming_encode(data)
        self.show_result(f"Girdi: {data}\nHamming Kodu: {hamming_code}", bits=hamming_code)
        self.encoded_data = hamming_code  # Belleğe yazmak için sakla

    def hamming_encode(self, data):
        # Hamming SEC-DED (genel amaçlı, parity bitleri ile)
        m = len(data)
        # Parity bit sayısını bul
        r = 0
        while (2 ** r) < (m + r + 1):
            r += 1
        n = m + r + 1  # +1 overall parity
        code = ['0'] * n
        j = 0
        # Data bitlerini parity olmayan yerlere yerleştir
        for i in range(1, n):
            if (i & (i - 1)) != 0:
                code[i] = data[j]
                j += 1
        # Parity bitlerini hesapla
        for i in range(r):
            idx = 2 ** i
            parity = 0
            for j in range(1, n):
                if j & idx:
                    parity ^= int(code[j])
            code[idx] = str(parity)
        # Overall parity (SEC-DED için)
        overall_parity = sum(int(bit) for bit in code[1:]) % 2
        code[0] = str(overall_parity)
        return ''.join(code)

    def write_memory(self):
        if not hasattr(self, 'encoded_data'):
            messagebox.showerror("Hata", "Önce veriyi kodlayınız.")
            return
        self.memory = self.encoded_data
        self.show_result(f"Belleğe yazıldı:\n{self.memory}", bits=self.memory)

    def read_memory(self):
        if not hasattr(self, 'memory'):
            messagebox.showerror("Hata", "Bellekte veri yok.")
            return
        self.show_result(f"Bellekten okunan veri:\n{self.memory}", bits=self.memory)

    def add_error(self):
        if not hasattr(self, 'memory'):
            messagebox.showerror("Hata", "Bellekte veri yok.")
            return
        code = list(self.memory)
        n = len(code)
        def apply_error():
            try:
                pos = int(pos_entry.get())
                if not (0 <= pos < n):
                    raise ValueError
            except ValueError:
                messagebox.showerror("Hata", f"Geçerli bir bit pozisyonu giriniz (0-{n-1})")
                return
            code[pos] = '1' if code[pos] == '0' else '0'
            self.memory = ''.join(code)
            self.show_result(f"{pos}. bit terslendi!\nYeni veri: {self.memory}", bits=self.memory, error_index=pos)
            error_win.destroy()
        error_win = tk.Toplevel(self)
        error_win.title("Hata Ekle")
        error_win.geometry("300x100")
        tk.Label(error_win, text=f"Hangi bit pozisyonunda hata oluşturulsun? (0-{n-1})").pack(pady=5)
        pos_entry = ttk.Entry(error_win, width=10)
        pos_entry.pack()
        ttk.Button(error_win, text="Hata Ekle", command=apply_error).pack(pady=5)

    def correct_error(self):
        if not hasattr(self, 'memory'):
            messagebox.showerror("Hata", "Bellekte veri yok.")
            return
        code = list(self.memory)
        n = len(code)
        r = 0
        while (2 ** r) < n:
            r += 1
        syndrome = 0
        for i in range(r):
            idx = 2 ** i
            parity = 0
            for j in range(1, n):
                if j & idx:
                    parity ^= int(code[j])
            if parity != int(code[idx]):
                syndrome += idx
        overall_parity = sum(int(bit) for bit in code[1:]) % 2
        if overall_parity != int(code[0]):
            overall_error = True
        else:
            overall_error = False
        result = f"Bellekteki veri: {''.join(code)}\nSendrom: {syndrome}"
        if syndrome == 0 and not overall_error:
            result += "\nHata yok."
            self.show_result(result, bits=code)
        elif syndrome != 0:
            result += f"\nHatalı bit pozisyonu: {syndrome}"
            code[syndrome] = '1' if code[syndrome] == '0' else '0'
            result += f"\nDüzeltilmiş veri: {''.join(code)}"
            self.memory = ''.join(code)
            self.show_result(result, bits=code, error_index=syndrome)
        elif syndrome == 0 and overall_error:
            result += "\nÇift hata tespit edildi (düzeltilemez)."
            self.show_result(result, bits=code)

if __name__ == "__main__":
    app = HammingSimulator()
    app.mainloop() 