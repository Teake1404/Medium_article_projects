# Medium_article_projects

This is the source code repo for Medium articles that I am writing.

## 📚 Projects

### 🛒 Ecommerce MCP Server

A flexible Model Context Protocol (MCP) server for e-commerce analytics that integrates with Claude Desktop to provide intelligent campaign analysis and optimization insights.

#### 🚀 Features

- **Flexible Campaign Analysis**: Query campaign data using natural language
- **AI-Powered Insights**: Get intelligent recommendations using Claude AI
- **Multi-Platform Support**: Analyze campaigns across Shopify, Klaviyo, and Google Ads
- **Real-time Optimization**: Get platform-specific optimization suggestions
- **Comprehensive Reporting**: Generate detailed performance reports

#### 📊 Available Data

The MCP server includes sample campaign data with the following metrics:
- **Campaign Performance**: ROAS, revenue, spend, orders, clicks, impressions
- **Platforms**: Shopify, Klaviyo, Google Ads
- **Channels**: Email, social, direct, SMS, CPC, display
- **Creative & Offer Tracking**: Creative IDs and offer IDs for performance analysis

#### 🛠️ Installation

1. **Navigate to the project directory**:
   ```bash
   cd ecommerce_mcp
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Set up environment variables**:
   Create a `.env` file with your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

#### 🎯 Usage

##### Command Line Interface

```bash
# Test the MCP server
uv run mcp_server.py --test

# Generate platform report
uv run mcp_server.py --platform shopify

# Get campaign optimization
uv run mcp_server.py --campaign shopify_001

# Start MCP server for Claude Desktop integration
uv run mcp_server.py
```

##### Claude Desktop Integration

Once connected to Claude Desktop, you can ask questions like:

**📈 Performance Analysis**
- "Show me the top 3 campaigns by ROAS"
- "Which campaigns are underperforming?"
- "Compare platform performance"
- "What's the channel performance breakdown?"

**🤖 AI-Powered Insights**
- "What insights can you find in my campaign data?"
- "Which platform should I invest more in?"
- "How can I improve my overall ROAS?"
- "What patterns do you see in my marketing performance?"

**🔍 Detailed Analytics**
- "Show me email list performance"
- "Analyze creative performance"
- "Find campaigns with high spend but low ROAS"
- "What's the correlation between clicks and revenue?"

#### 🏗️ Architecture

The MCP server provides four main functions:

1. **`platform_report()`**: Generate platform-specific performance reports
2. **`optimize_campaign()`**: Get AI-powered optimization suggestions for specific campaigns
3. **`analyze_campaign_data()`**: Flexible data analysis with keyword recognition
4. **`ai_analysis()`**: Natural language query processing using Claude AI

#### 📁 Project Structure

```
ecommerce_mcp/
├── mcp_server.py          # Main MCP server implementation
├── requirements.txt       # Python dependencies
├── requirements.lock      # Locked dependency versions
├── campaign_data.csv      # Sample campaign data (auto-generated)
├── start_mcp.sh          # Startup script
└── README.md             # This file
```

#### 🔧 Configuration

##### Claude Desktop Setup

1. Add the MCP server to your Claude Desktop configuration:
   ```json
   {
     "mcpServers": {
       "ecommerce-analytics": {
         "command": "uv",
         "args": ["run", "mcp_server.py"],
         "cwd": "/path/to/ecommerce_mcp"
       }
     }
   }
   ```

2. Restart Claude Desktop to load the new MCP server

#### 📊 Sample Data

The server automatically generates sample campaign data if `campaign_data.csv` doesn't exist, including:
- 9 campaigns across 3 platforms
- Realistic performance metrics
- Various UTM sources and email lists
- Creative and offer tracking

---

**Built with ❤️ for e-commerce analytics and AI-powered insights**
