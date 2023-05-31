import logging

import cv2
import numpy as np
from skimage.morphology import skeletonize

logger = logging.getLogger(__name__)


def process_image(image_path, lee_skeleton_path):
    image = cv2.imread(image_path)
    binary = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(binary, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    skeleton = skeletonize(binary // 255, method="lee")
    skel_image_opencv = np.asarray(skeleton, dtype=np.uint8) * 255
    cv2.imwrite(lee_skeleton_path, skel_image_opencv)
    return skeleton
