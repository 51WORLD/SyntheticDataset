# 51WORLD虚拟标注数据集使用者工具
为了方便大家使用51WORLD虚拟标注数据集，这里提供两个数据解析的工具，分别是数据加载工具和将数据集转换到kitti格式的工具。
## 环境配置
使用者工具是基于Python开发，您所需要配置的环境有：

```
python 3.5+
opencv
easydict
numpy
path
```

## 参数说明与配置

您需要根据需求配置***loader_config.py***中参数。

您需要关注是以下6个配置参数

```python
loader_cfg.TRAINING_LOADER_FLAGS  = dict(...)             
loader_cfg.TESTING_LOADER_FLAGS   = dict(...)            
loader_cfg.DATASET_DIR            = '' 
loader_cfg.REMAINED_ID            = dict(...) 
loader_cfg.PHYSICAL_SURFACES      = dict(...)    
loader_cfg.POINTS_THRES           = dict(...) 
```

其中 *TRAINING_LOADER_FLAGS* 用来配置在训练时需要加载的数据源，*TESTING_LOADER_FLAGS* 用来配置测试时需要加载的数据源。通过将标志位设置为 *True* 加载需要的数据，各个标注位含义如下。

```Python
TRAINING_LOADER_FLAGS = dict(
    use_pointcloud = True, # 激光点云文件
    use_image_segmentation = False, # 图像语义分割文件
    use_dump_settings = True, # 数据集下载时的一些参数配置，如相机和雷达的内外参
    use_flow_groundtruth_forward = False, # 前向光流真值
    use_flow_flagbit_forward = False, # 前向光流位移
    use_flow_groudtruth = False, # 后向光流真值
    use_flow_flagbit = False, # 后向光流偏移
    use_depth = False, # 深度图
    use_image_annos = False, # 图像的目标真值
    use_pcd_annos = False, # 激光点云的目标真值
    use_fusion_annos = True, # 图像和激光点云的目标真值同时加载，通常在融合算法中使用
    use_image = True, # 图像
    use_image_instance = False, # 图像实例分割图
    use_flow_panoptic = True # 图像全景分割图
)      
```

*DATASET_DIR* 用来配置数据存放的文件夹。

```
DATASET_DIR = '' 
```

*REMAINED_ID* 用来配置关注的目标类别编号及其对应的物理含义。如在算法中需要检测出来的目标是行人，那么将  *'4' : 'Pedestrian'* 添加到字典结构中。

```Python
REMAINED_ID = {
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
```

*PHYSICAL_SURFACES* 这个参数没有实际使用到，放在配置文件中是为了方便查找类别标号对应的物理材质。

```Python
PHYSICAL_SURFACES      = dict(...)
```

*POINTS_THRES* 这个参数是通过激光雷达中目标被打到点的个数来过滤目标，通过过滤减少激光雷达算法和融合算法的训练难度。如 *'Pedestrian': 15* 表示当打个行人的激光点的个数小于15，那么这个目标会被过滤 。

```Python
POINTS_THRES = {
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
```

## 数据加载工具

*simone_loader.py* 是一个非常的方便的数据加载工具，只需要实例化 *SimoneDataLoader* , 然后调用 *next()* 函数即可加载数据，如：

```python
if __name__ == "__main__":
    dataset_loader = SimoneDatasetLoader(loader_cfg.DATASET_DIR, \ 
    					loader_cfg.TRAINING_LOADER_FLAGS, True)
    num = dataset_loader.get_total_num()
    for i in range(num):
        data = dataset_loader.next()
```

## Kitti数据集转换工具

很多算法研究者都会在kitti数据集上做研究。为了能够让kitti数据集做研究的用户快速使用simone数据集，这里提供了一个将Simone数据集转换成kitti 数据的工具。使用方法如下

```python
parser = argparse.ArgumentParser()
print('Usage: simone2kitti.py --input=inputpath --output=outpath')
parser.add_argument('--input', default=loader_cfg.DATASET_DIR, required=False,
                    help='a path input file')
parser.add_argument('--output', default='/media/jhli/57DF22050921ED01/exchange/dl_dataset/fusion/temp', required=False,
                    help='a path out file')
args = parser.parse_args()
dataset_loader = simone_loader.SimoneDatasetLoader(args.input, loader_cfg.TESTING_LOADER_FLAGS, True)
gci(dataset_loader, args)
```

