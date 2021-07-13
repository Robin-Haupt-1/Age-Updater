import csv
import datetime


def read_contacts(csv_file):
    contacts = list(csv.reader(open(csv_file, "r", encoding="utf-8"), delimiter=","))

    print(contacts[0])
    try:
        birthday_row = contacts[0].index("Birthday")
    except ValueError as e:
        print("not a valid contacts csv", e)
        return None

    is_outlook = False
    all_contacts_w_birthday = [x for x in contacts[1:] if x[birthday_row]]

    if all_contacts_w_birthday[0][birthday_row].find(".") != -1:  # check if its in Google or Outlook format: Google is YYYY-MM-DD, Outlook is DD.MM.YYYY.
        is_outlook = True
    contacts_w_birthday = []

    for count, x in enumerate(contacts[1:]):
        if not x[birthday_row]:
            continue  # no date of birth given for contact
        name, date_of_birth = (None, None)

        if is_outlook:
            if x[1]:  # has middle name?
                name = " ".join([x[0], x[1], x[2]])
            else:
                name = " ".join([x[0], x[2]])

            print(name, x[birthday_row])

            date_of_birth = None

            try:  # convert DD.MM.YYYY. to YYYY-MM-DD
                date_of_birth = datetime.datetime.strptime(x[birthday_row], "%d.%m.%Y")
                date_of_birth = date_of_birth.strftime("%Y-%m-%d")

            except ValueError as e:
                print("ValueError while converting birthday date from Outlook to Google for ", x[0], e)

        else:
            name = x[0]  # Google has the whole name in the first column

            try:  # check that the date is valid by parsing it with datetime
                date_of_birth = datetime.datetime.strptime(x[birthday_row], "%Y-%m-%d")
                date_of_birth = x[birthday_row]

            except ValueError as e:
                print("ValueError while parsing birthday date for ", x[0], e)
        if name and date_of_birth:
            contacts_w_birthday.append((name, date_of_birth))

    return contacts_w_birthday
