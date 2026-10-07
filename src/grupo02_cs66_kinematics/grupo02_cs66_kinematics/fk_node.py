import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import numpy as np


DH_PARAMS = [
    [0.1625,  0.0,    -np.pi/2],  # A01
    [0.0,     0.427,   0.0],      # A12
    [0.1475,  0.3905,  0.0],      # A23
    [0.0,     0.0,    -np.pi/2],  # A34
    [0.0965,  0.0,     np.pi/2],  # A45
    [0.095,   0.0,     0.0]       # A56
]

def dh_transform(q, d, a, alpha):
    ct, st = np.cos(q), np.sin(q)
    ca, sa = np.cos(alpha), np.sin(alpha)
    return np.array([
        [ct, -st * ca,  st * sa, a * ct],
        [st,  ct * ca, -ct * sa, a * st],
        [0.0,      sa,       ca,      d],
        [0.0,     0.0,      0.0,    1.0]
    ])

def forward_kinematics(q):
    T = np.eye(4)
    for i in range(6):
        d, a, alpha = DH_PARAMS[i]
        
        if i == 0:
            theta = q[i] + np.pi
        else:
            theta = q[i]
            
        T = T @ dh_transform(theta, d, a, alpha)
        
    return T

class FKNode(Node):
    def __init__(self):
        super().__init__('fk_node')
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10)
        self.get_logger().info('Nodo FK iniciado.')

    def joint_state_callback(self, msg):
        # Mapear las posiciones articulares asegurando el orden correcto
        joint_positions = dict(zip(msg.name, msg.position))
        
        # Nombres típicos de las 6 articulaciones
        expected_names = [
            'shoulder_pan_joint',
            'shoulder_lift_joint',
            'elbow_joint',
            'wrist_1_joint',
            'wrist_2_joint',
            'wrist_3_joint'
        ]
        
        q = []
        for name in expected_names:
            if name in joint_positions:
                q.append(joint_positions[name])
            else:
                if len(msg.position) >= 6:
                    q = list(msg.position[:6])
                    break
                return

        q = np.array(q)
        
        T_total = forward_kinematics(q)
        pos = T_total[:3, 3]
        
        self.get_logger().info(
            f'\nCINEMÁTICA DIRECTA (FK)'
            f'\nÁngulos q (rad): {np.round(q, 3)}'
            f'\nPosición del efector final:'
            f'\n  X: {pos[0]:.4f} m'
            f'\n  Y: {pos[1]:.4f} m'
            f'\n  Z: {pos[2]:.4f} m'
        )

def main(args=None):
    rclpy.init(args=args)
    node = FKNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Apagando por interrupción del usuario...')
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()