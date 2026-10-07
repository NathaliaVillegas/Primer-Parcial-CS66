import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
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

def get_position(q):
    T = np.eye(4)
    for i in range(6):
        d, a, alpha = DH_PARAMS[i]
        
        if i == 0:
            theta = q[i] + np.pi
        else:
            theta = q[i]
        T = T @ dh_transform(theta, d, a, alpha)
    return T[:3, 3]

def compute_jacobian_position(q, eps=1e-6):
    J = np.zeros((3, 6))
    p0 = get_position(q)
    for i in range(6):
        q_inc = np.copy(q)
        q_inc[i] += eps
        p_inc = get_position(q_inc)
        J[:, i] = (p_inc - p0) / eps
    return J

class IKNode(Node):
    def __init__(self):
        super().__init__('ik_node')
        
        self.subscription = self.create_subscription(
            Point,
            '/target',
            self.target_callback,
            10)
        
        self.publisher = self.create_publisher(JointState, '/joint_states', 10)
        
        self.q_current = np.array([0.0, -np.pi/4, np.pi/2, -np.pi/4, 0.0, 0.0])
        self.timer = self.create_timer(0.05, self.publish_joint_states)
        self.get_logger().info('Nodo IK iniciado.')

    def publish_joint_states(self):
        joint_msg = JointState()
        joint_msg.header.stamp = self.get_clock().now().to_msg()
        
        joint_msg.name = [
            'shoulder_pan_joint',
            'shoulder_lift_joint',
            'elbow_joint',
            'wrist_1_joint',
            'wrist_2_joint',
            'wrist_3_joint'
        ]
        
        joint_msg.position = self.q_current.tolist()
        self.publisher.publish(joint_msg)

    def target_callback(self, msg):
        target_pos = np.array([msg.x, msg.y, msg.z])
        q_init = np.copy(self.q_current)
        q = np.copy(q_init)
        
        max_iter = 200
        tol = 1e-4
        alpha = 0.5
        converged = False
        
        self.get_logger().info(f'\n--- NUEVO OBJETIVO: [{msg.x:.3f}, {msg.y:.3f}, {msg.z:.3f}] ---')
        
        for i in range(max_iter):
            p_current = get_position(q)
            error = target_pos - p_current
            if np.linalg.norm(error) < tol:
                converged = True
                break
            J = compute_jacobian_position(q)
            q = q + alpha * (np.linalg.pinv(J) @ error)
        
        p_final = get_position(q)
        self.q_current = q
        
        self.get_logger().info(
            f'\nRESULTADOS IK:'
            f'\nSolución articular q*: {np.round(q, 3)}'
            f'\nPosición alcanzada:   {np.round(p_final, 4)}'
            f'\nError final:          {np.linalg.norm(target_pos - p_final):.6f} m'
            f'\n¿Convergió?:          {converged}'
        )

def main(args=None):
    rclpy.init(args=args)
    node = IKNode()
    
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