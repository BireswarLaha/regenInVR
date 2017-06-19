Tell the participants:
1. Keep your eyes fixated on the crosshair at the center of the screen, while getting the stimulation.
2. If its hard on your thumb to press down the trackpad for the entire session, use the other fingers, or the thumb in your other hand.

For the research co-ordinator:
1. The white noise video is on the desktop. Rest everything is on github.
2. On github, the branch that should be used in this study is titled "VERSION LOCKDOWN 0.5".
3. General outline:
a. Make sure all hardware connections are right - Vive basestations are powered up, vive is connected to the laptop.
b. Startup the laptop and login to your account.
c. Power up the hand controller.
d. Startup Steam VR (from the taskbar), and put on the Vive to make sure you see the white room, and the hand controller.
e. Startup Vizard (from the taskbar), and run vis_stim_round0.5.py by clicking on play, or pressing F5.
f. On the popup, select either experimental or control, based on the participant.

Need to train the coordinator on the following:
1. H/w and s/w for vive
2. vizard and github
3. Troubleshooting
a. If the vive software (steam VR) starts but shows some error (see point b below) - restart the laptop. No luck? restart again. Again, no luck, restart a third time! Its strange, but patience really pays off here.
b. Typical errors with the vive:
i. Steam VR says restart the vive - click on the link to restart
ii. Base stations are not detected - check if they are powered up alright.

First login with the research coordinator:
1. SU ID w/password
2. takes time - may be 5 minutes
3. welcome screen
4. computer and network policy notice is displayed
5. Notes for Bireswar:
a. Pin Vizard to taskbar, and make it the default editor for python files
b. Run steamVR and pin it to taskbar
c. Right click on steamVR, goto Settings > Developer > Untick "Enable VR Dashboard"
d. Download github and use it to download the regenVR branch
e. Download whitenoise movie from Stanford box: box -> sharing for study
f. Put the noise video and the readme file on the desktop
g. Word-wrap notepad for displaying the readme
h. Shutdown at the end of the day
*write a script for starting up all things they need at every startup
