# meson-7.2 rejected patches (from meson-6.12)

These failed `patch -p1 -N` against `linux-7.2.y` after the applying set.
They are kept here for porting; Armbian does not read this directory.

Failed (12):
- DRM/HDMI: 0016, 0047, 0052, 0053, 0057
- Ethernet/clk: 0018, 0020, 0023, 0024, 0026, 0027
- PWM revert: generic-Revert-pwm-meson-...

First GHA target: the 41 patches in `../meson-7.2/` that apply cleanly.
