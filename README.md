# 🧮 Clinical Trial Sample Size Calculator Agent

An AI-powered multi-agent system for clinical trial sample size calculation using LangChain and LangGraph.

## 🎯 Overview

This project transforms sophisticated R-based statistical calculations into a modern, user-friendly AI system that provides:

- **🤖 Multi-Agent Architecture**: 4 specialized AI agents handle different aspects of sample size calculation
- **🌐 Web Interface**: Beautiful Chainlit-based web application
- **📊 Statistical Rigor**: Based on proven R statistical methodology with MCP server integration
- **⚡ Speed**: Professional results in 30-60 seconds vs hours of manual calculation
- **📋 Regulatory Ready**: Comprehensive reports suitable for regulatory submissions

## 🏗️ Architecture

### Multi-Agent System
1. **Parameter Validator Agent**: Extracts and validates trial parameters from natural language
2. **Calculation Agent**: Performs statistical calculations via R MCP server or fallback methods
3. **Visualization Agent**: Creates clinical interpretations and professional reports
4. **Coordinator Agent**: Orchestrates workflow and assembles final results

### Technology Stack
- **Backend**: Python with LangChain/LangGraph
- **AI Model**: Azure OpenAI GPT-4
- **Statistical Engine**: R with MCP (Model Context Protocol) integration
- **Web Interface**: Chainlit framework
- **Workflow**: LangGraph state management

## 🚀 Quick Start

### Option 1: Web Application (Recommended)
```bash
# 1. Install dependencies
pip install -r requirements_multiagent.txt

# 2. Set up environment variables
cp .env.example .env
# Edit .env with your Azure OpenAI credentials

# 3. Launch web app
./launch_app.sh

# 4. Open browser
# Navigate to http://localhost:8000
```

### Option 2: Direct Python Usage
```python
import asyncio
from SampleSizeMultiAgent import MultiAgentSampleSizeCalculator, SampleSizeParameters

# Initialize calculator
calculator = MultiAgentSampleSizeCalculator()

# Define trial parameters
params = SampleSizeParameters(
    power=0.8,
    alpha=0.05,
    drop_rate=0.2,
    arm_names=["Placebo", "Treatment"],
    es_primary=[-0.4],
    # ... other parameters
)

# Run calculation
result = await calculator.run_analysis("Two-arm superiority trial...")
print(result)
```

### Option 3: Command Line Tools
```bash
# Quick calculations
python quick_calculator.py two-arm -0.4 0.8

# Interactive calculator
python my_sample_size_calculator.py

# Jupyter notebook
jupyter notebook MultiAgentSampleSize.ipynb
```

## 📊 Features

### Trial Types Supported
- ✅ **Two-arm superiority trials**
- ✅ **Multi-arm dose-response studies**
- ✅ **Complex multiplicity procedures**
- ✅ **Multiple primary/secondary endpoints**
- ✅ **Graphical procedures for Type I error control**

### Input Methods
- 🌐 **Web interface** with template buttons
- 💬 **Natural language** descriptions
- 📊 **Structured parameters** for programmatic use
- 📓 **Jupyter notebooks** for interactive analysis

### Output Features
- 🎯 **Sample size recommendations**
- 📈 **Statistical power analysis**
- 📄 **Comprehensive clinical reports**
- 💾 **Downloadable documentation**
- 📊 **Parameter sensitivity analysis**

## 🔧 Installation

### Prerequisites
- Python 3.8+
- Conda/Miniconda (recommended)
- Azure OpenAI API access
- R with required packages (optional, for full functionality)

### Setup Steps
```bash
# 1. Clone repository
git clone [repository-url]
cd SampleSizeCalculatorAgent

# 2. Create conda environment
conda create -n sample-size-calc python=3.12
conda activate sample-size-calc

# 3. Install dependencies
pip install -r requirements_multiagent.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your credentials:
# ILIAD_API_KEY=your_azure_openai_key
# ILIAD_URL_BASE=your_azure_openai_endpoint

# 5. Test installation
python -c "from SampleSizeMultiAgent import MultiAgentSampleSizeCalculator; print('✅ Installation successful')"
```

## 📚 Usage Examples

### Web Interface Examples

**Two-Arm Trial:**
```
Arms: Placebo, My_Treatment
Effect size: -0.4
Power: 80%
Dropout: 15%
→ Result: 116 subjects per arm
```

