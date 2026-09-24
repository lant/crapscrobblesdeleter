# Last.fm Scrobbles Deletion

I created this simple script to delete crappy scrobbles (not mine) from my last.fm account. 

Unfortunately there is no way to delete scrobbles from the API (as far as I know), so I had to just create a list of URLs that you need to click and confirm. It's painful, but it works. 

To run it you will need an `env` file with the following format: 

```
LAST_API="<your won api key>"
LAST_USERNAME="<your lastfm username>"
```

You also will need two text files (too lazy to code this) in the same directory where you are running the script (`whitelist.json` and `blacklist.json`) both with just `[]` in them.

Then just run it: 

```
python3 delete_crap_artists.py
```

The script will iterate through your scrobbles and ask if a band is "good" or not. 

The result will be a `to_delete.txt` file with the URLs that you need to use to delete the scrobbles. 
