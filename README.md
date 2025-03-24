# MouseAnalysis

MouseAnalysis is designed to analyse video footage of mice in homecage or enriched environment scenarios via a DeepLabCut network and then further process the resulting .csv files with a highly customizable python code to gain a quick overview of the data acquired.

---

For analysis of files created by using [DeepLabCut-Live](https://github.com/DeepLabCut/DeepLabCut-live-GUI) and [ActiveMouse](https://github.com/Lilli-K2/ActiveMouse-SFB1315/tree/main) please refer to this particular [tutorial](https://github.com/Lilli-K2/ActiveMouse-SFB1315/tree/main/Analysis).
<strong>ActiveMouse</strong> offers live monitoring of DeepLabCut tracking quality with immediate video analysis afterwards. Please refer to the [ActiveMouse-Tutorial](https://github.com/Lilli-K2/ActiveMouse-SFB1315/tree/main) for further information.

---

### Before you start

You need to have [DeepLabCut](https://github.com/DeepLabCut/DeepLabCut) installed on you Computer. The DeepLabCut documentation also provides an extensive guide on how to train your own networks.
To use this code without further complications it is however advised to use the [provided network](https://github.com/Lilli-K2/MouseAnalysis/tree/main/network) as most of code is specifically tailored to this model.

The network is designed to recognize and track a <strong>single mouse</strong> based on four tracking points from a <strong>top-view </strong> in the dark under red light. These points include the nose, neck, butt and tail of the animal. If your experiments were conducted under similar conditions and the network still doesn't recognize the mouse well enough consider retraining the pretrained network with more of your own video footage.
Save the pre-trained network to a location of your choice.
In the <strong>config.yaml</strong> file change the <strong>project path</strong> to the correct file path you saved the file to.

---

### Analyzing videos in DeepLabCut

Open DeepLabCut as usual (for more information please refer to [DeepLabCut-Tutorial](https://deeplabcut.github.io/DeepLabCut/docs/standardDeepLabCut_UserGuide.html)).
Now navigate to <strong>load project</strong>. Once the project is loaded go to <strong>analyze videos</strong> and select the videos you want to analyze from your folders. Make sure to check <strong>save as .csv</strong> as the entire MouseAnalysis code is csv based.

---

### Using MouseAnalysis

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

### Results

MouseAnalysis generates multiple figures indicating the quality of the tracking and general activity of your animal.
As of now these figures include:

- <strong>Accuracy pie chart</strong> The pie charts display the percentages of good and bad tracking, i.e. how well the tracking-points were recognized over the course of the recording.
  
</p>
<kbd>
<strong>Attention:</strong>
Please note that substandard distribution of good vs bad tracking is not necessarily representative of the actual tracking quality. If you start the recording before setting the animal up deeplabcut will inevitably struggle with recognizing the animal and contribute to the 'Bad Accuracy' percentage. The same goes for removing the animal before stopping the recording. Do not get discouraged by unsatisfactory 'Good Accuracy'. With our experiments  we found a percentage of around 8-10% for 'Bad Accuracy' in well recognized points (e.g. neck) to be fully adequate for a recording with the animal present the entire time. Should you however still encounter high percentages of 'Bad Accuracy' after recording only when the animal is present, you may want to consider retraining the network with additional videos or rethinking the camera and lighting conditions.
</kbd>
</p>

</p>
<kbd>
<strong>Additionally:</strong>
Please note that tail-tracking is usually sub-par and negatively affects the total Accuracy. As neck-tracking is usually the best it's what we have found to be most reliable for judging the actual tracking quality. Nose tracking is also usually satisfactory and butt tracking varies a bit more. It can still be useful to have these figures for all of your tracking points.
</kbd>
</p>

- <strong>Activity linegraph</strong> The linegraphs are standard path-time diagrams depicting the animal's speed each based on one of the tracked points. You are able to determine at a glance if and how much the animal moved over the course of the recording and can also gather how fast the animal moved on average, as well as the full distance it travelled.

</p>
<kbd>
<strong>Attention:</strong>
If the speed of your animal seems unusually high or low please check that you are using the correct conversion factor in the code for the resolution of your videofootage. Some outlier spikes are to be excpected, although we have found that the more processing the raw camera footage is put through, the less accurately the graph represents the actual speed. The graph may still offer you a general overview of whether and how much the animal moved, even if the speed is depicted incorrectly.
The tail graph will also look different from the other graphs either because the tracking was so unsatisfactory most values had to be excluded or, if tracking was satisfactory, because the tip of the tail does in fact move faster from side to side than the rest of the body can be moved.
</kbd>
</p>

- <strong>Exploration Heatmap</strong> The heatmaps allow you to quickly gather the extent of the explored space and easily identify areas of more frequent animal presence. All of the heatmaps are also generated with a transparent background to make superimposing them onto images etc. easier.

</p>
<kbd>
<strong>Attention:</strong>
If a heatmap seems to be representing only a part of your setup, it may be attributed to the animal not yet having explored most of it. To counteract this try allowing for a longer recording time. Once again do not be alarmed if the tail-based data doesn't look like the others, as tail-tracking usually has much worse accuracy than the other points.
</kbd>
</p>


