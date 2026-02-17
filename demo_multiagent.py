#!/usr/bin/env python3
"""
Demonstration script for the Multi-Agent Sample Size Calculator

This script shows how to use the multi-agent system for clinical trial
sample size calculation without requiring a Jupyter environment.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

try:
    from SampleSizeMultiAgent import MultiAgentSampleSizeCalculator

    print("✅ Successfully imported MultiAgentSampleSizeCalculator")
except ImportError as e:
    print(f"❌ Failed to import required modules: {e}")
    print(
        "Please install required packages: pip install -r requirements_multiagent.txt"
    )
    sys.exit(1)


def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80)


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "-" * 60)
    print(f" {title}")
    print("-" * 60)


async def demo_basic_calculation():
    """Demonstrate basic sample size calculation"""
    print_header("MULTI-AGENT SAMPLE SIZE CALCULATOR DEMO")

    # Initialize the calculator
    print("🚀 Initializing Multi-Agent System...")
    try:
        calculator = MultiAgentSampleSizeCalculator()
        print("✅ Multi-Agent System initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        return

    # Demo 1: Simple two-arm trial
    print_section("Demo 1: Simple Two-Arm Trial")

    simple_input = """
    Calculate sample size for a simple two-arm clinical trial:
    
    Study Design:
    - Treatment arms: Placebo, Active Treatment
    - Allocation ratio: 1:1
    - Primary endpoint effect size: -0.4 (medium effect)
    
    Statistical Parameters:
    - Required power: 80%
    - Significance level: 5%
    - Expected drop-out rate: 15%
    
    Sample Size Search:
    - Minimum: 30 per arm
    - Maximum: 150 per arm
    - Increment: 5
    
    Multiplicity Control:
    - Graphical procedure
    - Initial weights: [1.0]
    - Transition matrix: [0]
    - Success criteria: DisjunctivePower
    
    Simulation: 5000 iterations, seed 12345
    """

    try:
        print("🔄 Running simple two-arm trial analysis...")
        result = await calculator.run_analysis(simple_input)
        print("✅ Analysis completed!")
        print("\nRESULT:")
        print(result)
    except Exception as e:
        print(f"❌ Analysis failed: {e}")

    # Demo 2: Three-arm trial (similar to R example)
    print_section("Demo 2: Three-Arm Trial (R Example Style)")

    complex_input = """
    Please calculate sample size for a three-arm dose-response study:
    
    Study Arms:
    - Placebo (control)
    - ABBV932L (low dose)
    - ABBV932H (high dose)
    - Allocation: 1:1:1 (equal randomization)
    
    Efficacy Endpoints:
    - Primary endpoint effect sizes vs placebo: -0.33, -0.33
    - Secondary endpoint effect sizes vs placebo: -0.33, -0.33, -0.28, -0.28
    - Between-endpoints correlation: moderate (0.6)
    - Correlation matrix: [1, 0.6, 0.6, 0.6, 1, 0.6, 0.6, 0.6, 1]
    
    Statistical Requirements:
    - Power: 80%
    - Alpha: 5%
    - Dropout rate: 20%
    
    Sample Size Parameters:
    - Search range: 50 to 300 per arm
    - Step size: 10
    
    Multiplicity Adjustment:
    - Graphical procedure
    - Initial hypothesis weights: [0.5, 0.5]
    - Transition matrix: [0, 1, 1, 0]
    - Success criteria: DisjunctivePower
    
    Simulation:
    - 10000 replications
    - Random seed: 12345
    """

    try:
        print("🔄 Running three-arm trial analysis...")
        result = await calculator.run_analysis(complex_input)
        print("✅ Analysis completed!")
        print("\nRESULT:")
        print(result)
    except Exception as e:
        print(f"❌ Analysis failed: {e}")


async def demo_error_handling():
    """Demonstrate error handling with invalid input"""
    print_section("Demo 3: Error Handling")

    invalid_input = """
    Calculate sample size with invalid parameters:
    - Power: 150% (invalid - over 100%)
    - Alpha: -0.05 (invalid - negative)
    - Effect size: "large" (invalid - not numeric)
    - Arms: only one arm (invalid - need at least 2)
    """

    calculator = MultiAgentSampleSizeCalculator()

    try:
        print("🔄 Testing error handling with invalid input...")
        result = await calculator.run_analysis(invalid_input)
        print("📋 Error handling result:")
        print(result)
    except Exception as e:
        print(f"System-level error (expected): {e}")


def demo_synchronous():
    """Run the demo using asyncio for users who prefer synchronous interface"""
    print_header("SYNCHRONOUS DEMO RUNNER")

    async def run_all_demos():
        await demo_basic_calculation()
        await demo_error_handling()

    try:
        asyncio.run(run_all_demos())
    except KeyboardInterrupt:
        print("\n🛑 Demo interrupted by user")
    except Exception as e:
        print(f"❌ Demo failed: {e}")


if __name__ == "__main__":
    print("🎯 Multi-Agent Sample Size Calculator Demonstration")
    print(
        "This demo shows the capabilities of the LangChain + LangGraph multi-agent system"
    )
    print("for clinical trial sample size calculation.")

    # Check if we're in an asyncio context or need to create one
    try:
        # Try to get the current event loop
        loop = asyncio.get_running_loop()
        print("📝 Running in async context")
        # If we're already in an async context, we can't use asyncio.run()
        asyncio.create_task(demo_basic_calculation())
    except RuntimeError:
        # No event loop running, safe to use asyncio.run()
        print("📝 Creating new event loop")
        demo_synchronous()

    print("\n🎉 Demo completed!")
    print("\nNext steps:")
    print("1. Install R MCP server for full functionality")
    print("2. Customize agents for your specific use cases")
    print("3. Integrate with your clinical trial workflow")
    print("4. Explore the Jupyter notebook for interactive examples")
