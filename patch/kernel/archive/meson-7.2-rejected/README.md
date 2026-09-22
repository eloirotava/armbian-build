# Not applied on linux-7.2.y

These patches from domin144 meson-6.16 failed dry-apply on 7.2.7.

Eth RMII clock tree (0018) and mpeg_rtc (0025) were rewritten as
`../meson-7.2/0099-meson8b-eth-rmii-and-mpeg-rtc-clocks-for-7.2.patch`.

CVBS PHY (0007) skipped for now (MXQ is HDMI). MMC/WiFi/timer/xhci
WiPs left out until needed.
