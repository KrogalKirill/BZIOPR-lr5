"""Модуль графического интерфейса пользователя (GUI) на CustomTkinter."""

import threading
import customtkinter as ctk
from src.models import VariantConfig
from src.lfsr import LFSR32Generator
from src.optimizer import MonteCarloOptimizer


class MonteCarloApp(ctk.CTk):
    """Главное окно приложения СППР."""

    def __init__(self):
        super().__init__()

        self.title("СППР: Метод Монте-Карло (Вариант 6 — Резисторы)")
        self.geometry("980x740")
        self.minsize(880, 600)
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self._build_ui()

    def _build_ui(self):
        # 1. Заголовок
        self.header_label = ctk.CTkLabel(
            self,
            text="Принятие решений на основе метода Монте-Карло (LFSR №15)",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.header_label.pack(pady=(16, 10), padx=16, anchor="w")

        # 2. Панель параметров
        self.params_frame = ctk.CTkFrame(self, corner_radius=10)
        self.params_frame.pack(fill="x", padx=16, pady=6)

        # Сетка параметров: (лейбл, значение по умолчанию)
        param_defs = [
            ("Брак (A), %:", "15"),
            ("Контроль (B), руб.:", "7"),
            ("Подгонка (C), руб.:", "50"),
            ("Замена (D), руб.:", "125"),
            ("Партия (N), шт.:", "10000"),
        ]

        self.entries = {}
        for idx, (label_text, def_val) in enumerate(param_defs):
            container = ctk.CTkFrame(self.params_frame, fg_color="transparent")
            container.grid(row=0, column=idx, padx=6, pady=10, sticky="ew")
            self.params_frame.grid_columnconfigure(idx, weight=1)

            lbl = ctk.CTkLabel(container, text=label_text, font=ctk.CTkFont(size=11, weight="bold"))
            lbl.pack(anchor="w")

            ent = ctk.CTkEntry(container, height=28)
            ent.insert(0, def_val)
            ent.pack(fill="x", pady=(2, 0))
            self.entries[label_text] = ent

        self.btn_run = ctk.CTkButton(
            self.params_frame,
            text="Рассчитать",
            command=self._start_simulation_thread,
            font=ctk.CTkFont(weight="bold"),
            width=110,
            height=32
        )
        self.btn_run.grid(row=0, column=len(param_defs), padx=(8, 12), pady=10)

        # 3. Таблица результатов (прокручиваемый фрейм)
        self.table_container = ctk.CTkScrollableFrame(self, corner_radius=10)
        self.table_container.pack(fill="both", expand=True, padx=16, pady=10)

        self._build_table_headers()

        # 4. Итоговая карточка
        self.summary_frame = ctk.CTkFrame(self, fg_color=("#1E293B", "#0F172A"), corner_radius=10)
        self.summary_frame.pack(fill="x", padx=16, pady=(0, 16))

        self.lbl_summary = ctk.CTkLabel(
            self.summary_frame,
            text="Нажмите «Рассчитать» для проведения имитационного эксперимента.",
            font=ctk.CTkFont(size=13),
            text_color="white",
            justify="left"
        )
        self.lbl_summary.pack(padx=16, pady=12, anchor="w")

    def _build_table_headers(self):
        headers = [
            "Контроль (%)",
            "Затраты (Монте-Карло), руб.",
            "Мат. ожидание (Теория), руб.",
            "Отклонение (|Δ|), руб.",
            "Оптимум"
        ]
        widths = [130, 220, 220, 180, 100]

        for col_idx, (head, w) in enumerate(zip(headers, widths)):
            self.table_container.grid_columnconfigure(col_idx, weight=1)
            lbl = ctk.CTkLabel(
                self.table_container,
                text=head,
                font=ctk.CTkFont(size=12, weight="bold"),
                anchor="center",
                width=w
            )
            lbl.grid(row=0, column=col_idx, padx=4, pady=6, sticky="ew")

    def _start_simulation_thread(self):
        self.btn_run.configure(state="disabled", text="Расчёт...")
        self.lbl_summary.configure(text="Выполняется розыгрыш псевдослучайных чисел LFSR...")

        thread = threading.Thread(target=self._run_simulation_worker, daemon=True)
        thread.start()

    def _run_simulation_worker(self):
        try:
            config = VariantConfig(
                defect_rate=float(self.entries["Брак (A), %:"].get()) / 100.0,
                cost_inspection=float(self.entries["Контроль (B), руб.:"].get()),
                cost_adjustment=float(self.entries["Подгонка (C), руб.:"].get()),
                cost_replacement=float(self.entries["Замена (D), руб.:"].get()),
                trials_per_step=int(self.entries["Партия (N), шт.:"].get()),
            )

            rng = LFSR32Generator(seed=0x1337BEEF)
            results = MonteCarloOptimizer.run(config, rng, step=5)

            # Передаём обновление интерфейса в главный поток
            self.after(0, self._update_ui_results, results)

        except Exception as exc:
            self.after(0, self._show_error, str(exc))

    def _update_ui_results(self, results):
        # Очистка старых строк (сохраняя строку заголовков row=0)
        for widget in self.table_container.winfo_children():
            grid_info = widget.grid_info()
            if grid_info and int(grid_info["row"]) > 0:
                widget.destroy()

        # Отрисовка новых строк
        for row_idx, r in enumerate(results, start=1):
            bg_color = ("#DCFCE7", "#14532D") if r.is_optimal else "transparent"
            text_color = ("#15803D", "#86EFAC") if r.is_optimal else None

            values = [
                f"{r.percent} %",
                f"{r.simulated_cost:,.2f}",
                f"{r.theoretical_cost:,.2f}",
                f"{r.delta_cost:,.2f}",
                "★ ДА" if r.is_optimal else "—"
            ]

            for col_idx, val in enumerate(values):
                cell_lbl = ctk.CTkLabel(
                    self.table_container,
                    text=val,
                    fg_color=bg_color,
                    text_color=text_color,
                    corner_radius=4,
                    height=26,
                    font=ctk.CTkFont(size=12, weight="bold" if r.is_optimal else "normal")
                )
                cell_lbl.grid(row=row_idx, column=col_idx, padx=4, pady=2, sticky="ew")

        # Формирование итогового отчета
        best = next(r for r in results if r.is_optimal)
        savings = results[0].simulated_cost - best.simulated_cost

        summary_msg = (
            f"• Оптимальное решение: входной контроль {best.percent}% партии резисторов.\n"
            f"• Минимальные затраты (Монте-Карло): {best.simulated_cost:,.2f} руб. "
            f"(Аналитическая теория: {best.theoretical_cost:,.2f} руб.).\n"
            f"• Экономический эффект (чистая экономия) по сравнению с 0% контроля: {savings:,.2f} руб."
        )

        self.lbl_summary.configure(text=summary_msg)
        self.btn_run.configure(state="normal", text="Рассчитать")

    def _show_error(self, message: str):
        self.lbl_summary.configure(text=f"Ошибка валидации параметров: {message}")
        self.btn_run.configure(state="normal", text="Рассчитать")