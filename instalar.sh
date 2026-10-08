#!/usr/bin/env bash
set -eo pipefail

if [ ! -f /opt/ros/jazzy/setup.bash ]; then
  echo "ERROR: ROS 2 Jazzy no está instalado en /opt/ros/jazzy."
  exit 1
fi
source /opt/ros/jazzy/setup.bash

sudo apt update
sudo apt install -y \
  git \
  python3-colcon-common-extensions \
  python3-rosdep \
  python3-vcstool \
  ros-jazzy-xacro \
  ros-jazzy-rviz2 \
  ros-jazzy-robot-state-publisher \
  ros-jazzy-joint-state-publisher \
  ros-jazzy-joint-state-publisher-gui \
  ros-jazzy-urdf \
  ros-jazzy-urdfdom \
  ros-jazzy-urdf-tutorial \
  ros-jazzy-rmw-cyclonedds-cpp \
  liburdfdom-tools

if [ ! -e /etc/ros/rosdep/sources.list.d/20-default.list ]; then
  sudo rosdep init || true
fi
rosdep update || true

WS="$HOME/grupo_02_cs66_ws"
cd "$WS"
rosdep install --from-paths src --ignore-src -r -y --rosdistro jazzy || true

echo "Compilando el workspace"
colcon build --symlink-install

chmod +x "$WS/entorno.sh"

echo
echo "INSTALACIÓN COMPLETA - Elite Robots CS66"
echo "Workspace compilado correctamente en: $WS"
echo "Para abrir el robot ejecute:"
echo "  source entorno.sh"
echo "  ros2 launch grupo02_cs66_bringup display.launch.py"