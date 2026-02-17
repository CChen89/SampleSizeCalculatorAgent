#!/usr/bin/env python3
"""
Your Personal Sample Size Calculator
Easy-to-use script for clinical trial sample size calculation
"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from SampleSizeMultiAgent import MultiAgentSampleSizeCalculator, SampleSizeParameters


async def calculate_sample_size():
    """
    Main function to calculate sample size for your clinical trials
    Modify the parameters below for your specific trial design
    """

    print("🧮 Clinical Trial Sample Size Calculator")
    print("=" * 60)

    # Initialize the calculator
    calculator = MultiAgentSampleSizeCalculator()

    # =================================================================
    # CUSTOMIZE THESE PARAMETERS FOR YOUR TRIAL
    # =================================================================

    # Trial Design Parameters
    trial_params = SampleSizeParameters(
        # Basic Statistical Parameters
        power=0.8,  # Required power (80%)
        alpha=0.05,  # Significance level (5%)
        drop_rate=0.2,  # Expected dropout rate (20%)
        # Trial Arms
        arm_names=["Placebo", "ABBV932L", "ABBV932H"],  # Your arm names
        allocation_ratio="1:1:1",  # Equal allocation
        # Effect Sizes (vs placebo)
        es_primary=[-0.33, -0.33],  # Primary endpoint effect sizes
        es_secondary=[-0.33, -0.33, -0.28, -0.28],  # Secondary endpoint effect sizes
        # Sample Size Search Parameters
        n_min=50,  # Minimum sample size per arm
        n_max=300,  # Maximum sample size per arm
        n_step=10,  # Sample size increment
        # Multiplicity Control (Graphical Procedure)
        correlation_matrix=[1, 0.6, 0.6, 0.6, 1, 0.6, 0.6, 0.6, 1],  # 3x3 correlation
        transition_matrix=[0, 1, 1, 0],  # 2x2 transition matrix
        initial_weights=[0.5, 0.5],  # Initial hypothesis weights
        success_criteria=[{"Crit": "DisjunctivePower", "Parameters": None}],
        # Simulation Parameters
        n_simulations=10000,  # Number of simulations
        seed=12345,  # Random seed for reproducibility
    )

    # =================================================================
    # RUN THE CALCULATION
    # =================================================================

    print(f"📊 Trial Design:")
    print(f"   Arms: {', '.join(trial_params.arm_names)}")
    print(f"   Power: {trial_params.power * 100}%, Alpha: {trial_params.alpha * 100}%")
    print(f"   Dropout: {trial_params.drop_rate * 100}%")
    print(f"   Effect sizes: {trial_params.es_primary}")
    print(f"   Search range: {trial_params.n_min}-{trial_params.n_max} per arm")
    print()

    # Create the analysis state
    state = {
        "messages": [],
        "parameters": trial_params,
        "validation_result": {"valid": True},
        "calculation_result": None,
        "visualization_result": None,
        "mcp_tools": None,
        "current_step": "user_calculation",
        "errors": [],
        "intermediate_results": {},
    }

    print("🔄 Running statistical analysis...")

    # Run the multi-agent calculation
    state = await calculator.calculation_agent(state)
    state = await calculator.visualization_agent(state)

    # Get the final results
    final_report = calculator.compile_final_response(state)

    print("\n" + "=" * 80)
    print("📋 CLINICAL TRIAL SAMPLE SIZE ANALYSIS RESULTS")
    print("=" * 80)
    print(final_report)

    # Extract key recommendations
    if state.get("calculation_result"):
        result = state["calculation_result"].get("result", {})
        if "recommended_sample_size_per_arm" in result:
            n = result["recommended_sample_size_per_arm"]
            print(f"\n🎯 KEY RESULT: {n} subjects per arm recommended")
            print(f"   Total study size: {n * len(trial_params.arm_names)} subjects")
            print(f"   Accounting for {trial_params.drop_rate * 100}% dropout")


# =================================================================
# EASY MODIFICATION TEMPLATES
# =================================================================


async def two_arm_trial_example():
    """Template for two-arm superiority trial"""
    calculator = MultiAgentSampleSizeCalculator()

    params = SampleSizeParameters(
        power=0.9,  # 90% power
        alpha=0.05,  # 5% alpha
        drop_rate=0.15,  # 15% dropout
        arm_names=["Placebo", "Treatment"],
        allocation_ratio="1:1",
        es_primary=[-0.4],  # Single comparison
        es_secondary=None,  # No secondary endpoints
        n_min=30,
        n_max=150,
        n_step=5,
        correlation_matrix=[1.0],  # Single endpoint
        transition_matrix=[0.0],  # Single hypothesis
        initial_weights=[1.0],
        success_criteria=[{"Crit": "DisjunctivePower", "Parameters": None}],
        n_simulations=5000,
        seed=123,
    )

    # Run calculation (same as above)
    state = {
        "messages": [],
        "parameters": params,
        "validation_result": {"valid": True},
        "calculation_result": None,
        "visualization_result": None,
        "mcp_tools": None,
        "current_step": "two_arm",
        "errors": [],
        "intermediate_results": {},
    }

    state = await calculator.calculation_agent(state)
    result = state.get("calculation_result", {}).get("result", {})
    n = result.get("recommended_sample_size_per_arm", "Unknown")

    print(f"🎯 Two-arm trial result: {n} subjects per arm")
    return n


async def dose_response_trial_example():
    """Template for four-arm dose-response trial"""
    calculator = MultiAgentSampleSizeCalculator()

    params = SampleSizeParameters(
        power=0.85,
        alpha=0.025,  # More stringent alpha
        drop_rate=0.25,  # Higher dropout expected
        arm_names=["Placebo", "Low", "Medium", "High"],
        allocation_ratio="1:1:1:1",
        es_primary=[-0.2, -0.35, -0.5],  # Dose-response pattern
        es_secondary=[-0.15, -0.25, -0.35],
        n_min=40,
        n_max=200,
        n_step=10,
        correlation_matrix=[1, 0.4, 0.4, 1],  # 2 endpoints
        transition_matrix=[
            0,
            0.33,
            0.33,
            0.33,
            0.33,
            0,
            0.33,
            0.33,
            0.33,
        ],  # 3x3 for 3 comparisons
        initial_weights=[0.4, 0.4, 0.2],
        success_criteria=[{"Crit": "WeightedPower", "Parameters": [0.6, 0.4]}],
        n_simulations=5000,
        seed=456,
    )

    # Run calculation
    state = {
        "messages": [],
        "parameters": params,
        "validation_result": {"valid": True},
        "calculation_result": None,
        "visualization_result": None,
        "mcp_tools": None,
        "current_step": "dose_response",
        "errors": [],
        "intermediate_results": {},
    }

    state = await calculator.calculation_agent(state)
    result = state.get("calculation_result", {}).get("result", {})
    n = result.get("recommended_sample_size_per_arm", "Unknown")

    print(f"🎯 Four-arm dose-response result: {n} subjects per arm")
    return n


# =================================================================
# MAIN EXECUTION
# =================================================================

if __name__ == "__main__":
    print("Choose your calculation:")
    print("1. Custom three-arm trial (main example)")
    print("2. Two-arm superiority trial")
    print("3. Four-arm dose-response trial")

    choice = input("Enter choice (1-3) or press Enter for main example: ").strip()

    if choice == "2":
        asyncio.run(two_arm_trial_example())
    elif choice == "3":
        asyncio.run(dose_response_trial_example())
    else:
        asyncio.run(calculate_sample_size())
