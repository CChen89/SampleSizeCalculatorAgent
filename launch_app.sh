#!/bin/bash
# Launch Script for Clinical Trial Sample Size Calculator Chainlit App

echo "🧮 Clinical Trial Sample Size Calculator"
echo "======================================"
echo ""

# Check if in correct directory
if [[ ! -f "chainlit_sample_size_app.py" ]]; then
    echo "❌ Error: chainlit_sample_size_app.py not found"
    echo "Please run this script from the RAG directory"
    exit 1
fi

# Check environment
echo "🔍 Environment Check:"

# Check Python environment
if [[ -f "/homes/chencx29/miniconda3/envs/PyRAG/bin/python" ]]; then
    echo "✅ PyRAG environment found"
else
    echo "❌ PyRAG environment not found"
    exit 1
fi

# Check .env file
if [[ -f ".env" ]]; then
    echo "✅ Environment variables configured"
else
    echo "⚠️ .env file not found - some features may be limited"
fi

# Check R server
if curl -s http://127.0.0.1:9291 > /dev/null 2>&1; then
    echo "✅ R MCP server running (full functionality)"
else
    echo "⚠️ R MCP server not detected (fallback mode will be used)"
fi

echo ""
echo "🚀 Starting Chainlit App..."
echo "📍 App URL: http://localhost:8000"
echo "🛑 Press Ctrl+C to stop the app"
echo ""

# Start the chainlit app
/homes/chencx29/miniconda3/envs/PyRAG/bin/chainlit run chainlit_sample_size_app.py \
    --host 0.0.0.0 \
    --port 8000