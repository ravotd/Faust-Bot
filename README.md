# Faust-Bot
IRC Bot, derived from Pallaber Bot, Architectonic rework

Designed for non-technical channels

### Requirements

Install Python 3.5  (we don't guarantee it to work under any other python version), including pip
### Usage
```bash
# First load all needed strings into the database
# Per default german is used. If you want another language you need to 
# add an language file and modify the script.
# Later it will be refactored, so it uses arguments
python ReadInternationalization.py
# Start the bot using the given config file.
python Main.py --config ./config.txt
``` 
