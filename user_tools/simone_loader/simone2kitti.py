import os
import cv2
import numpy as np
import argparse
import os.path as osp
import shutil
import simone_loader
from loader_config import loader_cfg


kitti_cls_type  = dict( 
                    Pedestrian = 'Pedestrian',
                    Car = 'Car',
                    Rider = 'Cyclist',
                    TrafficLight = 'Misc',
                    Truck ='Truck',
                    Bus = 'Van',
                    SpecialVehicle = 'Misc',
                    SpeedLimitSign = 'Misc',
                    RoadObstacle = 'Misc'
                    )

def get_index_str(idx):
    return '{:06d}'.format(idx)

def convert_rotation_to_kitti(rots):
    return -(rots+3.14/2)

def get_kitti_format_cls(cls_type):
    if cls_type in kitti_cls_type:
        return kitti_cls_type[cls_type]
    else:
        raise Exception('ERROR: HAS NO CORRESPONDING LABEL')

def save_kitti_format_label(annos, type_info, idx, file_tail, args):
    path = osp.join(args.output, type_info, idx+file_tail)
    fi = open(path,'w')
    for k in annos:
        bbox2d = annos[k]['bboxes2D']['bbox']
        size = annos[k]['bboxes3D']['size']
        loc = annos[k]['bboxes3D']['relativePos']
        rot = convert_rotation_to_kitti(annos[k]['bboxes3D']['relativeRot'][2])
        cls_type = get_kitti_format_cls(annos[k]['bboxes2D']['type'])
        line =  cls_type + ' 0.0 0 {:.2f}'.format(rot)
        line += ' {:.2f} {:.2f} {:.2f} {:.2f}'.format(bbox2d[0], bbox2d[1], bbox2d[2], bbox2d[3])
        line += ' {:.2f} {:.2f} {:.2f}'.format(size[2], size[1], size[0])
        line += ' {:.2f} {:.2f} {:.2f} {:.2f}\n'.format(-loc[1], -loc[2], loc[0], rot)
        fi.write(line)
    fi.close()

def save_kitti_format_calib(dump_settings, type_info, idx, file_tail, args):
    fx = dump_settings['camera']['fx']
    fy = dump_settings['camera']['fy']
    cx = dump_settings['camera']['cx']
    cy = dump_settings['camera']['cy']
    p0_line = 'P0: -10.0 -10.0 -10.0 -10.0 -10.0 -10.0 -10.0 -10.0 -10.0 -10.0 -10.0 -10.0\n'
    p1_line = 'P1: -10.0 -10.0 -10.0 -10.0 -10.0 -10.0 -10.0 -10.0 -10.0 -10.0 -10.0 -10.0\n'
    p2_line = 'P2: {:.2f} 0.0 {:.2f} 0.0 0.0 {:.2f} {:.2f} 0.0 0.0 0.0 1.0 0.0\n'.format(fx, cx, fy, cy)
    print(p2_line)
    p3_line = '-10.0 -10.0 -10.0 -10.0 -10.0 -10.0 -10.0 -10.0 -10.0 -10.0 -10.0 -10.0\n'
    r0_line = 'R0_rect: 1.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 1.0\n'
    tr_velo2cam_line = 'Tr_velo_to_cam: 0.0 -1.0 0.0 0.0 0.0 0.0 -1.0 0.0 1.0 0.0 0.0 0.0\n'
    tr_imu2velo_line = 'Tr_imu_to_velo: 0.0 -1.0 0.0 0.0 0.0 0.0 -1.0 0.0 1.0 0.0 0.0 0.0\n'
    path = osp.join(args.output, type_info, idx+file_tail)
    fi = open(path, 'w')
    fi.write(p0_line+p1_line+p2_line+p3_line)
    fi.write(r0_line+tr_velo2cam_line+tr_imu2velo_line)
    fi.close()

def save_kitti_format_pcd(pcd, type_info, idx, file_tail, args):
    path = osp.join(args.output, type_info, idx+file_tail)
    pcd = pcd.reshape(-1)
    pcd.tofile(path)

def save_kitti_format_image_2(image, type_info, idx, file_tail, args):
    path = osp.join(args.output, type_info, idx+file_tail)
    cv2.imwrite(path, (image*255).astype(np.int32))

def make_save_dirs(args):
    if not os.path.exists(args.output):
        os.mkdir(args.output)
    path_type = ['image_2', 'label_2', 'velodyne', 'calib']
    for t in path_type:
        path = os.path.join(args.output, t)
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)
    return
    
def gci(dataset_loader, args):  
    make_save_dirs(args)
    count = 0
    stamp_num = dataset_loader.get_stamp_num()
    for i in range(stamp_num):
        idx_num = dataset_loader.get_idx_num()
        for j in range(idx_num):
            print(count, i, j)
            data_info = dataset_loader.next()
            idx_str = get_index_str(count)
            save_kitti_format_image_2(data_info['image'], 'image_2', idx_str, '.png', args)
            save_kitti_format_pcd(data_info['pointcloud'], 'velodyne', idx_str, '.bin', args)
            save_kitti_format_calib(data_info['dump_settings'], 'calib', idx_str, '.txt', args)
            save_kitti_format_label(data_info['fusion_annos'], 'label_2', idx_str, '.txt', args)
            count += 1
    return        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    print('Usage: simone2kitti.py --input=inputpath --output=outpath')
    parser.add_argument('--input', default=loader_cfg.DATASET_DIR, required=False,
                        help='a path input file')
    parser.add_argument('--output', default='/media/jhli/57DF22050921ED01/exchange/dl_dataset/fusion/temp', required=False,
                        help='a path out file')
    args = parser.parse_args()
    dataset_loader = simone_loader.SimoneDatasetLoader(args.input, loader_cfg.TESTING_LOADER_FLAGS, True)
    gci(dataset_loader, args)