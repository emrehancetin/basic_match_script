import random
import time
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path


def read_names(path: Path) -> list[str]:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    names = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

    if len(names) < 2:
        raise ValueError("The file must contain at least 2 non-empty lines (names).")

    if len(set(names)) != len(names):
        raise ValueError("Duplicate names detected. Please make all names unique.")

    return names


def make_pairs_even(names: list[str]) -> list[tuple[str, str]]:
    random.shuffle(names)
    pairs = []
    while names:
        a = names.pop()
        b = names.pop()
        pairs.append((a, b))
    return pairs


def make_assignments_odd(names: list[str]) -> list[tuple[str, str]]:
    # Find a derangement (no one matched to themselves)
    left = names[:]
    right = names[:]

    # For n >= 2 this usually finds a solution quickly
    while True:
        random.shuffle(right)
        if all(a != b for a, b in zip(left, right)):
            break

    return list(zip(left, right))


class MatchApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Random Matching Tool")
        self.geometry("820x520")
        self.minsize(780, 480)

        self.file_path_var = tk.StringVar(value="")
        self.delay_var = tk.DoubleVar(value=0.5)
        self.mode_var = tk.StringVar(value="auto")  # auto / pairs / assignments
        self.is_running = False

        self._build_ui()

    def _build_ui(self):
        # Top controls
        top = ttk.Frame(self, padding=12)
        top.pack(fill="x")

        ttk.Label(top, text="Names file:").grid(row=0, column=0, sticky="w")
        entry = ttk.Entry(top, textvariable=self.file_path_var, width=60)
        entry.grid(row=0, column=1, padx=8, sticky="we")

        browse_btn = ttk.Button(top, text="Browse...", command=self.browse_file)
        browse_btn.grid(row=0, column=2, sticky="e")

        ttk.Label(top, text="Mode:").grid(row=1, column=0, pady=(10, 0), sticky="w")
        mode = ttk.Combobox(
            top,
            textvariable=self.mode_var,
            values=["auto", "pairs", "assignments"],
            state="readonly",
            width=18,
        )
        mode.grid(row=1, column=1, pady=(10, 0), sticky="w")

        ttk.Label(top, text="Delay (sec):").grid(row=1, column=2, pady=(10, 0), sticky="e")
        delay_spin = ttk.Spinbox(top, from_=0.0, to=10.0, increment=0.1, textvariable=self.delay_var, width=8)
        delay_spin.grid(row=1, column=3, padx=(8, 0), pady=(10, 0), sticky="w")

        top.columnconfigure(1, weight=1)

        # Buttons
        btns = ttk.Frame(self, padding=(12, 0, 12, 12))
        btns.pack(fill="x")

        self.run_btn = ttk.Button(btns, text="Run", command=self.run)
        self.run_btn.pack(side="left")

        self.stop_btn = ttk.Button(btns, text="Stop", command=self.stop, state="disabled")
        self.stop_btn.pack(side="left", padx=8)

        ttk.Button(btns, text="Clear", command=self.clear_output).pack(side="left", padx=8)
        ttk.Button(btns, text="Save Results...", command=self.save_results).pack(side="left")

        # Output
        out_frame = ttk.Frame(self, padding=12)
        out_frame.pack(fill="both", expand=True)

        ttk.Label(out_frame, text="Output:").pack(anchor="w")

        self.output = tk.Text(out_frame, wrap="word", height=20)
        self.output.pack(fill="both", expand=True, pady=(6, 0))

        # Scrollbar
        scroll = ttk.Scrollbar(self.output, command=self.output.yview)
        self.output.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")

        # Hint
        self._append_line("Tip: Put one name per line. Use 'auto' mode to pair if even, assign if odd.")

    def browse_file(self):
        path = filedialog.askopenfilename(
            title="Select names file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if path:
            self.file_path_var.set(path)

    def clear_output(self):
        self.output.delete("1.0", "end")

    def save_results(self):
        content = self.output.get("1.0", "end").strip()
        if not content:
            messagebox.showinfo("No output", "There is nothing to save yet.")
            return

        path = filedialog.asksaveasfilename(
            title="Save results",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not path:
            return

        Path(path).write_text(content + "\n", encoding="utf-8")
        messagebox.showinfo("Saved", f"Results saved to:\n{path}")

    def stop(self):
        self.is_running = False
        self._append_line("\n[Stopped]\n")

    def run(self):
        if self.is_running:
            return

        file_path = self.file_path_var.get().strip()
        if not file_path:
            messagebox.showerror("Missing file", "Please select a names file first.")
            return

        try:
            names = read_names(Path(file_path))
        except Exception as e:
            messagebox.showerror("File error", str(e))
            return

        self.is_running = True
        self.run_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")

        # Run in background thread so UI doesn't freeze
        t = threading.Thread(target=self._run_logic, args=(names,), daemon=True)
        t.start()

    def _run_logic(self, names: list[str]):
        try:
            mode = self.mode_var.get()
            delay = float(self.delay_var.get())

            # Decide mode
            if mode == "auto":
                use_pairs = (len(names) % 2 == 0)
            elif mode == "pairs":
                if len(names) % 2 != 0:
                    raise ValueError("Pairs mode requires an even number of names.")
                use_pairs = True
            else:  # assignments
                use_pairs = False

            self._append_line("\n--- Running ---")
            self._append_line(f"Names: {len(names)} | Mode: {mode}")

            if use_pairs:
                results = make_pairs_even(names[:])
                for a, b in results:
                    if not self.is_running:
                        return
                    self._append_line(f"Selected match: {a} ↔ {b}")
                    time.sleep(delay)
            else:
                results = make_assignments_odd(names[:])
                for a, b in results:
                    if not self.is_running:
                        return
                    self._append_line(f"Match: {a} → {b}")
                    time.sleep(delay)

            self._append_line("--- Done ---\n")

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.is_running = False
            self.run_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")

    def _append_line(self, text: str):
        # Thread-safe UI update
        def _do():
            self.output.insert("end", text + "\n")
            self.output.see("end")
        self.after(0, _do)


if __name__ == "__main__":
    # Better default look on Windows
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    app = MatchApp()
    app.mainloop()
