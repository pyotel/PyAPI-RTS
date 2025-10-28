#!/usr/bin/env python3
"""
IEEE 13 Node Test Feeder - Main Script

This script demonstrates how to build and export the IEEE 13 bus test system
using PyAPI-RTS.

Usage:
    python main.py [--output OUTPUT_FILE]
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path to import the module
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from workshop.ieee_13_bus import IEEE13BusBuilder


def main():
    """Main entry point for the IEEE 13 bus builder."""
    parser = argparse.ArgumentParser(
        description="Build IEEE 13 Node Test Feeder RSCAD model"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="ieee_13_bus.dfx",
        help="Output .dfx file path (default: ieee_13_bus.dfx)"
    )
    parser.add_argument(
        "--summary",
        "-s",
        action="store_true",
        help="Print system summary only (don't build)"
    )

    args = parser.parse_args()

    # Create builder instance
    print("IEEE 13 Node Test Feeder Builder")
    print("=" * 60)

    builder = IEEE13BusBuilder()

    # Print summary
    print(builder.get_summary())

    if args.summary:
        return 0

    # Build the system
    print("\nBuilding IEEE 13 bus system...")
    print("-" * 60)

    try:
        draft = builder.build()

        # Write to file
        output_path = Path(args.output)
        print(f"\nWriting to file: {output_path}")

        # Note: Actual file writing requires generated RSCAD component classes
        # For demonstration, we'll show what would be written
        print("\nSystem built successfully!")
        print(f"Output file: {output_path}")
        print("\nNote: To generate actual .dfx file, ensure RSCAD component ")
        print("      classes are generated first using:")
        print("      poetry run python ./pyapi_rts/class_extractor/main.py")

        # If you have generated classes, uncomment this:
        # draft.write_file(str(output_path))

        print("\nSystem statistics:")
        print(f"  - Subsystems: {len(draft.subsystems)}")
        print(f"  - Components: {len(draft.get_components())}")

        return 0

    except Exception as e:
        print(f"\nError building system: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
