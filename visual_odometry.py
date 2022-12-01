#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from algorithms import dist_thresholding, nn, nndr
import numpy as np
import cv2

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

STAGE_FIRST_FRAME = 0
STAGE_SECOND_FRAME = 1
STAGE_DEFAULT_FRAME = 2
NUM_FEATURES = 1500
MATCHING_DIST_THRESHOLD = 1
MATCHING_NN = 2
MATCHING_NNDR = 3

lk_params = dict(winSize  = (21, 21),
                 criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))

def featureTracking(image_ref, image_cur, px_ref):
    kp2, st, err = cv2.calcOpticalFlowPyrLK(image_ref, image_cur, px_ref, None, **lk_params)
    st = st.reshape(st.shape[0])
    kp1 = px_ref[st == 1]
    kp2 = kp2[st == 1]
    return kp1, kp2


def featureMatching(image_ref, image_cur, matching_algorithm, threshold_value, feature_index, visualise) -> list:
    #The following line creates a SIFT detector
    detector = cv2.SIFT_create(nfeatures=NUM_FEATURES)

    #The following lines return a list of keypoints (kp) and a list of descriptors (des) for a given image
    kp1, des1 = detector.detectAndCompute(image_cur,None)
    kp2, des2 = detector.detectAndCompute(image_ref,None)

    visual_img = None
    my_matches = []

    if matching_algorithm == MATCHING_DIST_THRESHOLD:
        my_matches = dist_thresholding(des1, des2, threshold_value)
    elif matching_algorithm == MATCHING_NN:
        my_matches = nn(des1, des2, threshold_value)
    elif matching_algorithm == MATCHING_NNDR:
        my_matches = nndr(des1, des2, threshold_value)

    if visualise == True:
        visual_img = cv2.drawMatchesKnn(image_ref, kp1, image_cur, kp2, my_matches[:100], None, flags=2)
        cv2.imwrite('matches.png', visual_img)

    matches_list = getMatchesForFeature(my_matches, feature_index)
    return matches_list


#The following function returns a list of floats containing the Euclidean distance values of the feature matches returned by any of the three algorithms
def getMatchesForFeature(matches, feature_index) -> list:
    matches_list = []
    if feature_index >= len(matches):
        return None
    else:
        try:
            feature_matches = matches[feature_index]
            if type(feature_matches) is list:
                matches_list = [f.distance for f in feature_matches]
            else:
                matches_list = [feature_matches.distance]
        except:
            return []
        return matches_list

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class PinholeCamera:
    def __init__(self, width, height, fx, fy, cx, cy,
                k1=0.0, k2=0.0, p1=0.0, p2=0.0, k3=0.0):
        self.width = width
        self.height = height
        self.fx = fx
        self.fy = fy
        self.cx = cx
        self.cy = cy
        self.distortion = (abs(k1) > 0.0000001)
        self.d = [k1, k2, p1, p2, k3]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class VisualOdometry:
    def __init__(self, cam, annotations):
        self.frame_stage = 0
        self.cam = cam
        self.new_frame = None
        self.last_frame = None
        self.cur_R = None
        self.cur_t = None
        self.px_ref = None
        self.px_cur = None
        self.kps = None
        self.desc = None
        self.focal = cam.fx
        self.pp = (cam.cx, cam.cy)
        self.trueX, self.trueY, self.trueZ = 0, 0, 0
        self.detector =  cv2.SIFT_create(nfeatures=NUM_FEATURES)
        with open(annotations) as f:
            self.annotations = f.readlines()

    def getAbsoluteScale(self, frame_id):  #specialized for KITTI odometry dataset
        ss = self.annotations[frame_id-1].strip().split()
        x_prev = float(ss[3])
        y_prev = float(ss[7])
        z_prev = float(ss[11])
        ss = self.annotations[frame_id].strip().split()
        x = float(ss[3])
        y = float(ss[7])
        z = float(ss[11])
        self.trueX, self.trueY, self.trueZ = x, y, z
        return np.sqrt((x - x_prev)*(x - x_prev) + (y - y_prev)*(y - y_prev) + (z - z_prev)*(z - z_prev))

    def processFirstFrame(self):
        self.px_ref, self.desc = self.detector.detectAndCompute(self.new_frame, None)
        self.kps = self.px_ref
        self.px_ref = np.array([x.pt for x in self.px_ref], dtype=np.float32)
        self.frame_stage = STAGE_SECOND_FRAME
        return []

    def processSecondFrame(self, test_frame_id, matching_algorithm, threshold_value, feature_index, visualise):
        feature_matches = []
        self.px_ref, self.px_cur = featureTracking(self.last_frame, self.new_frame, self.px_ref)
        if (test_frame_id == 1):
            feature_matches = featureMatching(self.last_frame, self.new_frame, matching_algorithm, threshold_value, feature_index, visualise)
        E, mask = cv2.findEssentialMat(self.px_cur, self.px_ref, focal=self.focal, pp=self.pp, method=cv2.RANSAC, prob=0.999, threshold=1.0)
        _, self.cur_R, self.cur_t, mask = cv2.recoverPose(E, self.px_cur, self.px_ref, focal=self.focal, pp = self.pp)
        self.frame_stage = STAGE_DEFAULT_FRAME
        self.px_ref = self.px_cur
        return feature_matches

    def processFrame(self, frame_id, test_frame_id, matching_algorithm, threshold_value, feature_index, visualise):
        feature_matches = []
        self.px_ref, self.px_cur = featureTracking(self.last_frame, self.new_frame, self.px_ref)
        if (frame_id == test_frame_id):
            feature_matches = featureMatching(self.last_frame, self.new_frame, matching_algorithm, threshold_value, feature_index, visualise)
        E, mask = cv2.findEssentialMat(self.px_cur, self.px_ref, focal=self.focal, pp=self.pp, method=cv2.RANSAC, prob=0.999, threshold=1.0)
        _, R, t, mask = cv2.recoverPose(E, self.px_cur, self.px_ref, focal=self.focal, pp = self.pp)
        absolute_scale = self.getAbsoluteScale(frame_id)
        if(absolute_scale > 0.1):
            self.cur_t = self.cur_t + absolute_scale*self.cur_R.dot(t)
            self.cur_R = R.dot(self.cur_R)
        if(self.px_ref.shape[0] < NUM_FEATURES):
            self.px_cur, self.desc = self.detector.detectAndCompute(self.new_frame, None)
            self.kps = self.px_cur
            self.px_cur = np.array([x.pt for x in self.px_cur], dtype=np.float32)
        self.px_ref = self.px_cur
        return feature_matches

    def update(self, img, frame_id, test_frame_id, matching_algorithm, threshold_value, feature_index, visualise):
        feature_matches = []
        assert(img.ndim==2 and img.shape[0]==self.cam.height and img.shape[1]==self.cam.width), "Frame: provided image has not the same size as the camera model or image is not grayscale"
        if visualise == True:
            cv2.imshow('Road facing camera', img)
        self.new_frame = img
        if(self.frame_stage == STAGE_DEFAULT_FRAME):
            feature_matches = self.processFrame(frame_id, test_frame_id, matching_algorithm, threshold_value, feature_index, visualise)
        elif(self.frame_stage == STAGE_SECOND_FRAME):
            feature_matches = self.processSecondFrame(test_frame_id, matching_algorithm, threshold_value, feature_index, visualise)
        elif(self.frame_stage == STAGE_FIRST_FRAME):
            feature_matches = self.processFirstFrame()
        self.last_frame = self.new_frame
        return feature_matches

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# vim:set et sw=4 ts=4:
