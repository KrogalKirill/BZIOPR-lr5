"""Главный исполняемый модуль запуска приложения."""

from src.app import MonteCarloApp


def main():
    app = MonteCarloApp()
    app.mainloop()


if __name__ == "__main__":
    main()