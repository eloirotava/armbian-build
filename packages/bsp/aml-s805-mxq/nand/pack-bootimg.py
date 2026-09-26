#!/usr/bin/env python3
"""Monta o boot.img no formato Android que o storeboot do u-boot do
fabricante sabe ler.  Mesmo formato e mesmas checagens do
scripts/make-nand-image.sh do fork ws1508, so que alimentado por arquivos
soltos em vez de uma imagem de disco."""
import hashlib, struct, sys, zlib

if len(sys.argv) != 6:
    sys.exit("uso: pack-bootimg.py <uImage> <initrd.img> <dtb> <saida> <nome>")

kernel_p, ramdisk_p, second_p, out_p, name = sys.argv[1:6]
page = 0x800
kernel, ramdisk, second = (open(p, 'rb').read()
                           for p in (kernel_p, ramdisk_p, second_p))

# bootm acha o kernel com um "+ 0x800" fixo, entao a pagina tem que ser 2048.
if kernel[:4] != b'\x27\x05\x19\x56':
    sys.exit("kernel nao e uImage legado (magic errado): bootm nao acha o entry point")

# Conferir tamanho e CRC do uImage, nao so o magic.
#
# Isto existe porque uma copia truncada do uImage passou por aqui sem um
# pio: o cabecalho declarava 12.800.512 bytes e o arquivo tinha 12.533.696.
# O bootm calcula o CRC sobre o tamanho DECLARADO, leu alem do fim, o CRC
# nao bateu, ele abortou, e o storeboot caiu em recovery -- o "Android
# morto" na tela. Tres tentativas foram gastas procurando em enderecos de
# carga e tamanho de imagem antes de alguem conferir o obvio.
hsize, hcrc = struct.unpack('>I', kernel[12:16])[0], struct.unpack('>I', kernel[4:8])[0]
if len(kernel) - 64 != hsize:
    sys.exit(f"uImage truncado ou com sobra: cabecalho diz {hsize} bytes de "
             f"dados, arquivo tem {len(kernel) - 64}")
if zlib.crc32(kernel[64:]) & 0xffffffff != struct.unpack('>I', kernel[24:28])[0]:
    sys.exit("CRC dos dados do uImage nao confere")
hdr_zero = kernel[:4] + b'\x00\x00\x00\x00' + kernel[8:64]
if zlib.crc32(hdr_zero) & 0xffffffff != hcrc:
    sys.exit("CRC do cabecalho do uImage nao confere")
if second[:4] != b'\xd0\x0d\xfe\xed':
    sys.exit("segundo estagio nao e um dtb (magic errado)")
if ramdisk[:4] == b'\x27\x05\x19\x56':
    sys.exit("ramdisk e uInitrd; bootm nao desembrulha -- use o initrd.img cru")

def pad(b):
    return b + b'\x00' * (-len(b) % page)

# Enderecos de carga.  A primeira versao usava base 0, copiada do script do
# fork ws1508 -- outra placa, outro build de u-boot -- e a caixa nao deu
# video nenhum.  A imagem de fabrica desta caixa (o balbes 3.10.99 que
# estava na particao boot) usa base 0x10000000 com os deslocamentos
# padrao do Android, e e ela que este u-boot aceita:
BASE = 0x10000000

hdr  = b'ANDROID!'
hdr += struct.pack('<10I',
                   len(kernel),  BASE + 0x00008000,
                   len(ramdisk), BASE + 0x01000000,
                   len(second),  BASE + 0x00f00000,
                   BASE + 0x00000100,
                   page, 0, 0)
hdr += b''.ljust(16, b'\x00')           # name: vazio, como o de fabrica
hdr += b''.ljust(512, b'\x00')          # cmdline vazio: vem do env do u-boot

# id: SHA1 sobre cada parte e seu tamanho, como o mkbootimg faz.  O de
# fabrica vem preenchido; deixar zerado era mais uma diferenca gratuita.
sha = hashlib.sha1()
for blob in (kernel, ramdisk, second):
    sha.update(blob)
    sha.update(struct.pack('<I', len(blob)))
hdr += sha.digest().ljust(32, b'\x00')[:32]

with open(out_p, 'wb') as f:
    for blob in (hdr, kernel, ramdisk, second):
        f.write(pad(blob))

print("kernel=%d ramdisk=%d dtb=%d -> %s" %
      (len(kernel), len(ramdisk), len(second), out_p))
