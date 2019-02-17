## RAD RACER 
The purpose of the project is to do simple self-driving AI to the NES game Rad Racer with python. The idea and how I got started was this youtube series https://youtu.be/ks4MPfMq8aQ from sentdex.



### 1. Setting the window positioning
Fist task was to make script that will set the emulator window to same postion every time. SetWinPos.py will do that.

### 2. Take screenshots from the gamewindow
In racer.py there is a loop that takes screenshots from the gamewindow

### 3. Process the image and find lanes
To find lanes from the images, we need to first process the image.
These are the parts I did 
1. change image to gray
2. detect edges from the image
3. Blur the image
4. Cut ROI from the image
5. find lines from the image
6. detect lanelines from all the lines

![alt text](https://github.com/PaavoR/Rad-Racer/blob/master/images/lanelines.jpg "On the left is gamewindow and on the right is detected lines")