**Three-Arm Dose Response:**
```
Arms: Placebo, 5mg, 10mg
Effect sizes: -0.3, -0.5 vs placebo
Power: 85%
Dropout: 20%
→ Result: Comprehensive dose-response analysis
```

### Natural Language Input
```
"I need sample size for a four-arm dose-finding study with placebo 
and three doses (2.5mg, 5mg, 10mg). Effect sizes should be -0.2, 
-0.35, and -0.5 respectively. I need 85% power with 25% dropout."
```

## 🎯 Results & Performance

### Typical Results
| Trial Type | Effect Size | Power | Result (per arm) |
|-----------|-------------|-------|------------------|
| Two-arm | -0.4 | 80% | ~116 subjects |
| Two-arm | -0.4 | 90% | ~165 subjects |
| Three-arm | -0.33 | 80% | ~180 subjects |
| Four-arm | -0.3 to -0.5 | 85% | ~120-160 subjects |

### Performance Metrics
- ⚡ **Speed**: 30-60 seconds per calculation
- 🎯 **Accuracy**: Validated against R statistical methods
- 📊 **Reliability**: Robust fallback calculations
- 🔄 **Scalability**: Handles 2-10 arm trials

## 🔬 R Integration

The system integrates with R statistical computing for advanced calculations:

### R MCP Server
- Provides full graphical procedure analysis
- Handles complex multiplicity adjustments
- Generates detailed statistical outputs

### Fallback Mode
- Reliable simplified calculations when R server unavailable
- Maintains functionality without external dependencies
- Automatic failover with user notification

## 📋 File Structure

```
SampleSizeCalculatorAgent/
├── README.md                          # This file
├── requirements_multiagent.txt        # Python dependencies
├── .env.example                       # Environment template
│
├── SampleSizeMultiAgent.py           # Core multi-agent system
├── chainlit_sample_size_app.py       # Web application
├── my_sample_size_calculator.py      # Interactive calculator
├── quick_calculator.py               # Command line tool
├── working_example.py                # Direct usage examples
│
├── MultiAgentSampleSize.ipynb        # Jupyter notebook
├── demo_multiagent.py                # Demonstration script
│
├── launch_app.sh                     # Web app launcher
├── start_chainlit_app.py             # Alternative launcher
├── chainlit.md                       # Web app welcome page
├── .chainlit/                        # Chainlit configuration
│
├── USAGE_GUIDE.md                    # Detailed usage instructions
├── CHAINLIT_USAGE_GUIDE.md          # Web app usage guide
├── QUICK_START.md                    # 5-minute tutorial
└── README_MultiAgent.md             # Technical documentation
```

## 🧪 Testing

### Run Tests
```bash
# Test core functionality
python working_example.py

# Test web app components
python demo_multiagent.py

# Test command line tools
python quick_calculator.py two-arm -0.4 0.8
```

### Validation
- ✅ Validated against known statistical methods
- ✅ Compared with manual R calculations
- ✅ Tested across multiple trial designs
- ✅ Verified with clinical trial statisticians

## 🤝 Contributing

### Development Setup
```bash
# 1. Fork repository
# 2. Create feature branch
git checkout -b feature/your-feature

# 3. Install development dependencies
pip install -r requirements_multiagent.txt

# 4. Make changes and test
python -m pytest tests/  # When tests are added

# 5. Submit pull request
```

### Areas for Contribution
- 🧪 **Additional test cases**
- 📊 **New trial design templates**
- 🎨 **Web interface improvements**
- 📚 **Documentation enhancements**
- 🔧 **Performance optimizations**

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋 Support

### Documentation
- [Detailed Usage Guide](USAGE_GUIDE.md)
- [Web App Guide](CHAINLIT_USAGE_GUIDE.md)
- [Quick Start Tutorial](QUICK_START.md)
- [Technical Documentation](README_MultiAgent.md)

### Getting Help
1. Check the documentation files
2. Run example scripts to verify setup
3. Review error messages and troubleshooting guides
4. Open issues for bugs or feature requests

## 🎊 Acknowledgments

- **Statistical Methods**: Based on proven R-based graphical procedures
- **AI Framework**: Built with LangChain and LangGraph
- **Web Interface**: Powered by Chainlit
- **Clinical Expertise**: Developed with input from clinical trial statisticians

---

**Transform your clinical trial design workflow with AI-powered sample size calculations!** 🚀