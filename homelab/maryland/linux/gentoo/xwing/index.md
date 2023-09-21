# xwing
This is my main laptop, an LG Gram 14", with a 10th gen i7 (I forget what year. 2020 maybe?)

## Install steps
* I used my script Gentrine (https://github.com/SomethingGeneric/gentrine)
    * I had to update the Stage3 tarball in the script
    * I also had to manually install Grub, which is weird because the script should have done that for me.

## Other strange things
* All of the steps to get my DWM stack running (https://github.com/SomethingGeneric/suckless) were found in portage repos
* genkernel didn't find all of the toggles in the kernel config for my trackpad, but I was able to hunt them down with help from a friend.
    * For future reference, it was basically everything for I2C and USB HID/I2C built as modules.
* Since this Gram is a Tiger Lake device, I had to install `sof-firmware` for audio.
* Otherwise, all device drivers worked except for the fingerprint reader (Goodix doesn't have drivers for this specific one on *any* linux flavor)