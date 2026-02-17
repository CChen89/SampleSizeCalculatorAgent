#!/usr/bin/env python3
"""
Quick Sample Size Calculator - One-liner usage
For rapid calculations with minimal setup
"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from SampleSizeMultiAgent import MultiAgentSampleSizeCalculator, SampleSizeParameters


async def quick_calculation(arms, effect_sizes, power=0.8, alpha=0.05, dropout=0.2):
    """
    Quick sample size calculation with minimal parameters

    Args:
        arms: List of arm names, e.g., ["Placebo", "Treatment"]
        effect_sizes: List of effect sizes vs placebo, e.g., [-0.4]
        power: Required power (default 0.8)
        alpha: Significance level (default 0.05)
        dropout: Expected dropout rate (default 0.2)
    """

    calculator = MultiAgentSampleSizeCalculator()

    # Auto-generate parameters
    n_comparisons = len(arms) - 1  # Exclude placebo
    params = SampleSizeParameters(
        power=power,
        alpha=alpha,
        drop_rate=dropout,
        arm_names=arms,
        allocation_ratio=":".join(["1"] * len(arms)),
        es_primary=effect_sizes,
        es_secondary=None,
        n_min=30,
        n_max=200,
        n_step=5,
        correlation_matrix=[1.0] * (len(effect_sizes) ** 2),  # Identity-ish
        transition_matrix=[0.0] * (len(effect_sizes) ** 2),
        initial_weights=[1.0 / len(effect_sizes)] * len(effect_sizes),
        success_criteria=[{"Crit": "DisjunctivePower", "Parameters": None}],
        n_simulations=1000,  # Faster for quick calc
        seed=123,
    )

    # Run calculation
    state = {
        "parameters": params,
        "validation_result": {"valid": True},
        "calculation_result": None,
        "errors": [],
    }

    state = await calculator.calculation_agent(state)

    if state.get("calculation_result"):
        result = state["calculation_result"].get("result", {})
        n = result.get("recommended_sample_size_per_arm", "Unknown")
        total = int(n) * len(arms) if isinstance(n, (int, float)) else "Unknown"

        print(f"🎯 Quick Result:")
        print(f"   Arms: {', '.join(arms)}")
        print(f"   Effect sizes: {effect_sizes}")
        print(
            f"   Power: {power * 100}%, Alpha: {alpha * 100}%, Dropout: {dropout * 100}%"
        )
        print(f"   📊 Sample size: {n} per arm")
        print(f"   📊 Total enrollment: {total} subjects")
        return n
    else:
        print("❌ Calculation failed")
        return None


# Pre-defined quick calculations
async def quick_two_arm(effect_size=-0.4, power=0.8):
    """Two-arm superiority trial"""
    return await quick_calculation(
        arms=["Placebo", "Treatment"], effect_sizes=[effect_size], power=power
    )


async def quick_three_arm(low_effect=-0.3, high_effect=-0.4, power=0.8):
    """Three-arm dose-response trial"""
    return await quick_calculation(
        arms=["Placebo", "Low Dose", "High Dose"],
        effect_sizes=[low_effect, high_effect],
        power=power,
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        calc_type = sys.argv[1].lower()

        if calc_type == "two-arm":
            effect = float(sys.argv[2]) if len(sys.argv) > 2 else -0.4
            power = float(sys.argv[3]) if len(sys.argv) > 3 else 0.8
            asyncio.run(quick_two_arm(effect, power))

        elif calc_type == "three-arm":
            low = float(sys.argv[2]) if len(sys.argv) > 2 else -0.3
            high = float(sys.argv[3]) if len(sys.argv) > 3 else -0.4
            power = float(sys.argv[4]) if len(sys.argv) > 4 else 0.8
            asyncio.run(quick_three_arm(low, high, power))

        else:
            print(
                "Usage: python quick_calculator.py [two-arm|three-arm] [effect_size] [power]"
            )
    else:
        print("🚀 Quick Sample Size Calculator")
        print("Usage examples:")
        print("  python quick_calculator.py two-arm -0.4 0.8")
        print("  python quick_calculator.py three-arm -0.3 -0.4 0.85")
        print()
        print("Running default two-arm example...")
        asyncio.run(quick_two_arm())
