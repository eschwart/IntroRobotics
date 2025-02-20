import rclpy
from rclpy.node import Node

from irobot_create_msgs.msg import LightringLeds, InterfaceButtons
from random import randint

from rclpy.qos import qos_profile_sensor_data

class LightringNode(Node):
    def __init__(self):
        super().__init__('lightring_node')
        self.publisher = self.create_publisher(LightringLeds,'/robot1/cmd_lightring', 10)
        self.button_sub = self.create_subscription(InterfaceButtons, '/robot1/interface_buttons', self.button_callback, qos_profile_sensor_data)
        self.timer = self.create_timer(.5,self.timer_callback);
        self.button_colors = []
        self.button_colors.append([randint(0,255),randint(0,255),randint(0,255)])
        for i in range(5):
            #self.button_colors.append([randint(0,255),randint(0,255),randint(0,255)])
            self.button_colors.append([0,0,0])
        self.reverse = False
    def timer_callback(self):
        msg = LightringLeds()
        msg.override_system = True
        indices = range(len(msg.leds))
        if self.reverse:
            indices = reversed(indices)
        for i,j in enumerate(indices):
            msg.leds[j].red   = self.button_colors[i][0]
            msg.leds[j].green = self.button_colors[i][1]
            msg.leds[j].blue  = self.button_colors[i][2]
        self.button_colors.append(self.button_colors.pop(0))


        self.publisher.publish(msg)

    def button_callback(self,msg):
        self.reverse = msg.button_1.is_pressed




def main(args=None):

    rclpy.init(args=args)

    node = LightringNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
