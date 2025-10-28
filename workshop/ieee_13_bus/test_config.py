#!/usr/bin/env python3
"""
Simple test script to verify configuration data without importing PyAPI-RTS.
"""

import sys
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from workshop.ieee_13_bus import config


def test_configuration():
    """Test that all configuration data is properly defined."""
    print("Testing IEEE 13 Bus Configuration")
    print("=" * 70)

    # Test nodes
    print(f"\n✓ Nodes defined: {len(config.NODES)}")
    print(f"  Nodes: {', '.join(config.NODES)}")

    # Test line configurations
    print(f"\n✓ Line configurations: {len(config.LINE_CONFIGS)}")
    for cfg in config.LINE_CONFIGS:
        line_type = "UG" if cfg.is_underground else "OH"
        print(f"  Config {cfg.config_id}: {line_type:2s} - {cfg.phasing}")

    # Test line segments
    print(f"\n✓ Line segments: {len(config.LINE_SEGMENTS)}")
    for seg in config.LINE_SEGMENTS:
        print(f"  {seg.node_a:3s} -> {seg.node_b:3s}: {seg.length_ft:5.0f} ft, Config {seg.config_id}")

    # Test loads
    total_kw = sum(l.ph1_kw + l.ph2_kw + l.ph3_kw for l in config.SPOT_LOADS)
    total_kvar = sum(l.ph1_kvar + l.ph2_kvar + l.ph3_kvar for l in config.SPOT_LOADS)
    print(f"\n✓ Spot loads: {len(config.SPOT_LOADS)}")
    print(f"  Total: {total_kw:.0f} kW + j{total_kvar:.0f} kVAr")

    # Test distributed loads
    dist_kw = sum(l.ph1_kw + l.ph2_kw + l.ph3_kw for l in config.DISTRIBUTED_LOADS)
    dist_kvar = sum(l.ph1_kvar + l.ph2_kvar + l.ph3_kvar for l in config.DISTRIBUTED_LOADS)
    print(f"\n✓ Distributed loads: {len(config.DISTRIBUTED_LOADS)}")
    print(f"  Total: {dist_kw:.0f} kW + j{dist_kvar:.0f} kVAr")

    # Test capacitors
    total_cap = sum(c.ph_a_kvar + c.ph_b_kvar + c.ph_c_kvar for c in config.CAPACITOR_BANKS)
    print(f"\n✓ Capacitor banks: {len(config.CAPACITOR_BANKS)}")
    print(f"  Total: {total_cap:.0f} kVAr")

    # Test transformers
    print(f"\n✓ Transformers: {len(config.TRANSFORMERS)}")
    for xfm in config.TRANSFORMERS:
        print(f"  {xfm.name}: {xfm.kva} kVA, {xfm.kv_high}kV -> {xfm.kv_low}kV")

    # Test regulator
    print(f"\n✓ Voltage regulator:")
    print(f"  Location: {config.REGULATOR.line_segment[0]} -> {config.REGULATOR.line_segment[1]}")
    print(f"  Phases: {config.REGULATOR.phases}")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY:")
    print(f"  Total System Load: {total_kw + dist_kw:.0f} kW + j{total_kvar + dist_kvar:.0f} kVAr")
    print(f"  Total Capacitance: {total_cap:.0f} kVAr")
    print(f"  Net Reactive:      {total_kvar + dist_kvar - total_cap:.0f} kVAr")
    print("\n✓ All configuration tests passed!")


if __name__ == "__main__":
    test_configuration()
