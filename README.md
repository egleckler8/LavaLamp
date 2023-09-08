# LavaLamp
Psychedelic, procedurally generative art with Perlin noise. Generating an artistic product using only randomness and math was the goal of the project.

Look at some of the sample's in `art-samples` and you'll quickly understand the name `LavaLamp`!

Implements `noise.pnoise`, `Pillow`, and `numpy`, notably.

IF YOU RUN THIS PROGRAM:
Be warned, the image generation process can require many, many iterations. If you...
- Increase `img_size`
- Increase `total_frames`
- Increase the `octaves`, `persistence`, or `lacunarity` parameter
- Iteratively generate animations (e.g. `for i in range(500): createGif()`
  
You could experience wait times upwards of five minutes as your GIF generates... You could generate individual GIFs of size 50+ MB...

My MacBook has pretty good specs and an 800x800 animation still takes quite a while to generate for me! Optimizing the processes this program takes is always a work in progress, but python is sometimes just not the fastest. My intention was only to generate small-sized images, but I designed the program to be scalable to any-size images.

## TL;DR
Program pans through 3D Perlin noise, compiling many 2D slices into a list of frames that is saved as a GIF animation.

- The R, G, and B value in each pixel of each frame each correspond to one of three Perlin noise samples
- A loop iterates through a pixel map and sets each R, G, and B value at `(x, y)` to the noise value at `(x, y, z)` in a `pnoise3` sample, where `z` is fixed
- The program increments the `z` value in the 3D noise sample, slightly changing the values in the 2D slice and creates a new image, appending it to a list
- The list of these "frame" images is converted into an animated GIF using `Pillow`

## Inspirations

The inspiration for this project began with Minecraft.
This game has been the staple of an entire generation's childhood, and if you ask me, it's pretty amazing under the hood.

Each minecraft world is completely unique, generated randomly according to the rules of a mystical "seed."
What does this seed mean? How does it determine the location of every single geographical feautre of Minecraft?
Every cave and cliff, every desert and jungle, the depth of oceans, the height of mountains, and the seemingly infinite, winding networks of caves that all Minecraft players could probably admit getting lost in at some point.

Anyways, I was super curious so I found this youtube video: https://youtu.be/CSa5O6knuwI?feature=shared

By Henrik Kniberg, this extremely informative video delves into the math behind Minecraft's procedural terrain generation. Spoiler alert--careful manipulation of Perlin noise is the secret to Minecraft's lush, organic landscapes.

What is Perlin noise? --> https://en.wikipedia.org/wiki/Perlin_noise

Anyways, on to my project...

## My Project

Inspired by Minecraft's use of mathematical concepts to generate artful worlds, I decided to see what artsy application for Perlin noise I could come up with. Art and math seem like polar opposites, so it became my mission to combine them as effectively and beautifully as I think Minecraft did... (I'm a big nerd)

I started playing around with Perlin noise in matplotlib and seeing the textures I could form by adjusting the paramters, then decided to use Pillow instead, so I could manipulate pixelmaps of Perlin noise and add some color in. Of course, I decided to use the `noise` module's `noise.pnoise2(parameters)` function to access noise values at different points in the module's 2D Perlin noise, `pnoise2`, sample.

For the parameters of the `noise.pnoise2(parameters)`, there are several different values that change the texture of the noise. I recommend looking in the comments in my `lavalamp.py` file under the `createSample()` and `generateParams` functions for futher explanation. I pass a paramter list to the function that generates each array of Perlin noise values to basically "seed" the noise and adjust the paramters how I like. See the documentation in `lavalamp.py`!!

### 1 - Initial Methods: Black and White Images

We all know every pixel's color can be represented with an RGB value, so I started trying to manipulate the R, G, and B value of each pixel at the same noise by assigning each pixel a `pnoise2` value for each R, G, and B. So, my script used what I thought was three different `pnoise2` samples to genreate a... colorful image? I knew something was wrong when this method gave me black and white images.

Now may be a good time to interject--I used the numpy and Pillow librarys to create images. Here's the process (in pseudocode) that I used to create images with Perlin noise:

