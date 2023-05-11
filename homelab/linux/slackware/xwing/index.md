# xwing
This is my main laptop, (but it's not running Slack anymore), an LG Gram 14", with a 10th gen i7 (I forget what year. 2020 maybe?)

## Install steps
* I don't remember exactly what I selected, I believe it was "terse"
* I selected XFCE and not KDE, otherwise it was pretty much defaults

## Other strange things
* As I recall, most of the steps to get my DWM stack running (https://github.com/SomethingGeneric/suckless) were programs already in repos
* Some were installed through sbopkg though. (https://sbopkg.org/)
* Since this Gram is a Tiger Lake device, I had to install `sof-firmware` for audio. (Can't remember if that was in slackpkg, sbopkg, or from source)
* Otherwise, all device drivers worked except for the fingerprint reader (Goodix doesn't have drivers for this specific one on *any* linux flavor)