from easydict import EasyDict as edict


__C                         = edict()
loader_cfg                         = __C


loader_cfg.TRAINING_LOADER_FLAGS  = dict(
                            use_pointcloud = True,
                            use_image_segmentation = False,
                            use_dump_settings = True,
                            use_flow_groundtruth_forward = False,
                            use_flow_flagbit_forward = False,
                            use_flow_groudtruth = False,
                            use_flow_flagbit = False,
                            use_depth = True,
                            use_image_annos = False,
                            use_pcd_annos = False,
                            use_fusion_annos = True,
                            use_image = True,
                            use_image_instance = False,
                            use_flow_panoptic = True
                            )            


loader_cfg.TESTING_LOADER_FLAGS   = dict(
                            use_pointcloud = True,
                            use_image_segmentation = False,
                            use_dump_settings = True,
                            use_flow_groundtruth_forward = False,
                            use_flow_flagbit_forward = False,
                            use_flow_groudtruth = False,
                            use_flow_flagbit = False,
                            use_depth = True,
                            use_image_annos = False,
                            use_pcd_annos = False,
                            use_fusion_annos = True,
                            use_image = True,
                            use_image_instance = False,
                            use_flow_panoptic = True                            
                            )            


loader_cfg.DATASET_DIR             = '/home/jhli/Dataset/51WSD/train/' 


loader_cfg.REMAINED_ID             = {
                            '4' : 'Pedestrian',
                            '6' : 'Car',
                            '17' : 'Rider',
                            '15' : 'TrafficLight',
                            '18' : 'Truck',
                            '19' : 'Bus',
                            '20' : 'SpecialVehicle',
                            '26' : 'SpeedLimitSign',
                            '29' : 'RoadObstacle'
                            }
 

loader_cfg.PHYSICAL_SURFACES       = {   
                            '1' : 'Faliage',
                            '2' : 'Building',
                            '3' : 'Road',
                            '4' : 'Pedestrian',
                            '5' : 'Pole',
                            '6' : 'Car',
                            '7' : 'Static',
                            '8' : 'Bicycle',
                            '9' : 'Fence',
                            '10' : 'Sky',
                            '11' : 'SideWalk',
                            '12' : 'RoadMark',
                            '13' : 'TrafficSign',
                            '14' : 'Wall',
                            '15' : 'TrafficLight',
                            '16' : 'Terrain',
                            '17' : 'Rider',
                            '18' : 'Truck',
                            '19' : 'Bus',
                            '20' : 'SpecialVehicle',
                            '21' : 'Motorcycle',
                            '22' : 'Dynamic',
                            '23' : 'GuardRail',
                            '24' : 'Ground',
                            '25' : 'Bridge',
                            '26' : 'SpeedLimitSign',
                            '27' : 'StaticBicycle',
                            '28' : 'Parking',
                            '29' : 'RoadObstacle',
                            '30' : 'Tunnel',
                            '31' : 'Trashcan'
                            }   


loader_cfg.POINTS_THRES            = {
                            'Pedestrian': 15,
                            'Car': 30,
                            'Rider': 15,
                            'TrafficLight': 5,
                            'Truck': 40,
                            'Bus': 40,
                            'SpecialVehicle': 30,
                            'SpeedLimitSign': 15,
                            'RoadObstacle': 30
                            }