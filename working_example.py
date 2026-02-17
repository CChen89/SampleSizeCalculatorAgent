#!/usr/bin/env python3
"""
Working Example - Direct Parameter Usage
This bypasses the LLM parameter extraction and directly uses the working components.
"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from SampleSizeMultiAgent import MultiAgentSampleSizeCalculator, SampleSizeParameters


async def working_example():
    """Demonstrates the working core functionality"""
    print("🚀 WORKING EXAMPLE: Multi-Agent Sample Size Calculator")
    print("=" * 70)

    # Initialize calculator
    calculator = MultiAgentSampleSizeCalculator()

    # Example 1: Two-arm trial (WORKING)
    print("\n📊 Example 1: Two-Arm Superiority Trial")
    print("-" * 50)

    params_2arm = SampleSizeParameters(
        power=0.8,
        alpha=0.05,
        drop_rate=0.15,
        allocation_ratio="1:1",
        n_min=30,
        n_max=150,
        n_step=5,
        arm_names=["Placebo", "Treatment"],
        es_primary=[-0.4],  # Effect size vs placebo
        es_secondary=None,
        correlation_matrix=[1.0],  # Single endpoint
        transition_matrix=[0.0],  # Single hypothesis
        initial_weights=[1.0],
        success_criteria=[{"Crit": "DisjunctivePower", "Parameters": None}],
        n_simulations=5000,
        seed=12345,
    )

    result_2arm = await run_calculation(calculator, params_2arm, "Two-Arm Trial")
    print(f"✅ Result: {result_2arm}")

    # Example 2: Three-arm trial matching your R code (WORKING)
    print("\n📊 Example 2: Three-Arm Trial (R Example Format)")
    print("-" * 50)

    params_3arm = SampleSizeParameters(
        power=0.8,
        alpha=0.05,
        drop_rate=0.2,
        allocation_ratio="1:1:1",
        n_min=50,
        n_max=300,
        n_step=10,
        arm_names=["Placebo", "ABBV932L", "ABBV932H"],
        es_primary=[-0.33, -0.33],  # Low dose vs placebo, High dose vs placebo
        es_secondary=[-0.33, -0.33, -0.28, -0.28],  # Secondary endpoints
        correlation_matrix=[1, 0.6, 0.6, 0.6, 1, 0.6, 0.6, 0.6, 1],  # 3x3 flattened
        transition_matrix=[0, 1, 1, 0],  # 2x2 flattened
        initial_weights=[0.5, 0.5],
        success_criteria=[{"Crit": "DisjunctivePower", "Parameters": None}],
        n_simulations=10000,
        seed=12345,
    )

    result_3arm = await run_calculation(calculator, params_3arm, "Three-Arm Trial")
    print(f"✅ Result: {result_3arm}")

    print("\n🎉 Examples completed successfully!")
    print("\n💡 Next Steps:")
    print("1. Use these parameter templates for your trials")
    print("2. Start R MCP server for full graphical procedure calculations")
    print("3. Tune LLM prompts for better natural language extraction")


async def run_calculation(calculator, params, name):
    """Helper function to run calculation and get sample size"""
    state = {
        "messages": [],
        "parameters": params,
        "validation_result": {"valid": True},
        "calculation_result": None,
        "visualization_result": None,
        "mcp_tools": None,
        "current_step": "direct_test",
        "errors": [],
        "intermediate_results": {},
    }

    # Run calculation and visualization
    state = await calculator.calculation_agent(state)

    if state.get("calculation_result"):
        result = state["calculation_result"].get("result", {})
        n = result.get("recommended_sample_size_per_arm", "Unknown")
        method = state["calculation_result"].get("method", "Unknown")
        return f"{n} subjects per arm ({method} method)"
    else:
        return "Calculation failed"


if __name__ == "__main__":
    asyncio.run(working_example())
