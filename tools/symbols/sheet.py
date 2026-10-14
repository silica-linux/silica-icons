import os, sys, io, resvg_py
# Usage: python sheet.py sheet.png [px] [light|regular|semibold]
if len(sys.argv) > 3:
    os.environ['SILICA_SYMBOL_WEIGHT'] = sys.argv[3]
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0,'.')
import importlib, symbols as S
def _inter():
    import glob, os
    found = [os.environ.get('INTER_FONT', '')]
    here = os.path.dirname(os.path.abspath(__file__))
    found += glob.glob(os.path.join(here, '../../../silica-ui/fonts/Inter-Regular.ttf'))
    found += glob.glob(os.path.expanduser('~/.pub-cache/git/silica-ui-*/fonts/Inter-Regular.ttf'))
    return next((p for p in found if p and os.path.exists(p)), None)
FONT = _inter()
def render(name, px, sw=None, color='#000'):
    sw = S.WSW if sw is None else sw
    png = resvg_py.svg_to_bytes(svg_string=S.svg(name, sw=sw, color=color, size=px))
    return Image.open(io.BytesIO(bytes(png))).convert('RGBA')
def sheet(out, px=72, dark=False, cols=10):
    names=[n for c, _ in S.CATS for n in S.SYM if S.CAT[n] == c]
    bg=(30,30,32) if dark else (255,255,255); fg='#fff' if dark else '#000'
    cw, ch = px+40, px+34
    rows=(len(names)+cols-1)//cols
    im=Image.new('RGB',(cols*cw+20, rows*ch+20),bg); d=ImageDraw.Draw(im)
    fnt=ImageFont.truetype(FONT,11)
    for i,n in enumerate(names):
        x=10+(i%cols)*cw+20; y=10+(i//cols)*ch
        d.rectangle([x-1,y-1,x+px,y+px],outline=(80,80,80) if dark else (225,225,225))
        im.paste(render(n,px,color=fg),(x,y),render(n,px,color=fg))
        d.text((x+px/2,y+px+4),n,fill=(150,150,150),font=fnt,anchor='mt')
    im.save(out)
if __name__=='__main__':
    sheet(sys.argv[1], int(sys.argv[2]) if len(sys.argv)>2 else 72)
