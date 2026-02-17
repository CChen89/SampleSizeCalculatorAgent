"""
Clinical Trial Sample Size Calculator - Chainlit Web App
A user-friendly web interface for the multi-agent sample size calculator
"""

import chainlit as cl
import asyncio
import sys
from pathlib import Path
import json
import pandas as pd
from typing import Dict, List, Optional

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

from SampleSizeMultiAgent import MultiAgentSampleSizeCalculator, SampleSizeParameters

# Global calculator instance
calculator = None


@cl.on_chat_start
async def start():
    """Initialize the application when a new chat session starts"""
    global calculator

    await cl.Message(
        content="# 🧮 Clinical Trial Sample Size Calculator\n\n"
        "Welcome! I'm your AI-powered sample size calculator for clinical trials.\n\n"
        "I can help you calculate sample sizes for:\n"
        "- 📊 Two-arm superiority trials\n"
        "- 📈 Three-arm dose-response studies\n"
        "- 🔬 Complex multi-arm trials\n"
        "- 📋 Studies with multiple endpoints\n\n"
        "**Getting started:**\n"
        "1. Choose a trial template using the buttons below\n"
        "2. Or describe your trial design in natural language\n"
        "3. I'll calculate the optimal sample size with statistical justification\n\n"
        "🚀 **Initializing the multi-agent system...**"
    ).send()

    # Initialize the calculator
    try:
        calculator = MultiAgentSampleSizeCalculator()

        # Test MCP connection
        tools = await calculator.get_mcp_tools()
        mcp_status = (
            f"✅ Connected ({len(tools)} tools)" if tools else "⚠️ Fallback mode"
        )

        await cl.Message(
            content=f"✅ **System Ready!**\n\n"
            f"📊 Multi-agent system: **Operational**\n"
            f"🔗 R MCP server: **{mcp_status}**\n"
            f"🤖 AI agents: **4 specialized agents ready**\n\n"
            f"Choose how you'd like to proceed:"
        ).send()

        # Create action buttons for common trial types
        actions = [
            cl.Action(
                name="two_arm_trial",
                value="two_arm",
                label="📊 Two-Arm Superiority Trial",
            ),
            cl.Action(
                name="three_arm_trial",
                value="three_arm",
                label="📈 Three-Arm Dose Response",
            ),
            cl.Action(
                name="abbv932_trial", value="abbv932", label="🔬 ABBV932 Example Trial"
            ),
            cl.Action(
                name="custom_trial", value="custom", label="⚙️ Custom Trial Design"
            ),
            cl.Action(name="help", value="help", label="❓ Help & Examples"),
        ]

        await cl.Message(
            content="Select a trial template to get started quickly:", actions=actions
        ).send()

    except Exception as e:
        await cl.Message(
            content=f"❌ **Initialization Error**\n\n"
            f"Error: {str(e)}\n\n"
            f"Please check your environment setup and try again."
        ).send()


@cl.action_callback("two_arm_trial")
async def handle_two_arm_trial(action):
    """Handle two-arm trial template"""
    await cl.Message(
        content="# 📊 Two-Arm Superiority Trial Setup\n\n"
        "I'll help you set up a two-arm superiority trial. Please provide:\n\n"
        "**Required Parameters:**\n"
        "- Treatment arms (e.g., 'Placebo, My_Drug')\n"
        "- Expected effect size vs placebo (e.g., -0.4)\n"
        "- Required statistical power (e.g., 0.8 for 80%)\n"
        "- Expected dropout rate (e.g., 0.15 for 15%)\n\n"
        "**Example format:**\n"
        "```\n"
        "Arms: Placebo, Treatment_A\n"
        "Effect size: -0.4\n"
        "Power: 0.8\n"
        "Dropout: 0.15\n"
        "```\n\n"
        "Or simply describe your trial and I'll extract the parameters automatically!"
    ).send()

    # Remove the action buttons
    await action.remove()


