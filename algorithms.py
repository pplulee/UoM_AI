# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import cv2


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def dist_thresholding(des1, des2, threshold_value) -> list:
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=len(des1))
    result = []
    for m in matches:
        tmp = []
        for n in m:
            if threshold_value == -1:
                tmp.append(n)
            elif n.distance < threshold_value:
                tmp.append(n)
        result.append(tmp)
    return result


def nn(des1, des2, threshold_value) -> list:
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=1)
    result = []
    for m in matches:
        tmp = []
        for n in m:
            if threshold_value == -1:
                tmp.append(n)
            elif n.distance < threshold_value:
                tmp.append(n)
        result.append(tmp)
    return result


def nndr(des1, des2, threshold_value) -> list:
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)
    result = []
    for i in range(len(matches)):
        tmp = []
        if matches[i][0].distance < threshold_value * matches[i][1].distance:
            tmp.append(matches[i][0])
        result.append(tmp)
    return result

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# vim:set et sw=4 ts=4:
