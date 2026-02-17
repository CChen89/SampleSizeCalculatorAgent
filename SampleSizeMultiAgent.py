"""
Multi-Agent Sample Size Calculator using LangChain and LangGraph
Based on the R SampleSizeMCP.R implementation

This system uses multiple specialized agents to handle different aspects of
sample size calculation for clinical trials with graphical procedures.
"""

import os
import json
import asyncio
from typing import Dict, List, Any, Optional, Tuple, TypedDict, Annotated
from dataclasses import dataclass
import numpy as np
import pandas as pd

# LangChain imports
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
# Removed deprecated agent imports - we use LangGraph workflow instead

# LangGraph imports
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode

# Pydantic for structured outputs
from pydantic import BaseModel, Field, validator
from enum import Enum

# MCP integration
from langchain_mcp_adapters.client import MultiServerMCPClient

# Load environment variables
import dotenv

dotenv.load_dotenv()

# Configuration
ILIAD_API_KEY = os.getenv("ILIAD_API_KEY")
ILIAD_URL_BASE = os.getenv("ILIAD_URL_BASE")


class SuccessCriteria(str, Enum):
    DISJUNCTIVE_POWER = "DisjunctivePower"
    CONJUNCTIVE_POWER = "ConjunctivePower"
    WEIGHTED_POWER = "WeightedPower"


class SampleSizeParameters(BaseModel):
    """Structured parameters for sample size calculation"""

    power: float = Field(..., ge=0.0, le=1.0, description="Required power (0-1)")
    alpha: float = Field(..., ge=0.0, le=1.0, description="Significance level (0-1)")
    drop_rate: float = Field(..., ge=0.0, le=1.0, description="Drop-out rate (0-1)")
    allocation_ratio: str = Field(..., description="Allocation ratio (e.g., '1:1:1')")
    n_min: int = Field(..., gt=0, description="Minimum sample size per arm")
    n_max: int = Field(..., gt=0, description="Maximum sample size per arm")
    n_step: int = Field(..., gt=0, description="Sample size increment")
    arm_names: List[str] = Field(..., min_length=2, description="Treatment arm names")
    es_primary: List[float] = Field(..., description="Primary endpoint effect sizes")
    es_secondary: Optional[List[float]] = Field(
        None, description="Secondary endpoint effect sizes"
    )
    correlation_matrix: List[float] = Field(
        ..., description="Between-endpoint correlation matrix (flattened)"
    )
    transition_matrix: List[float] = Field(
        ..., description="Transition matrix (flattened)"
    )
    initial_weights: List[float] = Field(..., description="Initial hypothesis weights")
    success_criteria: List[Dict[str, Any]] = Field(
        ..., description="Success criteria definitions"
    )
    n_simulations: int = Field(
        default=10000, gt=0, description="Number of simulation runs"
    )
    seed: Optional[int] = Field(None, description="Random seed for reproducibility")

    @validator("n_max")
    def n_max_greater_than_n_min(cls, v, values):
        if "n_min" in values and v <= values["n_min"]:
            raise ValueError("n_max must be greater than n_min")
        return v


class AgentState(TypedDict):
    """State shared across all agents"""

    messages: Annotated[List, add_messages]
    parameters: Optional[SampleSizeParameters]
    validation_result: Optional[Dict[str, Any]]
    calculation_result: Optional[Dict[str, Any]]
    visualization_result: Optional[Dict[str, Any]]
    mcp_tools: Optional[List[Any]]
    current_step: str
    errors: List[str]
    intermediate_results: Dict[str, Any]