@cl.action_callback("three_arm_trial")
async def handle_three_arm_trial(action):
    """Handle three-arm trial template"""
    await cl.Message(
        content="# 📈 Three-Arm Dose Response Trial Setup\n\n"
        "Perfect! I'll help you design a three-arm dose-response study.\n\n"
        "**Please provide:**\n"
        "- Three treatment arms (e.g., 'Placebo, Low_Dose, High_Dose')\n"
        "- Effect sizes for each active arm vs placebo\n"
        "- Statistical power requirement\n"
        "- Expected dropout rate\n\n"
        "**Example format:**\n"
        "```\n"
        "Arms: Placebo, 5mg, 10mg\n"
        "Effect sizes: -0.3, -0.5\n"
        "Power: 0.8\n"
        "Dropout: 0.2\n"
        "```\n\n"
        "What are the details of your dose-response study?"
    ).send()

    await action.remove()


@cl.action_callback("abbv932_trial")
async def handle_abbv932_trial(action):
    """Handle the ABBV932 example trial"""
    await cl.Message(
        content="🔄 **Running ABBV932 Example Trial Analysis...**\n\nThis will demonstrate the full capabilities of the system."
    ).send()

    try:
        # Use the predefined ABBV932 parameters
        params = SampleSizeParameters(
            power=0.8,
            alpha=0.05,
            drop_rate=0.2,
            allocation_ratio="1:1:1",
            n_min=50,
            n_max=300,
            n_step=10,
            arm_names=["Placebo", "ABBV932L", "ABBV932H"],
            es_primary=[-0.33, -0.33],
            es_secondary=[-0.33, -0.33, -0.28, -0.28],
            correlation_matrix=[1, 0.6, 0.6, 0.6, 1, 0.6, 0.6, 0.6, 1],
            transition_matrix=[0, 1, 1, 0],
            initial_weights=[0.5, 0.5],
            success_criteria=[{"Crit": "DisjunctivePower", "Parameters": None}],
            n_simulations=10000,
            seed=12345,
        )

        result = await run_sample_size_calculation(params, "ABBV932 Three-Arm Trial")

        if result:
            await display_results(result, params)

    except Exception as e:
        await cl.Message(
            content=f"❌ **Error in ABBV932 calculation:** {str(e)}"
        ).send()

    await action.remove()


@cl.action_callback("custom_trial")
async def handle_custom_trial(action):
    """Handle custom trial design"""
    await cl.Message(
        content="# ⚙️ Custom Trial Design\n\n"
        "I can help you design any type of clinical trial! Please describe your study:\n\n"
        "**Include details about:**\n"
        "- Number and names of treatment arms\n"
        "- Expected effect sizes\n"
        "- Primary and secondary endpoints\n"
        "- Statistical requirements (power, alpha)\n"
        "- Expected dropout rate\n"
        "- Any special considerations\n\n"
        "**Example:**\n"
        '*"I\'m designing a 4-arm dose-finding study comparing placebo to 5mg, 10mg, and 20mg doses. I expect moderate effect sizes of -0.2, -0.35, and -0.5 respectively. I need 85% power with 5% alpha and expect 25% dropout."*\n\n'
        "What's your trial design?"
    ).send()

    await action.remove()


@cl.action_callback("help")
async def handle_help(action):
    """Handle help request"""
    await cl.Message(
        content="# ❓ Help & User Guide\n\n"
        "## 🎯 **Quick Start Examples**\n\n"
        "**Simple Two-Arm:**\n"
        "```\n"
        "Calculate sample size for:\n"
        "Arms: Placebo, Treatment\n"
        "Effect size: -0.4\n"
        "Power: 80%\n"
        "Dropout: 15%\n"
        "```\n\n"
        "**Three-Arm Dose Response:**\n"
        "```\n"
        "Three-arm trial with:\n"
        "Arms: Placebo, Low dose, High dose\n"
        "Effect sizes: -0.3 and -0.5 vs placebo\n"
        "Power: 85%\n"
        "Dropout: 20%\n"
        "```\n\n"
        "## 📊 **What I Can Calculate**\n\n"
        "- **Sample sizes** for 2-10 arm trials\n"
        "- **Power analyses** with multiple endpoints\n"
        "- **Graphical procedures** for multiplicity control\n"
        "- **Dropout adjustments** automatically included\n"
        "- **Clinical interpretations** and regulatory reports\n\n"
        "## 🔧 **Tips for Best Results**\n\n"
        "1. **Be specific** about effect sizes\n"
        "2. **Include dropout expectations**\n"
        "3. **Specify power requirements**\n"
        "4. **Describe endpoint relationships** if multiple\n\n"
        "Just describe your trial in natural language and I'll handle the rest!"
    ).send()

    await action.remove()


