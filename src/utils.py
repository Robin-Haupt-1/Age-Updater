from aqt.utils import showWarning, tooltip, showInfo
import datetime
from .lib import termcolor


def display_warning(text, header="Error"):
    showWarning((f"<b>{header}</b>: ") +
                text, title="Age Updater")


def log(text, start=None, end="\n", color="cyan"):
    if start is None:
        start = "{:<10} {:<13}\t".format(datetime.datetime.now().strftime('%H:%M:%S'), f"[AGE UPDATER]")
    print(termcolor.colored(f"{start}{text}", color), end=end)
