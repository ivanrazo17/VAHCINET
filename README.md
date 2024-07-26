# VAHCINET: Voice Activated Human Computer Interaction using Convolutional Neural Networks Algorithm
Escobar, R. C., Razo, I. W., Tabusao, F. I

A Human-Computer Interaction system, with custom datasets trained in EdgeImpulse, by classifying 34 HCI-based voice commands to perform computer navigations utilizing Convolutional Neural Network (CNN) algorithm.
# Running using VAHCINET.py

To run the VAHCINET, open any IDE and run VAHCINET.py. 

PyAudio will run for 5 seconds to capture input voices and automatically navigates the computer based on the voice command.

# List of Voice Commands:
 - Open Microsoft Word
 - Exit Microsoft Word
 - Open Microsoft Excel
 - Exit Microsoft Excel
 - Open Powerpoint
 - Exit Powerpoint
 - Open Zoom App
 - Exit Zoom App
 - Open Google
 - Exit Google
 - Open Calculator
 - Exit Calculator
 - Open Calendar
 - Exit Calendar
 - Open File Manager
 - Exit File Manager
 - Open Sticky Notes
 - Exit Sticky Notes
 - Open Notepad
 - Exit Notepad
 - Open Camera
 - Exit Camera
 - Open Paint
 - Exit Paint
 - Open Voice Recorder
 - Exit Voice Recorder
 - Open Google and Search <User Define> (i.e. Cats)
 - Open Youtube and Search <User Define> (i.e. Cats)
 - Open Browser and Search <User Define> (i.e. Cats)
 - Save File
 - Open Folder Downloads
 - Open File Documents
 - Print 
 - Shutdown Computer

# Running your impulse using WebAssembly in Node.js

For more information see the documentation at https://docs.edgeimpulse.com/docs/through-webassembly

To run the impulse open a terminal or command prompt and run:

```
$ node run-impulse.js "-19.8800, -0.6900, 8.2300, -17.6600, -1.1300, 5.9700, ..."
```

(Where you replace `"-19.8800, -0.6900, 8.2300, -17.6600, -1.1300, 5.9700, ..."` with your features, as described above).

To get some hints on how to integrate this into your own application, see `run-impulse.js` and the documentation above.

## Edge Impulse for Linux

If you plan to run your impulse from Node.js you probably want to take a look at Edge Impulse for Linux (https://docs.edgeimpulse.com/docs/edge-impulse-for-linux). It offers full hardware acceleration, bindings to cameras and microphones, and Node.js bindings.
