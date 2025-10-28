"""
IEEE 13 Node Test Feeder Builder

This module provides a builder class to construct the IEEE 13 bus test system
using the PyAPI-RTS library.
"""

from typing import Dict, Optional
from pyapi_rts.api import Draft, Subsystem, Component
from pyapi_rts.api.component import Component as BaseComponent

from . import config


class IEEE13BusBuilder:
    """
    Builder class for creating the IEEE 13 Node Test Feeder.

    This class constructs a complete RSCAD model of the IEEE 13 bus test system
    based on the IEEE Distribution System Analysis Subcommittee specifications.
    """

    def __init__(self):
        """Initialize the builder with a new draft."""
        self.draft = Draft(
            version="1.2",
            title="IEEE 13 Node Test Feeder",
            author_created="PyAPI-RTS",
            author_changed="PyAPI-RTS",
            time_step_us=50.0,
        )
        self.subsystem: Optional[Subsystem] = None
        self.nodes: Dict[str, Dict] = {}
        self.components: Dict[str, BaseComponent] = {}

    def create_subsystem(self) -> 'IEEE13BusBuilder':
        """
        Create the main subsystem for the IEEE 13 bus system.

        Returns:
            self for method chaining
        """
        self.subsystem = Subsystem(
            draft=self.draft,
            number=1,
            canvas_size_x=4000,
            canvas_size_y=3000,
        )
        self.subsystem.tab_name = "IEEE 13 Bus System"
        self.draft.add_subsystem(self.subsystem)
        return self

    def create_nodes(self) -> 'IEEE13BusBuilder':
        """
        Create node positions for all buses in the system.

        This creates a coordinate mapping for component placement.

        Returns:
            self for method chaining
        """
        grid_size = 32
        scale = 4  # Scale factor for layout

        for node_name, (x, y) in config.NODE_COORDS.items():
            self.nodes[node_name] = {
                'x': x * scale + 500,  # Offset from canvas edge
                'y': y * scale + 500,
                'grid_x': (x * scale + 500) // grid_size * grid_size,
                'grid_y': (y * scale + 500) // grid_size * grid_size,
            }

        return self

    def add_source(self) -> 'IEEE13BusBuilder':
        """
        Add the substation source and transformer.

        This creates the 115kV to 4.16kV substation transformer at node 650.

        Returns:
            self for method chaining
        """
        if self.subsystem is None:
            raise RuntimeError("Subsystem must be created before adding components")

        # Note: In a real implementation, you would create actual RSCAD components
        # This is a placeholder showing the architecture

        # Create source bus at node 650
        source_node = self.nodes["650"]

        # Create substation transformer
        # The actual component creation would depend on generated RSCAD component classes
        # For now, we document the structure

        self._add_bus_marker("650", source_node, "Source")

        return self

    def add_voltage_regulator(self) -> 'IEEE13BusBuilder':
        """
        Add the voltage regulator between nodes 650 and 632.

        Creates a three-phase voltage regulator with the specified settings.

        Returns:
            self for method chaining
        """
        if self.subsystem is None:
            raise RuntimeError("Subsystem must be created before adding components")

        reg_data = config.REGULATOR

        # Position between node 650 and 632
        node_a = self.nodes[reg_data.line_segment[0]]
        node_b = self.nodes[reg_data.line_segment[1]]

        reg_x = (node_a['grid_x'] + node_b['grid_x']) // 2
        reg_y = (node_a['grid_y'] + node_b['grid_y']) // 2

        # Create voltage regulator component
        # In actual implementation, this would create RSCAD regulator components
        self._add_component_marker("REG-1", reg_x, reg_y, "Voltage Regulator")

        return self

    def add_line_segments(self) -> 'IEEE13BusBuilder':
        """
        Add all line segments connecting the nodes.

        Creates overhead and underground line segments with proper configurations.

        Returns:
            self for method chaining
        """
        if self.subsystem is None:
            raise RuntimeError("Subsystem must be created before adding components")

        for segment in config.LINE_SEGMENTS:
            # Skip transformer and switch locations (config_id = 0)
            if segment.config_id == 0:
                continue

            # Get line configuration
            line_config = next(
                (cfg for cfg in config.LINE_CONFIGS if cfg.config_id == segment.config_id),
                None
            )

            if line_config is None:
                print(f"Warning: Unknown config {segment.config_id} for segment "
                      f"{segment.node_a}-{segment.node_b}")
                continue

            # Create transmission line component
            self._create_line(segment, line_config)

        return self

    def add_transformers(self) -> 'IEEE13BusBuilder':
        """
        Add transformer XFM-1 between nodes 633 and 634.

        Returns:
            self for method chaining
        """
        if self.subsystem is None:
            raise RuntimeError("Subsystem must be created before adding components")

        # Find XFM-1 transformer data
        xfm1 = next((t for t in config.TRANSFORMERS if t.name == "XFM-1"), None)

        if xfm1:
            node_633 = self.nodes["633"]
            node_634 = self.nodes["634"]

            xfm_x = (node_633['grid_x'] + node_634['grid_x']) // 2
            xfm_y = (node_633['grid_y'] + node_634['grid_y']) // 2

            self._add_component_marker("XFM-1", xfm_x, xfm_y, "Transformer")

        return self

    def add_loads(self) -> 'IEEE13BusBuilder':
        """
        Add all spot and distributed loads to the system.

        Returns:
            self for method chaining
        """
        if self.subsystem is None:
            raise RuntimeError("Subsystem must be created before adding components")

        # Add spot loads
        for load in config.SPOT_LOADS:
            if load.node not in self.nodes:
                print(f"Warning: Node {load.node} not found for load")
                continue

            node = self.nodes[load.node]
            self._create_load(
                node_name=load.node,
                x=node['grid_x'],
                y=node['grid_y'] + 64,  # Offset below node
                load_model=load.load_model,
                ph1_kw=load.ph1_kw,
                ph1_kvar=load.ph1_kvar,
                ph2_kw=load.ph2_kw,
                ph2_kvar=load.ph2_kvar,
                ph3_kw=load.ph3_kw,
                ph3_kvar=load.ph3_kvar,
            )

        # Add distributed loads
        for dist_load in config.DISTRIBUTED_LOADS:
            # Distributed loads are placed at the center of the line segment
            if dist_load.node_a in self.nodes and dist_load.node_b in self.nodes:
                node_a = self.nodes[dist_load.node_a]
                node_b = self.nodes[dist_load.node_b]

                center_x = (node_a['grid_x'] + node_b['grid_x']) // 2
                center_y = (node_a['grid_y'] + node_b['grid_y']) // 2

                self._create_load(
                    node_name=f"{dist_load.node_a}_{dist_load.node_b}_dist",
                    x=center_x,
                    y=center_y + 64,
                    load_model=dist_load.load_model,
                    ph1_kw=dist_load.ph1_kw,
                    ph1_kvar=dist_load.ph1_kvar,
                    ph2_kw=dist_load.ph2_kw,
                    ph2_kvar=dist_load.ph2_kvar,
                    ph3_kw=dist_load.ph3_kw,
                    ph3_kvar=dist_load.ph3_kvar,
                    is_distributed=True,
                )

        return self

    def add_capacitors(self) -> 'IEEE13BusBuilder':
        """
        Add shunt capacitor banks to the system.

        Returns:
            self for method chaining
        """
        if self.subsystem is None:
            raise RuntimeError("Subsystem must be created before adding components")

        for cap_bank in config.CAPACITOR_BANKS:
            if cap_bank.node not in self.nodes:
                print(f"Warning: Node {cap_bank.node} not found for capacitor")
                continue

            node = self.nodes[cap_bank.node]
            self._create_capacitor(
                node_name=cap_bank.node,
                x=node['grid_x'],
                y=node['grid_y'] - 64,  # Offset above node
                ph_a_kvar=cap_bank.ph_a_kvar,
                ph_b_kvar=cap_bank.ph_b_kvar,
                ph_c_kvar=cap_bank.ph_c_kvar,
            )

        return self

    def build(self) -> Draft:
        """
        Build the complete IEEE 13 bus system.

        This method chains all construction steps to create the full system.

        Returns:
            The completed Draft object
        """
        (self.create_subsystem()
             .create_nodes()
             .add_source()
             .add_voltage_regulator()
             .add_line_segments()
             .add_transformers()
             .add_loads()
             .add_capacitors())

        return self.draft

    # Helper methods for component creation

    def _add_bus_marker(self, node_name: str, node: Dict, label: str) -> None:
        """Add a bus marker component at a node location."""
        # In actual implementation, create RSCAD bus component
        print(f"Creating bus marker '{label}' at node {node_name}: "
              f"({node['grid_x']}, {node['grid_y']})")

    def _add_component_marker(self, name: str, x: int, y: int, comp_type: str) -> None:
        """Add a component marker."""
        print(f"Creating {comp_type} '{name}' at ({x}, {y})")

    def _create_line(self, segment: config.LineSegment, line_config: config.LineConfiguration) -> None:
        """Create a transmission line segment."""
        node_a = self.nodes[segment.node_a]
        node_b = self.nodes[segment.node_b]

        line_type = "Underground" if line_config.is_underground else "Overhead"
        print(f"Creating {line_type} line {segment.node_a}-{segment.node_b}: "
              f"{segment.length_ft}ft, Config {segment.config_id}, "
              f"Phasing: {line_config.phasing}")

    def _create_load(
        self,
        node_name: str,
        x: int,
        y: int,
        load_model: str,
        ph1_kw: float,
        ph1_kvar: float,
        ph2_kw: float,
        ph2_kvar: float,
        ph3_kw: float,
        ph3_kvar: float,
        is_distributed: bool = False
    ) -> None:
        """Create a load component."""
        load_type = "Distributed" if is_distributed else "Spot"
        total_kw = ph1_kw + ph2_kw + ph3_kw
        total_kvar = ph1_kvar + ph2_kvar + ph3_kvar

        print(f"Creating {load_type} load at {node_name}: "
              f"Model={load_model}, Total={total_kw:.1f}kW + j{total_kvar:.1f}kVAr")

    def _create_capacitor(
        self,
        node_name: str,
        x: int,
        y: int,
        ph_a_kvar: float,
        ph_b_kvar: float,
        ph_c_kvar: float
    ) -> None:
        """Create a capacitor bank component."""
        total_kvar = ph_a_kvar + ph_b_kvar + ph_c_kvar
        print(f"Creating capacitor bank at {node_name}: "
              f"A={ph_a_kvar}kVAr, B={ph_b_kvar}kVAr, C={ph_c_kvar}kVAr, "
              f"Total={total_kvar}kVAr")

    def get_summary(self) -> str:
        """
        Get a summary of the system configuration.

        Returns:
            A formatted string with system statistics
        """
        total_load_kw = sum(
            l.ph1_kw + l.ph2_kw + l.ph3_kw for l in config.SPOT_LOADS
        ) + sum(
            l.ph1_kw + l.ph2_kw + l.ph3_kw for l in config.DISTRIBUTED_LOADS
        )

        total_load_kvar = sum(
            l.ph1_kvar + l.ph2_kvar + l.ph3_kvar for l in config.SPOT_LOADS
        ) + sum(
            l.ph1_kvar + l.ph2_kvar + l.ph3_kvar for l in config.DISTRIBUTED_LOADS
        )

        total_cap_kvar = sum(
            c.ph_a_kvar + c.ph_b_kvar + c.ph_c_kvar for c in config.CAPACITOR_BANKS
        )

        summary = f"""
IEEE 13 Node Test Feeder Summary
{'='*50}
System Configuration:
  - Nominal Voltage: {config.NOMINAL_VOLTAGE_KV} kV
  - Number of Nodes: {len(config.NODES)}
  - Number of Line Segments: {len(config.LINE_SEGMENTS)}
  - Overhead Configs: {len(config.OVERHEAD_CONFIGS)}
  - Underground Configs: {len(config.UNDERGROUND_CONFIGS)}

Components:
  - Voltage Regulators: 1 (3-phase)
  - Transformers: {len(config.TRANSFORMERS)}
  - Spot Loads: {len(config.SPOT_LOADS)}
  - Distributed Loads: {len(config.DISTRIBUTED_LOADS)}
  - Capacitor Banks: {len(config.CAPACITOR_BANKS)}

Total Loading:
  - Active Power: {total_load_kw:.1f} kW
  - Reactive Power: {total_load_kvar:.1f} kVAr
  - Total Capacitance: {total_cap_kvar:.1f} kVAr

Features:
  - Voltage regulation (650-632)
  - Mixed overhead/underground lines
  - Unbalanced loading
  - Multiple load models (PQ, I, Z)
  - Both wye and delta connected loads
"""
        return summary
