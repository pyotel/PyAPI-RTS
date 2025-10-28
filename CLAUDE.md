# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PyAPI-RTS is a Python library for reading and manipulating RSCAD draft files (.dfx). RSCAD is used for real-time digital simulation of power systems. This library provides an API to programmatically create, modify, and analyze RSCAD circuit models.

## Development Commands

### Setup
```bash
# Install poetry
pip install poetry

# Install dependencies
poetry install
```

### Class Generation (Required Before First Use)
Before using the project, generate component classes from RSCAD master library:

```bash
# Copy COMPONENTS directory files to pyapi_rts/class_extractor/COMPONENTS/ first
poetry run python ./pyapi_rts/class_extractor/main.py
```

Options:
- `-d`: Delete output folder before generation
- `-o`: Include OBSOLETE folder (recommended for older .dfx files)
- `-p <path>`: Set path to COMPONENTS folder
- `-t <count>`: Set thread count (default: 8)

### Testing
```bash
# Run all tests
poetry run pytest

# Run with multiple processes
poetry run pytest -n auto

# Run with coverage
poetry run pytest --cov=pyapi_rts
```

### Type Checking
```bash
poetry run mypy
```

Note: mypy.ini excludes `pyapi_rts/generated/`, `docs`, and `tests` directories.

### Code Formatting
```bash
poetry run black pyapi_rts/
```

## Architecture Overview

### Core Hierarchy

The library uses a hierarchical structure to represent RSCAD files:

1. **Draft** (`pyapi_rts/api/draft.py`): Top-level object representing an entire RSCAD .dfx file
   - Contains metadata (title, author, dates, simulation parameters)
   - Manages multiple Subsystems
   - Provides file I/O via `Draft.from_file(path)` and `draft.write_file(path)`
   - Uses cp1252 encoding for file operations

2. **Subsystem** (`pyapi_rts/api/subsystem.py`): A canvas/worksheet containing components
   - Inherits from both `DfxBlock` and `Container`
   - Each subsystem has a tab name and canvas dimensions
   - Contains Components, Hierarchies, and Groups

3. **Component** (`pyapi_rts/api/component.py`): Base class for all RSCAD components
   - Has parameters (accessed via `get_by_key(key)`, `set_by_key(key, value)`)
   - Positioned on grid (GRID_SIZE = 32)
   - Has rotation, mirror, and UUID
   - Can be connected to other components via connection points

4. **Container** (`pyapi_rts/api/container.py`): Abstract class for objects containing components
   - Used by Subsystem, Hierarchy, and Group
   - Provides methods: `get_components()`, `get_draft_vars()`, `search_by_name()`
   - Traverses hierarchy via `box_parent` property

5. **Hierarchy** (`pyapi_rts/api/hierarchy.py`): A component that can contain other components
   - Nested container structure for organizing circuits
   - Inherits from generated HIERARCHY class and Container

6. **Group** (`pyapi_rts/api/group.py`): Grouping mechanism for components
   - Similar to Hierarchy but for visual grouping

### Parameter System

Components have parameters stored in `_parameters` dict:
- **Parameter** (`pyapi_rts/api/parameters/parameter.py`): Base parameter class
- Typed parameters: `IntegerParameter`, `FloatParameter`, `StringParameter`, `EnumParameter`, `ColorParameter`
- **ParameterCollection**: Groups related parameters
- **ConnectionPoint**: Special parameter for electrical connections

### Graph Representation

The library can convert circuits to NetworkX graphs (`pyapi_rts/api/graph.py`):
- Nodes represent components (by UUID)
- Edges represent electrical connections with types:
  - `GRID`: Grid-based connections
  - `NAME`: Bus label connections through hierarchies
  - `LABEL`: Wire label connections
  - `TLINE`: Transmission line endpoints
  - `XRTRF`: Cross-rack transformer connections
  - `LINK`: Linked bus labels or nodes
  - `TLINE_CALC`: Transmission line calculation blocks

Use `draft.get_graph()` to generate the graph.

### Block Parsing System

RSCAD .dfx files are parsed using a block-based reader:
- **BlockReader** (`pyapi_rts/api/internals/blockreader.py`): Splits file into logical blocks
- **Block** (`pyapi_rts/api/internals/block.py`): Represents a section of the file
- **DfxBlock** (`pyapi_rts/api/internals/dfxblock.py`): Base class for objects that read/write blocks
- **ParametersBlock** (`pyapi_rts/api/internals/parameters_block.py`): Handles parameter parsing

### Class Generation System

The `class_extractor/` module generates Python classes from RSCAD component definition files:

1. **Readers** parse component definition files from COMPONENTS directory
2. **Extracted** data structures hold intermediate representation
3. **Generators** create Python class files in `pyapi_rts/generated/` directory
4. **Templates** provide code templates for generation

Generated classes inherit from Component and add component-specific parameters and graphics.

Key files:
- `class_extractor/main.py`: Entry point for class generation
- `class_extractor/generators/component_generator.py`: Generates component classes
- `class_extractor/generators/class_loader_generator.py`: Creates class loader
- Generated output: `pyapi_rts/generated/` (gitignored)

### TLine and Lark Parsing

Transmission line constants are parsed from .tli files:
- `pyapi_rts/api/lark/tli_transformer.py`: Lark-based parser for .tli files
- `pyapi_rts/api/lark/rlc_tline.py`: RLC transmission line representation
- Draft methods: `get_tline_constants(name)`, `get_rlc_tline(name)`

## File Structure Conventions

- Main API: `pyapi_rts/api/`
- Generated classes: `pyapi_rts/generated/` (not in version control)
- Component definitions: `pyapi_rts/class_extractor/COMPONENTS/` (not in version control)
- Tests mirror source structure: `tests/rscad_file_api/` and `tests/class_extractor/`
- Examples in Jupyter notebooks: `examples/*/`

## Common Patterns

### Reading a Draft
```python
from pyapi_rts.api import Draft
draft = Draft.from_file("path/to/file.dfx")
```

### Finding Components
```python
# Get all components recursively
components = draft.get_components(recursive=True)

# Get components by type
tlines = draft.get_components_by_type("lf_rtds_sharc_sld_TLINE")

# Search by name
comp = subsystem.search_by_name("BUS1", case_sensitive=False)

# Get by UUID
comp = draft.get_by_id(uuid_string)
```

### Modifying Parameters
```python
component.set_by_key("Name", "NewName")
value = component.get_by_key("Voltage")
```

### Working with Graph
```python
graph = draft.get_graph()
# graph is a networkx.MultiGraph
connected = get_connected_to(graph, component.uuid)
```

## Testing Notes

- Test files use unittest framework
- Test data typically in `tests/*/models/` directories
- Many test files are gitignored (see .gitignore for compiled RSCAD files)
- Use `PATH = pathlib.Path(__file__).parent.absolute().resolve()` pattern for test data paths

## Important Implementation Details

- File encoding: Always use `cp1252` for .dfx file I/O
- Grid size: Component positions snap to 32-unit grid
- UUIDs: Components have unique IDs accessible via `.uuid` property
- Cloning: `get_components()` returns deep copies by default (`clone=True`)
- Parameter access: Use `.get_by_key()` / `.set_by_key()` rather than direct parameter access
- Enumerations: Components can have enumeration applied (e.g., "BUS#1" → "BUS#2")
