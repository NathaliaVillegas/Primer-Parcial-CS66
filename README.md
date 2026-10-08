# Primer Parcial - Cinemática Directa e Inversa del Robot Elite CS66

**Grupo:** 02  
**Integrantes:** Nathalia Villegas | Thais Mayta
**Robot:** Elite CS66 (6-DoF)  
**Sistema:** ROS 2 Jazzy / Ubuntu 24.04  


## Requisitos e Instalación

### Prerrequisitos
- ROS 2 instalado (versión Jazzy o Humble).
- Herramientas `colcon`, `rosdep` y `python3-numpy`.

### 1. Clonar el repositorio
Abra una terminal y clona este repositorio directamente en su directorio `HOME`. 
Dependiendo de cómo tenga configurada su conexión a GitHub en tu PC, elija una de las dos opciones:

**Opción A: Vía SSH (Si se tiene la key SSH configurada)**
```bash
cd ~
git clone git@github.com:NathaliaVillegas/Primer-Parcial-CS66.git grupo_02_cs66_ws

```

**Opción B: Vía HTTPS (Si no usa SSH)**
```bash
cd ~
git clone https://github.com/NathaliaVillegas/Primer-Parcial-CS66 grupo_02_cs66_ws

```

### 2. Instalación y Compilación
Ejecute el script de instalación para descargar dependencias y compilar el workspace:

```bash
cd ~/grupo_02_cs66_ws
chmod +x instalar.sh
./instalar.sh
```

## Guía de Ejecución y Pruebas

Para evaluar el correcto funcionamiento del paquete y los nodos de cinemática, es necesario abrir **cuatro terminales diferentes**. 

### Terminal 1: Lanzar el Entorno Visual (RViz)
Esta terminal iniciará la simulación del robot Elite CS66 y abrirá una ventana con deslizadores para controlar las articulaciones manualmente.

1. Abra una terminal nueva y ejecute:
```bash
cd ~/grupo_02_cs66_ws
source entorno.sh
ros2 launch grupo02_cs66_bringup display.launch.py
```
> Se abrirá RViz con el modelo 3D del robot y una ventana adicional llamada *Joint State Publisher*. Aún no mueva los deslizadores.

### Terminal 2: Probar la Cinemática Directa (FK)
Esta terminal ejecutará el nodo que lee los ángulos actuales del robot y calcula matemáticamente la posición y orientación del efector final.

1. Abra una segunda terminal y ejecute:
```bash
cd ~/grupo_02_cs66_ws
source entorno.sh
ros2 run grupo02_cs66_kinematics fk_node
```
> **Para probarlo** 
> - Vaya a la ventana de *Joint State Publisher* (abierta por la Terminal 1).
> - Mueva los deslizadores de las articulaciones (joint1, joint2, etc.).
> - Observe la **Terminal 2**: verá cómo se imprime en tiempo real la matriz de transformación y las coordenadas (X, Y, Z) del efector final calculadas por el algoritmo.

### Terminal 3: Ejecutar el nodo para la Cinemática Inversa (IK)
Esta terminal iniciará el nodo que queda a la espera de recibir coordenadas espaciales para calcular los ángulos de las articulaciones.

1. Abra una tercera terminal y ejecute:
```bash
cd ~/grupo_02_cs66_ws
source entorno.sh
ros2 run grupo02_cs66_kinematics ik_node
```
El nodo se quedará corriendo a la espera de recibir datos.

### Terminal 4: Enviar coordenadas para probar la IK
Para que el nodo de cinemática inversa calcule los ángulos, deberá publicarle una posición objetivo (X, Y, Z) mediante un tópico.

1. Abra una cuarta terminal y ejecute el comando para enviar las coordenadas una sola vez:

```bash
cd ~/grupo_02_cs66_ws
source entorno.sh
ros2 topic pub --once /target geometry_msgs/msg/Point "{x: 0.3, y: 0.2, z: 0.4}"
```

> **Para probarlo** 
> - Al ejecutar este comando en la Terminal 4, vuelva a mirar la Terminal 3.
> - La Terminal 3 recibirá las coordenadas enviadas y la pantalla imprimirá los valores articulares requeridos para que el robot alcance esa posición.


## Estructura del Proyecto

- `src/elite_robots_description/`: Archivos URDF y mallas 3D del fabricante.
- `src/grupo02_cs66_bringup/`: Archivos Launch y de visualización.
- `src/grupo02_cs66_kinematics/`: Nodos de Python con el cálculo de FK e IK.
- `Informe_CS66.pdf`: Documentación teórica y desarrollo matemático del parcial.