import numpy as np
from skimage.transform import resize
from skimage import measure
from skimage.measure import regionprops
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import platedetection


license_plate = np.invert(platedetection.plate_similar[0])
labelled_plate = measure.label(license_plate)

fig, ax1 = plt.subplots(1)
ax1.imshow(license_plate, cmap="gray")

char_dims = (0.35*license_plate.shape[0], 0.60*license_plate.shape[0], 0.05*license_plate.shape[1], 0.15*license_plate.shape[1])
min_height, max_height, min_width, max_width = char_dims

characters = []
counter=0
column_list = []
for regions in regionprops(labelled_plate):
    y0, x0, y1, x1 = regions.bbox
    height = y1 - y0
    width = x1 - x0

    if height > min_height and height < max_height and width > min_width and width < max_width:
        roi = license_plate[y0:y1, x0:x1]
        border = patches.Rectangle((x0, y0), x1 - x0, y1 - y0, edgecolor="blue",
                                       linewidth=2, fill=False)
        ax1.add_patch(border)
        resized_char = resize(roi, (20, 20))
        characters.append(resized_char)
        column_list.append(x0)

plt.show()
