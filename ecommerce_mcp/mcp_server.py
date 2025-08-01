import os
import pandas as pd
from dotenv import load_dotenv
from anthropic import Anthropic
from mcp.server.fastmcp import FastMCP
import json
import sys

# 1. Load environment variables
load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not found in .env file")

# 2. Initialize Claude client (lazy loading)
client = None

def get_claude_client():
    """Lazy load Claude client only when needed"""
    global client
    if client is None:
        try:
            client = Anthropic(api_key=ANTHROPIC_API_KEY)
            print("✅ Claude client initialized successfully")
        except Exception as e:
            print(f"❌ Claude initialization failed: {str(e)}")
            raise e
    return client

# 3. Load campaign data
if not os.path.exists("campaign_data.csv"):
    # If the CSV doesn't exist, generate it
    import numpy as np
    from datetime import datetime, timedelta
    import random

    def generate_platform_data():
        platforms = {
            "shopify": {
                "prefix": "shopify_",
                "utm_sources": ["email", "social", "direct"],
                "email_lists": ["list_a", "list_c", None]
            },
            "klaviyo": {
                "prefix": "klaviyo_",
                "utm_sources": ["sms", "email"],
                "email_lists": ["list_b", "list_d"]
            },
            "google_ads": {
                "prefix": "googleads_",
                "utm_sources": ["cpc", "display"],
                "email_lists": [None]
            }
        }
        data = []
        for platform, config in platforms.items():
            for i in range(1, 4):  # 3 campaigns per platform
                spend = random.randint(200, 1500)
                roas = round(random.uniform(2.5, 5.0), 2)
                revenue = round(spend * roas)
                data.append({
                    "campaign_id": f"{config['prefix']}{i:03d}",
                    "spend": spend,
                    "revenue": revenue,
                    "orders": random.randint(10, 100),
                    "clicks": random.randint(200, 1000),
                    "impressions": random.randint(5000, 30000),
                    "ctr": f"{random.uniform(2.0, 6.0):.2f}%",
                    "cpc": round(spend / random.randint(200, 1000), 2),
                    "roas": roas,
                    "start_date": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
                    "end_date": (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d"),
                    "email_list": random.choice(config["email_lists"]),
                    "creative_id": f"cre_{random.randint(100, 999)}",
                    "offer_id": f"off_{random.randint(100, 999)}",
                    "platform": platform,
                    "utm_source": random.choice(config["utm_sources"])
                })
        return pd.DataFrame(data)

    df = generate_platform_data()
    df.to_csv("campaign_data.csv", index=False)
else:
    df = pd.read_csv("campaign_data.csv")

# 4. Initialize MCP agent
mcp = FastMCP("EcomAI")

@mcp.tool()
def platform_report(platform: str) -> str:
    """Generate platform-specific performance report"""
    # Clean the input - remove whitespace and newlines
    platform = platform.strip()
    
    platform_data = df[df["platform"] == platform]
    
    if platform_data.empty:
        available_platforms = df['platform'].unique()
        return f"""
    ❌ PLATFORM NOT FOUND
    Platform '{platform}' not found in the data.
    
    Available platforms: {', '.join(available_platforms)}
    
    Please use one of the available platform names.
    """
    
    report = f"""
    {platform.upper()} PERFORMANCE
    • Avg ROAS: {platform_data['roas'].mean():.2f}
    • Total Revenue: ${platform_data['revenue'].sum():,.0f}
    • Best Campaign: {platform_data.loc[platform_data['roas'].idxmax()]['campaign_id']}
    """
    return report

@mcp.prompt()
def optimize_campaign(campaign_id: str) -> str:
    """Get Claude's optimization suggestions"""
    # Clean the input - remove whitespace and newlines
    campaign_id = campaign_id.strip()
    
    campaign_data = df[df["campaign_id"] == campaign_id]
    
    if campaign_data.empty:
        available_campaigns = df['campaign_id'].tolist()
        return f"""
    ❌ CAMPAIGN NOT FOUND
    Campaign '{campaign_id}' not found in the data.
    
    Available campaign IDs:
    {', '.join(available_campaigns)}
    
    Please use one of the available campaign IDs.
    """
    
    campaign = campaign_data.iloc[0]
    prompt = f"""
    Campaign {campaign_id} ({campaign['platform']}) Results:
    - Spend: ${campaign['spend']}
    - Revenue: ${campaign['revenue']} (ROAS: {campaign['roas']:.2f})
    - Channel: {campaign['utm_source']}
    Provide 3 platform-specific optimizations.
    """
    claude_client = get_claude_client()
    response = claude_client.messages.create(
        model="claude-sonnet-4-20250514",  # Updated to correct model name
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

@mcp.tool()
def analyze_campaign_data(query: str) -> str:
    """Analyze campaign data based on any user query - flexible and open-ended"""
    try:
        # Clean the input
        query = query.strip().lower()
        
        # Handle different types of queries
        if "top" in query or "best" in query or "highest" in query:
            if "roas" in query:
                top_campaigns = df.nlargest(3, 'roas')[['campaign_id', 'platform', 'roas', 'revenue', 'spend']]
                return f"""
TOP 3 CAMPAIGNS BY ROAS:
{top_campaigns.to_string(index=False)}
                """
            elif "revenue" in query:
                top_campaigns = df.nlargest(3, 'revenue')[['campaign_id', 'platform', 'revenue', 'roas', 'spend']]
                return f"""
TOP 3 CAMPAIGNS BY REVENUE:
{top_campaigns.to_string(index=False)}
                """
            elif "spend" in query:
                top_campaigns = df.nlargest(3, 'spend')[['campaign_id', 'platform', 'spend', 'revenue', 'roas']]
                return f"""
TOP 3 CAMPAIGNS BY SPEND:
{top_campaigns.to_string(index=False)}
                """
            else:
                # Default top analysis
                top_campaigns = df.nlargest(3, 'roas')[['campaign_id', 'platform', 'roas', 'revenue', 'spend']]
                return f"""
TOP 3 CAMPAIGNS BY ROAS (DEFAULT):
{top_campaigns.to_string(index=False)}
                """
        
        elif "platform" in query and ("compare" in query or "summary" in query or "overview" in query):
            platform_summary = df.groupby('platform').agg({
                'spend': 'sum',
                'revenue': 'sum',
                'roas': 'mean',
                'orders': 'sum',
                'clicks': 'sum'
            }).round(2)
            platform_summary['total_roas'] = (platform_summary['revenue'] / platform_summary['spend']).round(2)
            return f"""
PLATFORM COMPARISON:
{platform_summary.to_string()}
                """
        
        elif "channel" in query or "utm_source" in query:
            channel_performance = df.groupby('utm_source').agg({
                'spend': 'sum',
                'revenue': 'sum',
                'roas': 'mean',
                'orders': 'sum'
            }).round(2)
            channel_performance['total_roas'] = (channel_performance['revenue'] / channel_performance['spend']).round(2)
            return f"""
CHANNEL PERFORMANCE:
{channel_performance.to_string()}
                """
        
        elif "email" in query and "list" in query:
            email_list_performance = df[df['email_list'].notna()].groupby('email_list').agg({
                'spend': 'sum',
                'revenue': 'sum',
                'roas': 'mean',
                'orders': 'sum'
            }).round(2)
            if not email_list_performance.empty:
                email_list_performance['total_roas'] = (email_list_performance['revenue'] / email_list_performance['spend']).round(2)
                return f"""
EMAIL LIST PERFORMANCE:
{email_list_performance.to_string()}
                """
            else:
                return "No email list data available."
        
        elif "stats" in query or "summary" in query or "overview" in query:
            total_spend = df['spend'].sum()
            total_revenue = df['revenue'].sum()
            total_orders = df['orders'].sum()
            avg_roas = df['roas'].mean()
            total_campaigns = len(df)
            
            return f"""
CAMPAIGN DATA OVERVIEW:
• Total Campaigns: {total_campaigns}
• Total Spend: ${total_spend:,.0f}
• Total Revenue: ${total_revenue:,.0f}
• Total Orders: {total_orders:,}
• Average ROAS: {avg_roas:.2f}
• Overall ROAS: {total_revenue/total_spend:.2f}
                """
        
        elif "underperforming" in query or "worst" in query or "low" in query:
            if "roas" in query:
                worst_campaigns = df.nsmallest(3, 'roas')[['campaign_id', 'platform', 'roas', 'revenue', 'spend']]
                return f"""
UNDERPERFORMING CAMPAIGNS (LOWEST ROAS):
{worst_campaigns.to_string(index=False)}
                """
            else:
                # Default underperforming analysis
                worst_campaigns = df.nsmallest(3, 'roas')[['campaign_id', 'platform', 'roas', 'revenue', 'spend']]
                return f"""
UNDERPERFORMING CAMPAIGNS (LOWEST ROAS):
{worst_campaigns.to_string(index=False)}
                """
        
        elif "creative" in query or "offer" in query:
            creative_performance = df.groupby('creative_id').agg({
                'spend': 'sum',
                'revenue': 'sum',
                'roas': 'mean'
            }).round(2)
            creative_performance['total_roas'] = (creative_performance['revenue'] / creative_performance['spend']).round(2)
            return f"""
CREATIVE PERFORMANCE:
{creative_performance.to_string()}
                """
        
        else:
            # Default to general data exploration
            return f"""
AVAILABLE DATA ANALYSIS OPTIONS:
• Ask about "top campaigns by ROAS/revenue/spend"
• Request "platform comparison" or "platform summary"
• Query "channel performance" or "utm source analysis"
• Check "email list performance"
• Get "campaign stats" or "overview"
• Find "underperforming campaigns"
• Analyze "creative performance"

CURRENT DATA:
• {len(df)} campaigns across {df['platform'].nunique()} platforms
• Date range: {df['start_date'].min()} to {df['end_date'].max()}
• Total spend: ${df['spend'].sum():,.0f}
• Total revenue: ${df['revenue'].sum():,.0f}

Try asking something specific like "show me top campaigns by ROAS" or "compare platform performance"
                """
    
    except Exception as e:
        return f"Error analyzing data: {str(e)}"
    
    # Final safety check - ensure we always return a string
    return """
CAMPAIGN DATA ANALYSIS HELP:
I couldn't match your query to a specific analysis. Here are some examples you can try:

• "Show me top campaigns by ROAS"
• "Compare platform performance" 
• "Analyze channel performance"
• "Get campaign overview"
• "Find underperforming campaigns"
• "Check email list performance"

Or try the ai_analysis tool for natural language queries!
    """

@mcp.tool()
def ai_analysis(query: str) -> str:
    """Use Claude AI to analyze campaign data based on natural language queries"""
    try:
        # Get a summary of the data for Claude
        data_summary = f"""
CAMPAIGN DATA SUMMARY:
• Total campaigns: {len(df)}
• Platforms: {', '.join(df['platform'].unique())}
• Date range: {df['start_date'].min()} to {df['end_date'].max()}
• Total spend: ${df['spend'].sum():,.0f}
• Total revenue: ${df['revenue'].sum():,.0f}
• Average ROAS: {df['roas'].mean():.2f}

TOP PERFORMING CAMPAIGNS:
{df.nlargest(3, 'roas')[['campaign_id', 'platform', 'roas', 'revenue', 'spend']].to_string(index=False)}

PLATFORM SUMMARY:
{df.groupby('platform').agg({'spend': 'sum', 'revenue': 'sum', 'roas': 'mean'}).round(2).to_string()}

CHANNEL PERFORMANCE:
{df.groupby('utm_source').agg({'spend': 'sum', 'revenue': 'sum', 'roas': 'mean'}).round(2).to_string()}
        """
        
        prompt = f"""
You are an e-commerce analytics expert. Analyze this campaign data and answer the user's question.

{data_summary}

USER QUESTION: {query}

Please provide:
1. A clear, actionable answer to their question
2. Specific insights from the data
3. Recommendations if applicable
4. Any relevant metrics or comparisons

Keep your response concise but comprehensive.
        """
        
        claude_client = get_claude_client()
        response = claude_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    
    except Exception as e:
        return f"Error in AI analysis: {str(e)}"

def process_command(command):
    """Handle incoming MCP commands"""
    try:
        if command.get("prompt") == "platform_report":
            result = platform_report(command["args"]["platform"])
        elif command.get("prompt") == "optimize_campaign":
            result = optimize_campaign(command["args"]["campaign_id"])
        elif command.get("prompt") == "analyze_campaign_data":
            result = analyze_campaign_data(command["args"]["query"])
        elif command.get("prompt") == "ai_analysis":
            result = ai_analysis(command["args"]["query"])
        else:
            result = {"error": "Unknown command"}
        return json.dumps({"result": result})
    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    print("🟢 MCP Server Starting...")
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            # Test mode with default values
            print(platform_report("shopify"))
            print(optimize_campaign("shopify_001"))
        elif sys.argv[1] == "--platform" and len(sys.argv) > 2:
            # Platform report mode
            platform = sys.argv[2]
            print(platform_report(platform))
        elif sys.argv[1] == "--campaign" and len(sys.argv) > 2:
            # Campaign optimization mode
            campaign_id = sys.argv[2]
            print(optimize_campaign(campaign_id))
        elif sys.argv[1] == "--help":
            # Help mode
            print("""
Usage: uv run mcp_server.py [OPTIONS]

Options:
  --test                    Run with default test values (shopify platform, shopify_001 campaign)
  --platform PLATFORM       Generate platform report for specified platform (e.g., shopify, klaviyo, google_ads)
  --campaign CAMPAIGN_ID    Get optimization suggestions for specified campaign ID (e.g., shopify_001, klaviyo_002)
  --help                    Show this help message
  (no args)                 Start MCP server in stdio mode for integration

Examples:
  uv run mcp_server.py --platform shopify
  uv run mcp_server.py --campaign klaviyo_001
  uv run mcp_server.py --test
  uv run mcp_server.py
            """)
        else:
            print("❌ Invalid arguments. Use --help for usage information.")
    else:
        # Standard MCP operation
        try:
            mcp.run(transport='stdio')
        except (BrokenPipeError, ValueError):
            # Handle graceful shutdown when stdin/stdout are closed
            pass
    
    # Only print if we're not in stdio mode
    if len(sys.argv) > 1:
        print("🔴 MCP Server Stopped")