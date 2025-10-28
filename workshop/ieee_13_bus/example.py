#!/usr/bin/env python3
"""
Example usage of the IEEE 13 bus builder.

This script demonstrates various ways to use the IEEE13BusBuilder class.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from workshop.ieee_13_bus import IEEE13BusBuilder, config
from workshop.ieee_13_bus.utils import (
    print_system_report,
    calculate_total_load,
    calculate_load_balance,
    get_node_connectivity,
    find_path,
    export_network_graph,
)


def example_1_basic_build():
    """Example 1: Basic system build"""
    print("Example 1: Basic Build")
    print("-" * 60)

    builder = IEEE13BusBuilder()
    draft = builder.build()

    print(f"Built system with {len(draft.subsystems)} subsystem(s)")
    print(f"Total components: {len(draft.get_components())}")
    print()


def example_2_step_by_step():
    """Example 2: Step-by-step construction"""
    print("Example 2: Step-by-Step Construction")
    print("-" * 60)

    builder = IEEE13BusBuilder()

    print("Creating subsystem...")
    builder.create_subsystem()

    print("Creating nodes...")
    builder.create_nodes()

    print("Adding source...")
    builder.add_source()

    print("Adding voltage regulator...")
    builder.add_voltage_regulator()

    print("Adding line segments...")
    builder.add_line_segments()

    print("Adding transformers...")
    builder.add_transformers()

    print("Adding loads...")
    builder.add_loads()

    print("Adding capacitors...")
    builder.add_capacitors()

    print("\nConstruction complete!")
    print()


def example_3_system_analysis():
    """Example 3: System analysis using utilities"""
    print("Example 3: System Analysis")
    print("-" * 60)

    # Calculate total load
    total_kw, total_kvar, total_kva = calculate_total_load()
    print(f"Total Load: {total_kw:.1f} kW + j{total_kvar:.1f} kVAr = {total_kva:.1f} kVA")

    # Phase balance
    print("\nPhase Balance:")
    phase_loads = calculate_load_balance()
    for phase, (kw, kvar) in phase_loads.items():
        print(f"  Phase {phase}: {kw:.1f} kW, {kvar:.1f} kVAr")

    # Network connectivity
    print("\nNode Connectivity:")
    connectivity = get_node_connectivity()
    for node, neighbors in sorted(connectivity.items()):
        if neighbors:
            print(f"  {node}: {', '.join(neighbors)}")

    # Path finding
    print("\nPath from 650 to 611:")
    path = find_path("650", "611")
    print(f"  {' -> '.join(path)}")

    print()


def example_4_configuration_access():
    """Example 4: Accessing configuration data"""
    print("Example 4: Configuration Data Access")
    print("-" * 60)

    # List all nodes
    print("Nodes:")
    print(f"  {', '.join(config.NODES)}")

    # Show line configurations
    print("\nLine Configurations:")
    for line_config in config.LINE_CONFIGS:
        line_type = "Underground" if line_config.is_underground else "Overhead"
        print(f"  Config {line_config.config_id}: {line_type}, "
              f"Phasing: {line_config.phasing}")

    # Show loads
    print("\nSpot Loads:")
    for load in config.SPOT_LOADS:
        total_kw = load.ph1_kw + load.ph2_kw + load.ph3_kw
        print(f"  Node {load.node}: {total_kw:.0f} kW ({load.load_model})")

    # Show capacitors
    print("\nCapacitor Banks:")
    for cap in config.CAPACITOR_BANKS:
        total_kvar = cap.ph_a_kvar + cap.ph_b_kvar + cap.ph_c_kvar
        print(f"  Node {cap.node}: {total_kvar:.0f} kVAr")

    print()


def example_5_network_export():
    """Example 5: Export network graph"""
    print("Example 5: Network Graph Export")
    print("-" * 60)

    dot_graph = export_network_graph()

    output_file = Path(__file__).parent / "ieee_13_network.dot"
    with open(output_file, "w") as f:
        f.write(dot_graph)

    print(f"Network graph exported to: {output_file}")
    print("\nTo visualize, run:")
    print(f"  dot -Tpng {output_file} -o ieee_13_network.png")
    print(f"  # or")
    print(f"  dot -Tsvg {output_file} -o ieee_13_network.svg")
    print()


def example_6_custom_summary():
    """Example 6: Custom system summary"""
    print("Example 6: Custom Summary")
    print("-" * 60)

    builder = IEEE13BusBuilder()
    print(builder.get_summary())


def main():
    """Run all examples"""
    print("=" * 70)
    print("IEEE 13 NODE TEST FEEDER - EXAMPLES")
    print("=" * 70)
    print()

    # Run examples
    example_1_basic_build()
    example_2_step_by_step()
    example_3_system_analysis()
    example_4_configuration_access()
    example_5_network_export()
    example_6_custom_summary()

    # Print full system report
    print("\n" + "=" * 70)
    print("COMPLETE SYSTEM REPORT")
    print("=" * 70)
    print_system_report()


if __name__ == "__main__":
    main()
