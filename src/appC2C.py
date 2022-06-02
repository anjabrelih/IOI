# C2C pattern generation application
# Anja Brelih
# ab0555@student.uni-lj.si

import streamlit as st
from PIL import Image, ImageOps, ImageDraw, ImageFont
from io import BytesIO




def main():
    select_box = st.sidebar.selectbox('Menu', ('About application','C2C pattern generator','Video'))

    if select_box =='About application':
        Instructions()
    if select_box == 'C2C pattern generator':
        uploadImage()
    if select_box == 'Video':
        video()


def Instructions():
    st.header("C2C crochet pattern generation")
    st.write("This web applicaiton will generate you a corner-2-corner pattern from your image!")
    st.write("Under C2C pattern generator you can upload your photo and create pattern with selected size and number of colors. You can see video instructions under section Video.")
    st.write("Project was created as a school project at University of Ljubljana, Faculty of Computer and Information Science for course Interaction and Information design.")

    st.image('fri.png', use_column_width=True)


def uploadImage():
    st.header("Generate pattern")
    image = st.file_uploader("Upload your image", type=["png", "jpg", "jpeg"])
    show_file = st.empty()

    if image is not None:
        show_file.image(image)
        imgdraw = patternGenerator(image)
        if st.button('Generate pattern'):
            st.image(imgdraw, use_column_width=True) 

            # Download
            img_byte_arr = BytesIO()
            imgdraw.save(img_byte_arr, format='PDF')
            img_byte_arr = img_byte_arr.getvalue()
            st.download_button(label="Download pattern", data=img_byte_arr, file_name="pattern.pdf" ,mime="image/pdf")


def video():
    st.header("Video instructions")


    video_file = open("appC2c_video.mp4", "rb")
    video_bytes = video_file.read()
    st.video(video_bytes)


def patternGenerator(image):

    image = Image.open(image)

    width_old, height_old = image.size
    
    # Input pattern size
    new_width = st.slider("Change pattern size", min_value = 30, max_value = 90)
    new_height = round(height_old*new_width/width_old)

    # Set a standard size for the output
    width = 3508 # A4 width
    height = round(height_old*width/width_old)

    if (image.mode == 'RGBA'):
        image.load()
        r, g, b, a = image.split()
        image = Image.merge('RGB', (r,g,b))

    # Resize to reduce number of pixels
    imageNEW = image.resize((new_width,new_height), resample=Image.NEAREST)
    pattern = imageNEW.resize((width,height), Image.NEAREST)

    # Input number of colors
    no_colors = st.slider("Change number of colors", min_value = 2, max_value = 15)

    # Convert image to pallet to recude number of colors
    out = pattern.convert('P', palette=Image.ADAPTIVE, colors=no_colors+1)
    colors = out.convert("RGB").getcolors()
    #st.write(colors)

    # Expand image border
    border = 100
    imgdraw = ImageOps.expand(out.convert("RGB"), border, fill="white") #img needs to be converted to RBG otherwise image becomes black

    # Draw grid
    draw = ImageDraw.Draw(imgdraw)
    # draw on X axis
    for i in range (new_width):
        draw.line((i*(width/new_width)+border,0+border, i*(width/new_width)+border,height+border), fill="black", width=2)
    #draw on Y axis
    for j in range (new_height):
        draw.line((0+border,j*(height/new_height)+border, width+border, j*(height/new_height)+border), fill="black", width=2)
    # draw border around image
    draw.line((border+0,border+0, border+0,border+height), fill="black", width=4)
    draw.line((border+0,border+0, border+width,border+0), fill="black", width=4)
    draw.line((border+width,border+0, border+width,border+height), fill="black", width=4)
    draw.line((border+0,border+height, border+width,border+height), fill="black", width=4)

    # Print numbers
     # x axis
    for i in range(new_width):
        draw = ImageDraw.Draw(imgdraw)
        font = ImageFont.truetype("arial.ttf", round(30+(30/new_width)))
        draw.text(((border+0.2*(width/new_width)+i*(width/new_width)), border-50), str(i+1), (0,0,0), font=font)  #(border+10+i*(width/new_width)), border-50)
        draw.text(((width+border-0.75*(width/new_width)-i*(width/new_width)), height+border+5), str(i+1), (0,0,0), font=font) #(width+border-40-i*(width/new_width)), height+border+5)
    # y axis
    for j in range(new_height):
        draw = ImageDraw.Draw(imgdraw)
        font = ImageFont.truetype("arial.ttf", round(30+(30/new_width)))
        draw.text((border-55, border+0.2*(height/new_height)+j*(height/new_height)), str(j+1), (0,0,0), font=font)   #(border-55, border+10+j*(height/new_height)
        draw.text((width+border+15, height+border-0.7*(height/new_height)-j*(height/new_height)), str(j+1), (0,0,0), font=font)  #(width+border+15, height+border-40-j*(height/new_height))

    #st.image(imgdraw, use_column_width=True)
    return(imgdraw)


main()