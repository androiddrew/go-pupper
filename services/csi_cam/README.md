# CSI CAM

A service to provide a ffmpeg video stream over IP from a CSI camera.

## Requirements

**Note** if you want to check the contents of a .deb package before installing it use the commands
`apt download <package>` and then `dpkg -c <path to .deb>`.

### Constraints

This needs to run both on Raspbian and Ubuntu OS so that uses can use a Pi4 or a Jetson board so we will use the following
constraints: 

- [V4L2] will provide the driver that an application like [FFmpeg] will use to interface with the the video device at
 /dev/videoX.
- A program like [GStreamer] using the [FFmpeg/libav plug-in] can be used to pipeline video into a format suitable for 
an ip camera. In this way our cam will be offered as an IP streaming service, which can be integrated into our control 
software.

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

On my raspberry pi I used `v4l2-ctl --list-devices`

```
pi@pupper(rw):~$ /usr/bin/v4l2-ctl --list-devices
bcm2835-codec-decode (platform:bcm2835-codec):
	/dev/video10
	/dev/video11
	/dev/video12

mmal service 16.1 (platform:bcm2835-v4l2):
	/dev/video0
```

### Check for Gstreamer

We can check if gstreamer is available in the repos available on our system under `/etc/apt/sources.list` or 
`/etc/apt/sources.list.d/`.

`sudo apt list | grep gstreamer`

Likewise we can check if it is installed

`sudo apt list --installed | grep gstreamer`

On Raspbian I didn't have any of the gstreamer libs installed. The gstreamer website recommends a lot of packages that 
totaled to 900+MB. I don't believe we need to successfully build our service. Since we are focusing on python3 services 
let's start with the python3 gstreamer bindings which will installed a minimum number of package dependencies including 
the core gstreamer libs. We are also going to install `gstreamer1.0-tools` which provides the `gst-launch-1.0` binary.
```
sudo apt show python3-gst-1.0 gstreamer1.0-tools
sud apt install python3-gst-1.0 gstreamer1.0-too

# Might also need
gstreamer1.0-plugins-bad
```
raspivid -fps 26 -h 450 -w 600 -vf -n -t 5 -b 200000 -o ~/sample_video
### What can the camera do?

We can use `v4l2-ctl --list-formats-ext` to check the camera's capabilities.



### Resources
- [GStreamer on Pi]

### Raspbian troubleshooting

#### The datetime on my Pupper isnt' correct

The raspberry pi that powers my Pupper is consistently reporting the wrong time. It's July 2020:
```
pi@pupper(rw):~$ timedatectl status
               Local time: Thu 2019-02-14 08:25:02 EST
           Universal time: Thu 2019-02-14 13:25:02 UTC
                 RTC time: n/a
                Time zone: America/Detroit (EST, -0500)
System clock synchronized: no
              NTP service: inactive
          RTC in local TZ: no
```
This is causing some issues with the certs validation used when running `sudo apt update` or a `pip install` command. 
Notice that NTP service is inactive. Use `man timedatectl` to check out all of the management goodness. I could set the 
time manually  `sudo timedatectl set-time 'Y:M:D HH:mm:ss'` but this isn't persistent across boots for me.

Checking the journalctl messages for the service I see that the read only filesystem causing problems:
```
pi@pupper(ro):~$ sudo journalctl | grep systemd-timesyncd.servic
Feb 14 05:12:01 pupper systemd[356]: systemd-timesyncd.service: Failed to set up special execution directory in /var/lib: Read-only file system
Feb 14 05:12:01 pupper systemd[356]: systemd-timesyncd.service: Failed at step STATE_DIRECTORY spawning /lib/systemd/systemd-timesyncd: Read-only file system
Feb 14 05:12:01 pupper systemd[1]: systemd-timesyncd.service: Main process exited, code=exited, status=238/STATE_DIRECTORY
Feb 14 05:12:01 pupper systemd[1]: systemd-timesyncd.service: Failed with result 'exit-code'.
Feb 14 05:12:01 pupper systemd[1]: systemd-timesyncd.service: Service has no hold-off time (RestartSec=0), scheduling restart.
Feb 14 05:12:01 pupper systemd[1]: systemd-timesyncd.service: Scheduled restart job, restart counter is at 1.
```

With a little googling it appears that the systemd unit file for timesyncd


[FFmpeg]: https://en.wikipedia.org/wiki/FFmpeg
[V4L2]: https://en.wikipedia.org/wiki/Video4Linux
[GStreamer]: https://gstreamer.freedesktop.org/
[GStreamer on Pi]: https://platypus-boats.readthedocs.io/en/latest/source/rpi/video/video-streaming-gstreamer.html
[FFmpeg/libav plug-in]: https://gstreamer.freedesktop.org/documentation/libav/index.html?gi-language=c

[Time sync for Pi]:https://raspberrytips.com/time-sync-raspberry-pi/
[Read only filesystem for Pi]: https://medium.com/swlh/make-your-raspberry-pi-file-system-read-only-raspbian-buster-c558694de79
