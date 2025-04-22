# 环境介绍
ros2,humble版本，python==3.10
现在已有moveit，ros humble版本，现在需要从包的创建，到完成pick-place任务。基于moveit,机械臂是panda机械臂，分步骤详细说明。代码以及对应的bash命令。抓取任务基于pybullet
# 目标
基于 MoveIt! 的机械臂运动规划
验收标准（流程和大致项目跑通+可以改用自己规划的算法）
1.	机械臂加载，可以代码控制任意关节移动，ur5机械臂(实现)
2.	实现内置函数的运动规划，搭建障碍物，实现轨迹规划
3.	使用机械臂实现抓取和摆放任务，可以是开源项目，但是效果一定要有抓取任务，整个流程用导图显示出来。(参考开源项目,[基于pybullet的抓取任务](https://github.com/leesweqq/ur5_grasp_object_pybullet))
## MoveIt抓取任务模块分解
MoveIt抓取流程：设置目标位姿 → 规划路径 → 碰撞检查 → 执行运动 → 夹爪闭合 → 状态验证
PyBullet抓取流程：生成目标物体 → 计算IK解 → 驱动关节 → 物理仿真步进 → 接触检测 → 力控制保持
## ToDo
1.moveit python接口，可以实现机械臂末端移动到指定位置，夹爪闭合和打开，然后移动到指定位置，
2.位置的获取采用opencv，输入图像，返回需要的目标点的坐标，物体和盒子的位置

# 从零搭建自己的机器人具体的实现步骤
## 1.创建机器人urdf包
具体的机器人urdf文件可以自己编写，也可以寻找开源机器人urdf文件。
```bash
# Navigate to your ROS 2 workspace
cd ~/ros2_ws/src

# Create a new ROS 2 package
ros2 pkg create --build-type ament_cmake my_robot_description
# Navigate to your package directory
cd ~/ros2_ws/src/my_robot_description

# Create a 'urdf' directory
mkdir urdf

# Copy your robot's URDF file into the 'urdf' directory
cp /path/to/your/robot.urdf urdf/
```
添加cmake依赖：
```cmake
# Install URDF files(cmakelist.txt)
install(DIRECTORY
  urdf
  DESTINATION share/${PROJECT_NAME}/
)
```
添加package依赖：
```xml
# package.xml
<build_depend>ament_cmake</build_depend>
<exec_depend>robot_state_publisher</exec_depend>
```
编译加载：
```bash
cd ~/ros2_ws
colcon build --packages-select my_robot_description
source ~/ros2_ws/install/setup.bash
```
## 2.利用setup_assitant创建Moveit_config
启动可视化moveit助手：
```bash
ros2 launch moveit_setup_assistant setup_assistant.launch.py
```
具体步骤和对应的解释参考[moveit官网](https://moveit.picknik.ai/main/doc/examples/setup_assistant/setup_assistant_tutorial.html)
保存的文件夹为：ur5_moveit_config
```bash
cd ~/ws_moveit2
colcon build --packages-select ur5_moveit_config
source install/setup.bash
```
## 3.启动
```bash
ros2 launch panda_moveit_config demo.launch.py
```

# 本项目使用步骤
## 1.加载ur5机器人，然后利用rviz的moveit插件来实现基本任务
编译加载路径：
```bash
cd ~/ros2_ws
colcon build --packages-select ur5_moveit_config
source install/setup.bash
```
启动：
```bash
ros2 launch ur5_moveit_config demo.launch.py
```
## 2.实现ur5机器人完成抓取任务
采用现有的moveit2的任务建立包，实现里面的demo,具体的步骤参考[Moveit2官网](https://moveit.picknik.ai/main/doc/tutorials/pick_and_place_with_moveit_task_constructor/pick_and_place_with_moveit_task_constructor.html)


# 实现过程中的收获
大部分功能，甚至是机器人都是现成的，调用他们实现自己的功能是关键。
要调用的话前提需要掌握：
1.调用的原理是什么，一定是文件所在的位置一定需要提前了解，知道文件在哪，才可以调用，，在当前工作空间中的Install文件夹下
2.launch函数很有用，这个相当于整合关键的骨架，需要确定一个任务需要哪几个部分，然后这几个部分对应是什么函数。相当于把需要用到的节点都启动

install文件是编译完的文件，build是编译的中间文件。可执行文件在install/pkg_name下面,可执行文件对应的源码在src下面，具体的可以通过tree|grep 来得到。
rviz2显示的原理是什么，rviz节点会自动订阅相关的话题吗，然后显示吗，这些订阅的话题一般需要我们手动设置吗，不手动设置的话那么相关话题是否话题名字需要固定，写成规范的
moveit2里面的关键部分有哪些，这些和rviz中的moveit插件是对应的吗

# 存在的问题
1.节点和文件位置怎么找知道
2.代码基本都是c++文件，阅读困难，为什么不采用
3.遇到的问题，  没有python包的问题,no Module ‘lark’。。
解决办法，由于我采用的是miniconda环境，这个环境里是有lark pkg.但是ros2中没有这个路径，所以解决思路是将conda路径对应的python路径添加到PYTHONPATH中
```bash
echo $PYTHONPATH
export PYTHONPATH=/home/li/miniconda3/envs/ros_humble/lib/python3.10/site-packages:$PYTHONPATH #替换为你自己的conda路径,这段是添加path路径
echo $PYTHONPATH
```

# 相关资料
1. [moveit_python接口](https://moveit.picknik.ai/main/doc/examples/motion_planning_python_api/motion_planning_python_api_tutorial.html#getting-started)
2. [pick_and_place](https://moveit.picknik.ai/main/doc/tutorials/pick_and_place_with_moveit_task_constructor/pick_and_place_with_moveit_task_constructor.html#getting-started)
3. [moveit_python api介绍](https://moveit.picknik.ai/main/doc/api/python_api/api.html)