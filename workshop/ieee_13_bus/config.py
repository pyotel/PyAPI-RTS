"""
IEEE 13 Node Test Feeder Configuration Data

This module contains all configuration data for the IEEE 13 bus test system
based on the IEEE Distribution System Analysis Subcommittee Report.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple


# System base values
NOMINAL_VOLTAGE_KV = 4.16
BASE_VOLTAGE_KV_LL = 4.16  # Line-to-line
BASE_VOLTAGE_KV_LN = 4.16 / (3 ** 0.5)  # Line-to-neutral
SUBSTATION_VOLTAGE_KV = 115.0


@dataclass
class ConductorData:
    """Conductor characteristics"""
    size: str
    type: str  # AA, ACSR, CU
    resistance_ohm_per_mile: float
    diameter_inch: float
    gmr_ft: float
    ampacity: int


@dataclass
class LineConfiguration:
    """Line configuration data"""
    config_id: int
    phasing: str
    phase_conductor: str
    neutral_conductor: str
    spacing_id: int
    is_underground: bool = False


@dataclass
class LineSegment:
    """Line segment between two nodes"""
    node_a: str
    node_b: str
    length_ft: float
    config_id: int


@dataclass
class SpotLoad:
    """Spot load at a node"""
    node: str
    load_model: str  # Y-PQ, Y-I, Y-Z, D-PQ, D-I, D-Z
    ph1_kw: float
    ph1_kvar: float
    ph2_kw: float
    ph2_kvar: float
    ph3_kw: float
    ph3_kvar: float


@dataclass
class DistributedLoad:
    """Distributed load along a line segment"""
    node_a: str
    node_b: str
    load_model: str
    ph1_kw: float
    ph1_kvar: float
    ph2_kw: float
    ph2_kvar: float
    ph3_kw: float
    ph3_kvar: float


@dataclass
class CapacitorBank:
    """Shunt capacitor bank"""
    node: str
    ph_a_kvar: float
    ph_b_kvar: float
    ph_c_kvar: float


@dataclass
class TransformerData:
    """Transformer specification"""
    name: str
    kva: int
    kv_high: float
    kv_low: float
    connection_high: str  # D, Gr.Y, Gr.W
    connection_low: str
    r_percent: float
    x_percent: float


@dataclass
class RegulatorData:
    """Voltage regulator specification"""
    regulator_id: int
    line_segment: Tuple[str, str]
    location: str
    phases: str
    connection: str
    bandwidth_volts: float
    pt_ratio: int
    ct_rating: int
    r_setting: Dict[str, float]
    x_setting: Dict[str, float]
    voltage_level: Dict[str, float]


# Overhead conductor data (from Table 3)
CONDUCTORS = {
    "556500_ACSR": ConductorData("556.5 kcmil", "ACSR", 0.1859, 0.927, 0.0313, 730),
    "4/0_ACSR": ConductorData("4/0", "ACSR", 0.592, 0.563, 0.00814, 340),
    "1/0_ACSR": ConductorData("1/0", "ACSR", 1.12, 0.398, 0.00446, 230),
    "1/0_AA": ConductorData("1/0", "AA", 0.970, 0.368, 0.0111, 310),
    "250_AA": ConductorData("250 kcmil", "AA", 0.410, 0.567, 0.0171, 329),
}

# Underground cable data (from Tables 5 and 6)
CABLES = {
    "250_AA_CN": {
        "type": "Concentric Neutral",
        "size": "250 kcmil",
        "dia_insulation": 1.06,
        "dia_screen": 1.16,
        "dia_outside": 1.29,
        "neutral": "13 x 14 AWG",
        "ampacity": 260
    },
    "1/0_AA_TS": {
        "type": "Tape Shielded",
        "size": "1/0",
        "dia_insulation": 0.82,
        "dia_shield": 0.88,
        "jacket_mil": 80,
        "dia_outside": 1.06,
        "ampacity": 165
    }
}

# Overhead line configurations (from Overhead Line Configuration Data)
OVERHEAD_CONFIGS = [
    LineConfiguration(601, "B A C N", "556500_ACSR", "4/0_ACSR", 500, False),
    LineConfiguration(602, "C A B N", "4/0_ACSR", "4/0_ACSR", 500, False),
    LineConfiguration(603, "C B N", "1/0_ACSR", "1/0_ACSR", 505, False),
    LineConfiguration(604, "A C N", "1/0_ACSR", "1/0_ACSR", 505, False),
    LineConfiguration(605, "C N", "1/0_ACSR", "1/0_ACSR", 510, False),
]

# Underground line configurations (from Underground Line Configuration Data)
UNDERGROUND_CONFIGS = [
    LineConfiguration(606, "A B C N", "250_AA_CN", "None", 515, True),
    LineConfiguration(607, "A N", "1/0_AA_TS", "1/0_Cu", 520, True),
]

# All line configurations
LINE_CONFIGS = OVERHEAD_CONFIGS + UNDERGROUND_CONFIGS

# Line segments (from Line Segment Data)
LINE_SEGMENTS = [
    LineSegment("632", "645", 500, 603),
    LineSegment("632", "633", 500, 602),
    LineSegment("633", "634", 0, 0),  # XFM-1 location
    LineSegment("645", "646", 300, 603),
    LineSegment("650", "632", 2000, 601),
    LineSegment("684", "652", 800, 607),
    LineSegment("632", "671", 2000, 601),
    LineSegment("671", "684", 300, 604),
    LineSegment("671", "680", 1000, 601),
    LineSegment("671", "692", 0, 0),  # Switch location
    LineSegment("684", "611", 300, 605),
    LineSegment("692", "675", 500, 606),
]

# Spot loads (from Spot Load Data)
SPOT_LOADS = [
    SpotLoad("634", "Y-PQ", 160, 110, 120, 90, 120, 90),
    SpotLoad("645", "Y-PQ", 0, 0, 170, 125, 0, 0),
    SpotLoad("646", "D-Z", 0, 0, 230, 132, 0, 0),
    SpotLoad("652", "Y-Z", 128, 86, 0, 0, 0, 0),
    SpotLoad("671", "D-PQ", 385, 220, 385, 220, 385, 220),
    SpotLoad("675", "Y-PQ", 485, 190, 68, 60, 290, 212),
    SpotLoad("692", "D-I", 0, 0, 0, 0, 170, 151),
    SpotLoad("611", "Y-I", 0, 0, 0, 0, 170, 80),
]

# Distributed loads (from Distributed Load Data)
DISTRIBUTED_LOADS = [
    DistributedLoad("632", "671", "Y-PQ", 17, 10, 66, 38, 117, 68),
]

# Capacitor banks (from Capacitor Data)
CAPACITOR_BANKS = [
    CapacitorBank("675", 200, 200, 200),
    CapacitorBank("611", 0, 0, 100),
]

# Transformer data
TRANSFORMERS = [
    TransformerData(
        name="Substation",
        kva=5000,
        kv_high=115.0,
        kv_low=4.16,
        connection_high="D",
        connection_low="Gr.Y",
        r_percent=1.0,
        x_percent=8.0
    ),
    TransformerData(
        name="XFM-1",
        kva=500,
        kv_high=4.16,
        kv_low=0.48,
        connection_high="Gr.W",
        connection_low="Gr.W",
        r_percent=1.1,
        x_percent=2.0
    ),
]

# Voltage regulator data
REGULATOR = RegulatorData(
    regulator_id=1,
    line_segment=("650", "632"),
    location="650",
    phases="A-B-C",
    connection="3-Ph,LG",
    bandwidth_volts=2.0,
    pt_ratio=20,
    ct_rating=700,
    r_setting={"A": 3, "B": 3, "C": 3},
    x_setting={"A": 9, "B": 9, "C": 9},
    voltage_level={"A": 122, "B": 122, "C": 122}
)

# All nodes in the system
NODES = [
    "650",  # Source/Regulator
    "632",  # Main bus
    "633", "634",  # Transformer branch
    "645", "646",  # Branch 1
    "671", "680", "684", "692", "675",  # Main feeder
    "652",  # Underground lateral
    "611",  # Single phase lateral
]

# Node coordinates for visualization (approximate, for layout purposes)
NODE_COORDS = {
    "650": (0, 0),
    "632": (200, 0),
    "633": (300, 50),
    "634": (350, 50),
    "645": (200, -100),
    "646": (200, -150),
    "671": (400, 0),
    "680": (400, -100),
    "684": (500, 0),
    "692": (600, 0),
    "675": (700, 0),
    "652": (550, 50),
    "611": (550, -50),
}
