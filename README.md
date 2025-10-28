# PyAPI-RTS

**A Python library to read and manipulate RSCAD draft files.**

See <a href="examples/simple_example/simple_example.ipynb">examples/simple_example/simple_example.ipynb</a> for a short preview of the API or take a look into our <a href="docs/pyapi_rts.pdf">documentation</a>.

## Installation

To install this project, perform the following steps:

1. Clone the project
2. `cd` into the cloned directory
3. `pip install poetry`
4. `poetry install`

## Generate classes from RSCAD components

Before the first use of the project, the classes for the components in the RSCAD master library need to be generated.

1. Copy the files from the `COMPONENTS` directory into `pyapi_rts/pyapi_rts/class_extractor/COMPONENTS`.

2. Run `poetry run python ./pyapi_rts/class_extractor/main.py`

Other options for the class generation:

- \-d: Set to delete the output folder before new classes are generated
- \-o: Set to include the OBSOLETE folder in the generation. Recommended if you use .dfx files converted from older versions
- \-p: Set path to COMPONENTS folder
- \-t: Set thread count used to parse the files. Default: 8 

! The progress bar is not accurate due to optimizations applied during generation.

## Run tests

`poetry run pytest`

## Workshop Projects

The `workshop/` directory contains example implementations and projects built with PyAPI-RTS:

### IEEE 13 Node Test Feeder

A complete implementation of the IEEE 13 bus distribution test system. This project demonstrates how to use PyAPI-RTS to build standard benchmark distribution systems.

**Location**: `workshop/ieee_13_bus/`

**Features**:
- Complete system configuration data (13 nodes, 12 line segments)
- Automated builder class for RSCAD model generation
- Load analysis and validation utilities
- Network topology visualization
- Comprehensive documentation

**Quick Start**:
```python
from workshop.ieee_13_bus import IEEE13BusBuilder

builder = IEEE13BusBuilder()
print(builder.get_summary())

# Generate .dfx file (requires RSCAD component classes)
# draft = builder.build()
# draft.write_file("ieee_13_bus.dfx")
```

**Documentation**: See `workshop/ieee_13_bus/README.md` for detailed information.

**System Specifications**:
- Nominal Voltage: 4.16 kV
- Total Load: 3,466 kW + 2,102 kVAr
- Components: 1 voltage regulator, 2 transformers, 8 spot loads, 2 capacitor banks
- Mixed overhead and underground lines
- Unbalanced loading with multiple load models (PQ, I, Z)

For more workshop projects and examples, see `workshop/README.md`.

## Citing

> M. Weber, J. Enzinger, H. K. Çakmak, U. Kühnapfel and V. Hagenmeyer, "PyAPI-RTS: A Python-API for RSCAD Modeling," 2023 Open Source Modelling and Simulation of Energy Systems (OSMSES), Aachen, Germany, 2023, pp. 1-7, doi: [10.1109/OSMSES58477.2023.10089671](https://doi.org/10.1109/OSMSES58477.2023.10089671).