@cl.on_message
async def main(message: cl.Message):
    """Handle user messages and perform sample size calculations"""

    if not calculator:
        await cl.Message(
            content="❌ System not initialized. Please refresh the page."
        ).send()
        return

    user_input = message.content.strip()

    if not user_input:
        await cl.Message(
            content="Please describe your clinical trial design or use one of the template buttons above."
        ).send()
        return

    # Show processing message
    processing_msg = await cl.Message(
        content="🔄 **Processing your trial design...**\n\nAnalyzing parameters with AI agents..."
    ).send()

    try:
        # Use the natural language processing workflow
        result = await calculator.run_analysis(user_input)

        # Update processing message
        await processing_msg.update(
            content="✅ **Analysis Complete!**\n\nGenerating detailed results..."
        )

        # Display the results
        await display_natural_language_results(result, user_input)

    except Exception as e:
        await processing_msg.update(content=f"❌ **Error during analysis:** {str(e)}")

        # Offer fallback options
        actions = [
            cl.Action(
                name="try_template", value="template", label="📊 Try a Template Instead"
            ),
            cl.Action(name="help", value="help", label="❓ Get Help"),
        ]

        await cl.Message(
            content="Having trouble with that input. Would you like to try a template or get help?",
            actions=actions,
        ).send()


async def run_sample_size_calculation(
    params: SampleSizeParameters, trial_name: str
) -> Optional[Dict]:
    """Run the multi-agent calculation workflow"""

    try:
        # Create state
        state = {
            "messages": [],
            "parameters": params,
            "validation_result": {"valid": True},
            "calculation_result": None,
            "visualization_result": None,
            "mcp_tools": None,
            "current_step": "chainlit_calculation",
            "errors": [],
            "intermediate_results": {},
        }

        # Run agents sequentially
        await cl.Message(
            content="🧮 **Calculation Agent:** Computing optimal sample size..."
        ).send()
        state = await calculator.calculation_agent(state)

        await cl.Message(
            content="📊 **Visualization Agent:** Creating clinical interpretation..."
        ).send()
        state = await calculator.visualization_agent(state)

        await cl.Message(
            content="🎯 **Coordinator Agent:** Assembling final report..."
        ).send()
        final_report = calculator.compile_final_response(state)

        return {"state": state, "final_report": final_report, "trial_name": trial_name}

    except Exception as e:
        await cl.Message(content=f"❌ **Calculation Error:** {str(e)}").send()
        return None


