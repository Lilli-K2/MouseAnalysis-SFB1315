This is the [network]() we have been using as we conduct our experiments. It is trained to track a <strong>single mouse</strong> based on <strong>four tracking points</strong> from a top-view in the dark under red light.
These points include the nose, neck, butt and tail of the animal. If your experiments were conducted under similar conditions and the network still doesn't recognize the mouse well enough consider retraining the pretrained network with more of your own video footage.

Save the pre-trained network to a location of your choice. In the config.yaml file change the project path to the correct file path you saved the file to.

</p>
<kbd>
<strong>Attention!</strong>
This network will obviously not work for your experiments if you are using multiple mice under different camera or lighting conditions or other animal species altogether. In this case refer to DeepLabCut to train your own network and adjust the ActiveMouse code according to the points you consider in your tracking.
</kbd>
</p>

