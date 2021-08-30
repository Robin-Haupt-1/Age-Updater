from .constants import *
import datetime
from .utils import *

def create_age_card(mw, name, date_of_birth, deck):

    # check if note for this person already exists

    duplicate_cards = mw.col.findNotes(f'"note:{NOTETYPE_NAME}" AND "{NAME_FIELD}:{name}" AND "{DATE_OF_BIRTH_FIELD}:{date_of_birth}"')
    if duplicate_cards:
        return

    # select deck and model (from https://addon-docs.ankiweb.net/#/getting-started?id=a-simple-add-on => Import a text file into the collection)
    # select deck
    did = mw.col.decks.id(deck)
    # showInfo(str(did))
    mw.col.decks.select(did)
    # anki defaults to the last note type used in the selected deck
    m = mw.col.models.byName(NOTETYPE_NAME)
    # showInfo(str(m))
    deck = mw.col.decks.get(did)
    deck['mid'] = m['id']
    mw.col.decks.save(deck)
    # and puts cards in the last deck used by the note type
    m['did'] = did
    mw.col.models.save(m)
    note = mw.col.newNote()
    field_associations = {NAME_FIELD: name, DATE_OF_BIRTH_FIELD: date_of_birth}
    for (name, value) in note.items():
        if name in field_associations:
            note[name] = field_associations[name]
    mw.col.addNote(note)


def update_age_cards(mw):
    log("Updating age notes...",end="\t")
    updated_cards=0
    try:

        age_card_ids = mw.col.find_cards(f'"note:{NOTETYPE_NAME}" AND "card:1"')  # Only select card type 1 because the user may want to create more card types from the same notes (Name => Birthday for example)
        for card_id in age_card_ids:
            card = mw.col.getCard(card_id)
            note = card.note()
            birthday_date = note[DATE_OF_BIRTH_FIELD]

            born = datetime.datetime.strptime(birthday_date, DATE_FORMAT)
            try:
                anki_age = int(note[AGE_FIELD])
            except ValueError:  # The user may have entered text into the age field
                anki_age = -1
            today = datetime.date.today()

            current_age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))  # Solution from here: https://stackoverflow.com/questions/2217488/age-from-birthdate-in-python/9754466#9754466

            if not current_age == anki_age:
                note[AGE_FIELD] = str(current_age)
                note.flush()
                #  Reset the card to 'new' if the age has changed
                #  I copied the card parameters to be reset from AnkiConnect's forgetCard() function: collection().db.execute('update cards set type=0, queue=0, left=0, ivl=0, due=0, odue=0, factor=0 where id in ' + scids)
                card.queue = anki.consts.QUEUE_TYPE_NEW
                card.due = 0
                card.ivl = 0
                card.odue = 0
                card.type = anki.consts.CARD_TYPE_NEW
                card.factor = 0
                card.left = 0
                card.flush()
                updated_cards+=1


    except Exception as e:
        showInfo("Error in Update Age Cards: " + str(e))
        pass
    log(f"{updated_cards} notes updated",start="")
