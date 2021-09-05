from aqt.qt import *
from .read_contacts import *
from .notes import *


class ImportContactsDialog(QDialog):

    def import_google_contacts(self):
        try:
            deck = self.deck_label.text()
            if deck == "":
                display_warning("Please select a deck first")
                return
            w = QWidget()
            fname = QFileDialog.getOpenFileName(w, 'Open file', 'c:\\', "Contact Export File (Google/Outlook) (*.csv)")
            if not fname[0]:
                return
            self.filename = fname[0]
            self.contacts_file.setText(self.filename)
            contacts = read_contacts(fname[0])
            if contacts:
                imported_contacts = []
                for c in contacts:
                    try:
                        create_age_card(self.mw, c[0], c[1], deck)
                        imported_contacts.append(c)
                    except Exception as e:
                        display_warning("Error while importing the contact for " + c[0])

                update_age_cards(self.mw)
                showInfo("The following contacts have been imported:<br><br>- " + "<br> - ".join([f'{x[0]} ({x[1]})' for x in imported_contacts]) + "<br>")
        except Exception as e:
            display_warning("Error while importing contacts:<br><br>" + e)


    def deck_with_most_age_cards(self):
        age_cards = self.mw.col.find_cards(f'"note:{NOTETYPE_NAME}"')
        if age_cards:
            count_decks = {}
            card_decks = self.mw.col.decks.for_card_ids(age_cards)
            for x in card_decks:
                count_decks[x] = count_decks[x] + 1 if x in count_decks else 1
            deck_with_most_age_cards = sorted(list(count_decks.items()), key=lambda i: i[1], reverse=True)[0][0]
            deck_with_most_age_cards = self.mw.col.decks.get(deck_with_most_age_cards)
            deck_with_most_age_cards_name = deck_with_most_age_cards["name"]
            # showInfo(str(deck_with_most_age_cards_name))
            return deck_with_most_age_cards_name

    def refresh_deck_list(self):
        filter_text = self.filter_deck_textbox.text().lower()
        filtered_decks = [deck for deck in self.mw.col.decks.all() if deck["name"].lower().find(filter_text) != -1]
        self.deck_list_widget.clear()
        for c, x in enumerate(sorted(filtered_decks, key=lambda y: y["name"])):
            self.deck_list_widget.insertItem(c, x["name"])
        self.deck_list_widget.setCurrentRow(0)
        # self.select_deck_button.setFocus()

    def on_deck_doubleclicked(self, item, widget):
        self.deck_label.setText(item.text())
        widget.close()

    def on_select_deck_button_push(self, item, widget):
        self.deck_label.setText(item.text())
        widget.close()

    def select_deck(self):

        self.select_deck_widget.setMinimumSize(650, 500)
        grid = QGridLayout()
        self.deck_list_widget.setObjectName("filter...")

        self.deck_list_widget.itemDoubleClicked.connect(lambda item: self.on_deck_doubleclicked(item, self.select_deck_widget))

        self.filter_deck_textbox.textChanged.connect(self.refresh_deck_list)
        t = self.filter_deck_textbox
        t.installEventFilter(self)
        select_deck_button = self.select_deck_button
        select_deck_button.setText("select this deck")
        select_deck_button.clicked.connect(lambda *args: self.on_deck_doubleclicked(self.deck_list_widget.currentItem(), self.select_deck_widget))
        grid.addWidget(self.filter_deck_textbox, 0, 0)
        grid.addWidget(self.deck_list_widget, 1, 0)
        grid.addWidget(select_deck_button, 2, 0)
        # select_deck_button.setFocus()
        # select_deck_button.focusWidget()
        self.refresh_deck_list()
        self.select_deck_widget.setLayout(grid)
        self.select_deck_widget.show()

    def __init__(self, mw):
        super(ImportContactsDialog, self).__init__()
        self.setWindowTitle("Import Contacts into Age Updater")
        self.filename = ""
        QDialog.__init__(self)
        grid = QGridLayout()
        # self.setFixedSize(300,300)
        self.mw = mw
        self.contacts_file = QLabel('')
        if deck_name := self.deck_with_most_age_cards():
            self.deck_label = QLabel(deck_name)
        else:
            self.deck_label = QLabel("")

        import_button = QPushButton(self)
        import_button.setText("Select .csv file")
        import_button.setFixedSize(200, 30)
        import_button.clicked.connect(self.import_google_contacts)

        select_deck_button = QPushButton(self)
        select_deck_button.setText("Select deck")
        select_deck_button.setFixedSize(200, 30)
        select_deck_button.clicked.connect(self.select_deck)
        # select_deck_button.setFocus()

        grid.setSpacing(10)

        grid.addWidget(select_deck_button, 0, 0)

        grid.addWidget(self.deck_label, 0, 1)

        grid.addWidget(import_button, 1, 0)
        grid.addWidget(self.contacts_file, 1, 1)
        self.setLayout(grid)

        # initialize widgets
        self.select_deck_widget = QWidget()
        self.deck_list_widget = QListWidget()
        self.filter_deck_textbox = QLineEdit()
        self.filter_deck_textbox.setPlaceholderText(" Filter...")
        self.select_deck_button = QPushButton()

    def eventFilter(self, obj: QObject, evt: QEvent) -> bool:  # inspired by Anki studydeck.py
        if isinstance(evt, QKeyEvent) and evt.type() == QEvent.KeyPress:
            new_row = current_row = self.deck_list_widget.currentRow()
            rows_count = self.deck_list_widget.count()
            key = evt.key()

            if key == Qt.Key_Up:
                new_row = current_row - 1
            elif key == Qt.Key_Down:
                new_row = current_row + 1

            if rows_count:
                new_row %= rows_count  # don't let row index overflow/underflow
            if new_row != current_row:
                self.deck_list_widget.setCurrentRow(new_row)
                return True
        return False


def on_import_google_contacts_call(mw):
    d = ImportContactsDialog(mw)
    # use both show() and exec_() to make the dialog not be removed by garbage collection: https://www.mail-archive.com/pyqt@riverbankcomputing.com/msg12512.html
    d.show()
    d.exec()
