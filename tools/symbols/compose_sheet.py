import sys
from PIL import Image, ImageDraw, ImageFont
import symbols as S
FONT='/Users/emanuelefrascella/Progetti/silica/packages/silica_ui/fonts/Inter-Regular.ttf'
names=[n for c, _ in S.CATS for n in S.SYM if S.CAT[n] == c]
def load(n,k):
    im=Image.open(f'export/png/{n}@{"0.2x" if k==1 else "0.4x"}.png').convert('RGBA')
    return im
def tint(im,rgb):
    a=im.split()[3]; out=Image.new('RGBA',im.size,rgb+(0,)); out.putalpha(a); return out
def section(k,dark):
    bg=(30,30,32) if dark else (255,255,255); fg=(255,255,255) if dark else (0,0,0)
    fs=13*k; cols=8; cw=200*k; rh=34*k
    W=cols*cw+40*k; H=(len(names)+cols-1)//cols*rh+60*k
    im=Image.new('RGB',(W,H),bg); d=ImageDraw.Draw(im)
    font=ImageFont.truetype(FONT,fs)
    d.text((20*k,14*k),f'{k}× · Inter {fs}px · simboli medium (tela {13*1.4126*k:.1f}px) esportati da Sketch',fill=(140,140,145),font=font)
    asc=font.getmetrics()[0]
    for i,n in enumerate(names):
        x=20*k+(i%cols)*cw; y=50*k+(i//cols)*rh
        base=y+asc; capc=base-0.3638*fs
        sym=tint(load(n,k),fg)
        sx=x; sy=round(capc-sym.size[1]/2)
        im.paste(sym,(sx,sy),sym)
        d.text((x+sym.size[0]+5*k,y),n,fill=fg,font=font)
    return im
out=[]
for dark in (False,True):
    a=section(1,dark); b=section(2,dark)
    W=max(a.size[0],b.size[0]); H=a.size[1]+b.size[1]
    im=Image.new('RGB',(W,H),(30,30,32) if dark else (255,255,255)); im.paste(a,(0,0)); im.paste(b,(0,a.size[1]))
    im.save(f'sheet-{"dark" if dark else "light"}.png')
