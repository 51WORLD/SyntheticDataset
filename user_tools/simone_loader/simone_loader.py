import os
import cv2 
import json
import random
from path import Path
import numpy as np
from loader_config import loader_cfg
import cv2


def filter_bboxes_by_name(bboxes, remained_id):
    new_bboxes = []
    for bbox in bboxes:
        if str(bbox['type']) in remained_id:
            bbox['type'] = remained_id[str(bbox['type'])]
            new_bboxes.append(bbox)
    return new_bboxes

def filter_bboxes2D_by_threshold(bboxes2D, pixel_thres=0.3, rect_thres=0.3, width_thres=40, height_thres=40):
    new_bboxes2D = []
    for bbox in bboxes2D:
        if bbox['pixelRate'] < pixel_thres or bbox['rectRate'] < rect_thres:
            continue
        w = bbox['bbox'][2] - bbox['bbox'][0]
        h = bbox['bbox'][3] - bbox['bbox'][1]
        if w < width_thres and h < height_thres:
            continue
        new_bboxes2D.append(bbox)
    return new_bboxes2D

def filter_bboxes3D_by_threshold(bboxes3D, points_thres):
    new_bboxes3D = []
    for bbox in bboxes3D:
        if bbox['totalPoints'] >= points_thres[bbox['type']]:
            new_bboxes3D.append(bbox)
    return new_bboxes3D 

def filter_gts_by_merge(gts):
    new_gts = {}
    for obj_id in gts:
        if 'bboxes2D' in gts[obj_id] and 'bboxes3D' in gts[obj_id]:
            new_gts.update({obj_id:gts[obj_id]})
    return new_gts

