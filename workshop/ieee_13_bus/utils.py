"""
Utility functions for the IEEE 13 bus test feeder.

This module provides helper functions for validation, analysis, and visualization.
"""

from typing import Dict, List, Tuple
import math
from . import config


def calculate_total_load() -> Tuple[float, float, float]:
    """
    Calculate total system load.

    Returns:
        Tuple of (total_kw, total_kvar, total_kva)
    """
    total_kw = 0.0
    total_kvar = 0.0

    # Sum spot loads
    for load in config.SPOT_LOADS:
        total_kw += load.ph1_kw + load.ph2_kw + load.ph3_kw
        total_kvar += load.ph1_kvar + load.ph2_kvar + load.ph3_kvar

    # Sum distributed loads
    for load in config.DISTRIBUTED_LOADS:
        total_kw += load.ph1_kw + load.ph2_kw + load.ph3_kw
        total_kvar += load.ph1_kvar + load.ph2_kvar + load.ph3_kvar

    # Calculate apparent power
    total_kva = math.sqrt(total_kw**2 + total_kvar**2)

    return total_kw, total_kvar, total_kva


def calculate_load_balance() -> Dict[str, Tuple[float, float]]:
    """
    Calculate load per phase.

    Returns:
        Dictionary with phase names (A, B, C) and (kW, kVAr) tuples
    """
    phase_loads = {"A": [0.0, 0.0], "B": [0.0, 0.0], "C": [0.0, 0.0]}

    # Process spot loads
    for load in config.SPOT_LOADS:
        # Note: Phase mapping depends on load connection (Y or D)
        # For simplicity, we use phase 1->A, 2->B, 3->C
        phase_loads["A"][0] += load.ph1_kw
        phase_loads["A"][1] += load.ph1_kvar
        phase_loads["B"][0] += load.ph2_kw
        phase_loads["B"][1] += load.ph2_kvar
        phase_loads["C"][0] += load.ph3_kw
        phase_loads["C"][1] += load.ph3_kvar

    # Process distributed loads
    for load in config.DISTRIBUTED_LOADS:
        phase_loads["A"][0] += load.ph1_kw
        phase_loads["A"][1] += load.ph1_kvar
        phase_loads["B"][0] += load.ph2_kw
        phase_loads["B"][1] += load.ph2_kvar
        phase_loads["C"][0] += load.ph3_kw
        phase_loads["C"][1] += load.ph3_kvar

    return {
        phase: (kw, kvar)
        for phase, (kw, kvar) in phase_loads.items()
    }


def calculate_load_imbalance() -> float:
    """
    Calculate percentage load imbalance between phases.

    Returns:
        Maximum percentage deviation from average load
    """
    phase_loads = calculate_load_balance()

    # Calculate total load per phase
    phase_totals = {
        phase: math.sqrt(kw**2 + kvar**2)
        for phase, (kw, kvar) in phase_loads.items()
    }

    avg_load = sum(phase_totals.values()) / 3
    if avg_load == 0:
        return 0.0

    max_deviation = max(abs(load - avg_load) for load in phase_totals.values())
    return (max_deviation / avg_load) * 100


def calculate_total_line_length() -> Dict[str, float]:
    """
    Calculate total line length by type.

    Returns:
        Dictionary with 'overhead', 'underground', and 'total' lengths in feet
    """
    overhead_length = 0.0
    underground_length = 0.0

    for segment in config.LINE_SEGMENTS:
        # Skip transformers and switches
        if segment.config_id == 0:
            continue

        # Find configuration
        line_config = next(
            (cfg for cfg in config.LINE_CONFIGS if cfg.config_id == segment.config_id),
            None
        )

        if line_config:
            if line_config.is_underground:
                underground_length += segment.length_ft
            else:
                overhead_length += segment.length_ft

    return {
        "overhead": overhead_length,
        "underground": underground_length,
        "total": overhead_length + underground_length,
    }


