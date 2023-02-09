import os
import pandas as pd
import numpy as np
from typing import Tuple, List, Dict
import hashlib
from collections.abc import Iterable


def find_images(
        root: str,
        img_extensions: Tuple[str, ...] = ('.png', '.jpg', '.jpeg')
        ) -> pd.DataFrame:
    """Finds all image files in folder and subfolders.

    Args:
        root (str): The root folder where to look for images.
        img_extensions (Tuple[str, ...], optional): Image extensions to look for, by default ('.png', '.jpg', '.jpeg').

    Returns:
        Dataframe of relative paths of the images.
    """

    data = [] 
    for path, directories, files in os.walk(root):
        for file in files:
            if file.lower().endswith(tuple(img_extensions)):
                data.append({'path': os.path.relpath(path, start=root), 'file': file})
    return pd.DataFrame(data)

def create_id(string_col: pd.Series) -> pd.Series:
    """Creates unique ids from string based on MD5 hash.

    Args:
        string_col (pd.Series): List of ids.

    Returns:
        List of encoded ids.
    """

    entity_id = string_col.apply(lambda x: hashlib.md5(x.encode()).hexdigest()[:16])
    assert len(entity_id.unique()) == len(entity_id)
    return entity_id

def bbox_segmentation(bbox: List[float]) -> List[float]:
    """Convert bounding box to segmentation.

    Args:
        bbox (List[float]): Bounding box in the form [x, y, w, h].

    Returns:
        Segmentation mask in the form [x1, y1, x2, y2, ...].
    """

    return [bbox[0], bbox[1], bbox[0]+bbox[2], bbox[1], bbox[0]+bbox[2], bbox[1]+bbox[3], bbox[0], bbox[1]+bbox[3], bbox[0], bbox[1]]

def segmentation_bbox(segmentation: List[float]) -> List[float]:
    """Convert segmentation to bounding box.

    Args:
        segmentation (List[float]): Segmentation mask in the form [x1, y1, x2, y2, ...].

    Returns:
        Bounding box in the form [x, y, w, h].
    """

    x = segmentation[0::2]
    y = segmentation[1::2]
    x_min = np.min(x)
    x_max = np.max(x)
    y_min = np.min(y)
    y_max = np.max(y)
    return [x_min, y_min, x_max-x_min, y_max-y_min]

def is_annotation_bbox(
        segmentation: List[float],
        bbox: List[float],
        tol: float = 0
        ) -> bool:
    """Checks whether segmentation is bounding box.

    Args:
        segmentation (List[float]): Segmentation mask in the form [x1, y1, x2, y2, ...].
        bbox (List[float]): Bounding box in the form [x, y, w, h].
        tol (float, optional): Tolerance for difference.

    Returns:
        True if segmentation is bounding box within tolerance.
    """

    bbox_seg = bbox_segmentation(bbox)
    if len(segmentation) == len(bbox_seg):
        for x, y in zip(segmentation, bbox_seg):
            if abs(x-y) > tol:
                return False
    else:
        return False
    return True

def convert_keypoint(
        keypoint: List[float],
        keypoints_names: List[str]
        ) -> Dict[str, object]:
    # TODO: check if used. if yes, write documentation. if not, delete
    '''
    Converts list of keypoints into a dictionary named by keypoint_names.
    '''
    keypoint_dict = {}
    if isinstance(keypoint, Iterable):
        for i in range(len(keypoints_names)):
            x = keypoint[2*i]
            y = keypoint[2*i+1]
            if np.isfinite(x) and np.isfinite(y):
                keypoint_dict[keypoints_names[i]] = [x, y]
    return keypoint_dict

def convert_keypoints(
        keypoints: pd.Series,
        keypoints_names: List[str]
        ) -> List[Dict[str, object]]:
    # TODO: check if used. if yes, write documentation. if not, delete
    '''
    Converts dataframe of lists of keypoints into a dictionary named by keypoint_names.
    '''
    return [convert_keypoint(keypoint, keypoints_names) for keypoint in keypoints]