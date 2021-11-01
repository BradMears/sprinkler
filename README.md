# sprinkler
Automation of the Open Sprinkler Pi (OSPI) hardware &amp; software

The Open Sprinkler Pi project (https://opensprinkler.com/product/opensprinkler-pi/) is a great product for controlling a home's sprinkler system. It provides a browser interface to automate the sprinkler schedule. However, one thing it doesn't help with is the process of blowing out the lines in preparation for winter. That's what this project is all about.

To blow out the lines, you turn off the water and hook up an air compressor to the main line. Then you open each zone (aka line) and let the air rush through there for some period of time. Opening a zone is done by triggering a relay which in turn opens the valve for that zone. The OSPI browser interface provides an easy way to open and close these valves. You can do this in the browser but you can also do it with wget, which is what my script does.

The only complicating factor with this task is that my air compressor is woefully undersized. It empties its small air tank before a zone has been completely purged. Professional sprinkler service companies use an enormous compressor that can easily keep ahead of the load imposed by a typical sprinkler system. To work around this limitation, I have to open a valve, let the air blow until the compressor is depleted, turn off the valve, let the compressor refill, re-open the valve, etc, etc until the entire system is purged.

To make this easier, I had to find a way to let my software know that the compressor was refilling and to close the sprinkler valve while that was happening. Since my cheap air compressor didn't come with a serial, Wi-Fi, or Bluetooth interface, I improvised one. I put a current sensor on the compressor's AC line, fed that signal to a rectifier, and then fed the resulting DC signal through a 3.3V voltage regulator. Voila - I had a reasonably clean signal that was compatible with the Rasperry Pi's GPIO pins. Once I had that, it was pretty simple to automate the entire process.

There were other ways to detect whether the compressor waas running. A vibration sensor could detect the motor turning. A microphone could pick up the increase in ambient noise. A webcam and OpenCV could read the pressure gauge. But I wanted to do it with the current sensor. It was pretty straight forward and works well.
