from skimage.io import imread
from skimage.filters import threshold_otsu
import matplotlib.pyplot as plt
import imutils
from skimage import measure
from skimage.measure import regionprops
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def fromVideo():
    filename = 'video1.mp4'
    import cv2
    cap = cv2.VideoCapture(filename)
    count = 0
    while cap.isOpened():
        ret,frame = cap.read()
        if ret == True:
            #cv2.imshow('video-frame',frame)
            cv2.imwrite("output/frame%d.jpg" % count, frame)
            count = count + 1
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()

    imgwithplate = imread("output/frame%d.jpg"%(count-1), as_gray=True)
    imgwithplate = imutils.rotate(imgwithplate, 270)
    return imgwithplate


#if from video
#imgwithplate=fromVideo()
#if from image
imgwithplate = imread("11.jpg", as_gray=True)

#Converting into gray if not
gray_imgwithplate = imgwithplate * 255
fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.imshow(gray_imgwithplate, cmap="gray")

#COnverting to binary using otsu threshold
thresholdval = threshold_otsu(gray_imgwithplate)
binary_imgwithplate = gray_imgwithplate > thresholdval
ax2.imshow(binary_imgwithplate, cmap="gray")
plt.show()

#all the connected regions and groups them together
labelimg = measure.label(binary_imgwithplate)

#maximum width, height and minimum width and height of a license plate(Assumed)
#Have taken 3%-8% height of image as assumed height and 15%-30% as width
assumed_plate_dim = (0.03*labelimg.shape[0], 0.08*labelimg.shape[0], 0.15*labelimg.shape[1], 0.3*labelimg.shape[1])
#Have taken 8%-20% height of image as assumed height and 15%-40% as width
assumed_plate_dim2 = (0.08*labelimg.shape[0], 0.2*labelimg.shape[0], 0.15*labelimg.shape[1], 0.4*labelimg.shape[1])
min_height, max_height, min_width, max_width = assumed_plate_dim
plate_coordinates = []
plate_similar = []

fig, (ax1) = plt.subplots(1)
ax1.imshow(gray_imgwithplate, cmap="gray")
flag =0

#Extracting the proper license area out of all the predicted regions
for region in regionprops(labelimg):
    if region.area < 50:
        continue
    min_row, min_col, max_row, max_col = region.bbox
    height = max_row - min_row
    width = max_col - min_col

    # checking if the region satisfies the condition of our assumed size
    if height >= min_height and height <= max_height and width >= min_width and width <= max_width and width > height:
        flag = 1
        plate_similar.append(binary_imgwithplate[min_row:max_row,
                                  min_col:max_col])
        plate_coordinates.append((min_row, min_col,
                                         max_row, max_col))
        border = patches.Rectangle((min_col, min_row), max_col - min_col, max_row - min_row, edgecolor="blue",
                                       linewidth=2, fill=False)
        ax1.add_patch(border)
if(flag == 1):
    plt.show()

#if not satisfied take another assumed region
if(flag==0):
    min_height, max_height, min_width, max_width = assumed_plate_dim2
    plate_coordinates = []
    plate_similar = []
    fig, (ax1) = plt.subplots(1)
    ax1.imshow(gray_imgwithplate, cmap="gray")
    for region in regionprops(labelimg):
        if region.area < 50:
            continue
        min_row, min_col, max_row, max_col = region.bbox
        height = max_row - min_row
        width = max_col - min_col
        if height >= min_height and height <= max_height and width >= min_width and width <= max_width and width > height:
            plate_similar.append(binary_imgwithplate[min_row:max_row,
                                      min_col:max_col])
            plate_coordinates.append((min_row, min_col,
                                             max_row, max_col))
            border = patches.Rectangle((min_col, min_row), max_col - min_col, max_row - min_row, edgecolor="red",
                                           linewidth=2, fill=False)
            ax1.add_patch(border)
    plt.show()
