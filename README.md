# GoogleCalendarFreeTime

## Setup Settings.json

### Credentials.json
The credentials file is essential for communicating with the Google api services.
#### How to
First, follow the following guide regarding setup for desktop client: 
> https://developers.google.com/workspace/guides/create-credentials

Then download the client secret file, rename to credentials.json and then drag into the solution


### Settings.json
#### Calendars
The calendar key will determine which calendars which will be used when fetching events.
This file follows the following format:
<sub> ["primary", anotherId"] </sub>
>To find a calendar id: https://docs.simplecalendar.io/find-google-calendar-id/
#### Summary keywords
Summary will be searched for these keywords, and instantly determine that a day is no longer available if found.

Example file:
> {
  "calendars":  ["primary", "dwadwawd@import.calendar.google.com"],
  "summaryKeywords": ["exam"]
}