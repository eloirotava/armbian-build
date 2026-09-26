# Not applied on linux-7.2.y

These patches from domin144 meson-6.16 failed dry-apply on 7.2.7.

Eth RMII clock tree (0018) and mpeg_rtc (0025) were rewritten as
`../meson-7.2/0099-meson8b-eth-rmii-and-mpeg-rtc-clocks-for-7.2.patch`.

CVBS PHY (0007) skipped for now (MXQ is HDMI). MMC/WiFi/timer/xhci
WiPs left out until needed.

Also already present in linux-7.2.y (Armbian fails on reverse-apply):
- 0001-mmc-meson-mx-sdhc-Use-devm_mmc_alloc_host-helper
- 0090-wifi-rtw88-re-enable-AP-and-ad-hoc-interface-modes

## Fora de propósito: o que o 6.12 que dá partida não tinha

A imagem 7.2 não passava da espera pela raiz no SD, sem erro claro. Estes
patches não existem no meson-6.12, que funciona na mesma MXQ, e mexem no
que trava um boot em silêncio. Saem até o 7.2 dar partida; depois voltam
um a um.

- 0091, 0092 pwm-regulator: o regulador PWM é o que dá a tensão da CPU
  (vcck) e do núcleo (vddee) na MXQ; o 0092 é um "FIXUP!" em andamento
- 0093 clocks de CVBS e HDMI ativos ao mesmo tempo (em andamento)
- 0080 mpll: muda o cálculo dos clocks derivados do MPLL

Sem eles o 7.2 deu partida pelo SD na MXQ (raiz montada, systemd, login;
SD sem avisos). O 0064 (HDMI) já voltou; os demais voltam um a um.
