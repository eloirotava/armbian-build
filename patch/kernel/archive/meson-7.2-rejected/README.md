# Not applied on linux-7.2.y

These patches from domin144 meson-6.16 failed dry-apply on 7.2.7.

Eth RMII clock tree (0018) and mpeg_rtc (0025) were rewritten as
`../meson-7.2/0099-meson8b-eth-rmii-and-mpeg-rtc-clocks-for-7.2.patch`.

CVBS PHY (0007) was ported to 7.2 and moved back to ../meson-7.2: 0052
makes the HHI regmap optional, and without 0007 meson_venc_init still
wrote the CVBS DAC through it (NULL on Meson8b, oops at bind). The timer WiP (0087) and its revert (0088) cancel out and stay here.
Ported to 7.2 and moved back to ../meson-7.2:
- 0077 xhci Etron GPIO: the Makefile gained xhci-pci-prom21 at that spot
- 0089 rtw88 sdio TX work: 7.2 allocated tx_handler_data with kmalloc_obj
Already in linux-7.2.y, nothing to port: 0082-0085 (the meson-mx-sdio
regmap, clock and disabled-child rework).

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
- 0080 mpll: muda o cálculo dos clocks derivados do MPLL

Sem eles o 7.2 deu partida pelo SD na MXQ (raiz montada, systemd, login;
SD sem avisos). O 0064 (HDMI) e o 0093 (clocks de vídeo) já voltaram; os demais voltam
um a um.
