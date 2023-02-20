import numpy as np
import wfc


def wave_function_collapse(input_texture, x, y):
    # Create the wave function collapse object
    wfc = wfc.WaveFunctionCollapse(input_texture)

    # Set the size of the output pattern
    wfc.set_output_size(x, y)

    # Generate the output pattern
    output = wfc.generate()

    return output
