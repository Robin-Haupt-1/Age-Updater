from aqt import gui_hooks
from aqt import mw

from .import_contacts import *
from .model import check_model
from .notes import *

last_update = 0


def interval_update():
    global last_update
    now = datetime.datetime.now().timestamp()
    if now - last_update > 3600:
        last_update = now
        update_age_cards(mw)


def init():
    check_model(mw.col)
    update_age_cards(mw)

gui_hooks.profile_did_open.append(lambda *args: init())
gui_hooks.profile_will_close.append(lambda *args: update_age_cards(mw))
gui_hooks.sync_will_start.append(lambda *args: update_age_cards(mw))
gui_hooks.reviewer_did_show_question.append(lambda *args: interval_update())
gui_hooks.editor_did_init.append(lambda *args: interval_update())
gui_hooks.add_cards_did_add_note(lambda *args: update_age_cards(mw))


# Set up menu items

menu = mw.form.menuTools.addMenu("Age Updater")

action = QAction("Update age notes", mw)
qconnect(action.triggered, lambda *args: update_age_cards(mw))
menu.addAction(action)

options_action = QAction("Import contacts from .csv", mw)
options_action.triggered.connect(lambda _, o=mw: on_import_google_contacts_call(mw))
menu.addAction(options_action)
