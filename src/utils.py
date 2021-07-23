from aqt.utils import showWarning, tooltip, showInfo

def display_warning(text, header="Error"):
    showWarning((f"<b>{header}</b>: ") +
                text, title="Age Updater")