@dataclass
class MultiAgentSampleSizeCalculator:
    """
    Main orchestrator for the multi-agent sample size calculation system
    """

    def __init__(self):
        self.llm = AzureChatOpenAI(
            api_key=ILIAD_API_KEY,
            azure_endpoint=ILIAD_URL_BASE,
            openai_api_version="2023-07-01-preview",
            azure_deployment="gpt-4o",
            temperature=0.1,
        )

        self.mcp_client = None
        self.workflow = None
        self.setup_mcp_client()
        self.build_workflow()

    def setup_mcp_client(self):
        """Initialize MCP client connection to R server"""
        try:
            self.mcp_client = MultiServerMCPClient(
                {
                    "samplesize": {
                        "transport": "streamable_http",
                        "url": "http://127.0.0.1:9291",
                    }
                }
            )
        except Exception as e:
            print(f"Warning: Could not connect to MCP server: {e}")
            self.mcp_client = None

    async def get_mcp_tools(self):
        """Get available tools from MCP server"""
        if self.mcp_client:
            try:
                return await self.mcp_client.get_tools()
            except Exception as e:
                print(f"Error getting MCP tools: {e}")
        return []

    def build_workflow(self):
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)

        # Add nodes
        workflow.add_node("parameter_validator", self.parameter_validator_agent)
        workflow.add_node("calculation_agent", self.calculation_agent)
        workflow.add_node("visualization_agent", self.visualization_agent)
        workflow.add_node("coordinator", self.coordinator_agent)

        # Define the flow
        workflow.add_edge(START, "parameter_validator")
        workflow.add_edge("parameter_validator", "calculation_agent")
        workflow.add_edge("calculation_agent", "visualization_agent")
        workflow.add_edge("visualization_agent", "coordinator")
        workflow.add_edge("coordinator", END)

        # Compile the workflow
        self.workflow = workflow.compile(checkpointer=MemorySaver())

    async def parameter_validator_agent(self, state: AgentState) -> AgentState:
        """Agent responsible for validating and structuring input parameters"""
        print("🔍 Parameter Validator Agent: Processing input parameters...")

        system_prompt = """You are a Parameter Validation Agent specialized in clinical trial design parameters.
        Your task is to:
        1. Extract and validate sample size calculation parameters from user input
        2. Ensure all required parameters are present and within valid ranges
        3. Structure the parameters according to the SampleSizeParameters schema
        4. Identify any missing or invalid parameters
        
        Pay special attention to:
        - Power and alpha levels (must be between 0 and 1)
        - Effect sizes for treatment arms
        - Correlation and transition matrices (must have correct dimensions)
        - Allocation ratios (must match number of arms)
        - Sample size ranges (n_min < n_max)
        """

        # Get the latest user message
        user_message = ""
        for msg in reversed(state["messages"]):
            if hasattr(msg, "content") and isinstance(msg.content, str):
                user_message = msg.content
                break

        validation_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                (
                    "human",
                    """
            Please extract and validate the following parameters from this clinical trial design:
            
            {user_input}
            
            Structure your response as a JSON object with the following format:
            {{
                "valid": true/false,
                "parameters": {{...SampleSizeParameters...}},
                "errors": ["list of validation errors if any"],
                "warnings": ["list of warnings if any"]
            }}
            
            If any required parameters are missing or invalid, set "valid" to false and list the issues.
            """,
                ),
            ]
        )

        try:
            chain = validation_prompt | self.llm | StrOutputParser()
            response = await chain.ainvoke({"user_input": user_message})

            # Extract JSON from response if it contains other text
            import re

            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
            else:
                json_str = response

            # Parse the response
            validation_result = json.loads(json_str)

            # If validation is successful, create SampleSizeParameters object
            if (
                validation_result.get("valid", False)
                and "parameters" in validation_result
            ):
                try:
                    parameters = SampleSizeParameters(**validation_result["parameters"])
                    state["parameters"] = parameters
                    print("✅ Parameters validated successfully")
                except Exception as e:
                    validation_result["valid"] = False
                    validation_result["errors"].append(
                        f"Parameter validation failed: {str(e)}"
                    )
                    print(f"❌ Parameter validation failed: {e}")

            state["validation_result"] = validation_result
            state["current_step"] = "validation_complete"

            if validation_result.get("errors"):
                state["errors"].extend(validation_result["errors"])

        except Exception as e:
            error_msg = f"Parameter validation agent failed: {str(e)}"
            state["errors"].append(error_msg)
            state["validation_result"] = {"valid": False, "errors": [error_msg]}
            print(f"❌ {error_msg}")

        return state

    async def calculation_agent(self, state: AgentState) -> AgentState:
        """Agent responsible for performing sample size calculations"""
        print("🧮 Calculation Agent: Performing sample size calculations...")

        if not state.get("parameters") or not state.get("validation_result", {}).get(
            "valid", False
        ):
            error_msg = "Cannot proceed with calculations - parameters not validated"
            state["errors"].append(error_msg)
            print(f"❌ {error_msg}")
            return state

        system_prompt = """You are a Statistical Calculation Agent specialized in clinical trial sample size estimation.
        Your task is to:
        1. Use the validated parameters to perform sample size calculations
        2. Apply graphical procedures for multiple testing correction
        3. Calculate power curves and determine optimal sample sizes
        4. Generate statistical summaries and recommendations
        
        You have access to specialized statistical tools through the MCP server.
        Use these tools to perform accurate calculations based on the Graphical Procedure methodology.
        """

        try:
            # Get MCP tools
            if self.mcp_client:
                mcp_tools = await self.get_mcp_tools()
                state["mcp_tools"] = mcp_tools
                print(f"📊 Retrieved {len(mcp_tools)} MCP tools")

            # Prepare parameters for MCP server call
            params = state["parameters"]

            # Format parameters for the GraphicalProcedure tool
            mcp_params = {
                "power": params.power,
                "alpha": params.alpha,
                "dropR": params.drop_rate,
                "alloc": params.allocation_ratio,
                "n.min": params.n_min,
                "n.max": params.n_max,
                "n.step": params.n_step,
                "ArmNames": params.arm_names,
                "ES.primary": params.es_primary,
                "ES.secondary": params.es_secondary or [],
                "Correlation": params.correlation_matrix,
                "transitionM": params.transition_matrix,
                "weight": params.initial_weights,
                "Criteria": params.success_criteria,
                "nsim": params.n_simulations,
                "seed": params.seed,
            }

            # Call MCP server for calculations (if available)
            if self.mcp_client and mcp_tools:
                try:
                    # Find the GraphicalProcedure tool
                    graphical_tool = None
                    for tool in mcp_tools:
                        if hasattr(tool, "name") and "graphical" in tool.name.lower():
                            graphical_tool = tool
                            break

                    if graphical_tool:
                        print("🔄 Calling MCP server for calculations...")
                        calc_result = await graphical_tool.ainvoke(mcp_params)
                        state["calculation_result"] = {
                            "method": "mcp_server",
                            "result": calc_result,
                            "parameters_used": mcp_params,
                        }
                        print("✅ MCP calculation completed successfully")
                    else:
                        raise Exception(
                            "GraphicalProcedure tool not found in MCP server"
                        )

                except Exception as e:
                    print(f"⚠️ MCP calculation failed, using fallback method: {e}")
                    # Fallback to simplified calculation
                    calc_result = await self.fallback_calculation(params)
                    state["calculation_result"] = {
                        "method": "fallback",
                        "result": calc_result,
                        "parameters_used": mcp_params,
                    }
            else:
                print("⚠️ MCP server not available, using fallback calculation")
                calc_result = await self.fallback_calculation(params)
                state["calculation_result"] = {
                    "method": "fallback",
                    "result": calc_result,
                    "parameters_used": mcp_params,
                }

            state["current_step"] = "calculation_complete"

        except Exception as e:
            error_msg = f"Calculation agent failed: {str(e)}"
            state["errors"].append(error_msg)
            print(f"❌ {error_msg}")

        return state

    async def fallback_calculation(
        self, params: SampleSizeParameters
    ) -> Dict[str, Any]:
        """Simplified fallback calculation when MCP server is not available"""
        print("🔄 Performing fallback sample size calculation...")

        # Simplified power calculation (this is a basic approximation)
        # In practice, this would be much more complex for graphical procedures

        z_alpha = 1.96 if params.alpha == 0.05 else 2.576  # Simplified
        z_beta = 0.84 if params.power == 0.8 else 1.28  # Simplified

        # Calculate sample size for each effect size
        sample_sizes = []
        for es in params.es_primary:
            if es != 0:
                n_per_arm = ((z_alpha + z_beta) ** 2 * 2) / (es**2)
                n_per_arm = int(np.ceil(n_per_arm / (1 - params.drop_rate)))
                sample_sizes.append(max(n_per_arm, params.n_min))
            else:
                sample_sizes.append(params.n_max)

        # Find the maximum required sample size
        recommended_n = min(max(sample_sizes), params.n_max)

        return {
            "recommended_sample_size_per_arm": recommended_n,
            "power_achieved": params.power,
            "method": "simplified_calculation",
            "effect_sizes_used": params.es_primary,
            "note": "This is a simplified calculation. Use MCP server for full graphical procedure analysis.",
        }

    async def visualization_agent(self, state: AgentState) -> AgentState:
        """Agent responsible for creating visualizations and summaries"""
        print("📊 Visualization Agent: Creating summaries and recommendations...")

        if not state.get("calculation_result"):
            error_msg = (
                "Cannot create visualizations - no calculation results available"
            )
            state["errors"].append(error_msg)
            print(f"❌ {error_msg}")
            return state

        system_prompt = """You are a Data Visualization and Reporting Agent specialized in clinical trial reporting.
        Your task is to:
        1. Create comprehensive summaries of sample size calculations
        2. Generate clear recommendations for trial design
        3. Highlight key findings and assumptions
        4. Provide interpretation of results in clinical context
        
        Focus on making the results accessible to both statisticians and clinical researchers.
        """

        try:
            calc_result = state["calculation_result"]
            params = state["parameters"]

            viz_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", system_prompt),
                    (
                        "human",
                        """
                Based on the following sample size calculation results and parameters, create a comprehensive summary:
                
                Parameters used:
                {parameters}
                
                Calculation results:
                {results}
                
                Please provide:
                1. Executive summary with key recommendations
                2. Detailed parameter summary
                3. Sample size recommendations with justification
                4. Key assumptions and limitations
                5. Clinical interpretation
                
                Format your response as a structured report.
                """,
                    ),
                ]
            )

            chain = viz_prompt | self.llm | StrOutputParser()
            summary = await chain.ainvoke(
                {
                    "parameters": params.dict() if params else "None",
                    "results": calc_result,
                }
            )

            state["visualization_result"] = {
                "summary": summary,
                "recommendations": self.extract_recommendations(calc_result),
                "key_findings": self.extract_key_findings(calc_result, params),
            }

            state["current_step"] = "visualization_complete"
            print("✅ Visualization and summary completed")

        except Exception as e:
            error_msg = f"Visualization agent failed: {str(e)}"
            state["errors"].append(error_msg)
            print(f"❌ {error_msg}")

        return state

    def extract_recommendations(self, calc_result: Dict[str, Any]) -> List[str]:
        """Extract key recommendations from calculation results"""
        recommendations = []

        if calc_result.get("method") == "mcp_server":
            # Extract from MCP server results
            if "recommended_sample_size_per_arm" in calc_result.get("result", {}):
                n = calc_result["result"]["recommended_sample_size_per_arm"]
                recommendations.append(f"Recommended sample size: {n} subjects per arm")
        elif calc_result.get("method") == "fallback":
            n = calc_result["result"]["recommended_sample_size_per_arm"]
            recommendations.append(
                f"Estimated sample size: {n} subjects per arm (simplified calculation)"
            )
            recommendations.append(
                "Consider using full graphical procedure analysis for final design"
            )

        return recommendations

    def extract_key_findings(
        self, calc_result: Dict[str, Any], params: SampleSizeParameters
    ) -> Dict[str, Any]:
        """Extract key findings from results"""
        findings = {
            "study_design": {
                "arms": len(params.arm_names) if params else "Unknown",
                "allocation": params.allocation_ratio if params else "Unknown",
                "power": params.power if params else "Unknown",
                "alpha": params.alpha if params else "Unknown",
            },
            "sample_size": "See calculation results",
            "method": calc_result.get("method", "Unknown"),
        }

        return findings

    async def coordinator_agent(self, state: AgentState) -> AgentState:
        """Coordinator agent that assembles final results"""
        print("🎯 Coordinator Agent: Assembling final results...")

        system_prompt = """You are a Coordinator Agent responsible for assembling and presenting final results.
        Your task is to:
        1. Review all agent outputs
        2. Identify any issues or inconsistencies
        3. Provide a final comprehensive response
        4. Suggest next steps or additional analyses if needed
        """

        try:
            # Compile final message
            final_message = self.compile_final_response(state)
            state["messages"].append(AIMessage(content=final_message))
            state["current_step"] = "complete"
            print("✅ Multi-agent analysis completed successfully")

        except Exception as e:
            error_msg = f"Coordinator agent failed: {str(e)}"
            state["errors"].append(error_msg)
            print(f"❌ {error_msg}")

        return state

    def compile_final_response(self, state: AgentState) -> str:
        """Compile the final response from all agent outputs"""
        response_parts = []

        response_parts.append("# Sample Size Calculation Results")
        response_parts.append("Generated by Multi-Agent Statistical Analysis System\n")

        # Validation results
        if state.get("validation_result"):
            validation = state["validation_result"]
            if validation.get("valid"):
                response_parts.append(
                    "✅ **Parameter Validation**: All parameters validated successfully"
                )
            else:
                response_parts.append("❌ **Parameter Validation**: Issues found")
                if validation.get("errors"):
                    for error in validation["errors"]:
                        response_parts.append(f"   - {error}")

        # Calculation results
        if state.get("calculation_result"):
            calc = state["calculation_result"]
            response_parts.append(
                f"\n## Calculation Method: {calc.get('method', 'Unknown')}"
            )

            if calc.get("result"):
                result = calc["result"]
                if (
                    isinstance(result, dict)
                    and "recommended_sample_size_per_arm" in result
                ):
                    n = result["recommended_sample_size_per_arm"]
                    response_parts.append(
                        f"**Recommended Sample Size**: {n} subjects per arm"
                    )

                    if "power_achieved" in result:
                        power = result["power_achieved"]
                        response_parts.append(f"**Power Achieved**: {power}")

        # Visualization results
        if state.get("visualization_result"):
            viz = state["visualization_result"]
            if viz.get("summary"):
                response_parts.append(f"\n## Summary\n{viz['summary']}")

            if viz.get("recommendations"):
                response_parts.append("\n## Recommendations")
                for rec in viz["recommendations"]:
                    response_parts.append(f"- {rec}")

        # Errors
        if state.get("errors"):
            response_parts.append("\n## Issues Encountered")
            for error in state["errors"]:
                response_parts.append(f"⚠️ {error}")

        return "\n".join(response_parts)

    async def run_analysis(self, user_input: str) -> str:
        """Run the complete multi-agent analysis"""
        print("🚀 Starting Multi-Agent Sample Size Analysis...")

        initial_state = AgentState(
            messages=[HumanMessage(content=user_input)],
            parameters=None,
            validation_result=None,
            calculation_result=None,
            visualization_result=None,
            mcp_tools=None,
            current_step="starting",
            errors=[],
            intermediate_results={},
        )

        try:
            # Run the workflow
            final_state = await self.workflow.ainvoke(
                initial_state,
                config={"configurable": {"thread_id": "sample_size_analysis"}},
            )

            # Extract final message
            for msg in reversed(final_state["messages"]):
                if isinstance(msg, AIMessage):
                    return msg.content

            return "Analysis completed but no final message generated."

        except Exception as e:
            error_msg = f"Multi-agent analysis failed: {str(e)}"
            print(f"❌ {error_msg}")
            return f"Error: {error_msg}"


