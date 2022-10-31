# Give me feedback
 
**Next time you go through airport security or to a doctor's appointment give feedback on the service by showing a gesture to a camera. Easy way to collect and see people's impressions of a service.**

The application uses a classification model that has been trained to recongise 3 gestures (peace, devil horns and thumbs up), all the other hand gestures are recongised as "other". 

**NB! the dataset that was used to train the classification model is limited as it only used gestures used by the author, for a more generalised applicaiton of the application, the classificaiton model needs to be improved!!!**

This was a project put together for the Hack the Middlands 7. 

## Installation
NB! There are probably a number of dependiencies that are not neccessary, yet the virtual envioroment with the given dependencies in the "dependencies.txt" file, should allow to launch the applicaiton.

```
python3 -m htm-env
python3 -m pip install -r dependencies.txt
source ./htm-env/bin/activate
```
## Launching the applicaiton
1) Eddit the settings,json file, change to the approprite path:
    * **video_ip** - ip address for an ip camera.
    * **model** - path to the model in the *./data/model* folder used for classifying the gesture.

... There are exaple pathS in the settings file.

2) Launch as a pytonh script and the application will be availabe on a local address. (check terminal for the address)




