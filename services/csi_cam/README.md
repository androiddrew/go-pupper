# CSI CAM

A service to provide a video stream over IP from a CSI camera.

## Requirements

**Note** if you want to check the contents of a .deb package before installing it use the commands
`apt download <package>` and then `dpkg -c <path to .deb>`.

This needs to run both on Raspbian and Ubuntu OS so that uses can use a Pi4 or a Jetson board so we will use the following
constraints: 
- [V4L2] will provide the driver that an application like [FFmpeg] will use to interface with the the video device at
 /dev/videoX.
- A program like [GStreamer] using the [FFmpeg/libav plug-in] can be used to pipeline video into a format suitable for 
an ip camera. In this way our cam will be offered as an IP streaming service from our control board. 

### Do we have V4L2?

[V4L2] Provides the driver that an application like [FFmpeg] we will use to interface with the video device 
at `/dev/videoX`. On Ubuntu this is available in the universe repository as `libv4l-0`. Because I want you to learn 
more about the software we are going to build our services on let's first check out the description of libv4l-0 with 
`apt show libv4l-0`. 

Since this is actually such a ubiquitous package my Ubuntu desktop already has this installed. You can view where the 
shared library `libv4l2.so` has been installed on your system using `dpkg`.

```
toor@ubuntu:/usr/lib/x86_64-linux-gnu$ dpkg -L libv4l-0
/.
/usr
/usr/lib
/usr/lib/x86_64-linux-gnu
/usr/lib/x86_64-linux-gnu/libv4l
/usr/lib/x86_64-linux-gnu/libv4l/plugins
/usr/lib/x86_64-linux-gnu/libv4l/plugins/libv4l-mplane.so
/usr/lib/x86_64-linux-gnu/libv4l/v4l1compat.so
/usr/lib/x86_64-linux-gnu/libv4l/v4l2convert.so
/usr/lib/x86_64-linux-gnu/libv4l1.so.0.0.0
/usr/lib/x86_64-linux-gnu/libv4l2.so.0.0.0
/usr/share
/usr/share/doc
/usr/share/doc/libv4l-0
/usr/share/doc/libv4l-0/README.Debian
/usr/share/doc/libv4l-0/README.gz
/usr/share/doc/libv4l-0/README.lib-multi-threading
/usr/share/doc/libv4l-0/README.libv4l.gz
/usr/share/doc/libv4l-0/TODO
/usr/share/doc/libv4l-0/copyright
/usr/share/lintian
/usr/share/lintian/overrides
/usr/share/lintian/overrides/libv4l-0
/usr/lib/x86_64-linux-gnu/libv4l1.so.0
/usr/lib/x86_64-linux-gnu/libv4l2.so.0
/usr/share/doc/libv4l-0/changelog.Debian.gz
```
 
We can make some tasks easier on ourselves with a series of utils built for v4l2. Let's look at `apt search v4l-utils`. 
This was not included on my system install so let's `sudo apt install v4l-utils`. If you didn't already have the 
libv4l-0 package installed, it will be installed as a dependency for the `v4l-utils`.

We can see that we have a new binary `/usr/bin/v4l-ctl` by checking listing the contents of the installed package again 
with `dpgk -L v4l-utils`. 

### Check the available video devices

We can check for a list of video devices identified by the kernel with:
```
ls -ltrh /dev/video*
```
This would be the case if you were using a CSI camera with the Pi or Jetson.

If the device is connected via usb use `lsusb`. If it's a PCI device you can find it with `lspci`.








### Resources
- [GStreamer on Pi]

### Raspbian


[FFmpeg]: https://en.wikipedia.org/wiki/FFmpeg
[V4L2]: https://en.wikipedia.org/wiki/Video4Linux
[GStreamer]: https://gstreamer.freedesktop.org/
[GStreamer on Pi]: https://platypus-boats.readthedocs.io/en/latest/source/rpi/video/video-streaming-gstreamer.html
[FFmpeg/libav plug-in]: https://gstreamer.freedesktop.org/documentation/libav/index.html?gi-language=c


