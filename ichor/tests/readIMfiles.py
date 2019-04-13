import numpy as np
import matplotlib.pyplot as plt
from ichorlib.imClasses.IMSpectrum import IMSpectrum
import cv2
from skimage import data, io, filters, feature
from scipy import ndimage as ndi


def openAmphitriteProject(filename):
    """Open an Amphitrite data file, and check that the format
    is correct.

    :parameter filename: Absolute path to data file
    :returns: mzAxis, arrival time axis and intensity matrix as a list
    """
    try:
        dataList = np.load(filename)
        # mz axis, atd axis, intensity matrix
        return [dataList[0], dataList[1], dataList[2]]
    except:
        print('Opening amphitrite file failed: %s' % filename)
        return False


def plotHeatmapFromMatrix(matrix, x, y, ax=False, **kwargs):
    """Create a heatmap from provided information instead of using
    this object's properties.

    :parameter matrix: numpy array (intensity data)
    :parameter x: numpy array (m/z axis)
    :parameter y: numpy array (arrival time axis)
    :parameter ax: matplotlib Axes instance or boolean
    :parameter \*\*kwargs: matplotlib.pyplot.plot() arguments
    """
    if not ax:
        ax = plt
    ax.imshow(matrix, origin=[0, 0], aspect='auto',
              extent=[x.min(), x.max(), y.min(), y.max()], **kwargs)


file = '130508_cytc1_001.a'


im = IMSpectrum()
im.load_amphi_file(file)

matrix = im.matrix
mzAxis = im.xvals
atdAxis = im.atdaxis


submatrix1 = matrix[1:200,1550:1600]
submatrix2 = matrix[30:60,1:2000]


print(submatrix1)
print(np.average(submatrix1))
print(np.max(submatrix1))

grad = np.gradient(submatrix1)

print(grad[0])

fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(12, 4),
                                    sharex=False, sharey=False)


#plotHeatmapFromMatrix(submatrix1, mzAxis, atdAxis, ax=ax1)
ax1.imshow(submatrix1)
ax1.quiver(grad[0], grad[1])
#ax2.imshow(grad[0])
ax2.quiver(grad[0], grad[1])
#plotHeatmapFromMatrix(submatrix1, mzAxis, atdAxis, ax=ax2)
ax3.plot(im.xvals, im.yvals)


#fig.tight_layout()
plt.show()

# Load an color image in grayscale
#img = cv2.imread('figure_2.png',0)
#cv2.imshow('image',img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()


#img = cv2.imread('messi5.jpg',0)
#plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
#plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
#plt.show()