def get_node_connectivity() -> Dict[str, List[str]]:
    """
    Build node adjacency list.

    Returns:
        Dictionary mapping each node to its connected neighbors
    """
    connectivity = {node: [] for node in config.NODES}

    for segment in config.LINE_SEGMENTS:
        if segment.node_a in connectivity:
            connectivity[segment.node_a].append(segment.node_b)
        if segment.node_b in connectivity:
            connectivity[segment.node_b].append(segment.node_a)

    return connectivity


def find_path(start: str, end: str) -> List[str]:
    """
    Find path between two nodes using BFS.

    Args:
        start: Starting node name
        end: Ending node name

    Returns:
        List of nodes forming the path, or empty list if no path exists
    """
    connectivity = get_node_connectivity()

    # BFS to find path
    queue = [(start, [start])]
    visited = {start}

    while queue:
        node, path = queue.pop(0)

        if node == end:
            return path

        for neighbor in connectivity.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return []


def validate_system() -> List[str]:
    """
    Validate system configuration for common issues.

    Returns:
        List of warning/error messages (empty if no issues)
    """
    issues = []

    # Check for isolated nodes
    connectivity = get_node_connectivity()
    for node in config.NODES:
        if node != "650" and not connectivity.get(node):
            issues.append(f"Warning: Node {node} appears to be isolated")

    # Check if all load nodes exist
    for load in config.SPOT_LOADS:
        if load.node not in config.NODES:
            issues.append(f"Error: Load node {load.node} not in node list")

    for load in config.DISTRIBUTED_LOADS:
        if load.node_a not in config.NODES:
            issues.append(f"Error: Distributed load node {load.node_a} not in node list")
        if load.node_b not in config.NODES:
            issues.append(f"Error: Distributed load node {load.node_b} not in node list")

    # Check if all capacitor nodes exist
    for cap in config.CAPACITOR_BANKS:
        if cap.node not in config.NODES:
            issues.append(f"Error: Capacitor node {cap.node} not in node list")

    # Check line segment nodes
    for segment in config.LINE_SEGMENTS:
        if segment.node_a not in config.NODES:
            issues.append(f"Error: Line segment node {segment.node_a} not in node list")
        if segment.node_b not in config.NODES:
            issues.append(f"Error: Line segment node {segment.node_b} not in node list")

    # Check for duplicate line segments
    segment_pairs = set()
    for segment in config.LINE_SEGMENTS:
        pair = tuple(sorted([segment.node_a, segment.node_b]))
        if pair in segment_pairs:
            issues.append(f"Warning: Duplicate line segment {segment.node_a}-{segment.node_b}")
        segment_pairs.add(pair)

    # Check for valid configuration IDs
    valid_config_ids = {cfg.config_id for cfg in config.LINE_CONFIGS} | {0}
    for segment in config.LINE_SEGMENTS:
        if segment.config_id not in valid_config_ids:
            issues.append(f"Error: Unknown config ID {segment.config_id} in segment "
                        f"{segment.node_a}-{segment.node_b}")

    return issues


