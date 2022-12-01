#!/usr/bin/env python3
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import sys
import os.path
from typing import List
import numpy as np
import cv2

from visual_odometry import PinholeCamera, VisualOdometry

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

image_dataset_path = ''
max_frame = 500
test_frame_id = -1
matching_algorithm = 1
threshold_value = -1
feature_index = -1

def drive_car(
    image_dataset_path: str,  frame_id: int,  matching_algo: int, threshold: float, feature_index: int, visualise: bool) -> List:
    cam = PinholeCamera(1241.0, 376.0, 718.8560, 718.8560, 607.1928, 185.2157)
    vo = VisualOdometry(cam, os.path.join(image_dataset_path, 'poses', '00.txt'))
    traj = np.zeros((600,600,3), dtype=np.uint8)
    max_frame = frame_id + 1

    my_matches = None

    for img_id in range(max_frame):
        img = cv2.imread(os.path.join(image_dataset_path, 'gray', '00', 'image_0', str(img_id).zfill(6)+'.png'), 0)

        matches = vo.update(img, img_id, frame_id, matching_algo, threshold, feature_index, visualise)
        if img_id == frame_id:
            my_matches = matches

        cur_t = vo.cur_t
        if(img_id > 2):
            x, y, z = cur_t[0], cur_t[1], cur_t[2]
        else:
            x, y, z = 0., 0., 0.
        draw_x, draw_y = int(x)+290, int(z)+90
        true_x, true_y = int(vo.trueX)+290, int(vo.trueZ)+90

        cv2.circle(traj, (draw_x,draw_y), 1, (0, 255, 0), 1)
        cv2.circle(traj, (true_x,true_y), 1, (0, 0, 255), 1)
        cv2.rectangle(traj, (10, 20), (600, 60), (0,0,0), -1)
        text = "Coordinates: x=%2fm y=%2fm z=%2fm"%(x,y,z)
        cv2.putText(traj, text, (20,40), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1, 8)

        if visualise == True:
            cv2.imshow('Trajectory', traj)
            cv2.waitKey(1)

    return my_matches


def view_trajectory(image_dataset_path: str):
    drive_car(image_dataset_path, max_frame, matching_algorithm, threshold_value, feature_index, True)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Debug
if __name__ == '__main__':
    if len(sys.argv) > 2:
        sys.argv[2] = "'{}'".format( os.path.expanduser(sys.argv[2]) )
        cmd = "{}({})".format(sys.argv[1], ",".join(sys.argv[2:]))
        print("debug run:", cmd)
        ret = eval(cmd)
        print("ret value:", ret)
    else:
        sys.stderr.write("Usage: run_VO.py view_trajectory <dataset_path>\n")
        sys.stderr.write("   Or: run_VO.py drive_car <dataset_path> <frame_id> <matching_algo> <threshold> <feature_number> <visualise>\n")
        sys.exit(1)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# vim:set et sw=4 ts=4:
