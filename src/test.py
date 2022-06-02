from PIL import Image, ImageOps, ImageDraw, ImageFont
import PIL
import argparse
import tempfile
import numpy as np
import matplotlib.pyplot as plt


def change_resolution2(filename):

    new_width = 52
    
    image = PIL.Image.open(filename)
    import pdb
    #pdb.set_trace()

    width_old, height_old = image.size
    new_height = round(height_old*new_width/width_old)
    width = 3508 # A4 width
    height = round(height_old*width/width_old)

    if (image.mode == 'RGBA'):
        image.load()
        r, g, b, a = image.split()
        image = Image.merge('RGB', (r,g,b))

    
    
    imageNEW = image.resize((new_width,new_height), resample=Image.NEAREST)

    imageNEW = imageNEW.resize((width,height), Image.NEAREST)

    
    imageNEW.save('pattern1.png')

    pattern = PIL.Image.open('pattern1.png')


    out = pattern.convert('P', palette=Image.ADAPTIVE, colors=6) 
    colors = out.convert("RGB").getcolors()
    
  

    #print(out.mode)

    out.save('pattern2.png')

    border = 100
    exp_img = ImageOps.expand(out.convert("RGB"), border, fill="white") 
    
    imgdraw = exp_img

    exp_img.save('pattern_expand.png')

    draw = ImageDraw.Draw(imgdraw)
    # draw on x axis
    for i in range (new_width):
        draw.line((i*(width/new_width)+border,0+border, i*(width/new_width)+border,height+border), fill="black", width=2)
    #draw on y axis
    for j in range (new_height):
        draw.line((0+border,j*(height/new_height)+border, width+border, j*(height/new_height)+border), fill="black", width=2)
    
    
    
    draw = ImageDraw.Draw(imgdraw)
    # draw border around image
    draw.line((border+0,border+0, border+0,border+height), fill="black", width=4)
    draw.line((border+0,border+0, border+width,border+0), fill="black", width=4)
    draw.line((border+width,border+0, border+width,border+height), fill="black", width=4)
    draw.line((border+0,border+height, border+width,border+height), fill="black", width=4)

    imgdraw.save('pattern3.png')


    print(width, height)

    # print numbers
    # x axis
    for i in range(new_width):
        draw = ImageDraw.Draw(imgdraw)
        font = ImageFont.truetype("arial.ttf", 40)
        draw.text(((border+10+i*(width/new_width)), border-50), str(i+1), (0,0,0), font=font)
        draw.text(((width+border-50-i*(width/new_width)), height+border+5), str(i+1), (0,0,0), font=font)


    # y axis
    for j in range(new_height):
        draw = ImageDraw.Draw(imgdraw)
        font = ImageFont.truetype("arial.ttf", 40)
        draw.text((border-55, border+10+j*(height/new_height)), str(j+1), (0,0,0), font=font)
        draw.text((width+border+15, height+border-50-j*(height/new_height)), str(j+1), (0,0,0), font=font)

    imgdraw.save('pattern4.png')


    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', type=str, default="butterfly.jpg")
    args = parser.parse_args()
    change_resolution2(args.filename)