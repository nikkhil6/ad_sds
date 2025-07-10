# Autonomous Sensor Data Processing Stack

## 🚗 Project Overview

This project aims to build a modular and real-time sensor data processing pipeline for autonomous driving applications. The system collects data from various sensors (e.g., LiDAR, camera, IMU, GPS), synchronizes the data using timestamps, and forwards it to a central compute unit such as a **Jetson Nano** or **Jetson AGX Xavier**.

The project is implemented using **ROS** (Robot Operating System) and **Python**, and is designed to run on real embedded hardware as a home robotics and learning project.

## 🧠 Learning Goals

- Gain hands-on experience with ROS and sensor drivers
- Learn to interface with real-world sensors
- Implement time synchronization and data logging
- Understand and build a scalable data acquisition stack for autonomous systems

## 🛠️ Tech Stack

| Component      | Technology           |
|----------------|----------------------|
| Programming    | Python               |
| Middleware     | ROS (Noetic / Humble)|
| Platform       | Jetson Nano / AGX    |
| Logging        | ROS bags / custom logs |
| Sync           | NTP / ROS Time / GPS-based |
| Sensors        | LiDAR, Camera, IMU, GPS |

## 🔧 Features

- Multi-sensor integration using ROS
- Time synchronization and unified timestamping
- Logging to disk with structured filenames and metadata
- Live monitoring and debug nodes
- Easily deployable on Jetson devices

## 🏁 Project Status

- [ ] Setup ROS environment
- [ ] Interface basic sensors (e.g., IMU, camera)
- [ ] Add timestamp synchronization
- [ ] Logging infrastructure (ROS bags or custom)
- [ ] Modular data publishing and subscribing
- [ ] Real-world testing on Jetson Nano

## 🗂️ Directory Structure

autonomous-sensor-stack/
├── config/                  # Configuration files (sensor calibration, parameters, etc.)
├── launch/                  # ROS launch files to start nodes
│   └── sample_talker.launch
├── nodes/                   # Custom ROS Python nodes
│   └── sample_talker.py     # Example publisher node
├── scripts/                 # Utility scripts (e.g., calibration, logging helpers)
├── logs/                    # Collected log data and rosbag files
├── docs/                    # Project documentation, diagrams, setup notes
├── requirements.txt         # Python dependencies
└── README.md                # Project overview and instructions
