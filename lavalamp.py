from PIL import Image
import numpy as np
import noise
import random
import time
import json
import os
from typing import Tuple, List, Any


# The image is a square, so this is the size of each side in pixels. Feel free to change!
# Bigger is cooler, but remember that it might take a LOT longer to process...
# I still need to work on optimizing this program


class LampGen:
    """
    This class contains all the code necessary to generate a trippy, swirly animation.
    Default size is 256x256, default frames is 50.

    Parameters:
        size:   a 2-tuple with the size of the images this generator
                will create in pixels (width, height)
        frames: the number of frames of the gifs this generator will create

    """

    # DEFAULTS
    def __init__(self, size: Tuple[int, int] = (256, 256), frames=50):
        self.img_width = size[0]
        self.img_height = size[1]
        self.total_frames = frames

    def create_sample(self, p: List[int | float | Any]):
        """
        Creates a random 3D perlin noise field.

        Parameters:
            p: list of parameters for the perlin noise field

        Return:
            An np array with a perlin noise field.
            REMEMBER - accessing it will be sample[row][column], which
            might be confused with x and y... really, the rows are the y/height
            of the image and the columns are the x/width of the image.

        """

        scale = p[0]  # Adjust this value to control the "zoom" of the noise
        octaves = p[1]  # Number of layers of noise to combine
        persistence = p[2]  # Controls the increase in amplitude with each octave
        lacunarity = p[3]  # Controls the increase in frequency with each octave
        z = p[4]    # we use a 2D "slice" of a 3d noise field at a random z-coordinate
        weight = p[5]  # this is how strong the noise layer will come through in the final image as a percentage

        # EXPLANATION OF THIS PART OF THE PROGRAM

        # Notice the sample is initialized as a 2D array
        # We'll end up creating a sample for every frame of the animation, and each frame is obviously 2D
        # The sample array represents the R, G, and B values (3 sets of 3D noise fields for the image)
        # We'll initialize the array to zeros, then use nested for loops to set each point in the array
        # to the value of a pnoise3 sample at the corresponding x, y, z (while z is fixed, x and y vary)

        # Why don't use the z value? That's because the z value only changes between each frame of the animation.
        # This shifting z value gives us the swirly effect. Imagine cutting a cube of
        # swiss cheese into a bunch of little slices...
        # Each "frame" of our animation is one of those slices.
        # The transition between each slice is smooth, since Perlin noise is smooth
        # Exactly like cheese! Our "motion" is just tracing the "holes" of the swiss cheese, if that makes sense.
        # So, the loop that later makes each frame will submit a different parameter list p to this function
        # Each iteration of the loop will submit a slightly different p,
        # the only difference being a slightly incremented p
        # Well, we might play around with other parameters too... but that's for later notes... ;)
        # The z-increment is the "width" of our slice, think "dz" from calculus

        # We'll end up making "total_frames" frames (50 is default) for each R, G, and B.
        # This means we'll call this function 3 * total_frames times.
        # Calling the pnoise() function so many times could be expensive, depending on the parameters
        # e.g. higher octaves value usually takes longer to process

        # Again, this is the chunk of the program that is the most expensive.
        # We're iterating over every pixel in every frame 3 times (R, G, and B)!!
        # So, the total time it takes to create every frame heavily depends on image size and total frames.
        # Increasing image size by a factor of 2 (e.g. 200x200 --> 400x400) increases the
        # runtime of this part by at least 4x! (excluding other factors)

        # Anyway... here we go with the initialization of the zeroes array
        rows = self.img_height
        columns = self.img_width
        sample = np.zeros((rows, columns))

        # Next we'll set each index of the array to a noise value
        for x in range(columns):
            for y in range(rows):

                noise_value = noise.pnoise3(x / scale,
                                            y / scale,
                                            z,
                                            octaves=octaves,
                                            persistence=persistence,
                                            lacunarity=lacunarity)

                # This little calculation determines how much this noise layer will shine though
                # Since each noise layer corresponds to the R, G, or B of each pixel,
                # this is how one could change the "mood" of their LampGen
                # Yeah the weight basically changes the color of the whole thing
                # Everything is multiplied by 256 to make the sample's noise fit into RGB
                # INTERESTING FACT: Pillow wraps negative RBG values around;
                # and RGB of -10 will be read as 255 - 10 = 245 basically, so no need to abs() the noise_value
                sample[y][x] = 256 * weight * noise_value

        return sample

    def create_swirl(self, amplitude=1.0):
        """
        Returns a list of smooth noise values to create swirls.
        We'll use this function to control the parameter swirls, like if we want the scale to change
        frame by frame, or lacunarity, etc. This gives us a smooth, random change so each GIF stays completely.
        unique. We could've used math.sin() or something to give a smooth wave, but the fun here is that it's random

        Amplitude controls... well, yeah... Amplitude defaults at 1, which means the step values will range 0-1
        """

        swirl_noise = np.zeros(self.total_frames)

        for x in range(self.total_frames):
            # this 0.888 is SUPER IMPORTANT because perlin noise always is 0 at int values!!
            noise_value = noise.pnoise1(x - 0.888, octaves=6)
            swirl_noise[x] = amplitude * noise_value

        return swirl_noise

    @staticmethod
    def rand_seed():
        """

        A Random 3-item list of 17-digit numbers, the first 16 digits of which are used.
        It must have a range that extends to 17-digit so that the second digit can vary freely between 0 and 9.
        In other words, we generate a list of numbers where 16 digits vary 1-9

       """

        # We should seed the random thing so each lavalamp is
        # created uniquely, even in quick succession...
        rand_seed = int.from_bytes(os.urandom(16), byteorder='big') + int(time.time() * 1e6)
        random.seed(rand_seed)

        seed = []
        for i in range(3):
            seed.append(random.randint(10000000000000000, 19999999999999999))

        time.sleep(0.01)

        return seed

    @staticmethod
    def generate_params(seed):
        """

        This method returns a parameter list for an image using a seed as an input.
               
        IMPORTANT: THE SEED SHOULD BE A 17-DIGIT NUMBER FOR THIS TO WORK AS INTENDED!
        This program will mostly just use the above rand_seed, but if a "user choice" seed feature is ever implemented,
        We'll need to code in a workaround to getting a seed like "1234" or "dog." Just like Minecraft... :)

        p[0] = scale -  How "zoomed in" the noise is. RANGE = (10.0, 210.0), MU ≅ 110.0

        p[1] = octaves - how many overtones are added to smooth the noise. RANGE = (1, 11), MU ≅ 6.00

        p[2] = persistence - the relative amplitude of each next octave. RANGE = (0, 0.95), MU ≅ 0.475

        p[3] = lacunarity - the relative frequency of each next octave. RANGE = (1.0, 4.0), MU ≅  2.50

        p[4] = z value - where it "starts" in the 3D field. RANGE = (0.0, 1.0), MU ≅ 0.50

        p[5] = strength - how powerful the noise field is. RANGE = (0.0, 1.0), MU ≅ 0.50

        """

        # uses the last three digits
        scale = 10 + 200 * (seed % (10 ** 3)) / (10.0 ** 3)  # RANGE = (10.0, 210.0), MU ≅ 110.0
        # scale = 110 # for testing purposes

        # uses the fourth digit as an int, so the range of octaves is 3-12. Keeping octaves
        # decently low reduces processing time
        octaves = 1 + (seed % (10 ** 4)) / (10.0 ** 3)  # RANGE = (1, 11), MU ≅ 6.00
        # octaves = 6 # for testing purposes

        # uses the last 7 digits to create a number between 0 and 0.9. The last four digits are repeats,
        # but this doesn't matter much because their decimal place is insignificant
        persistence = (seed % (10 ** 7)) / (10.0 ** 7)  # RANGE = (0, 1), MU ≅ 0.5
        # persistence = 0.5 # for testing purposes

        # uses the last 10 digits as a number between 0 and 1
        lacunarity = 1 + 3 * (seed % (10 ** 10)) / (10.0 ** 10)  # RANGE = (1.0, 4.0), MU ≅  2.50
        # lacunarity = 2.50 # for testing purposes

        # uses all the digits, but mainly the 11th & 12th, as a number between 0 and 1
        z = (seed % (10 ** 12)) / (10.0 ** 12)  # RANGE = (0.0, 1.0), MU ≅ 0.50
        # z = 0.5 # for testing purposes

        # uses the first three digits as a number between 0 and 1
        strength = (seed % (10 ** 15)) / (10.0 ** 15)  # RANGE = (0.0, 1.0), MU ≅ 0.50
        # strength = 0.5 # for testing purposes

        # This is important, since the noise module will take only ints for the octaves value
        # In createSample(), the xyz coordinates must be ints, as they represent pixels,
        # and they are divided by scale, so scale must be int
        scale = int(scale)
        octaves = int(octaves)

        return [scale, octaves, persistence, lacunarity, z, strength]

    def create_gif(self, s=None, filepath=""):
        """

        Creates trippy gif and saves it.

       By default, the gif is generated using a random seed and saved to the working directory
       Also by default, the randSeed() method is called to generate a seed. Eventually, I hope to write
       a function to be called below that converts any input seed into the (17dig, 17dig, 17dig) mess we
       currently require... Additionally, I'd love to find a way to make the seed super compact but retain the
       unfathomable randomness of 3 very large random numbers.

       This is the primary method that will be called by users of the LampGen class.
       It's the only one we need to ever look at outside of this class!!! Yay!
       Makes it easy for anyone to call the method and make their own generative art.

       Parameters:
       s (3-item list of 17-digit numbers...)  A seed for the image
       filepath (string): the filepath where the gif will be saved.


       Return:
        A json object with the data of the generated gif
        Formatted like:

            {
                "filename":<filename>,
                "size":     {
                                "width":<pixel width>,
                                "height":<pixel height>,
                            },
                "gen_time":<time it took to generate>,
                "seed":     {
                                "r_seed":<red layer seed,
                                "g_seed":<green layer seed,
                                "b_seed":<blue layer seed
                            },
                "params":   {
                                "r_params":<red layer parameters>,
                                "g_params":<green layer parameters>,
                                "b_params":<blue layer parameters>
                            }
            }

        """

        # Let's keep track of how long this takes
        before = time.perf_counter()

        # Right here is where some future "seed converter" method would go.
        # I'd write seed = convertSeed(s) and it'd guarantee the seed works
        # no matter what the user inputs.

        # If nothing is supplied to the default, we'll generate a random seed
        # If something is, then use it, by golly!
        if s is None:
            seed = self.rand_seed()
        else:
            seed = s

        # Create a new blank image with a specified size and color mode
        image = Image.new("RGB", (self.img_width, self.img_height), "black")

        # Turn the image into a 3D NumPy array
        # The array is in the form (height, width, RGB)
        # That is, the first two dimensions are width and height with length img_size
        # The value at each (width, height) is set by the noise sample we'll create
        image_bitmap = np.array(image)

        # Using the seeds, generate the parameters for each color noise layer
        # Basically, the first term in the seed list goes to Red
        # Second goes to Blue, third to Green
        # And from those seeds we generate the params for the noise field for each color. Phew!
        params = [self.generate_params(seed[0]), self.generate_params(seed[1]), self.generate_params(seed[2])]

        # just for references in terminal
        print("Seed: " + str(seed))
        print("Parameters: " + str(params))

        # This is where the image files for each frame will be opened and stored to as they are generated
        frame_files = []

        # Send user a message to let them know what's up
        print("Generating gif...")

        # Create the files for each frame using our createSample() function
        # and add each trippy, colorful frame to a list of all the files
        for i in range(self.total_frames):

            # Each of these three 2D pnoise samples will correspond to the R, G, or B
            # (order respective) or each pixel in the image
            # These three lines should take the runtime of 3 * total_frames * ((img_size**2) * noise complexity)
            # Where "noise complexity" is the time it takes to access one sample of the noise module's pnoise3
            # With the parameters given as list p. This can vary based on the value of some parameters.
            sample_red = self.create_sample(params[0])
            sample_green = self.create_sample(params[1])
            sample_blue = self.create_sample(params[2])

            # This loop sets the color every pixel in the image (now a 3D np array, the 3rd D is the 3-term RGB array)
            # This is the part that actually binds each pixel of the image pixel map to an RGB value!
            for row in range(self.img_height):
                for column in range(self.img_width):
                    # map[x][y] sets the z dimension of the map
                    # The z dimension, according the PIL library, is to be 3 term lists of (R, G, B) values
                    # So here we finally colorize the image!!
                    image_bitmap[row][column] = (
                                                 sample_red[row][column],
                                                 sample_green[row][column],
                                                 sample_blue[row][column]
                                                 )

            # The following code turns the np array, fully colorized, to an image files
            # and appends it to the frame_files array
            # Later, we'll turn frame_files into a gif!
            frame = Image.fromarray(image_bitmap)
            frame_files.append(frame)

            # *** MODULATION STATION ***
            # To give the swirly motion, this code shifts the z value of each parameter array
            # a little bit between each frame
            # Remember, we're still in a for loop!
            # Because the noise we're using for each of the RGB fields is actually a
            # 2D slice (at a random pos.) of a fixed 3D noise field,
            # Incrementer the z parameter will slowly swipe through the 3D field and
            # give the impression of smooth, swirly, smoke-like motion
            # Added color shifting (param[5]) too!
            # Think of slices of swiss cheese, like earlier.
            # Or, go back to the createSample() function to clarify. It's explained in detail there a little more.

            # COMMENTED OUR FOR NOW... THESE FEATURES MAY RETURN
            # NO SWIRLING YET... WE'LL BE WORKING ON THIS
            # This creates the smooth noise pattern for the color swirl effect.
            # Adjust amplitude so it is large enough to noticeably affect RGB
            # color_swirl = createSwirl()
            # scale_swirl = createSwirl(20)

            for param in params:
                # param[0] += scale_swirl[i]
                param[4] += 0.04

                # This little conditional makes sure the RGB values don't go
                # negative or over 255 and reverse, ruining the smoothness of the piece
                # step = color_swirl[i]
                # if step < param[5] or param[5] + step > 255:
                # param[5] += color_swirl[i]

        # Saves the array of frames as a gif!
        # My reasoning for the arguably obnoxious filename:
        # When custom seeding is implemented, I want each image to be recreatable if possible
        # I didn't want to have to go into the file notes, etc. and edit because I want this
        # program to be compatible on all operating systems with python3
        filename = f"IMG[{seed[0]}, {seed[1]}, {seed[2]}]-[{time.time()}].gif"
        fp = filepath + '/' + filename
        gen_time = 0
        # print(fp)

        try:
            # Thanks to ChatGPT for teaching me how to use Pillow to save a list of images as a gif
            frame_files[0].save(fp, save_all=True, append_images=frame_files[1:], duration=100,
                                loop=0)  # 0 means infinite loop

            # Check the time
            after = time.perf_counter()
            gen_time = after - before

            print(
                f"***************************************************"
                f"***************************************************\n"
                f"Image successfully generated; it is now located at:\n  {fp}\n"
                f"Generation time: {gen_time}\n"
                f"***************************************************"
                f"***************************************************")
        except Exception as e:
            print(
                f"***************************************************"
                f"***************************************************\n"
                f" ERROR: {e}\n  Image could not be generated.\n"
                f"***************************************************"
                f"***************************************************")

        # Now, let's craft the return json object.
        data = {
            "filename": filename,
            "size": {
                "width": self.img_width,
                "height": self.img_height,
            },
            "gen_time": gen_time,
            "seed": {
                "r_seed": seed[0],
                "g_seed": seed[1],
                "b_seed": seed[2]
            },
            "params": {
                "r_params": params[0],
                "g_params": params[1],
                "b_params": params[2]
            }
        }

        return json.dumps(data)
