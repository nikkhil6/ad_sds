"""
Synthetic Automotive Radar Data Generator
========================================

This script generates realistic synthetic radar data for autonomous vehicle 
sensor processing development. It simulates a Bosch LRR4-like automotive radar
sensor operating in an urban environment.

Key Features:
- Realistic radar physics and detection models
- Target tracking with persistent IDs
- Ground clutter simulation
- Multipath reflection effects
- Detection probability based on range and RCS
- Realistic motion patterns for moving targets

Author: AD Sensor Stack Development

"""

import csv
import random
import math
import time
from enum import Enum
from datetime import datetime

class TargetClass(Enum):
    """Target classification for radar detections."""
    VEHICLE = "vehicle"
    PEDESTRIAN = "pedestrian"
    BICYCLE = "bicycle"
    STATIC_OBJECT = "static_object"

# =============================================================================
# RADAR SYSTEM PARAMETERS (Based on Bosch LRR4 specifications)
# =============================================================================

RANGE_MIN = 0.2    # meters
RANGE_MAX = 250.0  # meters
ANGLE_MIN = -60.0  # degrees
ANGLE_MAX = 60.0   # degrees
VEL_MIN = -50.0    # m/s
VEL_MAX = 50.0     # m/s
RCS_MIN = -10.0    # dBsm
RCS_MAX = 30.0     # dBsm

# =============================================================================
# SIMULATION PARAMETERS
# =============================================================================

NUM_FRAMES = 100
FRAME_PERIOD = 0.1  # seconds

NOISE_STD_RANGE = 0.1
NOISE_STD_ANGLE = 0.1
NOISE_STD_VEL = 0.1
NOISE_STD_RCS = 0.5

# =============================================================================
# DETECTION PROBABILITY PARAMETERS
# =============================================================================

DETECTION_PROB_BASE = 0.95
RANGE_DECAY_FACTOR = 0.001
RCS_THRESHOLD = -10.0

# =============================================================================
# MULTIPATH AND CLUTTER PARAMETERS
# =============================================================================

MULTIPATH_PROB = 0.15
CLUTTER_DENSITY = 0.02
GROUND_CLUTTER_RANGE = 2.0

class Target:
    """Represents a radar target with realistic motion and detection characteristics."""
    def __init__(self, target_id, target_class, initial_range, angle, velocity, rcs, is_static=True):
        self.target_id = target_id
        self.target_class = target_class
        self.range = initial_range
        self.angle = angle
        self.velocity = velocity
        self.rcs = rcs
        self.is_static = is_static
        self.track_quality = 1.0
        self.age = 0
        self.acceleration = 0.0
        self.angular_velocity = 0.0

    def update(self, dt):
        """Update target position and motion for the next time step."""
        if not self.is_static:
            self.velocity += self.acceleration * dt
            self.range += self.velocity * dt
            self.angle += self.angular_velocity * dt
            self.acceleration += random.gauss(0, 0.5)
            self.angular_velocity += random.gauss(0, 0.1)
            self.velocity = max(VEL_MIN, min(VEL_MAX, self.velocity))
            self.angle = max(ANGLE_MIN, min(ANGLE_MAX, self.angle))
            self.range = max(RANGE_MIN, min(RANGE_MAX, self.range))
        self.age += 1

    def get_detection_probability(self):
        """Calculate the probability that this target will be detected by the radar."""
        range_factor = math.exp(-RANGE_DECAY_FACTOR * self.range)
        rcs_factor = max(0, (self.rcs - RCS_THRESHOLD) / (RCS_MAX - RCS_THRESHOLD))
        return DETECTION_PROB_BASE * range_factor * rcs_factor

def generate_ground_clutter():
    """Generate realistic ground clutter points."""
    clutter_points = []
    num_clutter = int(CLUTTER_DENSITY * 100)
    for _ in range(num_clutter):
        range_clutter = random.uniform(2.0, 10.0)
        angle_clutter = random.uniform(ANGLE_MIN, ANGLE_MAX)
        rcs_clutter = random.uniform(-15.0, -5.0)
        clutter_points.append({
            'range': range_clutter,
            'angle': angle_clutter,
            'rcs': rcs_clutter,
            'is_clutter': True
        })
    return clutter_points

def add_multipath_effects(targets):
    """Add multipath reflection effects for moving targets."""
    multipath_targets = []
    for target in targets:
        if random.random() < MULTIPATH_PROB and not target.is_static:
            multipath_range = target.range + random.uniform(5.0, 15.0)
            multipath_angle = target.angle + random.uniform(-5.0, 5.0)
            multipath_rcs = target.rcs - random.uniform(5.0, 10.0)
            multipath_targets.append({
                'range': multipath_range,
                'angle': multipath_angle,
                'rcs': multipath_rcs,
                'is_multipath': True
            })
    return multipath_targets