def print_system_report() -> None:
    """Print a comprehensive system report."""
    print("=" * 70)
    print("IEEE 13 NODE TEST FEEDER - SYSTEM REPORT")
    print("=" * 70)

    # Basic info
    print("\n[SYSTEM CONFIGURATION]")
    print(f"Nominal Voltage: {config.NOMINAL_VOLTAGE_KV} kV")
    print(f"Number of Nodes: {len(config.NODES)}")
    print(f"Number of Line Segments: {len(config.LINE_SEGMENTS)}")

    # Load analysis
    total_kw, total_kvar, total_kva = calculate_total_load()
    print("\n[TOTAL LOADING]")
    print(f"Active Power (P):    {total_kw:8.2f} kW")
    print(f"Reactive Power (Q):  {total_kvar:8.2f} kVAr")
    print(f"Apparent Power (S):  {total_kva:8.2f} kVA")
    print(f"Power Factor:        {total_kw/total_kva:8.4f}")

    # Phase balance
    phase_loads = calculate_load_balance()
    imbalance = calculate_load_imbalance()
    print("\n[LOAD BALANCE BY PHASE]")
    for phase, (kw, kvar) in phase_loads.items():
        kva = math.sqrt(kw**2 + kvar**2)
        pf = kw / kva if kva > 0 else 0
        print(f"Phase {phase}: {kw:7.1f} kW + j{kvar:7.1f} kVAr = {kva:7.1f} kVA (PF={pf:.3f})")
    print(f"Load Imbalance:  {imbalance:.2f}%")

    # Line lengths
    line_lengths = calculate_total_line_length()
    print("\n[LINE LENGTHS]")
    print(f"Overhead:     {line_lengths['overhead']:8.0f} ft ({line_lengths['overhead']/5280:.3f} mi)")
    print(f"Underground:  {line_lengths['underground']:8.0f} ft ({line_lengths['underground']/5280:.3f} mi)")
    print(f"Total:        {line_lengths['total']:8.0f} ft ({line_lengths['total']/5280:.3f} mi)")

    # Components
    print("\n[COMPONENTS]")
    print(f"Voltage Regulators:  1")
    print(f"Transformers:        {len(config.TRANSFORMERS)}")
    print(f"Spot Loads:          {len(config.SPOT_LOADS)}")
    print(f"Distributed Loads:   {len(config.DISTRIBUTED_LOADS)}")
    print(f"Capacitor Banks:     {len(config.CAPACITOR_BANKS)}")

    # Capacitor total
    total_cap = sum(c.ph_a_kvar + c.ph_b_kvar + c.ph_c_kvar for c in config.CAPACITOR_BANKS)
    print(f"\nTotal Capacitance:   {total_cap:.0f} kVAr")

    # Validation
    issues = validate_system()
    print("\n[VALIDATION]")
    if issues:
        print(f"Found {len(issues)} issue(s):")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("System configuration validated successfully ✓")

    print("\n" + "=" * 70)


def export_network_graph() -> str:
    """
    Export network topology in DOT format for visualization.

    Returns:
        DOT format string suitable for Graphviz
    """
    dot = ["digraph IEEE13Bus {"]
    dot.append('  rankdir=LR;')
    dot.append('  node [shape=circle];')
    dot.append('')

    # Add nodes with labels
    for node in config.NODES:
        load = next((l for l in config.SPOT_LOADS if l.node == node), None)
        cap = next((c for c in config.CAPACITOR_BANKS if c.node == node), None)

        label = node
        if load:
            total_kw = load.ph1_kw + load.ph2_kw + load.ph3_kw
            label += f"\\n{total_kw:.0f}kW"
        if cap:
            total_kvar = cap.ph_a_kvar + cap.ph_b_kvar + cap.ph_c_kvar
            label += f"\\n{total_kvar:.0f}kVAr"

        color = "lightblue"
        if node == "650":
            color = "lightgreen"
        elif load:
            color = "lightyellow"

        dot.append(f'  {node} [label="{label}", style=filled, fillcolor={color}];')

    dot.append('')

    # Add edges
    for segment in config.LINE_SEGMENTS:
        length_mi = segment.length_ft / 5280
        if segment.config_id == 0:
            # Transformer or switch
            label = "XFM" if "633" in [segment.node_a, segment.node_b] else "SW"
            style = "dashed"
        else:
            line_config = next(
                (cfg for cfg in config.LINE_CONFIGS if cfg.config_id == segment.config_id),
                None
            )
            if line_config:
                line_type = "UG" if line_config.is_underground else "OH"
                label = f"{line_type}\\n{length_mi:.2f}mi"
                style = "dotted" if line_config.is_underground else "solid"
            else:
                label = f"{length_mi:.2f}mi"
                style = "solid"

        dot.append(f'  {segment.node_a} -> {segment.node_b} '
                  f'[label="{label}", style={style}, dir=none];')

    dot.append('}')
    return '\n'.join(dot)


if __name__ == "__main__":
    # Run system report when module is executed
    print_system_report()
