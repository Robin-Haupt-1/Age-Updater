import anki.consts

NAME_FIELD = "Name"
AGE_FIELD = "Age"
DATE_OF_BIRTH_FIELD = "Date of birth (YYYY-MM-DD)"
FIELD_NAMES = [NAME_FIELD, AGE_FIELD, DATE_OF_BIRTH_FIELD]
DATE_FORMAT = '%Y-%m-%d'
DECK_NAME = "Age Updater"
DATE_OF_BIRTH_FIELD_NO = 2

# Model information

NOTETYPE_NAME = "Age Updater Note"

CARD_FRONT = """\
<span id="header">
    How old are they?
</span>
<br>
<br>
{{NAME_FIELD}}

<br>
<span id="birthday_notification"><br>It's their birthday today! 🎂<br><br></span>


<script>
    var today = new Date();
    var dd = String(today.getDate());
    var mm = String(today.getMonth() + 1); //January is 0
    var today_string = mm + "-" + dd;
    var yyyy = today.getFullYear();
    var cardOutput = "{{text:Date of birth}}";

    var dob = "{{text:Date of birth}}".split("-");

    mm = String(parseInt(dob[1])) // parseInt to remove leading zeros
    dd = String(parseInt(dob[2])) // parseInt to remove leading zeros
    var dob_string = mm + "-" + dd;

    birthday_today = false;
    
    if (today_string == dob_string) {
        birthday_today = true;
    }
    // handle leap year birthdays
    is_leap_year =new Date(yyyy, 1, 29).getDate() === 29;
    if (today_string == "3-1" && dob_string == "2-29" && is_leap_year) {
        birthday_today = true;
    }
    if (birthday_today) {
        document.getElementById("birthday_notification").style.display = "block";
    }

</script>\
"""  # solution for checking if present year is a leap year: https://stackoverflow.com/questions/16353211/check-if-year-is-leap-year-in-javascript

CARD_BACK = """\
{{FrontSide}}

<hr id=answer>

{{AGE_FIELD}}
\
"""

CARD_FRONT = CARD_FRONT.replace("NAME_FIELD", NAME_FIELD)
CARD_BACK = CARD_BACK.replace("AGE_FIELD", AGE_FIELD)

CARD_CSS = """\
.card {
    font-family: arial;
    font-size: 20px;
    text-align: center;
    color: black;
    background-color: white;
}

#header {
    color: #00b1c4;
    font-size: 18px;
   
}

#birthday_notification {
    display: none;
    color: #00b1c4;
    font-size: 20px;
}
\
"""
