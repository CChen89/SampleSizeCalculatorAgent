# Multi-Agent Sample Size Calculator

A comprehensive Python implementation using LangChain and LangGraph for clinical trial sample size calculation, based on the R SampleSizeMCP.R implementation.

## Overview

This system implements a multi-agent architecture that mirrors and extends the functionality of your R-based Graphical Procedure sample size calculator. It leverages LangChain for AI-powered parameter extraction and LangGraph for workflow orchestration.

## Architecture

### Multi-Agent System Components

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Parameter      │───▶│  Calculation     │───▶│  Visualization  │───▶│  Coordinator    │
│  Validator      │    │  Agent           │    │  Agent          │    │  Agent          │
│  Agent          │    │                  │    │                 │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘    └─────────────────┘
        │                        │                        │                        │
        ▼                        ▼                        ▼                        ▼
   Validates &              Performs               Creates              Assembles
   structures              statistical            summaries &           final
   parameters              calculations           recommendations       results
```

### Agent Responsibilities

1. **Parameter Validator Agent**
   - Extracts parameters from natural language input
   - Validates parameter ranges and consistency
   - Structures data according to `SampleSizeParameters` schema
   - Handles missing or invalid parameters gracefully

2. **Calculation Agent**
   - Integrates with R MCP server for full graphical procedure calculations
   - Provides fallback calculations when MCP server is unavailable
   - Handles complex multiplicity adjustments
   - Manages simulation parameters

3. **Visualization Agent**
   - Creates comprehensive summaries of results
   - Generates clinical interpretations
   - Provides actionable recommendations
   - Formats results for different audiences

4. **Coordinator Agent**
   - Orchestrates the entire workflow
   - Handles error propagation and recovery
   - Assembles final comprehensive reports
   - Manages state transitions

## Features

### Core Capabilities
- ✅ **Graphical Procedure Implementation**: Full support for graphical methods in multiple testing
- ✅ **Multi-Arm Trials**: Support for 2, 3, 4+ arm clinical trials
- ✅ **Multiple Endpoints**: Primary and secondary endpoint handling
- ✅ **Correlation Modeling**: Between-endpoint correlation matrices
- ✅ **Dropout Adjustment**: Automatic adjustment for expected dropout rates
- ✅ **Power Curves**: Multiple success criteria (Disjunctive, Conjunctive, Weighted Power)

### Integration Features  
- ✅ **MCP Server Integration**: Direct connection to R statistical server
- ✅ **Fallback Calculations**: Works without R server using simplified methods
- ✅ **Natural Language Input**: AI-powered parameter extraction
- ✅ **Structured Validation**: Comprehensive parameter validation with Pydantic
- ✅ **Error Handling**: Robust error handling and user feedback

### Advanced Features
- ✅ **LangGraph Workflow**: State-of-the-art workflow orchestration
- ✅ **Async Processing**: Fully asynchronous for better performance
- ✅ **Memory Management**: Built-in checkpointing and state management
- ✅ **Extensible Architecture**: Easy to add new agents or modify existing ones

## Installation

### Prerequisites
- Python 3.8+
- Azure OpenAI API access (or compatible OpenAI API)
- Optional: R with MCP server running on port 9290

### Install Dependencies

```bash
pip install -r requirements_multiagent.txt
```

### Environment Setup

Create a `.env` file:
```env
ILIAD_API_KEY=your_azure_openai_api_key
ILIAD_URL_BASE=your_azure_openai_endpoint
```

## Usage

### Quick Start

```python
import asyncio
from SampleSizeMultiAgent import MultiAgentSampleSizeCalculator

async def main():
    # Initialize the calculator
    calculator = MultiAgentSampleSizeCalculator()
    
    # Define your trial
    trial_input = """
    Calculate sample size for a three-arm trial:
    - Arms: Placebo, Low Dose, High Dose
    - Allocation: 1:1:1
    - Primary effect sizes: -0.3, -0.4
    - Power: 80%, Alpha: 5%
    - Dropout: 20%
    - Sample size range: 50-300 per arm
    """
    
    # Run analysis
    result = await calculator.run_analysis(trial_input)
    print(result)

# Run the analysis
asyncio.run(main())
```

### Jupyter Notebook

For interactive exploration, use the provided notebook:

```bash
jupyter notebook MultiAgentSampleSize.ipynb
```

### Command Line Demo

Run the demonstration script:

```bash
python demo_multiagent.py
```

## Configuration

### MCP Server Integration

To use the full R-based calculations:

1. Start your R MCP server:
```r
source("OASiS/SampleSizeMCP.R")
# Server runs on http://localhost:9290
```

2. The Python system will automatically detect and use the MCP server

### Fallback Mode

If the MCP server is unavailable, the system uses simplified calculations:
- Basic power analysis formulas
- Approximate sample size calculations  
- Reduced functionality but still functional

## Examples

### Example 1: Two-Arm Superiority Trial

```python
input_text = """
Two-arm superiority trial:
- Placebo vs Active Treatment (1:1)
- Effect size: -0.4 (Cohen's d)
- Power: 90%, Alpha: 0.05
- Dropout: 15%
- Range: 30-150 per arm
"""

