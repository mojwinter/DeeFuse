from .ui.main_window import App   # relative import (the dot is important)


def main() -> None:               # noqa: D401
    """Launch the DeeFuse GUI."""
    App().mainloop()


if __name__ == "__main__":
    main()