async def display_results(result: Dict, params: SampleSizeParameters):
    """Display the calculation results in a nice format"""

    state = result["state"]
    final_report = result["final_report"]
    trial_name = result["trial_name"]

    # Extract key results
    calc_result = state.get("calculation_result", {})
    if calc_result:
        method = calc_result.get("method", "unknown")
        calc_data = calc_result.get("result", {})

        if (
            isinstance(calc_data, dict)
            and "recommended_sample_size_per_arm" in calc_data
        ):
            n_per_arm = calc_data["recommended_sample_size_per_arm"]
            total_n = n_per_arm * len(params.arm_names)
            power = calc_data.get("power_achieved", params.power)

            # Create summary card
            summary = f"""# 🎯 **Sample Size Results: {trial_name}**

## 📊 **Key Results**
- **Sample Size per Arm:** {n_per_arm} subjects
- **Total Enrollment:** {total_n} subjects  
- **Power Achieved:** {power * 100:.1f}%
- **Calculation Method:** {method.title()}

## 📋 **Trial Design Summary**
- **Arms:** {", ".join(params.arm_names)}
- **Allocation:** {params.allocation_ratio}
- **Effect Sizes:** {params.es_primary}
- **Alpha Level:** {params.alpha * 100:.1f}%
- **Dropout Rate:** {params.drop_rate * 100:.1f}%
"""

            await cl.Message(content=summary).send()

            # Create detailed report as a file
            report_file = cl.File(
                name="detailed_report.md",
                content=final_report.encode(),
                display="inline",
            )

            await cl.Message(
                content="## 📄 **Detailed Clinical Report**\n\n"
                "Complete statistical analysis with clinical interpretation:",
                elements=[report_file],
            ).send()

            # Create parameter summary table
            param_data = {
                "Parameter": [
                    "Power",
                    "Alpha",
                    "Dropout Rate",
                    "Arms",
                    "Min N",
                    "Max N",
                    "Step Size",
                ],
                "Value": [
                    f"{params.power * 100:.1f}%",
                    f"{params.alpha * 100:.1f}%",
                    f"{params.drop_rate * 100:.1f}%",
                    len(params.arm_names),
                    params.n_min,
                    params.n_max,
                    params.n_step,
                ],
            }

            param_df = pd.DataFrame(param_data)

            await cl.Message(
                content="## ⚙️ **Parameters Used**\n\n"
                + param_df.to_markdown(index=False)
            ).send()

            # Offer next actions
            actions = [
                cl.Action(
                    name="new_calculation", value="new", label="🔄 New Calculation"
                ),
                cl.Action(
                    name="modify_params", value="modify", label="⚙️ Modify Parameters"
                ),
                cl.Action(
                    name="export_results", value="export", label="📤 Export Results"
                ),
            ]

            await cl.Message(
                content="What would you like to do next?", actions=actions
            ).send()

    else:
        await cl.Message(content="❌ **No calculation results available**").send()


async def display_natural_language_results(result: str, user_input: str):
    """Display results from natural language processing"""

    await cl.Message(
        content=f"# 🎯 **Analysis Results**\n\n"
        f"**Your Request:** *{user_input[:100]}...*\n\n"
        f"{result}"
    ).send()

    # Check if result contains sample size information
    if "subjects per arm" in result.lower():
        # Extract sample size if possible
        import re

        size_match = re.search(r"(\d+)\s*subjects?\s*per\s*arm", result.lower())
        if size_match:
            n = size_match.group(1)

            await cl.Message(
                content=f"## 🎯 **Quick Summary**\n\n"
                f"**Recommended Sample Size:** {n} subjects per arm\n\n"
                f"This recommendation includes statistical power calculations and dropout adjustments."
            ).send()

    # Offer follow-up actions
    actions = [
        cl.Action(
            name="refine_calculation", value="refine", label="🔧 Refine Parameters"
        ),
        cl.Action(name="new_calculation", value="new", label="🔄 New Calculation"),
        cl.Action(name="more_details", value="details", label="📋 More Details"),
    ]

    await cl.Message(content="How can I help you further?", actions=actions).send()


@cl.action_callback("new_calculation")
async def handle_new_calculation(action):
    """Start a new calculation"""
    await cl.Message(
        content="# 🔄 **New Sample Size Calculation**\n\n"
        "Let's design another clinical trial! Choose from the options below or describe your study:"
    ).send()

    actions = [
        cl.Action(name="two_arm_trial", value="two_arm", label="📊 Two-Arm Trial"),
        cl.Action(
            name="three_arm_trial", value="three_arm", label="📈 Three-Arm Trial"
        ),
        cl.Action(name="custom_trial", value="custom", label="⚙️ Custom Design"),
    ]

    await cl.Message(
        content="Select a template or describe your trial:", actions=actions
    ).send()

    await action.remove()


@cl.action_callback("modify_params")
async def handle_modify_params(action):
    """Handle parameter modification"""
    await cl.Message(
        content="# ⚙️ **Modify Parameters**\n\n"
        "Tell me what you'd like to change:\n\n"
        "- **Power requirement** (e.g., 'increase power to 90%')\n"
        "- **Effect size** (e.g., 'change effect size to -0.5')\n"
        "- **Dropout rate** (e.g., 'reduce dropout to 10%')\n"
        "- **Sample size range** (e.g., 'search 100-500 per arm')\n"
        "- **Add/remove arms**\n\n"
        "What would you like to modify?"
    ).send()

    await action.remove()


if __name__ == "__main__":
    # This allows the app to be run directly
    pass