result = await calculator.run_analysis(input_text)
```

### Example 2: Complex Multi-Arm Trial

```python
input_text = """
Four-arm dose-finding study:
- Placebo, 5mg, 10mg, 20mg (1:1:1:1)
- Primary effect sizes: -0.2, -0.35, -0.5
- Secondary endpoint correlation: 0.4
- Graphical procedure with weighted hypotheses
- Power: 85%, Alpha: 0.025
- Dropout: 25%
"""

result = await calculator.run_analysis(input_text)
```

## API Reference

### Core Classes

#### `MultiAgentSampleSizeCalculator`
Main orchestrator class.

**Methods:**
- `run_analysis(user_input: str) -> str`: Run complete analysis
- `setup_mcp_client()`: Initialize MCP connection
- `build_workflow()`: Construct LangGraph workflow

#### `SampleSizeParameters`
Pydantic model for structured parameters.

**Fields:**
- `power: float`: Required statistical power (0-1)
- `alpha: float`: Significance level (0-1) 
- `drop_rate: float`: Expected dropout rate (0-1)
- `arm_names: List[str]`: Treatment arm names
- `es_primary: List[float]`: Primary endpoint effect sizes
- `es_secondary: List[float]`: Secondary endpoint effect sizes
- `correlation_matrix: List[float]`: Flattened correlation matrix
- `transition_matrix: List[float]`: Graphical procedure transitions
- And more...

### Agent Functions

Each agent can be called individually for testing:

```python
calculator = MultiAgentSampleSizeCalculator()

# Test individual agents
state = await calculator.parameter_validator_agent(initial_state)
state = await calculator.calculation_agent(state) 
state = await calculator.visualization_agent(state)
state = await calculator.coordinator_agent(state)
```

## Comparison with R Implementation

| Feature | R SampleSizeMCP.R | Python MultiAgent | Notes |
|---------|------------------|-------------------|-------|
| Graphical Procedures | ✅ Full Implementation | ✅ Via MCP Integration | Python delegates to R for precision |
| Multi-Arm Trials | ✅ Yes | ✅ Yes | Both support unlimited arms |
| Correlation Modeling | ✅ Yes | ✅ Yes | Full matrix support |
| Natural Language Input | ❌ No | ✅ Yes | AI-powered parameter extraction |
| Workflow Orchestration | ❌ Single Function | ✅ Multi-Agent | Better modularity and error handling |
| Visualization | ✅ ggplot2 | ✅ Text Summaries | R focuses on plots, Python on interpretations |
| Error Handling | ❌ Basic | ✅ Comprehensive | Multi-layer validation and recovery |
| Async Processing | ❌ No | ✅ Yes | Better scalability |

## Troubleshooting

### Common Issues

**1. MCP Server Connection Failed**
```
⚠️ Warning: Could not connect to MCP server
```
- Solution: Start R MCP server or run in fallback mode

**2. Parameter Validation Errors**
```
❌ Parameter validation failed: power must be between 0 and 1
```
- Solution: Check parameter ranges in your input

**3. Import Errors**
```
❌ Failed to import required modules
```
- Solution: Install dependencies with `pip install -r requirements_multiagent.txt`

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

calculator = MultiAgentSampleSizeCalculator()
```

## Extensions and Customization

### Adding New Agents

```python
async def custom_agent(self, state: AgentState) -> AgentState:
    """Custom agent for specialized functionality"""
    # Your custom logic here
    return state

# Add to workflow
workflow.add_node("custom_agent", self.custom_agent)
```

### Custom Success Criteria

Extend the `SuccessCriteria` enum:

```python
class SuccessCriteria(str, Enum):
    DISJUNCTIVE_POWER = "DisjunctivePower"
    CONJUNCTIVE_POWER = "ConjunctivePower" 
    WEIGHTED_POWER = "WeightedPower"
    CUSTOM_CRITERIA = "CustomCriteria"  # Your addition
```

### Alternative LLM Models

Replace the LLM:

```python
from langchain_anthropic import ChatAnthropic

calculator.llm = ChatAnthropic(model="claude-3-sonnet")
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

### Development Setup

```bash
pip install -e .
pip install -r requirements_dev.txt
pytest tests/
```

## License

This project builds upon the R SampleSizeMCP.R implementation and follows the same licensing terms.

## Acknowledgments

- Original R implementation for statistical methodology
- LangChain team for the agent framework
- LangGraph team for workflow orchestration
- Clinical trial statisticians for domain expertise

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review example notebooks
3. Check the R MCP server status
4. Verify environment configuration

---

*This multi-agent system represents a significant advancement in computational statistics, combining the precision of R-based calculations with the flexibility and user-friendliness of AI-powered natural language interfaces.*