1. Choose a size of image to set as a constant --> `SIZE = 250` where the size is a 250x250 square for simplicity
2. Initialize an 2D zero array with `np.zeros`.
3. Set each point `(x, y)` of the array to the value at `pnoise2` `(x, y)`.
4. Repeat steps one and two three times to generate 3 total arrays of noise values, `sampleRed`, `sampleGreen`, `sampleBlue`. The names will make sense in a sec
5. Then, initialize a pixelmap using Pillow
6. Set the RGB value of each pixel in the map to `(sampleRed[x][y], sampleGreen[x][y], sampleBlue[x][y])`
7. Save the pixelmap to an image

Now, this was working great--except all my images were boring black and white. At this point I did some research and realized that `noise.pnoise2()` uses the same 2D Perlin noise sample of noise values and onlt adjusts the Perlin noise algorithm with the paremeters. In other words, this results in the all three of the (R, G, B) values in Step 6 to be the same, meaning each pixel was a shade of gray from (0, 0, 0) - (255, 255, 255).

### 2 - Introducing 3D Perlin noise

To overcome this artistic roadblock and get colorful images, I again took inspiration from Minecraft... this time, I tried (with great success) using 3D Perlin noise (`pnoise2`) instead of `pnoise2`. After all, Minecraft's terrain is 3D.

To circumvent the "sameness" of each `pnoise2` sample, I just used a `pnoise3` sample at different z-values for each `sampleRed`, `sampleGreen`, `sampleBlue` noise arrays. All the `pnoise3` samples are also the same, just as `pnoise2`, but one can easily cut them into 2D "slices" of (x,y) planes that will be all be different as long as the "slice" is taken from a different z-position in the 3D noise.

Boom, problem solved. Color acheived.

### 3 - MAD SCIENCE

Then, I got a crazy idea... Every z-slice of 3D Perlin noise is different, right? But, Perlin noise is smooth; so, adjacent z-slices should only be slightly different. If one were to generate a bunch of adjacent slices in sequence and them slap them together into a slideshow, they'd have a smooth animation! 

This is where things get really interesting... By adding the z-position of each noise sample to the list of parameters, it would be easy to generate a bunch of images, simply incrementing `z` a tiny bit every time, so that each image is a little bit different; each z-slice is shifted a little bit in the 3D noise field.

Using Pillow, it's easy to save a list of image files to a gif--I have to credit my script for this to ChatGPT. So, you just have to declare an int `total_frames` and append these steps to the pseudocode above to generate an animation:

8. Append the new image file to a list
9. Increment the `z` parameter in the paramter list to generate a slightly different 2D noise sample for the next frame
10. Repeat steps 2-9 `total_frames` times to generate a list of all frames
11. Save the list of image files to a gif

And just like that, we have a psychedlic gif!!

### 4 - MADDER SCIENCE

As stated above, each noise array (`sampleRed`, `sampleGreen`, `sampleBlue`) has a set of parameters that include `z`, their position in the 3D `pnoise2` field. Why would we only increment the `z` parameter? We could change the color and texture of each color's noise field throughout the animation! 

I'm still working on implementing this. It was easy to make the "swirling" happen, but there's some fine tuning to be done to the increment value of each of the parameters so that the program produces an artistic result every time, and not a blurry or grainy mess.

### 5 - Cleaning up the script

I liked the art my program was producing, so I decided to shift my attention to other ways I could improve this project. Some ideas came to mind, but they all involved user interfaces... So I decided to turn my `lavalamp.py` into a veritable python module and add a class for `LampGen` that could be imported and used to generate little gifs with little to no tinkering around in the orignial code.

Thus, I went through the arduous task of turning the whole file into classes and functions and doing a whole lot of debugging

## Future of this Project

Here are some of my ideas for where this project could go:

### 1 - GUI & User Control of Paramters

It would be super practical if a user could just click a button that said "generate art." On top of this, it would enchance the "artistic experience" in some ways if they could manually tinker with the all the parameters behind each image and play around with making the kind of LavaLamp animation that they personally think is cool. Generating random GIFs is cool, but having control over the result is probably a more attractive feature for users who want to generate art.

I'll definitely be using `tkinter` for this GUI. Nothing too fancy!! The fanciness is all in the generated image.

In the GUI, I'm working on adding:
1. "Create art" button
3. User input save location
4. Sliders and entries for every paramter
5. Tutorial/tooltips explaining how to get the result one desires
6. Checkboxes for enabling/disabling different features like color swirl, noise swirl, etc.
7. Multiple "design menus." e.g. "Basic," "Advanced," etc. Give users the option between being possibly overwhelmed with controlling all paramters, and having the option to control only the few, most influential ones.
8. Preview popup of image before saving to computer?
