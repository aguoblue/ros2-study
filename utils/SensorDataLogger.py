#!/usr/bin/env python3

"""
名称: SensorDataLogger

用途说明:
该 ROS 2 节点订阅三个话题：
- /wrapper/psdk_ros2/perception_stereo_left_stream (Image)
- /wrapper/psdk_ros2/perception_stereo_right_stream (Image)
- /wrapper/psdk_ros2/imu (Imu)

节点会将接收到数据时的系统当前时间，以及消息头中的时间戳记录到名为 "timestamp_log.txt" 的文本文件中。
日志文件中的每一条记录都包含系统时间（以纳秒为单位）、接收到的数据类型（left_img、right_img、imu），以及相应的消息时间戳。
"""


"""
Name: SensorDataLogger

Description:
This ROS 2 node subscribes to three topics:
- /wrapper/psdk_ros2/perception_stereo_left_stream (Image)
- /wrapper/psdk_ros2/perception_stereo_right_stream (Image)
- /wrapper/psdk_ros2/imu (Imu)

The node logs the system's current time when data is received, as well as the 
timestamp from the message header, to a text file named "timestamp_log.txt".
Each entry in the log file records the system time in nanoseconds, the type of 
data received (left_img, right_img, imu), and the corresponding message timestamp.

"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, Imu
import time

class SensorDataLogger(Node):
    def __init__(self):
        super().__init__('data_logger')

        self.output_file = "timestamp_log.txt"

        # 订阅三个话题
        self.left_image_subscriber = self.create_subscription(
            Image,
            '/wrapper/psdk_ros2/perception_stereo_left_stream',
            self.left_image_callback,
            10)
        
        self.right_image_subscriber = self.create_subscription(
            Image,
            '/wrapper/psdk_ros2/perception_stereo_right_stream',
            self.right_image_callback,
            10)

        self.imu_subscriber = self.create_subscription(
            Imu,
            '/wrapper/psdk_ros2/imu',
            self.imu_callback,
            10)

    def log_to_file(self, data_type, msg_time, header_time):
        with open(self.output_file, "a") as file:
            file.write(f"{msg_time}   {data_type}   {header_time}\n")

    def left_image_callback(self, msg):
        # 获取接收到数据时的系统时间（以纳秒为单位）
        current_time_ns = int(time.time() * 1e9)
        # 获取消息中的时间戳（header 中的时间戳）
        header_time_ns = msg.header.stamp.sec * 1e9 + msg.header.stamp.nanosec
        # 记录到文件中
        self.log_to_file("left_img", current_time_ns, header_time_ns)

    def right_image_callback(self, msg):
        current_time_ns = int(time.time() * 1e9)
        header_time_ns = msg.header.stamp.sec * 1e9 + msg.header.stamp.nanosec
        self.log_to_file("right_img", current_time_ns, header_time_ns)

    def imu_callback(self, msg):
        current_time_ns = int(time.time() * 1e9)
        header_time_ns = msg.header.stamp.sec * 1e9 + msg.header.stamp.nanosec
        self.log_to_file("imu", current_time_ns, header_time_ns)

def main(args=None):
    rclpy.init(args=args)
    node = SensorDataLogger()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    # 关闭节点
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
