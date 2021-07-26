import anki.consts

NAME_FIELD = "Name"
AGE_FIELD = "Age"
DATE_OF_BIRTH_FIELD = "Date of birth (YYYY-MM-DD)"
FIELD_NAMES = [NAME_FIELD, AGE_FIELD, DATE_OF_BIRTH_FIELD]
DATE_FORMAT = '%Y-%m-%d'
DECK_NAME = "Age Updater"

# Model information

NOTETYPE_NAME = "Age Updater Note"

CARD_FRONT = """\
<span id="header">
    How old are they?
</span>
<br>
<br>
{{Name}}

<br><br>
<span id="birthday_notification">
	It's their birthday today! 🎂
<br><br></span>

<span id="use_desktop_warning">
	⚠️ This card is outdated. Please launch Anki on your desktop to update your Age Updater notes.
<br><br></span>

<script>

    var today = new Date();
    var today_dd =today.getDate();
    var today_mm = today.getMonth() + 1; //January is 0
    var today_string =String(today_mm) + "-" + String(today_dd);
    var today_yyyy = today.getFullYear();
    var dob = "{{text:Date of birth (YYYY-MM-DD)}}".split("-");
	var anki_age=parseInt("{{text:Age}}");
	

    dob_mm = parseInt(dob[1])
    dob_dd = parseInt(dob[2])
    dob_yyyy=parseInt(dob[0])
    var dob_string = String(dob_mm) + "-" +String(dob_dd);

    birthday_today = false;
    
    if (today_string == dob_string) {
        birthday_today = true;
    }

    // handle leap year birthdays
    is_leap_year =new Date(today_yyyy, 1, 29).getDate() === 29;
    if (!is_leap_year && today_string == "3-1" && dob_string == "2-29") {
        birthday_today = true;
    }
    if (birthday_today) {
        document.getElementById("birthday_notification").style.display = "block";
    }
    
    // check if age in card is still current
    var current_age= (today_yyyy - dob_yyyy) - 1
    if ((today_mm>dob_mm)||(today_mm===dob_mm && today_dd>=dob_dd)){
		 current_age+=1
    }
    if (!(current_age===anki_age)){
        document.getElementById("use_desktop_warning").style.display = "block";
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
