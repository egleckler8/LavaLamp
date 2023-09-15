import tkinter as tk
from lavalamp import LampGen

g = LampGen()

root = tk.Tk()
root.title('Lava Lamp Creator')

panel = tk.LabelFrame(root, text='Color')
 # I want to have an "artsy" controls and then an "advanced" controls
 # Artsy had few controls with parameters named ambiguosly, leaving more up to random
 # Advanced has all the possible parameters 


# Method for updating the variables
def updateVars(event=None):
    
    redValue = red_scale.get()
    greenValue = green_scale.get()
    blueValue = blue_scale.get()

    # c here will be a string in the format of a hex color so like #FF000
    c = str('#' + float_to_RGBhex_str(redValue) + float_to_RGBhex_str(greenValue) + float_to_RGBhex_str(blueValue))

    # This little statement causes the little color strip at the top of the panel to change... oh yeah ;)
    goButton.config(fg=c)
    color.config(bg=c)
    goButton.update()
    color.update


def generateArt(event=None):
    ''' Handles the art generation process when the goButton is clicked'''

    # Get the params from the relevant scales!!
    red_strength = red_scale.get()
    green_strength = green_scale.get()
    blue_strength = blue_scale.get()

    print(red_strength, blue_strength, green_strength)

    # Shut down all the widgets to preserve order during the generation just in case
    
    #fp = filepath_entry.get()
    fp = "/Users/eli/Desktop/noise-art/imgs/"

    try:
        g.createGIF(filepath=fp,
                    R_strength=red_strength, 
                    B_strength=blue_strength, 
                    G_strength=green_strength   )
    except Exception as e:
        print("ERROR ENCOUNTERED: " + e)

    


# Create all the widgets
red_scale = tk.Scale(panel, label='R', orient='vertical', from_=1.0, to=0.01, resolution=0.01, command=updateVars)
blue_scale = tk.Scale(panel, label='G', orient='vertical', from_=1.0, to=0.01, resolution=0.01, command=updateVars)
green_scale = tk.Scale(panel, label='B', orient='vertical', from_=1.0, to=0.01, resolution=0.01, command=updateVars)
color = tk.Label(panel, width=35, height=1, bg='white')
goButton = tk.Button(panel, width=8, height=8, text="Generate art", fg="white", command=generateArt)
filepath_entry = tk.Entry(panel, width=35, textvariable='Enter filepath to save GIF to')

# This is used in goButton to disable/re-enable all widgets



# Pack 'em up
filepath_entry.pack(side='bottom')
color.pack(side='top')
red_scale.pack(side='left')
blue_scale.pack(side='left')
green_scale.pack(side='left')
goButton.pack(side='bottom')

panel.pack()


def float_to_RGBhex_str(f):
    ''' Takes the float [0.0-1) and returns a two-char hex value string
        We can combine three of these to make the RGB hex value str
        Idk why tk.config(bg=) will not take an RGB tuple...
        But this is my solution...  '''
    
    hex_val = hex(int(255 * f))

    hex_val_str = str(hex_val)[2:] # everything after the first two characters to get rid of the 0x denoting hexademical
    if len(hex_val_str) < 2: # if it's single digit, we need to add a zero so we don't end up pass config(bg=) a 5-char str and getting an error
        hex_val_str = '0' + hex_val_str
    
    return hex_val_str


root.mainloop()


# size
# R, G, B [CHECK]
# chaos control (scale --> higher chaos = higher octaves)
# violence control (speed of stuff)
# buttons for gen by seed, gen by rand, gen by param ctrls
# checkboxes for color and scale swirls