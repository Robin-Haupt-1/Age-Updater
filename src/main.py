from aqt import gui_hooks
from aqt import mw

from .import_contacts import *
from .model import check_model
from .notes import *
from .constants import UPDATE_TIMER_TIMEOUT

update_timer = None


def init():
    global update_timer
    check_model(mw.col)
    update_age_cards(mw)
    update_timer = mw.progress.timer(UPDATE_TIMER_TIMEOUT, lambda *args: update_age_cards(mw), True)


# Set up hooks

gui_hooks.profile_did_open.append(lambda *args: init())
gui_hooks.profile_will_close.append(lambda *args: update_age_cards(mw))
gui_hooks.sync_will_start.append(lambda *args: update_age_cards(mw))
gui_hooks.add_cards_did_add_note(lambda *args: update_age_cards(mw))

# Set up menu items

menu = mw.form.menuTools.addMenu("Age Updater")

action = QAction("Update age notes", mw)
qconnect(action.triggered, lambda *args: update_age_cards(mw))
menu.addAction(action)

options_action = QAction("Import contacts from .csv", mw)
options_action.triggered.connect(lambda _, o=mw: on_import_google_contacts_call(mw))
menu.addAction(options_action)
