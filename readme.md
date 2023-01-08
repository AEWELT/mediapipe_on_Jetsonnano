#安装所需环境  
$sudo apt install -y python3-dev  
$sudo apt install -y cmake  
$sudo apt install -y protobuf-compiler  
  
$ python3 -m pip install cython  
$ python3 -m pip install numpy  
$ python3 -m pip install pillow  
$ python3 -m pip install mediapipe/dist/mediapipe-0.8-cp38-cp38-linux_aarch64.whl  
or   
$ python3 -m pip install mediapipe-python-aarch64/mediapipe-0.8.4-cp38-cp38-linux_aarch64.whl  

#解压protoc  
$unzip protoc-3.0.0-linux-aarch_64.zip  

#修改mediapipe/setup.py  
定位到  
protoc_command = [self._protoc, ‘-I.’, ‘–python_out=.’, source]  
改为  
protoc_command = [self._protoc, ‘-I.’, ‘-I/usr/local/include’, ‘–python_out=.’, source]  

#根据官方建议删除mediapipe中部分不必要的OpenCV模块和链接器  
$cd mediapipe  
$sed -i -e "/\"imgcodecs\"/d;/\"calib3d\"/d;/\"features2d\"/d;/\"highgui\"/d;/\"video\"/d;/\"videoio\"/d" third_party/BUILD  
$sed -i -e "/-ljpeg/d;/-lpng/d;/-ltiff/d;/-lImath/d;/-lIlmImf/d;/-lHalf/d;/-lIex/d;/-lIlmThread/d;/-lrt/d;/-ldc1394/d;/-lavcodec/d;/-lavformat/d;/-lavutil/d;/-lswscale/d;/-lavresample/d" third_party/BUILD  

#修改mediapipe/third_party/BUILD  
定位到  
“WITH_ITT”: “OFF”,  
“WITH_JASPER”: “OFF”,  
“WITH_WEBP”: “OFF”,  
在其后添加  
“ENABLE_NEON”: “OFF”,  
“WITH_TENGINE”: “OFF”,  

#为了让bazel编译时能找到CUDA，还需要将TensorFlow官方.bazelrc文件中的build:using_cuda和build:cuda的部分添加到Mediapipe文件夹下的.bazelrc  
build:using_cuda --define=usiing_cuda=true  
build:using_cuda --action_env TF_NEED_CUDA=1  
build:using_cuda --crosstool_top=@local_config_cuda//crosstool:toolchain  

#以下内容需要nvcc支持  
build:using_cuda --config=using_cuda  
build:using_cuda --define=using_cuda_nvcc=true  

#如果中途编译失败，清除缓存重新编译  
$rm -rf ~/.cache/bazel/  

#调用CUDA，将CUDA库的路径通过环境变量配置给TensorFlow  
export TF_CUDA_PATHS=/usr/local/cuda-x.x,/usr/lib/aarch64-linux-gnu,/usr/include  