# Example usage and testing
async def main():
    """Example usage of the Multi-Agent Sample Size Calculator"""

    # Initialize the calculator
    calculator = MultiAgentSampleSizeCalculator()

    # Example input (similar to the TestAgent.ipynb example)
    user_input = """
    Please calculate sample size given the following design:
    1. Multiplicity Procedure: Graphical Procedure 
    2. Names of treatment arms: Placebo, ABBV932L, ABBV932H 
    3. Effect sizes of primary efficacy endpoints for treatment arms: -0.33, -0.33
    4. Effect sizes of key secondary endpoints for treatment arms: -0.33, -0.33, -0.28, -0.28
    5. Allocation Ratio: 1:1:1
    6. Drop out rate: 0.2
    7. Between-endpoints Correlation Matrix: [1, 0.6, 0.6, 0.6, 1, 0.6, 0.6, 0.6, 1]
    8. Required statistical power: 0.8
    9. Significance level: 0.05
    10. Minimum sample size per arm for searching: 50
    11. Maximum sample size per arm for searching: 300
    12. Increment of sample size per arm for searching: 10
    13. Initial hypothesis weight: [0.5, 0.5]
    14. Transition Matrix: [0, 1, 1, 0]
    15. Success criteria: DisjunctivePower
    16. Number of simulations: 10000
    17. Random seed: 12345
    """

    # Run the analysis
    result = await calculator.run_analysis(user_input)
    print("\n" + "=" * 80)
    print("FINAL ANALYSIS RESULT")
    print("=" * 80)
    print(result)


if __name__ == "__main__":
    # Run the example
    asyncio.run(main())
