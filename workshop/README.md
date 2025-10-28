# PyAPI-RTS Workshop

This directory contains example projects and implementations built using the PyAPI-RTS library.

## Projects

### IEEE 13 Node Test Feeder

A complete implementation of the IEEE 13 bus distribution test system.

**Location**: `ieee_13_bus/`

**Description**: This module provides a full implementation of the IEEE 13 Node Test Feeder, a standard benchmark distribution system published by the IEEE Distribution System Analysis Subcommittee. The implementation includes all system components: voltage regulators, transformers, overhead and underground lines, loads, and capacitor banks.

**Features**:
- Complete system configuration data
- Automated builder class for RSCAD model generation
- Validation and analysis utilities
- Network visualization tools
- Comprehensive documentation

**Quick Start**:
```python
from workshop.ieee_13_bus import IEEE13BusBuilder

builder = IEEE13BusBuilder()
draft = builder.build()
draft.write_file("ieee_13_bus.dfx")
```

See `ieee_13_bus/README.md` for detailed documentation.

## Purpose

The workshop directory serves as:

1. **Learning Resource**: Examples demonstrating PyAPI-RTS capabilities
2. **Reference Implementation**: Best practices for building RSCAD models
3. **Testing Ground**: Validation of PyAPI-RTS functionality
4. **Template Collection**: Starting points for new projects

## Structure

```
workshop/
├── README.md                    # This file
└── ieee_13_bus/                 # IEEE 13 bus test feeder
    ├── __init__.py              # Module exports
    ├── config.py                # System configuration data
    ├── builder.py               # IEEE13BusBuilder class
    ├── utils.py                 # Analysis and validation tools
    ├── main.py                  # Command-line interface
    ├── example.py               # Usage examples
    ├── test_config.py           # Configuration tests
    └── README.md                # Project documentation
```

## Requirements

All workshop projects require:
- PyAPI-RTS installation
- Python 3.10 or higher
- Generated RSCAD component classes (see main README)

## Contributing

To add a new workshop project:

1. Create a new directory under `workshop/`
2. Include at minimum:
   - `README.md` - Project documentation
   - `__init__.py` - Module initialization
   - Configuration/data files
   - Builder/implementation code
   - Example usage

3. Follow the IEEE 13 bus project structure as a template
4. Update this README with a description of your project

## License

All workshop projects are part of PyAPI-RTS and licensed under LGPL-3.0.

## References

- PyAPI-RTS main documentation: `../docs/`
- IEEE test feeders: http://ewh.ieee.org/soc/pes/dsacom/testfeeders.html
