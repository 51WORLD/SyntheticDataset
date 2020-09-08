# rem Artifactory

CurrentPath=$(pwd)
echo $CurrentPath
cd $CurrentPath


if [ ! -d build  ];then
  mkdir build
fi
if [ ! -d pcd_bin  ];then
  mkdir pcd_bin
fi
cd build
cmake ../src -DCMAKE_BUILD_TYPE=Release -G "Unix Makefiles"
make -j4
cd ../
./PcdToBin
