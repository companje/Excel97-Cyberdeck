# Cyberdeck
 


# connections
![connectors](doc/connectors-1.jpg)

# audio generation
* sounds from the Speak & Spell toy

* sound produced with `say` command in MacOS.
```bash
say -v Zarvox "Welcome to the SETUP Utrecht  Microsoft Excel 97 CYBERDECK........[[rate 50]]enjoy your time[[rate 100]].......ha-ha-ha" -o welcome.aiff
```

* convert
```bash
ffmpeg -i saved2.aiff -filter:a "volume=2.0" /Volumes/Cyberdeck/github-repo/Excel/audio/saved2.wav -y
```