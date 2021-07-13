# Age Updater for Anki

This plugin allows you to remember the age of your friends and acquaintances in Anki.  You will have a card displaying the persons name and asking for their age.

When they celebrate their birthday, the card will be updated automatically to their new age and its learning status will be set to new.




# Usage

After installing the addon, you will have a new note type named "Age Updater Note".

In a deck of your choice, create a new note of this type and fill in your friend's name and date of birth, skip the age.

Make sure the date of birth is in the format YYYY-MM-DD (e.g. 1990-4-30, leading zeros are not required)

The addon will keep checking the notes for changes in the background and update the age values as needed. You can also force a refresh by launching the card editor / browser or clicking the sync button to sync your collection with AnkiWeb. 



# Importing Contacts from Google / Outlook

## Exporting

Export the contacts whose information you want to import into Anki as a .csv file. Only Google and Outlook are the accepted sources at this point. 

https://outlook.live.com/people/0/

https://contacts.google.com/

## Importing

Import the .csv file by clicking on Tools -> Age Updater -> Import contacts from .csv. 

First you need to select the deck for the new cards to be imported into. 

If you already have some notes of the "Age Updater Note" type, then the deck that has the most of them will automatically be selected and it's name will be displayed next to the "Select deck" button. You may continue with this deck or choose another one.

After you have selected the deck, click on "Select .csv file" and select your .csv file. 

Your contacts will be imported and a list of the contacts that have been imported will show.