Tell the participants:
1. Keep your eyes fixated on the crosshair at the center of the screen, while getting the stimulation.
2. If its hard on your thumb to press down the trackpad for the entire session, use the other fingers, or the thumb in your other hand.

For the research co-ordinator:
1. The white noise video is on the desktop. Rest everything is on github.
2. On github, the branch that should be used in this study is titled "VERSION LOCKDOWN 0.6".
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

DENSITY FACTORS FOR THE EXPERIMENTAL STIMULATION VIDEOS (created from HLMaxFiring branch on github version# bac3ae3, file - t_viveOptimal.m):
_DENSEST = 1
_DENSE = 4
_SPARSE = 8
_SPARSEST = 12

These videos, as well as the control video (white noise) are at resolution 1080x1080, and 30 frames/sec

In the "dense" experimental condition, during the first 30% and the last 30% of time, the _dense vids are shown, and the _densest videos are shown during the middle 40% of time.
In the "sparse" experimental condition, during the first 30% and the last 30% of time, the _sparsest vids are shown, and the _sparse videos are shown during the middle 40% of time.


==================================
EYE-TRACKING choices for the Vive (August, 2017):
ref: https://www.reddit.com/r/Vive/comments/6ggfty/aglass_vive_eye_tracker_from_7invensun_initial/ (accessed 8/9/2017)
1. SMI ~$12k+; latency: integrated (!), sampling at 250 Hz, 110 deg FOV, 0.2 degrees accuracy (https://www.smivision.com/wp-content/uploads/2016/11/smi_prod_eyetracking_hmd_HTC_Vive.pdf accessed on 8/14/17)
2. Tobii >$3500 (includes a $1200 business edition Vive, but that's still $2300); latency 10ms, sampling at 120 Hz, 110 degrees FOV, 0.5 degrees accuracy (https://www.tobiipro.com/product-listing/vr-integration/#Specifications accessed on 8/14/17)
3. Pupil Labs ~1400 euro (~$1550) HTC Vive Binocular Add-on (over 7 times the price of the aGlass system); latency of 5.7ms (camera) + 3-4ms (CPU), sampling at 120 Hz, >100 deg FOV, 0.6 degrees accuracy and 0.08 degrees precision (https://pupil-labs.com/pupil/ and https://pupil-labs.com/vr-ar/ accessed on 8/14/17)
4. aGlass ~$220 (http://www.aglass.com/) - https://www.youtube.com/watch?v=eBfWnaEwzRI; <5 ms latency, sampling at 120-380Hz, with >110 degrees FOV, and <0.5 degrees eye tracking precision (http://www.aglass.com/product accessed on 8/14/17)

