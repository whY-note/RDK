import numpy as np
from typing import Any, Dict, List, Tuple, Optional, Sequence, Union

def rpy_to_rot(roll: float, pitch: float, yaw: float) -> np.ndarray:
    """
    Euler angles (roll, pitch, yaw) -> Rotation matrix

    Defined R = Rz(yaw) * Ry(pitch) * Rx(roll) 
    """
    R_x = np.array([
        1, 0, 0,
        0, np.cos(roll), -np.sin(roll),
        0, np.sin(roll), np.cos(roll)
    ],
    dtype=float).reshape((3,3))

    R_y = np.array([
        np.cos(pitch), 0, np.sin(pitch),
        0, 1, 0,
        -np.sin(pitch), 0, np.cos(pitch)
    ],
    dtype=float).reshape((3,3))
    
    R_z = np.array([
        np.cos(yaw), -np.sin(yaw), 0,
        np.sin(yaw), np.cos(yaw), 0,
        0, 0, 1
    ],
    dtype=float).reshape((3,3))

    rotation_mat = R_z @ R_y @ R_x

    return rotation_mat

def rot_to_rpy(rotation_matrix: np.ndarray) -> Tuple[float, float, float]:
    """
    Rotation matrix -> Euler angles (roll, pitch, yaw) 

    Defined R = Rz(yaw) * Ry(pitch) * Rx(roll) 
    """
    R = np.asarray(rotation_matrix, dtype=float)
    if abs(R[2,0]) < 1.0:
        # 如果 cos(pitch) != 0, 即 | sin(pitch) | < 1
        pitch = np.arcsin(-R[2,0])
        yaw = np.arctan2(R[1,0], R[0,0])
        roll = np.arctan2(R[2,1], R[2,2])
    else:
        # 如果 cos(pitch) == 0
        pitch = np.pi/2 if R[2,0] <= -1.0 else -np.pi/2
        roll = 0.0
        yaw = np.arctan2(-R[0,1], R[1,1])
    
    return roll, pitch, yaw
        
def rpy_to_quat(roll: float, pitch: float, yaw: float) -> np.ndarray:
    """
    Euler angles (roll, pitch, yaw) -> Quaternion
    """
    pass

def rot_to_quat(rotation_matrix: np.ndarray) -> np.ndarray:
    """
    Rotation matrix -> Quaternion
    """
    pass

def quaternion_normalize(q: np.ndarray) -> np.ndarray:
    q = np.asarray(q, dtype=float)
    norm = np.linalg.norm(q)
    if norm < 1e-8:
        raise ValueError("Zero-norm quaternion cannot be normalized")
    return q/norm

def quat_to_rot(q: np.ndarray) -> np.ndarray:
    """
    Quaternion -> Rotation matrix 
    """
    w,x,y,z = quaternion_normalize(q)
    R = np.array([
        [1 - 2*y**2 - 2*z**2, 2*x*y - 2*z*w,       2*x*z + 2*y*w],
        [2*x*y + 2*z*w,       1 - 2*x**2 - 2*z**2, 2*y*z - 2*x*w],
        [2*x*z - 2*y*w,       2*y*z + 2*x*w,       1 - 2*x**2 - 2*y**2] 
    ])
    return R

# def make_T(pos, rpy):
#     '''利用pos, rpy来创建变换矩阵'''

#     pass

if __name__ == "__main__":
    roll = np.pi/2
    pitch = 0
    yaw = 0

    rot = rpy_to_rot(roll,pitch,yaw)
    print(f"Rotation Matrix: {rot}")
    print(f"rpy: {rot_to_rpy(rot)}")



