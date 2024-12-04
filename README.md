# Cyberdeck
![IMG_6086 copy](https://github.com/user-attachments/assets/54127bf0-03a0-4611-bc85-48a0d74e7727)


# connections
![connectors](doc/connectors.jpg)

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
