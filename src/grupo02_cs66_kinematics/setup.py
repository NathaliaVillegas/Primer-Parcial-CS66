from setuptools import find_packages, setup

package_name = 'grupo02_cs66_kinematics'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='nath',
    maintainer_email='nathalia.villegas@ucb.edu.bo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'fk_node = grupo02_cs66_kinematics.fk_node:main',
            'ik_node = grupo02_cs66_kinematics.ik_node:main',
        ],
    },
)
