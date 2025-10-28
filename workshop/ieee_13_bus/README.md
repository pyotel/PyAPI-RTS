# IEEE 13 Node Test Feeder

This module provides a complete implementation of the IEEE 13 bus test system using PyAPI-RTS for RSCAD modeling.

## Overview

The IEEE 13 Node Test Feeder is a standard benchmark distribution system published by the IEEE Distribution System Analysis Subcommittee. This implementation creates an RSCAD model of the system based on the official specification.

## System Characteristics

- **Nominal Voltage**: 4.16 kV
- **Number of Nodes**: 13
- **System Type**: 4-wire wye, radial distribution feeder
- **Features**:
  - One substation voltage regulator (3-phase, wye-connected)
  - Mixed overhead and underground lines
  - Various phasing configurations
  - Shunt capacitor banks
  - In-line transformer (4.16 kV to 0.48 kV)
  - Unbalanced spot and distributed loads
  - Multiple load models (constant PQ, constant I, constant Z)

## Installation

This module is part of the PyAPI-RTS workshop. Ensure you have PyAPI-RTS installed:

```bash
cd /path/to/PyAPI-RTS
poetry install
```

## Usage

### Basic Usage

```python
from workshop.ieee_13_bus import IEEE13BusBuilder

# Create builder
builder = IEEE13BusBuilder()

# Build the complete system
draft = builder.build()

# Write to .dfx file
draft.write_file("ieee_13_bus.dfx")
```

### Command Line Usage

```bash
# Build and show summary
python -m workshop.ieee_13_bus.main --summary

# Build and export to file
python -m workshop.ieee_13_bus.main --output my_model.dfx

# Or directly
cd workshop/ieee_13_bus
python main.py -o output.dfx
```

## System Components

### Nodes

The system consists of 13 nodes:
- **650**: Source node with voltage regulator
- **632**: Main distribution bus
- **633-634**: Transformer branch (4.16kV to 0.48kV)
- **645-646**: Lateral branch
- **671**: Main feeder junction
- **680, 684, 692, 675**: Main feeder nodes
- **652**: Underground lateral
- **611**: Single-phase lateral

### Line Segments

| From | To  | Length (ft) | Type | Configuration |
|------|-----|-------------|------|---------------|
| 650  | 632 | 2000        | OH   | 601 (B-A-C-N) |
| 632  | 633 | 500         | OH   | 602 (C-A-B-N) |
| 633  | 634 | 0           | -    | Transformer   |
| 632  | 645 | 500         | OH   | 603 (C-B-N)   |
| 645  | 646 | 300         | OH   | 603 (C-B-N)   |
| 632  | 671 | 2000        | OH   | 601 (B-A-C-N) |
| 671  | 684 | 300         | OH   | 604 (A-C-N)   |
| 671  | 680 | 1000        | OH   | 601 (B-A-C-N) |
| 671  | 692 | 0           | -    | Switch        |
| 684  | 652 | 800         | UG   | 607 (A-N)     |
| 684  | 611 | 300         | OH   | 605 (C-N)     |
| 692  | 675 | 500         | UG   | 606 (A-B-C-N) |

OH = Overhead, UG = Underground

### Loads

#### Spot Loads

| Node | Model | Ph-A (kW) | Ph-A (kVAr) | Ph-B (kW) | Ph-B (kVAr) | Ph-C (kW) | Ph-C (kVAr) |
|------|-------|-----------|-------------|-----------|-------------|-----------|-------------|
| 634  | Y-PQ  | 160       | 110         | 120       | 90          | 120       | 90          |
| 645  | Y-PQ  | 0         | 0           | 170       | 125         | 0         | 0           |
| 646  | D-Z   | 0         | 0           | 230       | 132         | 0         | 0           |
| 652  | Y-Z   | 128       | 86          | 0         | 0           | 0         | 0           |
| 671  | D-PQ  | 385       | 220         | 385       | 220         | 385       | 220         |
| 675  | Y-PQ  | 485       | 190         | 68        | 60          | 290       | 212         |
| 692  | D-I   | 0         | 0           | 0         | 0           | 170       | 151         |
| 611  | Y-I   | 0         | 0           | 0         | 0           | 170       | 80          |

#### Distributed Loads

