# MouseAnalysis
MouseAnalysis is designed to analyse video footage of mice in homecage or enriched environment scenarios via a DeepLabCut network and then further process the resulting .csv files with a highly customizable python code to gain a quick overview of the data acquired.

---

For analysis of files created by using [DeepLabCut-Live](https://github.com/DeepLabCut/DeepLabCut-live-GUI) and [ActiveMouse](https://github.com/Lilli-K2/ActiveMouse-SFB1315/tree/main) please refer to this particular [tutorial](https://github.com/Lilli-K2/ActiveMouse-SFB1315/tree/main/Analysis).

---

### Before you start

You need to have [DeepLabCut](https://github.com/DeepLabCut/DeepLabCut) installed on you Computer. The DeepLabCut documentation also provides an extensive guide on how to train your own networks.
To use this code without further complications it is however advised to use the [provided network](https://github.com/Lilli-K2/MouseAnalysis/tree/main/network) as most of code is specifically tailored to this model.

The network is designed to recognize and track a <strong>single mouse</strong> based on four tracking points from a <strong>top-view </strong> in the dark under red light. These points include the nose, neck, butt and tail of the animal. If your experiments were conducted under similar conditions and the network still doesn't recognize the mouse well enough consider retraining the pretrained network with more of your own video footage.


WHAT NETWORK???

Save the pre-trained network to a location of your choice.
In the <strong>config.yaml</strong> file change the <strong>project path</strong> to the correct file path you saved the file to.

---

### Analyzing videos in DeepLabCut

Open DeepLabCut as usual (for more information please refer to [DeepLabCut-Tutorial](https://deeplabcut.github.io/DeepLabCut/docs/standardDeepLabCut_UserGuide.html)).
Now navigate to <strong>load project</strong>. Once the project is loaded go to <strong>analyze videos</strong> and select the videos you want to analyze from your folders. Make sure to check <strong>save as .csv</strong> as the entire MouseAnalysis code is csv based.

---

### Use MouseAnalysis

Change the <strong>base</strong> to your desired output filename and load the correct .csv file you want to analyse into <strong>df</strong>.
</p>
<kbd>
<strong>Additional information:</strong>
The <strong>df1.rename</strong> command currently works with files provided to you by this particular network. Should you intend to use a different network that is also based on four tracking points the logic of this code may indeed still work for you, but a couple of things - starting with the assumed column name (in this case "DLC_resnet50_LastMouse4PointDec11shuffle1_550000") - have to be adjusted.
Please also note that for a 4-point network this change may suffice for analysing your data generally, but all of the figures etc. will still be named under the presumption of those points being nose, neck, butt and tail.
</kbd>
</p>

Now pick the correct <strong>conversion factor</strong> for all four tracked points. This factor is based on the resolution of the video files you previously analyzed. 
<strong>MouseAnalysis</strong> is already equipped with conversion factors for these standard resolutions:
- HD (1280x720)
- Full HD (1920x1080)
- 4K (4096x2160)

For any other resolution see this tutorial on finding your specific [resolution](https://github.com/Lilli-K2/ActiveMouse/tree/main/Resolution)

---

### Adding MouseCare

Make sure you have downloaded [ActiveMouse](https://github.com/Lilli-K2/ActiveMouse) from the repository.

<img align="right" src="https://github.com/Nasr-SFB1315/images/blob/main/dlclivecamera.png?raw=true" />
<p align="left">

Now we need to add ActiveMouse as the processor. Select the folder you saved ActiveMouse to with <strong>Browse</strong> under <strong>Processor Dir</strong>. Confirm that you want to add the folder to your dropdown list for a quicker set-up process the next time you open the deeplabcut-live gui.
Under <strong>Processor</strong> select <strong>MouseLickImageProcessor</strong>. Make sure to update the processor under <strong>Edit Proc Settings</strong> so everything is loaded correctly. Now <strong>Set Proc</strong> to assure it is in place.
</p>
<kbd>
<strong>Additional information:</strong>
The <strong>images</strong> used in the ActiveMouse pop-up can be adjusted to your liking, although we suggest sizing them to 800x600 as this size works best with the tkinter gui in our experience. Make sure to change the <strong>lick_image</strong> and <strong>no_lick_image</strong> paths to the actual images you are using.
You can also change the accuracy threshold for displaying an image indicating satisfactory tracking under <strong>lik_thresh</strong>. It is set to 0.9 by default which has worked well for our past experiments but can obviously be adjusted according to your needs e.g. 0.99 for only considering very accurately tracked points or 0.7 to also consider more inaccurately tracked points.
If you not only want the pop-up to consider less accurate tracking points but also generate the graphs based on the same accuracy you need to additionally change the <strong>df1.query</strong> command to use the accuracy value of your choosing.
Please note that you should update the Processor under <strong>Edit Proc Settings</strong> every time you make changes to the processor file.
</kbd>
</p>

</p>
<kbd>
<strong>Attention!</strong>
Any changes to the processor that disrupt regular dlc-live flow will inevitably crash the dlc-live gui. Should you find yourself unable to open the gui consider reverting back to ActiveMouse as it is provided in this guide. 
</kbd>
</p>

---



### Adding the network

Make sure you have downloaded the [trained network](https://github.com/Lilli-K2/ActiveMouse/tree/main/trained-network) from the repository.

<img align="right" src="https://github.com/Nasr-SFB1315/images/blob/main/dlclivecamera.png?raw=true" />
<p align="left">

Under <strong>DeepLabCut:</strong> select <strong>add DLC</strong>. Choose a distinct name for the network e.g. ActiveMouse for quicker setup the next time you need it. Now navigate to the folder that contains your exported deeplabcut network under <strong>model path</strong>.
</p>
<kbd>
<strong>Additional information:</strong>
Should deeplabcut-live not recognize the exported deeplabcut model it is very likely that the selected folder is not what dlc-live expexted. For the network provided in this repository select the folder named <strong>DLC_LastMouse4Point_resnet_50_iteration-1_shuffle-1</strong>.
</kbd>
</p>


Press <strong>Update</strong> to ensure all changes have been saved correctly. You will have to use the <strong>Update</strong> function under <strong>Update DLC Settings</strong> every time you use the dlc-live gui!
You can now either start the tracking immediately by hitting <strong>Init</strong> or choose to use the <strong>Display DLC Keypoints</strong> feature provided by dlc-live before initiating the tracking. 
</p>
<kbd>
<strong>Attention!</strong>
Using the display feature it is also worth noting that the default accuracy threshold for generating the displaypoints is set to 0.5. Setting the threshold to a lower value than the accuracy threshold in ActiveMouse could be confusing, but you need to figure out what works for you.
</kbd>
</p>

</p>
<kbd>
<strong>Additional information:</strong>
Displaying the Keypoints is a great visual aid in making sure that the network is loaded correctly and in fact tracking the animal. However, it should be noted that especially with higher resolution videos your CPU/GPU is already pretty engaged and insufficient or lagging display of the keypoints is to be expected. Lagging display or its complete absence is not necessarily an indicator of unsatisfactory tracking, but rather an overloaded CPU/GPU.
You will also probably find that your videofeed is interrupted while loading the network. As soon as the network is loaded correctly the feed should resume. Should you notice an unusually slow or otherwise faulty video feed consider for example updating from CPU to GPU or using a lower resolution video feed.
</kbd>
</p>

---

### Setting up the session

Now we can finally set up the session.


<img align="right" src="https://github.com/Lilli-K2/ActiveMouse/blob/main/pictures/recording%20on.png?raw=true" />
<p align="left">
Choose a folder using <strong>Browse</strong> under <strong>Directory</strong> you want the data to be saved to.
Now <strong>Set Up Session</strong>. Once again you may need to wait for the video feed to resume after a short while.
You will notice that you are now able to press the <strong>On-Button</strong> under <strong>Record</strong>.

</p>
<kbd>
<strong>Additional information:</strong>
Should you run into problems while setting up the Recording session or immediately after starting the recoring it is advised to check the terminal. Oftentimes an incorrect path to one of the images or a missing python package can lead to ActiveMouse not working as expected. Most issues are easily fixed by changing a path or pip installing a necessary python package.
</kbd>
</p>
  
As soon as you start your recording a <strong>pop-up window</strong> will appear, indicating the accuracy with which your animal is being tracked live.
With the code provided in ActiveMouse a positive image suggests the tracking of the mouse's neck tracking-point with 90% accuracy. It can easily be changed by adjusting the lik_thresh value as you please.
  
This allows you to quickly realise at any point that the tracking has been unsatisfactory for a significant amount of time and interfere while the experiment is still being run. Thereby hopefully allowing uncomplicated changes to be made to the setup and ensuring swift resumption of the experiment.

</p>
<kbd>
<strong>Additional information:</strong>
Common problems we have encountered with inadequate tracking are bad lighting conditions, poor camera angles or camera quality as well as unsuitable deeplabcut networks. For the latter we suggest retraining an already existing network with further video footage or considering training a model from scratch to fit your specific conditions. For a detailed guide on training your model see the deeplabcut documentation.
</kbd>
</p>

---

### Stopping the session

After you have tracked your animal for the duration of the experiment, use the <strong>Off-Button</strong> to stop the recording.
It is vital that you now press <strong>save video</strong> before proceeding. This will not only save the video generated by deeplabcut-live (with or without visible tracking points, depending on your previous selection), but also promptly generate three new figures with further information on the recording.

These figures currently consist of:
- <strong>Accuracy pie chart</strong>
The pie chart displays the percentages of good and bad tracking, i.e. how well the tracking-point (default neck with 90% accuracy) was recognized over the course of the recording.
</p>
<kbd>
<strong>Attention:</strong>
Please note that substandard distribution of good vs bad tracking is not necessarily representative of the actual tracking quality. If you start the recording before setting the animal up deeplabcut-live will inevitably struggle with recognizing the animal and contribute to the 'Bad Accuracy' percentage. The same goes for removing the animal before stopping the recording. Do not get discouraged by unsatisfactory 'Good Accuracy'. 
With our experiments using ActiveMouse we found a percentage of around 8-10% for 'Bad Accuracy' to be fully adequate for a recording with the animal present the entire time.
Should you however still encounter high percentages of 'Bad Accuracy' after recording only when the animal is present, you may want to consider our suggestions already listed under <strong>Setting up the session</strong>
</kbd>
</p>

- <strong>Activity linegraph</strong>
The linegraph is a standard path-time diagram depicting the animal's speed. We are able to determine at a glance if and how much the animal moved over the course of the recording and can also gather how fast the animal moved on average, as well as the full distance it travelled.

</p>
<kbd>
<strong>Attention:</strong>
If the speed of your animal seems unusually high or low please check that you are using the correct conversion factor in the code for the resolution of your video feed.
Some outlier spikes are to be excpected, although we have found that the more processing the raw camera footage is put through, the less accurately the graph represents the actual speed. The graph may still offer you a general overview of whether and how much the animal moved, even if the speed is depicted incorrectly.
</kbd>
</p>

- <strong>Exploration Heatmap</strong>
The heatmap allows you to quickly gather the extent of the explored space and easily identify areas of more frequent animal presence.
</p>
<kbd>
<strong>Attention:</strong>
If a heatmap seems to be representing only a part of your setup, it may be attributed to the animal not yet having explored most of it. To counteract this try allowing for a longer recording time.
</kbd>
</p>

We have found that the acquired data is generally better represented by the graphs if a runtime of atleast 5 minutes is reached. As ActiveMouse calculates the linegraph and heatmap only with the data deemed to be of acceptable accuracy you may encounter problems generating these figures with very short recordings and/or recordings with overall poor tracking.

---

### Further processing

How you proceed with your data is none of our business, but we humbly suggest checking out our [analysis](https://github.com/Lilli-K2/ActiveMouse/tree/main/Analysis) code. This code generates some basic figures for all of the tracked points and can also be adjusted however you need.
