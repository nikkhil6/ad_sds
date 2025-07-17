# Sensor Data Organization

This directory contains all sensor data for the AD Sensor Stack project.

## Directory Structure

```
data/
├── raw/                    # Raw sensor data files
│   ├── radar/             # Radar sensor data (CSV format)
│   ├── lidar/             # LiDAR sensor data (CSV/PCAP format)
│   ├── camera/            # Camera sensor data (images/videos)
│   └── imu/               # IMU sensor data (CSV format)
├── processed/             # Processed/filtered sensor data
└── ground_truth/          # Ground truth data (if available)
```

## File Naming Convention

All sensor data files follow this naming pattern:
- `synthetic_sensor_type]_data_YYYYMMDD_HHMMSS.csv`

Examples:
- `synthetic_radar_data_225716.csv`
- `synthetic_lidar_data_225716.csv`
- `synthetic_camera_data_2257164500## Data Generation Scripts

Scripts for generating synthetic sensor data are located in `scripts/`:
- `scripts/generate_radar_data.py` - Radar data generation
- `scripts/generate_lidar_data.py` - LiDAR data generation (template)
- `scripts/generate_camera_data.py` - Camera data generation (template)
- `scripts/generate_imu_data.py` - IMU data generation (template)

## Usage

1. Run data generation scripts from the project root:
   ```bash
   python3 scripts/generate_radar_data.py
   ```

2Data files will be automatically saved to the appropriate sensor directory with timestamps.

3. Each run creates a unique file, preventing data overwrites.

## Data Formats

### Radar Data
- **Format**: CSV
- **Columns**: timestamp, frame, target_id, range_m, angle_deg, radial_velocity_mps, rcs_dbsm, is_static, target_class, track_quality, age, is_clutter, is_multipath

### LiDAR Data (Template)
- **Format**: CSV
- **Columns**: timestamp, frame, point_id, range_m, azimuth_deg, elevation_deg, intensity, target_class

### Camera Data (Template)
- **Format**: MP4/Images
- **Content**: Synthetic camera frames with annotations

### IMU Data (Template)
- **Format**: CSV
- **Columns**: timestamp, frame, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z 