| From | To  | Model | Ph-A (kW) | Ph-A (kVAr) | Ph-B (kW) | Ph-B (kVAr) | Ph-C (kW) | Ph-C (kVAr) |
|------|-----|-------|-----------|-------------|-----------|-------------|-----------|-------------|
| 632  | 671 | Y-PQ  | 17        | 10          | 66        | 38          | 117       | 68          |

**Total Load**: 3266 kW + 1986 kVAr

### Capacitor Banks

| Node | Ph-A (kVAr) | Ph-B (kVAr) | Ph-C (kVAr) | Total (kVAr) |
|------|-------------|-------------|-------------|--------------|
| 675  | 200         | 200         | 200         | 600          |
| 611  | 0           | 0           | 100         | 100          |

**Total Capacitance**: 700 kVAr

### Voltage Regulator

- **Location**: Between nodes 650 and 632
- **Type**: 3-phase, wye-grounded
- **Settings**:
  - Voltage level: 122V (on 120V base)
  - Bandwidth: 2V
  - R setting: 3Ω (all phases)
  - X setting: 9Ω (all phases)
  - PT ratio: 20
  - CT rating: 700A

### Transformers

#### Substation Transformer
- **Rating**: 5000 kVA
- **Primary**: 115 kV, Delta
- **Secondary**: 4.16 kV, Grounded Wye
- **Impedance**: 1% R, 8% X

#### XFM-1 (In-line Transformer)
- **Rating**: 500 kVA
- **Primary**: 4.16 kV, Grounded Wye
- **Secondary**: 0.48 kV, Grounded Wye
- **Impedance**: 1.1% R, 2% X

## Module Structure

```
ieee_13_bus/
├── __init__.py          # Module exports
├── config.py            # System configuration data
├── builder.py           # IEEE13BusBuilder class
├── main.py              # Command-line interface
└── README.md            # This file
```

## Configuration Data

All system data is defined in `config.py`:

- **CONDUCTORS**: Overhead conductor specifications
- **CABLES**: Underground cable specifications
- **LINE_CONFIGS**: Line configuration details
- **LINE_SEGMENTS**: Network topology
- **SPOT_LOADS**: Node loads
- **DISTRIBUTED_LOADS**: Distributed line loads
- **CAPACITOR_BANKS**: Shunt capacitor specifications
- **TRANSFORMERS**: Transformer ratings
- **REGULATOR**: Voltage regulator settings
- **NODES**: List of all buses
- **NODE_COORDS**: Layout coordinates

## API Reference

### IEEE13BusBuilder

Main builder class for constructing the system.

#### Methods

- `__init__()`: Initialize a new builder
- `create_subsystem()`: Create the main subsystem canvas
- `create_nodes()`: Define node positions
- `add_source()`: Add substation and source
- `add_voltage_regulator()`: Add voltage regulator
- `add_line_segments()`: Create all transmission lines
- `add_transformers()`: Add transformer XFM-1
- `add_loads()`: Add all loads (spot and distributed)
- `add_capacitors()`: Add capacitor banks
- `build()`: Build complete system (chains all methods)
- `get_summary()`: Get system statistics

#### Example

```python
builder = IEEE13BusBuilder()

# Build step by step
builder.create_subsystem()
builder.create_nodes()
builder.add_source()
builder.add_voltage_regulator()
# ... etc

# Or build all at once
draft = builder.build()
```

## Notes

### Prerequisites

Before running this module, ensure that RSCAD component classes have been generated:

```bash
# Copy COMPONENTS directory to class_extractor/COMPONENTS/
poetry run python ./pyapi_rts/class_extractor/main.py
```

### Load Models

The system uses three types of load models:

- **PQ (Y-PQ, D-PQ)**: Constant power (kW and kVAr)
- **I (Y-I, D-I)**: Constant current
- **Z (Y-Z, D-Z)**: Constant impedance

For constant current and impedance models, the kW/kVAr values are converted assuming rated voltage (1.0 per-unit).

### Phasing Notation

- **Y**: Wye (star) connection
- **D**: Delta connection
- Phase order: A-B-C
- Wye loads: connected phase-to-ground (a-g, b-g, c-g)
- Delta loads: connected phase-to-phase (a-b, b-c, c-a)

## Reference

Based on: "Radial Distribution Test Feeders", IEEE Distribution System Analysis Subcommittee Report

Official data available at:
http://ewh.ieee.org/soc/pes/dsacom/testfeeders.html

## License

This implementation is part of PyAPI-RTS and follows the same license (LGPL-3.0).
