# IMPORTANT: READ ME... UP HERE!!!

# This is currently a big testing ground for an eventual GUI for the lavalamp!
# The idea is, users will be able to manually edit every paramter of every noise field
# Using sliders and entrys, and create a precise image to their own liking.

# I'll eventually try to link together the lavalamp generator and this GUI.
# It shouldn't be too hard, since the LampGen has already been turned into a class,
# making it relatively scalable. Hell, we could make 888888 images using a loop. 

# That's dannnngerous territory though! You could seriously clog up someone's storage.
# Maybe in the future I'll add a pop up that asks "are you sure you want to make these?"
# Or maybe I'll also add a loading bar and try to calculate expected wait time for each image.

# I could do data analytics on my own program?!?!? Yo...
# Using a machine learning model to predict generation time 
# based on noise field paramters, total_frames, and img_size...?

# I could multithread to train the model, starting an extra thread with a timer when
# the image generation script begins, then stopping them both at the same time and storing
# a list of how long each image takes paired up with their paramters.

# I'm just journaling right now... Anyways...
# Point is, this project has potential to grow in scale--it's a big work in progress
# This file is just a testing ground for new GUI ideas. 

# Feel free to run it and see what's going on.


import tkinter as tk

REFRESH_RATE = 0.1

root = tk.Tk()
root.title('Lava Lamp Creator')

panel = tk.LabelFrame(root, text='Color')
 # I want to have an "artsy" controls and then an "advanced" controls
 # Artsy had few controls with parameters named ambiguosly, leaving more up to random
 # Advanced has all the possible parameters 


# Create all the widgets
color = tk.Canvas(panel, background='#FF0000', width=200, height=10)

scale_scale = tk.Scale(panel, label='S', orient='vertical', from_=210, to=10, command=lambda scale: updateVar(scale_scale))
octaves_scale = tk.Scale(panel, label='O', orient='vertical', from_=11, to=1, command=lambda scale: updateVar(octaves_scale))
persistence_scale = tk.Scale(panel, label='P', orient='vertical', from_=1.0, to=0.0, resolution=0.01, command=lambda scale: updateVar(persistence_scale))
lacunarity_scale = tk.Scale(panel, label='L', orient='vertical', from_=4.0, to=1.0, resolution=0.01, command=lambda scale: updateVar(lacunarity_scale))
strength_scale = tk.Scale(panel, label='Str', orient='horizontal', from_=0.0, to=1.0, resolution=0.01, command=lambda scale: updateVar(strength_scale))
# No z-scale because that's a little redundant? You want each image to be unqiue



# Pack 'em up
color.pack(side='top')
strength_scale.pack(side='top')
scale_scale.pack(side='left')
persistence_scale.pack(side='left')
lacunarity_scale.pack(side='left')
panel.pack()

strength_scale.set(0.5)
scale_scale.set(110)
persistence_scale.set(0.5)
lacunarity_scale.set(2.5)

# These should go on the 'master' tab
#color_swirl_check = tk.Checkbutton(panel, text='Color Swirl')
#scale_swirl_check = tk.Checkbutton(panel, text='Scale Swirl')
#color_swirl_check.pack(side='bottom')
#scale_swirl_check.pack(side='bottom')

# Here's the code for how the sliders will adjust the variables, then send them off to the LavaLamp generator
scale = 110
octaves = 6
persistence = 0.5
lacunarity = 2.5
strength = 0.5

varMap = {  scale_scale: scale,
            octaves_scale: octaves,
            persistence_scale: persistence,
            lacunarity_scale: lacunarity,
            strength_scale: strength        }


def updateVar(w):
    ''' Takes the widget object input and changes the valuable of the variable it's assigned to using the varMap dict
    
        This banks on the tkinter widget having a 'get' method! Thankfully, both Entry and Scale do. The var must be casted to a float
        because when it is passed to the LampGen, it will be required to be a float. Entry's get() gets a string, so we have to convert
        to float. Also, we don't want the user typing words in the Entry! That's why we catch the ValueError exception '''
    
    try:
        varMap[w] = w.get()
    except ValueError:
        print('Please enter an number!')
    
    # This little statement causes the little color strip at the top of the panel to change... oh yeah ;)
    if w == strength_scale:
        hex_val = hex(int(255 * varMap[w]))

        hex_val_str = str(hex_val)[2:] # everything after the first two characters to get rid of the 0x denoting hexademical
        if len(hex_val_str) < 2: # if it's single digit, we need to add a zero so we don't end up pass config(bg=) a 5-char str and getting an error
            hex_val_str = '0' + hex_val_str

        color.config(background=str('#' + hex_val_str + '0000'))
        color.update()

def entrySet(w):
    pass




def updateScale(s):
    pass







root.mainloop()


# size
# R, G, B
# chaos control (scale --> higher chaos = higher octaves)
# violence control (speed of stuff)
# buttons for gen by seed, gen by rand, gen by param ctrls
# checkboxes for color and scale swirls