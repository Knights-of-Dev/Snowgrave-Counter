# Snowgrave-Counter
A simple Python program to count anything you want. Change the settings in config.json to your heart's content!
## How to run?
Run ```main.py``` to get the counter!
## How to exit?
Click on the counter and press the ```esc``` key.
## How to count it?
The default key to increment the counter is ```1```. Change ```thing``` in ```config.json``` to set the key to what you want!
## How to reset?
Close and open the program.
## What does everything do in ```config.json```?
```
{
	"count": "Snowgraves",			<-- Title (what's being counted)
	"countCol": "#00ccff",			<-- Color of the title
	"startNum": 1225,				<-- Starting number
	"numCol": "#00eeff",			<-- Color of the number
	"countKey": ["1"],				<-- The key to press to count up
	"countSoundPath": "snow.wav"	<-- The path to the sound file
}
```
## Why doesn't the program work on my computer?
This program only works for Windows systems, as far as it was tested.
