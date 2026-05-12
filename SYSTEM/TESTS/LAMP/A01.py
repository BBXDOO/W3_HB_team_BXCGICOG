# ============================================================
# A02.py
# Adaptive Semantic Luminance
# ============================================================

"""
Adaptive Semantic Luminance
ระบบการเรืองแสงเชิงบริบทสำหรับอักขระในสภาพแสงต่ำ

Research Category:
    - Perceptual Rendering
    - Typography Engineering
    - Human Visual Perception
    - Accessibility Computing

Objective:
    Improve information visibility in low-brightness environments
    without increasing global display luminance.

Author:
    W3_HB_team_BXCGICOG

Status:
    Research Draft / Experimental Framework
"""

# ============================================================
# IMPORT DOMAIN
# ============================================================

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


# ============================================================
# SEMANTIC PRIORITY MODEL
# ============================================================

class SemanticPriority(Enum):

    LOW         = 0.25
    MEDIUM      = 0.50
    HIGH        = 0.85
    CRITICAL    = 1.00


# ============================================================
# GLYPH CONFIGURATION
# ============================================================

@dataclass
class GlyphProfile:

    glyph_type: str

    edge_contrast: float

    luminance_gain: float

    semantic_weight: float

    glow_radius: float

    spectral_color: str


# ============================================================
# THAI TYPOGRAPHY MODEL
# ============================================================

THAI_GLYPH_SYSTEM = {

    "CONSONANT": GlyphProfile(
        glyph_type         = "Primary Character",
        edge_contrast      = 0.82,
        luminance_gain     = 0.74,
        semantic_weight    = 0.65,
        glow_radius        = 1.2,
        spectral_color     = "#7dd3fc"
    ),

    "VOWEL_TOP": GlyphProfile(
        glyph_type         = "Upper Vowel",
        edge_contrast      = 0.91,
        luminance_gain     = 0.88,
        semantic_weight    = 0.72,
        glow_radius        = 1.5,
        spectral_color     = "#5ffff2"
    ),

    "TONE_MARK": GlyphProfile(
        glyph_type         = "Tone Layer",
        edge_contrast      = 0.96,
        luminance_gain     = 0.94,
        semantic_weight    = 0.93,
        glow_radius        = 1.8,
        spectral_color     = "#c792ea"
    )
}


# ============================================================
# PERCEPTUAL VISIBILITY MODEL
# ============================================================

class VisibilityModel:

    """
    Vp = (Ce * Lg * Sw) - Vn

    Where:
        Vp = Perceived Visibility
        Ce = Edge Contrast
        Lg = Glyph Luminance
        Sw = Semantic Weight
        Vn = Visual Noise
    """

    @staticmethod
    def calculate_visibility(
        edge_contrast: float,
        luminance_gain: float,
        semantic_weight: float,
        visual_noise: float
    ) -> float:

        visibility = (
            edge_contrast
            * luminance_gain
            * semantic_weight
        ) - visual_noise

        return round(visibility, 4)


# ============================================================
# SEMANTIC LUMINANCE ENGINE
# ============================================================

class AdaptiveSemanticLuminanceEngine:

    """
    Core Rendering Principle:

        Allocate luminance
        to semantic importance
        instead of global brightness.
    """

    BACKGROUND_BRIGHTNESS = 0.18

    VISUAL_NOISE          = 0.11

    def __init__(self):

        self.render_pipeline = [
            "BackgroundAttenuation",
            "GlyphExtraction",
            "EdgeIllumination",
            "SemanticWeighting",
            "AdaptivePerception"
        ]

    def render_glyph(
        self,
        glyph_name: str
    ) -> Dict:

        glyph = THAI_GLYPH_SYSTEM[glyph_name]

        visibility_score = (
            VisibilityModel.calculate_visibility(
                edge_contrast   = glyph.edge_contrast,
                luminance_gain  = glyph.luminance_gain,
                semantic_weight = glyph.semantic_weight,
                visual_noise    = self.VISUAL_NOISE
            )
        )

        return {

            "glyph_type":
                glyph.glyph_type,

            "spectral_color":
                glyph.spectral_color,

            "glow_radius":
                glyph.glow_radius,

            "visibility_score":
                visibility_score
        }


# ============================================================
# EXPERIMENTAL DESIGN
# ============================================================

class ExperimentalProtocol:

    """
    Research Objective:
        Evaluate perceptual readability
        under low-brightness conditions.
    """

    TEST_ENVIRONMENT = {

        "display_brightness" : "< 20%",
        "ambient_light"      : "dark_room",
        "display_types"      : [
            "OLED",
            "IPS",
            "Mobile"
        ],

        "font_size"          : "constant",
        "viewing_distance"   : "controlled"
    }

    TEST_GROUPS = {

        "A":
            "Standard Typography",

        "B":
            "Static Glow Typography",

        "C":
            "Adaptive Semantic Luminance"
    }

    METRICS = [

        "reading_speed",
        "recognition_accuracy",
        "response_latency",
        "fixation_duration",
        "eye_fatigue_score"
    ]


# ============================================================
# ACCESSIBILITY APPLICATIONS
# ============================================================

ACCESSIBILITY_TARGETS = [

    "Low Vision Users",

    "Dark Environment Reading",

    "Long Duration Coding Sessions",

    "Dense Information Interface",

    "Cognitive Load Reduction"
]


# ============================================================
# RESEARCH CONTRIBUTION
# ============================================================

RESEARCH_CONTRIBUTION = {

    "domain_shift":
        (
            "Display-Centric Rendering "
            "-> "
            "Perception-Centric Rendering"
        ),

    "core_contribution":
        [
            "Semantic Luminance Allocation",
            "Localized Glyph Illumination",
            "Adaptive Typography Rendering",
            "Perceptual Visibility Optimization"
        ]
}


# ============================================================
# INITIALIZATION
# ============================================================

if __name__ == "__main__":

    engine = AdaptiveSemanticLuminanceEngine()

    tone_mark = engine.render_glyph("TONE_MARK")

    print("\n")
    print("================================================")
    print(" Adaptive Semantic Luminance Engine")
    print("================================================")
    print("\n")

    for key, value in tone_mark.items():

        print(f"{key:<20}: {value}")

    print("\n")
    print("Rendering Pipeline:")
    print("-------------------")

    for stage in engine.render_pipeline:

        print(f"  -> {stage}")

    print("\n")
    print("Research Status:")
    print("-------------------")
    print("Experimental Rendering Framework")
    print("\n")
