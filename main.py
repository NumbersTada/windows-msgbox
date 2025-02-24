import customtkinter as ctk
from PIL import Image,ImageDraw,ImageFont

# WARNING: this formatting is so bad bruh :sob:

def drawBox(image,position,width,height,tl,bl,tr,br,xu,xd,yl,yr):
    x,y=position
    image.paste(tl,(x,y))
    image.paste(bl,(x,y+height-bl.height))
    image.paste(tr,(x+width-tr.width,y))
    image.paste(br,(x+width-br.width,y+height-br.height))
    image.paste(xu.resize((width-(tl.width+tr.width),xu.height)),(x+tl.width,y))
    image.paste(xd.resize((width-(bl.width+br.width),xd.height)),(x+bl.width,y+height-xd.height))
    image.paste(yl.resize((yl.width,height-(tl.height+bl.height))),(x,y+tl.height))
    image.paste(yr.resize((yr.width,height-(tr.height+br.height))),(x+width-yr.width,y+tr.height))

def drawBold(draw,position,text,fill="#ffffff",font=ImageFont.load_default()):
    spacing=1
    x,y=position
    bbox=font.getbbox(text)
    w,h=bbox[2]-bbox[0],bbox[3]-bbox[1]
    for char in text:
        draw.text((x,y),char,fill=fill,font=font)
        draw.text((x+1,y),char,fill=fill,font=font)
        charWidth,_=draw.textbbox((0,0),char,font=font)[2:4]
        x+=charWidth+spacing

def getTextCenterCoords(draw,position,text,font=ImageFont.load_default()):
    x,y=position
    bbox=draw.textbbox((x,y),text,font=font)
    w,h=bbox[2]-bbox[0],bbox[3]-bbox[1]
    x-=w//2
    y-=h//2
    return x,y
def getRectCenterCoords(position,width,height):
    x,y=position
    x-=width//2
    y-=height//2
    return x,y

font=ImageFont.truetype("tahoma.ttf",16)
tl=Image.open("box/00.png")
bl=Image.open("box/01.png")
tr=Image.open("box/10.png")
br=Image.open("box/11.png")
xu=Image.open("box/x0.png")
xd=Image.open("box/x1.png")
yl=Image.open("box/y0.png")
yr=Image.open("box/y1.png")

def drawMessageBox(title,message,buttonTitle,icon="info"):
    width,height=75,108

    bbox=ImageDraw.Draw(Image.new("RGB",(2000,15))).textbbox((0,0),message,font=font)
    textWidth,textHeight=bbox[2]-bbox[0],bbox[3]-bbox[1]
    width+=textWidth
    height+=textHeight
    image=Image.new("RGBA",(width,height),"#d4d0c8")
    draw=ImageDraw.Draw(image)

    drawBox(image,(0,0),width,height,tl,bl,tr,br,xu,xd,yl,yr)

    close=Image.open("close.png")
    button=Image.open("button.png")
    icon=Image.open(f"{icon}.png")
    draw.rectangle(((tl.width,tl.height),(width-tr.width-1,tr.height+17)),fill="#000080")
    image.paste(close,(width-tr.width-close.width-2,tr.height+2),close.convert("RGBA").getchannel("A"))

    drawBold(draw,(6,6),title,fill="#ffffff",font=font)
    draw.text((65,42),message,fill="#000000",font=font)
    x,y=getTextCenterCoords(draw,(width//2,height-29),buttonTitle,font=font)
    image.paste(button,getRectCenterCoords((width//2,height-26),75,23),button.convert("RGBA").getchannel("A"))
    draw.text((x,y),buttonTitle,fill="#000000",font=font)
    image.paste(icon,(13,32),icon.convert("RGBA").getchannel("A"))
    return image

if __name__=="__main__":
    msg="Hello! This is a program that generates images\n"\
        "of Windows 2000 message boxes. Please download\n"\
        "all of the images provided, because they're\n"\
        "needed to create the final image. Use the\n"\
        "drawMessageBox function to create a Pillow image\n"\
        "object with the message box."
    image=drawMessageBox("NumbersTada",msg,"OK",icon="info")
    image.save("message.png")
    def click(event): app.destroy()

    app=ctk.CTk()
    cX,cY=getRectCenterCoords((app.winfo_screenwidth()//2,app.winfo_screenheight()//2),image.width,image.height)
    app.geometry(f"{image.width}x{image.height}+{cX}+{cY}")
    app.overrideredirect(True)
    ctkImage=ctk.CTkImage(image,size=(image.width,image.height))
    ctk.CTkLabel(app,text="",image=ctkImage).pack(fill="both",expand=True)
    app.bind("<Button-1>",click)
    app.mainloop()
