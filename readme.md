
# 目标
基于 MoveIt! 的机械臂运动规划（下周二验收）
验收标准（流程和大致项目跑通+可以改用自己规划的算法）
1.	机械臂加载，可以代码控制任意关节移动，ur5机械臂(实现)
2.	实现内置函数的运动规划，搭建障碍物，实现轨迹规划
3.	使用机械臂实现抓取和摆放任务，可以是开源项目，但是效果一定要有抓取任务，整个流程用导图显示出来。
硬性标准
1. Git项目一个，机械臂抓取
2. 详细的readme指导书
3. 思维导图绘制，针对项目，理解moveit里面的关键节点以及关键的接口设置
4. 抓取任务里面必须包含一般机械臂执行的部分，即感知一定要有，绘制思维导图
5. Readme里面得有一个规划图，初步的规划（文字）//结合代码/节点的规划图

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
colcon build --packages-select panda_moveit_config
source install/setup.bash
```
## 3.启动
```bash
ros2 launch panda_moveit_config demo.launch.py
```

# 本项目使用步骤
编译加载路径：
```bash
cd ~/ws_moveit2
colcon build --packages-select panda_moveit_config
source install/setup.bash
```
启动：
```bash
ros2 launch panda_moveit_config demo.launch.py
```

# 实现步骤
1.首先分析替换模型需要替换哪些东西，分析一下原来的panda机械臂和什么有关
2.github开源的可以得到ur5机械臂，替换调panda，实现加载任务
3.分析tutorial里面的抓取代码，pick_place函数，里面有感知吗？跟换为：https://moveit.picknik.ai/main/doc/tutorials/pick_and_place_with_moveit_task_constructor/pick_and_place_with_moveit_task_constructor.html#getting-started。。实现抓取的教程
4.机器人替换，实现ur5抓取任务

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
# 相关资料
1. moveit_python接口：https://moveit.picknik.ai/main/doc/examples/motion_planning_python_api/motion_planning_python_api_tutorial.html#getting-started
2. pick_and_place：https://moveit.picknik.ai/main/doc/tutorials/pick_and_place_with_moveit_task_constructor/pick_and_place_with_moveit_task_constructor.html#getting-started