class SimoneDatasetLoader():
    def __init__(self, dataset_dir, loader_flags, is_training):
        self.dataset_dir = dataset_dir
        self.stamp_list = self.get_stamp_list(self.dataset_dir, is_training)
        random.shuffle(self.stamp_list)
        self.stamp_count = 0
        self.idx_list = self.get_idx_list(self.dataset_dir, self.stamp_list[self.stamp_count], is_training)
        random.shuffle(self.idx_list)
        self.ids_count = 0
        self.loader_flags = loader_flags
        self.is_training = is_training

    def get_stamp_num(self):
        return len(self.stamp_list)

    def get_idx_num(self):
        return len(self.idx_list)

    def get_total_num(self):
        count = 0 
        for i in range(len(self.stamp_list)):
            count += len(self.get_idx_list(self.dataset_dir, self.stamp_list[i], self.is_training))
        return count

    def get_stamp_list(self, prefix, training):
        if training:
            path = Path(prefix) / 'train'
        else:
            path = Path(prefix) / 'test'
        return os.listdir(path)

    def get_idx_list(self, prefix, stamp, training):
        if training:
            path = Path(prefix) / 'train' / stamp / 'image'
        else:
            path = Path(prefix) / 'test' / stamp / 'image'
        return os.listdir(path) 

    def get_image_index_str(self, img_idx):
        return img_idx.split('.')[0]

    def get_simone_info_path(self, 
                            idx,
                            prefix,
                            info_type='image',
                            file_tail='.png',
                            training=True,
                            relative_path=True,
                            exist_check=True):
        img_idx_str = self.get_image_index_str(idx)
        img_idx_str += file_tail
        prefix = Path(prefix)
        if training:
            file_path = prefix / info_type / img_idx_str
        else:
            file_path = prefix / info_type / img_idx_str
        if exist_check and not (prefix / file_path).exists():
            raise ValueError('file not exist: {}'.format(file_path))
        if relative_path:
            return str(file_path)
        else:
            return str(prefix / file_path)

    def load_pointcloud(self, idx, prefix, training):
        path_file = self.get_simone_info_path(idx, prefix, 'pcd_bin', '.bin', training=training)
        return np.fromfile(path_file, np.float32).reshape(-1, 4)

    def load_image(self, idx, prefix, training, camera_num=0):
        path_file = self.get_simone_info_path(idx, prefix, 'image', '.png', training=training)
        return cv2.imread(path_file) / 255.0

    def load_image_segmentation(self, idx, prefix, training):
        path_file = self.get_simone_info_path(idx, prefix, 'image_segmentation', '.png', training=training) 
        return cv2.imread(path_file)       

    def load_flow_groundtruth_forward(self, idx, prefix, training):
        path_file = self.get_simone_info_path(idx, prefix, 'flow_groundtruth_forward', '', training=training)
        return np.fromfile(path_file, dtype=np.float32).reshape(1080, 1920, 2)

    def load_flow_flagbit_forward(self, idx, prefix, training):
        path_file = self.get_simone_info_path(idx, prefix, 'flow_flagbit_forward', '', training=training)
        return np.fromfile(path_file, dtype=np.int8).reshape(1080, 1920)

    def load_flow_groundtruth(self, idx, prefix, training):
        path_file = self.get_simone_info_path(idx, prefix, 'flow_groundtruth', '', training=training)
        return np.fromfile(path_file, dtype=np.float32)

    def load_flow_flagbit(self, idx, prefix, training):
        path_file = self.get_simone_info_path(idx, prefix, 'flow_flagbit', '', training=training)
        return np.fromfile(path_file, dtype=np.int8)

    def load_flow_panoptic(self, idx, prefix, training):
        path_file = self.get_simone_info_path(idx, prefix, 'flow_panoptic', '.png', training=training)
        return cv2.imread(path_file) / 255.0

    def load_depth(self, idx, prefix, training):
        path_file = self.get_simone_info_path(idx, prefix, 'depth', '.png', training=training)
        return cv2.imread(path_file)
   
    def load_image_instance(self, idx, prefix, training):
        path_file = self.get_simone_info_path(idx, prefix, 'image_instance', '.png', training=training)
        return cv2.imread(path_file).astype(np.int32)

    def load_image_annos(self, idx, prefix, training):
        path_file = self.get_simone_info_path(idx, prefix, 'image_label', '.json', training=training)
        with open(path_file) as f:
            label = json.load(f)
        label = filter_bboxes_by_name(label['bboxes'] + label['bboxesCulled'], loader_cfg.REMAINED_ID)
        label = filter_bboxes2D_by_threshold(label)
        return label
 
    def load_pcd_annos(self, idx, prefix, training):
        path_file = self.get_simone_info_path(idx, prefix, 'pcd_label', '.json', training=training)
        with open(path_file) as f:
            label = json.load(f)
        label = filter_bboxes_by_name(label['bboxes3D'], loader_cfg.REMAINED_ID)
        label = filter_bboxes3D_by_threshold(label, loader_cfg.POINTS_THRES)
        return label

    def load_dump_settings(self, prefix, training):
        path = os.path.join(prefix, 'DumpSettings.json')
        with open(path) as f:
            setting_cfg = json.load(f)
        return setting_cfg
        
    def load_fusion_annos(self, idx, prefix, training):
        path_file = self.get_simone_info_path(idx, prefix, 'image_label', '.json', training=training)
        with open(path_file) as f:
            annos2D = json.load(f)
        path_file = self.get_simone_info_path(idx, prefix, 'pcd_label', '.json', training=training)
        with open(path_file) as f:
            annos3D = json.load(f)
        annos2D = filter_bboxes_by_name(annos2D['bboxes'] + annos2D['bboxesCulled'], loader_cfg.REMAINED_ID)
        annos2D = filter_bboxes2D_by_threshold(annos2D)
        annos3D = filter_bboxes_by_name(annos3D['bboxes3D'], loader_cfg.REMAINED_ID)
        annos3D = filter_bboxes3D_by_threshold(annos3D, loader_cfg.POINTS_THRES)
        fusion_label = {}
        for bbox in annos2D:
            fusion_label.setdefault(str(bbox['id']), {})
            fusion_label[str(bbox['id'])]['bboxes2D'] = bbox
        for bbox in annos3D:
            fusion_label.setdefault(str(bbox['id']), {})
            fusion_label[str(bbox['id'])]['bboxes3D'] = bbox
        return filter_gts_by_merge(fusion_label)

    def load_data(self, prefix, idx, training):
        data_dict = {}
        if self.loader_flags['use_pointcloud']:
            data_dict['pointcloud'] = self.load_pointcloud(idx, prefix, training)
        if self.loader_flags['use_image']:
            data_dict['image'] = self.load_image(idx, prefix, training) 
        if self.loader_flags['use_image_segmentation']:
            data_dict['image_segmentation'] = self.load_image_segmentation(idx, prefix, training)
        if self.loader_flags['use_image_instance']:
            data_dict['image_instance'] = self.load_image_instance(idx, prefix, training)
        if self.loader_flags['use_flow_groundtruth_forward']:
            data_dict['flow_groundtruth_forward'] = self.load_flow_groundtruth_forward(idx, prefix, training)
        if self.loader_flags['use_flow_flagbit_forward']:
            data_dict['flow_flagbit_forward'] = self.load_flow_flagbit_forward(idx, prefix, training)
        if self.loader_flags['use_depth']:
            data_dict['depth'] = self.load_depth(idx, prefix, training)
        if self.loader_flags['use_dump_settings']:
            data_dict['dump_settings'] = self.load_dump_settings(prefix, training)
        if self.loader_flags['use_image_annos']:
            data_dict['image_annos'] = self.load_image_annos(idx, prefix, training)
        if self.loader_flags['use_pcd_annos']:
            data_dict['pcd_annos'] = self.load_pcd_annos(idx, prefix, training)
        if self.loader_flags['use_fusion_annos']:
            data_dict['fusion_annos'] = self.load_fusion_annos(idx, prefix, training)
        if self.loader_flags['use_flow_panoptic']:
            data_dict['flow_panoptic'] = self.load_flow_panoptic(idx, prefix, training)
        data_dict['index'] = prefix.split('/')[-1] + '/' + idx.split('.')[0]
        return data_dict

    def next(self):
        self.ids_count += 1  
        if self.ids_count >= len(self.idx_list)-1:        
            self.stamp_count += 1
            self.ids_count = 0
            if self.stamp_count >= len(self.stamp_list):
                self.stamp_count = 0
                random.shuffle(self.stamp_list)
            self.idx_list = self.get_idx_list(self.dataset_dir, self.stamp_list[self.stamp_count], self.is_training)
            random.shuffle(self.idx_list)
        if self.is_training:
            prefix = os.path.join(self.dataset_dir, 'train', self.stamp_list[self.stamp_count])
        else:
            prefix = os.path.join(self.dataset_dir, 'test', self.stamp_list[self.stamp_count])

        return self.load_data(prefix, self.idx_list[self.ids_count], self.is_training)


if __name__ == "__main__":
    dataset_loader = SimoneDatasetLoader(loader_cfg.DATASET_DIR, loader_cfg.TRAINING_LOADER_FLAGS, True)
    num = dataset_loader.get_total_num()
    for i in range(num):
        data = dataset_loader.next()
        print(i)