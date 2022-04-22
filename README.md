# Tracking-Info-Bot

This is a small bot that will pull cases from salesforce, then generate messages to send to customers. This was made to automate part of my workflow.

**Built With**

- Python
- [simple_salesforce](https://github.com/simple-salesforce/simple-salesforce) REST API to access Salesforce
- [gspread](https://github.com/burnash/gspread) To read and write data on Google Sheets
- [python-decuple](https://pypi.org/project/python-decouple/) To store variables in an .env file


**Usage**

This program was used to automatically pull info and fill out form messages. The messages were simple alerts to customers that their repaired computer or replacement part has been shipped. Due to how Amazon handles customers' messages, automatic messaging wasn't possible. This bot allowed me to automate the message creation and sorting so that I could send out messages to customers easier and faster

**Dependencies**

This program uses gspread to access a google sheet that stores data needed to run the bot.
This [example sheet](https://docs.google.com/spreadsheets/d/19zL2coJX3cy5hx-fuMDqnz7W4dTAv3k2Y9l3G-621Y4/edit?usp=sharing) shows the type of info read and written to the sheet. 
A Google service account is also needed to run this bot. The Gspread documentation has more info on how to set that up. 
[Gspread Authentication Docs](https://docs.gspread.org/en/latest/oauth2.html#authentication)

You will of course also need salesforce. The bot expects salesforce to set up in a specific way, so chances are this will not work on your own salesforce implementation. You would need to change a few things in the python script, mainly the SOQL query to match your needs. (Please contact me directly if you need any help with that)

**Roadmap**
This version is the last version of this project I will be making, as I no longer work with Amazon customers in my current position. No further updates will be made.