# =============================================================================
# SCENARIO DEFINITION - Urban Environment with Multiple Target Types
# =============================================================================

STATIC_TARGETS = [
    Target(0, TargetClass.STATIC_OBJECT, 15.0, -20.0, 0.0, 12.0, True),
    Target(1, TargetClass.STATIC_OBJECT, 30.0, 10.0, 0.0, 18.0, True),
    Target(2, TargetClass.STATIC_OBJECT, 50.0, 0.0, 0.0, 25.0, True),
    Target(3, TargetClass.STATIC_OBJECT, 80.0, 8.0, 0.0, 8.0, True),
]

MOVING_TARGETS = [
    Target(4, TargetClass.VEHICLE, 40.0, -10.0, -8.0, 15.0, False),
    Target(5, TargetClass.BICYCLE, 60.0, 5.0, 5.0, 5.0, False),
]

MOVING_TARGETS[0].acceleration = -0.5
MOVING_TARGETS[1].angular_velocity = 0.2

# =============================================================================
# DATA GENERATION
# =============================================================================

# Create unique filename with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_CSV = f'data/raw/radar/synthetic_radar_data_{timestamp}.csv'

with open(OUTPUT_CSV, 'w', newline='') as csvfile:
    fieldnames = [
        'timestamp', 'frame', 'target_id', 'range_m', 'angle_deg',
        'radial_velocity_mps', 'rcs_dbsm', 'is_static', 'target_class',
        'track_quality', 'age', 'is_clutter', 'is_multipath'
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    start_time = time.time()
    for frame in range(NUM_FRAMES):
        timestamp = start_time + frame * FRAME_PERIOD
        all_targets = STATIC_TARGETS + MOVING_TARGETS
        for target in all_targets:
            target.update(FRAME_PERIOD)
        clutter_points = generate_ground_clutter()
        multipath_points = add_multipath_effects(MOVING_TARGETS)
        detections = []
        for target in all_targets:
            if random.random() < target.get_detection_probability():
                noisy_range = target.range + random.gauss(0, NOISE_STD_RANGE)
                noisy_angle = target.angle + random.gauss(0, NOISE_STD_ANGLE)
                noisy_velocity = target.velocity + random.gauss(0, NOISE_STD_VEL)
                noisy_rcs = target.rcs + random.gauss(0, NOISE_STD_RCS)
                noisy_range = max(RANGE_MIN, min(RANGE_MAX, noisy_range))
                noisy_angle = max(ANGLE_MIN, min(ANGLE_MAX, noisy_angle))
                noisy_velocity = max(VEL_MIN, min(VEL_MAX, noisy_velocity))
                noisy_rcs = max(RCS_MIN, min(RCS_MAX, noisy_rcs))
                detections.append({
                    'timestamp': round(timestamp, 3),
                    'frame': frame,
                    'target_id': target.target_id,
                    'range_m': round(noisy_range, 2),
                    'angle_deg': round(noisy_angle, 2),
                    'radial_velocity_mps': round(noisy_velocity, 2),
                    'rcs_dbsm': round(noisy_rcs, 2),
                    'is_static': target.is_static,
                    'target_class': target.target_class.value,
                    'track_quality': round(target.track_quality, 2),
                    'age': target.age,
                    'is_clutter': False,
                    'is_multipath': False
                })
        for i, clutter in enumerate(clutter_points):
            if random.random() < 0.3:
                detections.append({
                    'timestamp': round(timestamp, 3),
                    'frame': frame,
                    'target_id': f'clutter_{frame}_{i}',
                    'range_m': round(clutter['range'], 2),
                    'angle_deg': round(clutter['angle'], 2),
                    'radial_velocity_mps': 0.0,
                    'rcs_dbsm': round(clutter['rcs'], 2),
                    'is_static': True,
                    'target_class': 'clutter',
                    'track_quality': 0.1,
                    'age': 0,
                    'is_clutter': True,
                    'is_multipath': False
                })
        for i, multipath in enumerate(multipath_points):
            if random.random() < 0.7:
                detections.append({
                    'timestamp': round(timestamp, 3),
                    'frame': frame,
                    'target_id': f'multipath_{frame}_{i}',
                    'range_m': round(multipath['range'], 2),
                    'angle_deg': round(multipath['angle'], 2),
                    'radial_velocity_mps': 0.0,
                    'rcs_dbsm': round(multipath['rcs'], 2),
                    'is_static': True,
                    'target_class': 'multipath',
                    'track_quality': 0.3,
                    'age': 0,
                    'is_clutter': False,
                    'is_multipath': True
                })
        for detection in detections:
            writer.writerow(detection)

print(f"synthetic radar data written to {OUTPUT_CSV}")