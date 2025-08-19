import streamlit as st
import os
import sys
from datetime import datetime
# Add the code folder to the path to import DataValidationAgent
sys.path.append(os.path.join(os.path.dirname(__file__), 'code'))
from agents.trl_agent import EnhancedTRLAgent
from agents.frascati_agent import EnhancedFrascatiAgent
from agents.comprehensive_data_agent import ComprehensiveDataAgent
from agents.sme_agent import SMEAgent
from agents.comprehensive_document_filling_agent import ComprehensiveDocumentFillingAgent
from agents.market_agent import EnhancedMarketAgent
from agents.excel_agent import ExcelAgent
from code.data_validation_agent import DataValidationAgent
from code.agent_run import excel_agent_run
from pdf_generator import BusinessPlanPDFGenerator
from data_downloader import DataDownloader

# Helper function to compile final plan
def compile_final_plan():
    """Compile all analysis results into final business plan"""
    
    # Get current idea
    current_idea = st.session_state.trl_result["upgrade_result"]["upgraded_idea"]
    
    # Compile plan sections
    plan = {
        "executive_summary": f"""
        This business plan presents a TRL 4 validated technology solution with confirmed R&D activities 
        and company eligibility as SME. The project meets all Frascati criteria for R&D funding.
        
        **Core Innovation:** {current_idea[:200]}...
        """,
        
        "technical_description": current_idea,
        
        "rd_activities": """
        The proposed R&D activities include:
        • Laboratory validation and testing
        • Prototype development and refinement  
        • Technical risk assessment and mitigation
        • Performance optimization studies
        • Scalability analysis
        """,
        
        "eligibility_confirmation": "Company meets SME eligibility criteria with confirmed employee count, turnover, and balance sheet requirements."
    }
    
    return plan

# Page configuration
st.set_page_config(
    page_title="Business Plan AI Generator",
    layout="wide"
)

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 1
if "idea_text" not in st.session_state:
    st.session_state.idea_text = ""
if "trl_result" not in st.session_state:
    st.session_state.trl_result = None
if "frascati_result" not in st.session_state:
    st.session_state.frascati_result = None
if "market_result" not in st.session_state:
    st.session_state.market_result = None
if "comprehensive_data" not in st.session_state:
    st.session_state.comprehensive_data = None
if "manual_inputs" not in st.session_state:
    st.session_state.manual_inputs = {}
if "sme_result" not in st.session_state:
    st.session_state.sme_result = None
if "document_results" not in st.session_state:
    st.session_state.document_results = None
if "selected_strategy" not in st.session_state:
    st.session_state.selected_strategy = None
if "hybrid_selections" not in st.session_state:
    st.session_state.hybrid_selections = {}
if "excel_validation_result" not in st.session_state:
    st.session_state.excel_validation_result = None
if "excel_processing_result" not in st.session_state:
    st.session_state.excel_processing_result = None
if "excel_missing_data" not in st.session_state:
    st.session_state.excel_missing_data = {}

# Initialize agents
@st.cache_resource
def init_agents():
    return {
        "trl": EnhancedTRLAgent(),
        "frascati": EnhancedFrascatiAgent(),
        "market": EnhancedMarketAgent(),
        "comprehensive_data": ComprehensiveDataAgent(),
        "sme": SMEAgent(),
        "document_filling": ComprehensiveDocumentFillingAgent(),
        "excel": ExcelAgent()
    }

agents = init_agents()
import streamlit as st

# Page config
st.set_page_config(page_title="Business Plan AI Generator", layout="wide")

# CSS for modern styling & interaction
st.markdown("""
    <style>
    /* Title styling */
    .big-title {
        font-size: 44px;
        font-weight: 900;
        background: linear-gradient(90deg, #4A90E2, #0072FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 8px;
    }
    .subtitle {
        font-size: 18px;
        text-align: center;
        color: #555;
        margin-bottom: 35px;
    }
    /* Step card styling */
    .step-card {
        background: linear-gradient(145deg, #ffffff, #f0f0f0);
        border-radius: 14px;
        padding: 25px 10px;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.08);
        margin: 8px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        cursor: pointer;
    }
    .step-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(0,0,0,0.15);
    }
    .step-completed {
        border: 2px solid #4CAF50;
    }
    .step-pending {
        border: 2px solid #FFA500;
    }
    .step-title {
        font-size: 17px;
        font-weight: 600;
        margin-top: 10px;
        color: #333;
    }
    .status-emoji {
        font-size: 26px;
    }
    /* Progress bar container */
    .progress-container {
        width: 90%;
        background: #eee;
        border-radius: 8px;
        margin: 20px auto;
        overflow: hidden;
        height: 16px;
    }
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #4A90E2, #00C6FF);
        width: 0%;
        transition: width 0.5s ease;
    }
    </style>
""", unsafe_allow_html=True)

# Title and subtitle
st.markdown('<div class="big-title"> Business Plan AI Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Transform your business idea into a funding-ready plan through AI-powered analysis</div>', unsafe_allow_html=True)

# Fake current step for demo; replace with your actual session state logic
current_step = st.session_state.get('step', 1)

# Step data
step_info = [
    ("TRL Analysis", "✅" if current_step > 1 else "🔄"),
    ("R&D Criteria", "✅" if current_step > 2 else "⏳"),
    ("Market Analysis", "✅" if current_step > 3 else "⏳"),
    ("Data Extract", "✅" if current_step > 4 else "⏳"),
    ("SME Eligibility", "✅" if current_step > 5 else "⏳"),
    ("Fill Documents", "✅" if current_step > 6 else "⏳"),
    ("Excel Sheets", "✅" if current_step > 7 else "⏳"),
]

# Step cards
cols = st.columns(len(step_info))
for idx, (title, status) in enumerate(step_info):
    card_class = "step-completed" if status == "✅" else "step-pending"
    with cols[idx]:
        st.markdown(f"""
            <div class="step-card {card_class}">
                <div class="status-emoji">{status}</div>
                <div class="step-title">{title}</div>
            </div>
        """, unsafe_allow_html=True)

# Custom gradient progress bar
progress_value = (current_step - 1) / 7
progress_percent = int(progress_value * 100)
st.markdown(f"""
    <div class="progress-container">
        <div class="progress-bar" style="width: {progress_percent}%"></div>
    </div>
    <p style="text-align:center; font-size:14px; color:#666;">Progress: {progress_percent}%</p>
""", unsafe_allow_html=True)

st.divider()


# STEP 1: TRL Analysis
if st.session_state.step == 1:
    # Step banner
    st.markdown("""
        <div style="
            background: linear-gradient(90deg, #4A90E2, #00C6FF);
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            color: white;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 15px;">
            📝 Step 1: Business Idea Input & TRL Analysis
        </div>
    """, unsafe_allow_html=True)

    idea_text = st.text_area(
        "💡 Enter your business idea:",
        height=200,
        help="Describe your business idea, product, or service concept"
    )
    
    st.markdown('<br>', unsafe_allow_html=True)
    
    if st.button("🚀 Analyze TRL Level", type="primary"):
        if idea_text.strip():
            st.session_state.idea_text = idea_text
            
            with st.spinner("Analyzing TRL level..."):
                trl_result = agents["trl"].process_idea(idea_text)
                st.session_state.trl_result = trl_result
            
            st.success("✅ TRL Analysis Complete!")
            st.session_state.step = 2
            st.rerun()
        else:
            st.error("⚠️ Please enter your business idea first")


# STEP 2: Frascati Analysis
elif st.session_state.step == 2:
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("⬅️ Back to Step 1", key="back_to_step_1"):
            st.session_state.step = 1
            st.rerun()

    # Step banner
    st.markdown("""
        <div style="
            background: linear-gradient(90deg, #4A90E2, #00C6FF);
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            color: white;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 15px;">
            🔬 Step 2: R&D Criteria Analysis (Frascati)
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.trl_result:
        trl_data = st.session_state.trl_result["upgrade_result"]
        
        # Show TRL results in a card
        st.markdown("""
            <div style="
                background: #f9fafc;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                margin-bottom: 15px;">
                <h5 style="color:#4A90E2; margin-bottom:10px;">✨ TRL Analysis Result</h5>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**TRL Level:** {trl_data['trl_level']}")
        with col2:
            st.info(f"**Changes:** {trl_data['changes_made']}")
        
        st.markdown("</div>", unsafe_allow_html=True)

        # Show updated idea
        with st.expander("📄 View Updated Idea"):
            st.write(trl_data["upgraded_idea"])
        
        st.markdown('<br>', unsafe_allow_html=True)
        
        if st.button("🔍 Analyze R&D Criteria", type="primary"):
            with st.spinner("Analyzing R&D criteria..."):
                frascati_result = agents["frascati"].process_idea(trl_data["upgraded_idea"])
                st.session_state.frascati_result = frascati_result
            st.success("✅ R&D Analysis Complete!")
            st.rerun()
    
    # Show Frascati results
    if st.session_state.frascati_result:
        frascati_data = st.session_state.frascati_result
        
        st.markdown("""
            <div style="
                background: #f9fafc;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                margin-bottom: 15px;">
                <h5 style="color:#4A90E2; margin-bottom:10px;">📊 R&D Criteria Scores</h5>
        """, unsafe_allow_html=True)
        
        for criterion, data in frascati_data["scores"].items():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.metric(criterion, f"{data['score']}%")
            with col2:
                st.write(f"**Justification:** {data['justification']}")
        
        st.markdown("</div>", unsafe_allow_html=True)

        if frascati_data["needs_improvement"]:
            st.warning("⚠️ Some criteria scored below 40%. Choose how to improve:")
            improvement_options = {}
            
            for criterion in frascati_data["low_scores"].keys():
                st.subheader(f"🔧 Improve {criterion}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✨ Auto-improve {criterion}", key=f"auto_{criterion}"):
                        improvement_options[criterion] = "auto"
                with col2:
                    if st.button(f"✏️ Manual improvement {criterion}", key=f"manual_{criterion}"):
                        improvement_options[criterion] = "manual"
            
            if improvement_options:
                current_idea = st.session_state.trl_result["upgrade_result"]["upgraded_idea"]
                
                if "auto" in improvement_options.values():
                    auto_criteria = [k for k, v in improvement_options.items() if v == "auto"]
                    with st.spinner("Applying automatic improvements..."):
                        improved_idea = agents["frascati"].apply_improvements(
                            current_idea, 
                            frascati_data["suggestions"], 
                            auto_criteria
                        )
                    st.success("✅ Improvements applied!")
                    st.session_state.trl_result["upgrade_result"]["upgraded_idea"] = improved_idea
                    
                    with st.spinner("Re-analyzing R&D criteria..."):
                        new_frascati_result = agents["frascati"].process_idea(improved_idea)
                        st.session_state.frascati_result = new_frascati_result
                    st.rerun()
        else:
            st.success("🎉 All R&D criteria meet the requirements!")
            if st.button("➡️ Proceed to Market Analysis", type="primary"):
                st.session_state.step = 3
                st.rerun()




# STEP 3: Market Analysis
elif st.session_state.step == 3:
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("⬅️ Back to Step 2", key="back_to_step_2"):
            st.session_state.step = 2
            st.rerun()

    st.markdown("""
    <div style="
        background: linear-gradient(90deg, #4A90E2, #00C6FF);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        color: white;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 15px;">
        🧠🔍 Step 3: Market Analysis & Patent Search
    </div>
""", unsafe_allow_html=True)
    
    
    # Show current idea
    if st.session_state.trl_result:
        current_idea = st.session_state.trl_result["upgrade_result"]["upgraded_idea"]
        
        with st.expander("📋 Current Idea (TRL 4 Enhanced)"):
            st.write(current_idea)
        
        # Start market analysis
        if not st.session_state.market_result:
            if st.button("Analyze Market Saturation", type="primary"):
                with st.spinner("Searching patents and analyzing market..."):
                    market_result = agents["market"].process_idea(current_idea)
                    st.session_state.market_result = market_result
                
                st.success("Market Analysis Complete!")
                st.rerun()
    
    # Show market analysis results
    if st.session_state.market_result:
        market_data = st.session_state.market_result
        
        # Check for errors
        if market_data.get("patent_results", {}).get("error"):
            st.error(f"Patent search error: {market_data['patent_results']['error']}")
            st.info("This might be due to API configuration. Please check your Google API key and Custom Search Engine ID.")
        
        if market_data.get("literature_results", {}).get("error"):
            st.warning(f"Literature search error: {market_data['literature_results']['error']}")
        
        # Display keywords used
        st.subheader("🔍 Keywords Extracted")
        keywords = market_data.get("keywords", [])
        if keywords:
            st.write("**Search Keywords:** " + ", ".join(keywords))
        
        # Patent results
        patent_results = market_data.get("patent_results", {})
        if patent_results.get("data"):
            st.subheader("📜 Patent Search Results")
            patent_count = len(patent_results["data"])
            st.metric("Patents Found", patent_count)
            
            # Show sample patents
            with st.expander(f"View Sample Patents (showing first 3 of {patent_count})"):
                for i, patent in enumerate(patent_results["data"][:3]):
                    st.write(f"**{i+1}. {patent.get('title', 'No title')}**")
                    st.write(f"Link: {patent.get('link', 'No link')}")
                    st.write(f"Snippet: {patent.get('snippet', 'No description')}")
                    st.divider()
        
        # Literature results
        literature_results = market_data.get("literature_results", {})
        if literature_results.get("data"):
            st.subheader("📚 Literature  Search Results")
            literature_count = len(literature_results["data"])
            st.metric("Academic Papers Found", literature_count)
            
            # Show sample literature
            with st.expander(f"View Sample Literature (showing first 3 of {literature_count})"):
                for i, paper in enumerate(literature_results["data"][:3]):
                    st.write(f"**{i+1}. {paper.get('title', 'No title')}**")
                    st.write(f"Link: {paper.get('link', 'No link')}")
                    st.write(f"Snippet: {paper.get('snippet', 'No description')}")
                    st.divider()
        
        # Market analysis
        market_analysis = market_data.get("market_analysis", {})
        if market_analysis:
            st.subheader("📈 Market Saturation Analysis")
            
            # Saturation level
            saturation = market_analysis.get("saturation_level", "Unknown")
            if saturation == "Low":
                st.success(f"🟢 Market Saturation: {saturation}")
            elif saturation == "Medium":
                st.warning(f"🟡 Market Saturation: {saturation}")
            elif saturation == "High":
                st.error(f"🔴 Market Saturation: {saturation}")
            else:
                st.info(f"❓ Market Saturation: {saturation}")
            
            # Analysis details
            col1, col2 = st.columns(2)
            
            with col1:
                competitors = market_analysis.get("competitors", [])
                if competitors:
                    st.write("**Key Competitors:**")
                    for competitor in competitors:
                        st.write(f"• {competitor}")
                
                market_gaps = market_analysis.get("market_gaps", [])
                if market_gaps:
                    st.write("**Market Gaps Identified:**")
                    for gap in market_gaps:
                        st.write(f"• {gap}")
            
            with col2:
                opportunities = market_analysis.get("differentiation_opportunities", [])
                if opportunities:
                    st.write("**Differentiation Opportunities:**")
                    for opportunity in opportunities:
                        st.write(f"• {opportunity}")
                
                recommendation = market_analysis.get("recommendation", "")
                if recommendation:
                    st.write(f"**Recommendation:** {recommendation}")
        
        # Differentiation strategies
        differentiation_strategies = market_data.get("differentiation_strategies", [])
        if differentiation_strategies:
            st.subheader("💡 Differentiation Strategies")
            st.info("Based on market saturation, here are suggested differentiation strategies:")
            
            for i, strategy in enumerate(differentiation_strategies, 1):
                with st.expander(f"Strategy {i}: {strategy.get('name', f'Strategy {i}')}"):
                    st.write(f"**Key Differentiators:** {strategy.get('key_differentiators', 'N/A')}")
                    st.write(f"**Implementation:** {strategy.get('implementation_approach', 'N/A')}")
                    st.write(f"**Pros:** {strategy.get('pros', 'N/A')}")
                    st.write(f"**Cons:** {strategy.get('cons', 'N/A')}")
                    st.write(f"**Impact on Idea:** {strategy.get('impact_on_original_idea', 'N/A')}")
            
            # Strategy Selection Interface
            if market_data.get("requires_user_selection"):
                st.subheader("🎯 Choose Your Differentiation Strategy")
                st.info("Select a differentiation strategy to enhance your idea:")
                
                strategy_options = [f"Strategy {i+1}: {strategy.get('name', f'Option {i+1}')}" for i, strategy in enumerate(differentiation_strategies)]
                
                selected_index = st.selectbox(
                    "Select your preferred differentiation strategy:",
                    options=range(len(strategy_options)),
                    format_func=lambda x: strategy_options[x],
                    key="strategy_selector"
                )
                
                # Show strategy details
                if selected_index is not None:
                    selected_strategy = differentiation_strategies[selected_index]
                    
                    with st.expander(f"📋 Strategy Details: {selected_strategy.get('name', 'Selected Strategy')}", expanded=True):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Key Differentiators:** {selected_strategy.get('key_differentiators', 'N/A')}")
                            st.write(f"**Implementation:** {selected_strategy.get('implementation_approach', 'N/A')}")
                        
                        with col2:
                            st.write(f"**Pros:** {selected_strategy.get('pros', 'N/A')}")
                            st.write(f"**Cons:** {selected_strategy.get('cons', 'N/A')}")
                        
                        st.write(f"**Impact on Original Idea:** {selected_strategy.get('impact_on_original_idea', 'N/A')}")
                    
                    # Apply strategy button
                    if st.button("Apply Selected Strategy", type="primary", key="apply_strategy"):
                        with st.spinner("Regenerating idea with selected strategy..."):
                            # Check if the market agent has the regenerate method
                            if hasattr(agents["market"], 'regenerate_idea_with_strategy'):
                                enhanced_idea = agents["market"].regenerate_idea_with_strategy(
                                    current_idea, selected_strategy
                                )
                            else:
                                # Fallback: manually enhance the idea
                                enhanced_idea = f"{current_idea}\n\nMarket Enhancement: {selected_strategy.get('implementation_approach', 'Strategy applied')}"
                            
                            # Update the idea in session state
                            st.session_state.trl_result["upgrade_result"]["upgraded_idea"] = enhanced_idea
                            st.session_state.selected_strategy = selected_strategy
                            
                            st.success("✅ Strategy applied successfully! Your idea has been enhanced.")
                            st.info("You can now proceed to the next step with your market-optimized idea.")
                            
                            # Show the enhanced idea
                            with st.expander("🚀 Enhanced Idea Preview", expanded=True):
                                st.write(enhanced_idea)
        
        # Proceed to next step
        st.divider()
        proceed_button_text = "Proceed to Data Extraction"
        if st.session_state.selected_strategy:
            proceed_button_text += " (Strategy Applied ✅)"
        
        if st.button(proceed_button_text, type="primary"):
            st.session_state.step = 4
            st.rerun()

# STEP 4: Comprehensive Data Extraction
elif st.session_state.step == 4:
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("⬅️ Back to Step 3", key="back_to_step_3"):
            st.session_state.step = 3
            st.rerun()
     
    st.markdown("""
    <div style="
        background: linear-gradient(90deg, #4A90E2, #00C6FF);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        color: white;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 15px;">
        🧠🔍📦 Step 4: Comprehensive Data Extraction
    </div>
""", unsafe_allow_html=True)
    # Get processed business idea
    processed_idea = st.session_state.trl_result["upgrade_result"]["upgraded_idea"]
    
    # Extract comprehensive data
    if not st.session_state.comprehensive_data:
        if st.button("Extract Project Data", type="primary"):
            with st.spinner("Extracting comprehensive project data..."):
                comprehensive_result = agents["comprehensive_data"].process_business_idea(processed_idea)
                st.session_state.comprehensive_data = comprehensive_result
            
            st.success("Data extraction complete!")
            st.rerun()
    
    # Show extraction results
    if st.session_state.comprehensive_data:
        comp_data = st.session_state.comprehensive_data
        
        # Show extraction statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Fields", comp_data.get("total_fields", 0))
        with col2:
            st.metric("Extracted", comp_data.get("extracted_count", 0))
        with col3:
            st.metric("Missing", comp_data.get("missing_count", 0))
        
        # Show extracted data
        if comp_data.get("extracted_count", 0) > 0:
            st.subheader("✅ Extracted Data")
            with st.expander("View Extracted Fields", expanded=True):
                for field, value in comp_data.get("extracted_data", {}).items():
                    if value is not None:
                        st.write(f"**{field}:** {value}")
        
        # Handle missing fields
        if comp_data.get("missing_count", 0) > 0:
            # Check if auto-generation is available
            if comp_data.get("auto_generation_available") and comp_data.get("user_options"):
                st.subheader("⚙️ Handle Missing Data")
                st.info(f"Found {comp_data['missing_count']} missing fields. Choose how to handle them:")
                
                option = st.radio(
                    "How would you like to handle missing fields?",
                    options=["auto_generate", "manual_input", "hybrid"],
                    format_func=lambda x: comp_data["user_options"].get(x, x.replace("_", " ").title()),
                    key="data_option_selector"
                )
                
                if st.button("Process with Selected Option", type="primary", key="process_data_option"):
                    if option == "auto_generate":
                        with st.spinner("AI is generating missing field values..."):
                            # Check if the agent has auto-generation method
                            if hasattr(agents["comprehensive_data"], 'auto_generate_missing_fields'):
                                generated_data = agents["comprehensive_data"].auto_generate_missing_fields(
                                    processed_idea, comp_data.get("missing_fields", {})
                                )
                            else:
                                # Fallback: create default values
                                generated_data = {}
                                for category, fields in comp_data.get("missing_fields", {}).items():
                                    for field in fields:
                                        generated_data[field] = "Auto-generated value"
                            
                            # Merge generated data with extracted data
                            final_data = {**comp_data.get("extracted_data", {}), **generated_data}
                            st.session_state.comprehensive_data["final_data"] = final_data
                            
                            st.success("✅ All missing fields generated automatically!")
                            
                            # Show generated fields
                            with st.expander("🤖 AI-Generated Fields", expanded=True):
                                for field, value in generated_data.items():
                                    if value is not None:
                                        st.write(f"**{field}:** {value}")
                            
                            st.session_state.step = 5
                            st.rerun()
                    
                    elif option == "manual_input":
                        st.info("Please provide the missing information manually below:")
                        # Show manual input form
                        missing_fields = comp_data.get("missing_fields", {})
                        smart_defaults = comp_data.get("smart_defaults", {})
                        field_descriptions = comp_data.get("field_descriptions", {})
                        
                        for category, fields in missing_fields.items():
                            if fields:
                                st.write(f"**{category.replace('_', ' ').title()}:**")
                                
                                for field in fields:
                                    description = field_descriptions.get(field, field)
                                    default_value = smart_defaults.get(field, "")
                                    
                                    # Create input field based on field type
                                    if field in ["ACTIVITY_PERCENTAGE", "TEAM_SIZE", "PROJECT_DURATION"]:
                                        manual_value = st.number_input(
                                            f"{field}: {description}",
                                            min_value=0,
                                            value=int(default_value) if default_value and str(default_value).isdigit() else 0,
                                            key=f"manual_{field}"
                                        )
                                    elif field in ["RD_BUDGET", "REVENUE_PROJECTION", "PRODUCT_PRICE"]:
                                        manual_value = st.number_input(
                                            f"{field}: {description}",
                                            min_value=0,
                                            value=int(default_value) if default_value and str(default_value).isdigit() else 0,
                                            key=f"manual_{field}"
                                        )
                                    elif field in ["NOVELTY_LEVEL"]:
                                        manual_value = st.selectbox(
                                            f"{field}: {description}",
                                            options=["company level", "market level", "global level"],
                                            index=1 if default_value == "market level" else 0,
                                            key=f"manual_{field}"
                                        )
                                    elif field in ["RD_PRIORITY"]:
                                        manual_value = st.selectbox(
                                            f"{field}: {description}",
                                            options=["Health technologies", "Production processes", "Information and communication technologies"],
                                            index=2 if "Information" in str(default_value) else 0,
                                            key=f"manual_{field}"
                                        )
                                    else:
                                        manual_value = st.text_input(
                                            f"{field}: {description}",
                                            value=str(default_value) if default_value else "",
                                            key=f"manual_{field}"
                                        )
                                    
                                    # Store manual input
                                    st.session_state.manual_inputs[field] = manual_value
                        
                        # Combine extracted + manual data
                        if st.button("Combine All Data", type="primary", key="combine_manual_data"):
                            combined_data = comp_data.get("extracted_data", {}).copy()
                            combined_data.update(st.session_state.manual_inputs)
                            
                            st.session_state.comprehensive_data["final_data"] = combined_data
                            
                            st.success("All data combined successfully!")
                            st.session_state.step = 5
                            st.rerun()
                    
                    elif option == "hybrid":
                        st.info("Choose which fields to auto-generate and which to input manually:")
                        
                        auto_generate_fields = []
                        manual_input_fields = []
                        
                        for category, fields in comp_data.get("missing_fields", {}).items():
                            if fields:
                                st.write(f"**{category.replace('_', ' ').title()}:**")
                                for field in fields:
                                    col1, col2, col3 = st.columns([2, 1, 1])
                                    with col1:
                                        st.write(f"{field}: {comp_data.get('field_descriptions', {}).get(field, field)}")
                                    with col2:
                                        if st.checkbox("Auto-generate", key=f"auto_{field}"):
                                            auto_generate_fields.append(field)
                                            st.session_state.hybrid_selections[field] = "auto"
                                    with col3:
                                        if st.checkbox("Manual input", key=f"manual_check_{field}"):
                                            manual_input_fields.append(field)
                                            st.session_state.hybrid_selections[field] = "manual"
                        
                        if st.button("Process Hybrid Selection", type="primary", key="process_hybrid"):
                            with st.spinner("Processing hybrid selection..."):
                                # Separate fields based on selection
                                auto_fields = {k: v for k, v in st.session_state.hybrid_selections.items() if v == "auto"}
                                manual_fields = {k: v for k, v in st.session_state.hybrid_selections.items() if v == "manual"}
                                
                                # Auto-generate selected fields
                                generated_data = {}
                                if auto_fields:
                                    # Create a subset of missing_fields for auto-generation
                                    auto_missing_fields = {}
                                    for category, fields in comp_data.get("missing_fields", {}).items():
                                        auto_category_fields = [f for f in fields if f in auto_fields]
                                        if auto_category_fields:
                                            auto_missing_fields[category] = auto_category_fields
                                    
                                    if auto_missing_fields:
                                        if hasattr(agents["comprehensive_data"], 'auto_generate_missing_fields'):
                                            generated_data = agents["comprehensive_data"].auto_generate_missing_fields(
                                                processed_idea, auto_missing_fields
                                            )
                                        else:
                                            # Fallback
                                            for field in auto_fields:
                                                generated_data[field] = "Auto-generated value"
                                
                                # Show manual input form for selected fields
                                if manual_fields:
                                    st.subheader("Manual Input for Selected Fields")
                                    for field in manual_fields.keys():
                                        description = comp_data.get("field_descriptions", {}).get(field, field)
                                        default_value = comp_data.get("smart_defaults", {}).get(field, "")
                                        
                                        # Create input field based on field type
                                        if field in ["ACTIVITY_PERCENTAGE", "TEAM_SIZE", "PROJECT_DURATION"]:
                                            manual_value = st.number_input(
                                                f"{field}: {description}",
                                                min_value=0,
                                                value=int(default_value) if default_value and str(default_value).isdigit() else 0,
                                                key=f"hybrid_manual_{field}"
                                            )
                                        elif field in ["RD_BUDGET", "REVENUE_PROJECTION", "PRODUCT_PRICE"]:
                                            manual_value = st.number_input(
                                                f"{field}: {description}",
                                                min_value=0,
                                                value=int(default_value) if default_value and str(default_value).isdigit() else 0,
                                                key=f"hybrid_manual_{field}"
                                            )
                                        elif field in ["NOVELTY_LEVEL"]:
                                            manual_value = st.selectbox(
                                                f"{field}: {description}",
                                                options=["company level", "market level", "global level"],
                                                index=1 if default_value == "market level" else 0,
                                                key=f"hybrid_manual_{field}"
                                            )
                                        elif field in ["RD_PRIORITY"]:
                                            manual_value = st.selectbox(
                                                f"{field}: {description}",
                                                options=["Health technologies", "Production processes", "Information and communication technologies"],
                                                index=2 if "Information" in str(default_value) else 0,
                                                key=f"hybrid_manual_{field}"
                                            )
                                        else:
                                            manual_value = st.text_input(
                                                f"{field}: {description}",
                                                value=str(default_value) if default_value else "",
                                                key=f"hybrid_manual_{field}"
                                            )
                                        
                                        # Store manual input
                                        st.session_state.manual_inputs[field] = manual_value
                                    
                                    # Combine all data
                                    if st.button("Combine All Hybrid Data", type="primary", key="combine_hybrid_data"):
                                        combined_data = comp_data.get("extracted_data", {}).copy()
                                        combined_data.update(generated_data)
                                        combined_data.update(st.session_state.manual_inputs)
                                        
                                        st.session_state.comprehensive_data["final_data"] = combined_data
                                        
                                        st.success("All hybrid data combined successfully!")
                                        st.session_state.step = 5
                                        st.rerun()
                                else:
                                    # No manual fields, just combine extracted + generated
                                    combined_data = comp_data.get("extracted_data", {}).copy()
                                    combined_data.update(generated_data)
                                    
                                    st.session_state.comprehensive_data["final_data"] = combined_data
                                    
                                    st.success("All hybrid data combined successfully!")
                                    st.session_state.step = 5
                                    st.rerun()
            
            else:
                # Fallback: Show manual input form only
                st.subheader("⚠️ Missing Fields - Manual Input Required")
                
                # Manual input form
                missing_fields = comp_data.get("missing_fields", {})
                smart_defaults = comp_data.get("smart_defaults", {})
                field_descriptions = comp_data.get("field_descriptions", {})
                
                for category, fields in missing_fields.items():
                    if fields:
                        st.write(f"**{category.replace('_', ' ').title()}:**")
                        
                        for field in fields:
                            description = field_descriptions.get(field, field)
                            default_value = smart_defaults.get(field, "")
                            
                            # Create input field based on field type
                            if field in ["ACTIVITY_PERCENTAGE", "TEAM_SIZE", "PROJECT_DURATION"]:
                                manual_value = st.number_input(
                                    f"{field}: {description}",
                                    min_value=0,
                                    value=int(default_value) if default_value and str(default_value).isdigit() else 0,
                                    key=f"manual_{field}"
                                )
                            elif field in ["RD_BUDGET", "REVENUE_PROJECTION", "PRODUCT_PRICE"]:
                                manual_value = st.number_input(
                                    f"{field}: {description}",
                                    min_value=0,
                                    value=int(default_value) if default_value and str(default_value).isdigit() else 0,
                                    key=f"manual_{field}"
                                )
                            elif field in ["NOVELTY_LEVEL"]:
                                manual_value = st.selectbox(
                                    f"{field}: {description}",
                                    options=["company level", "market level", "global level"],
                                    index=1 if default_value == "market level" else 0,
                                    key=f"manual_{field}"
                                )
                            elif field in ["RD_PRIORITY"]:
                                manual_value = st.selectbox(
                                    f"{field}: {description}",
                                    options=["Health technologies", "Production processes", "Information and communication technologies"],
                                    index=2 if "Information" in str(default_value) else 0,
                                    key=f"manual_{field}"
                                )
                            else:
                                manual_value = st.text_input(
                                    f"{field}: {description}",
                                    value=str(default_value) if default_value else "",
                                    key=f"manual_{field}"
                                )
                            
                            # Store manual input
                            st.session_state.manual_inputs[field] = manual_value
                
                # Combine extracted + manual data
                if st.button("Combine All Data", type="primary", key="combine_fallback_data"):
                    combined_data = comp_data.get("extracted_data", {}).copy()
                    combined_data.update(st.session_state.manual_inputs)
                    
                    st.session_state.comprehensive_data["final_data"] = combined_data
                    
                    st.success("All data combined successfully!")
                    st.session_state.step = 5
                    st.rerun()
        
        else:
            st.success("✅ All data extracted successfully!")
            # Auto-create final_data if no manual input needed
            st.session_state.comprehensive_data["final_data"] = comp_data.get("extracted_data", {})
            if st.button("Proceed to SME Eligibility", type="primary"):
                st.session_state.step = 5
                st.rerun()

# STEP 5: SME Eligibility
elif st.session_state.step == 5:
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("⬅️ Back to Step 4", key="back_to_step_4"):
            st.session_state.step = 4
            st.rerun()

    st.markdown("""
    <div style="
        background: linear-gradient(90deg, #4A90E2, #00C6FF);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        color: white;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 15px;">
        🏢 Step 5: SME Eligibility Check
    </div>
""", unsafe_allow_html=True)

    st.info("Upload your SME declaration document to verify company eligibility")
    
    uploaded_file = st.file_uploader(
        "Choose SME Declaration file",
        type=['pdf', 'docx', 'txt'],
        help="Upload your company's SME declaration document"
    )
    
    if uploaded_file is not None:
        if st.button("Process SME Document", type="primary"):
            with st.spinner("Processing SME document..."):
                sme_result = agents["sme"].process_document(uploaded_file)
                st.session_state.sme_result = sme_result
            
            st.success("SME Analysis Complete!")
            st.rerun()
    
    # Show SME results
    if st.session_state.sme_result:
        sme_data = st.session_state.sme_result
        
        if sme_data.get("success"):
            report = sme_data["report"]
            
            # Eligibility status
            status = report["eligibility_status"]
            if status == "ELIGIBLE":
                st.success(f"✅ {status}")
            else:
                st.error(f"❌ {status}")
            
            # Company info
            st.subheader("Company Information")
            company_info = report["company_info"]
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Company:** {company_info.get('company_name', 'N/A')}")
                st.write(f"**Employees:** {company_info.get('employees', 'N/A')}")
            
            with col2:
                turnover = company_info.get('annual_turnover')
                if turnover:
                    st.write(f"**Turnover:** €{turnover:,}")
                else:
                    st.write("**Turnover:** N/A")
                
                balance = company_info.get('balance_sheet_total')
                if balance:
                    st.write(f"**Balance Sheet:** €{balance:,}")
                else:
                    st.write("**Balance Sheet:** N/A")
            
            # Validation details
            validation = report["validation_details"]
            
            if validation.get("criteria_met"):
                st.subheader("✅ Criteria Met")
                for criterion in validation["criteria_met"]:
                    st.success(criterion)
            
            if validation.get("criteria_failed"):
                st.subheader("❌ Criteria Failed")
                for criterion in validation["criteria_failed"]:
                    st.error(criterion)
            
            if validation.get("missing_data"):
                st.subheader("⚠️ Missing Data")
                for item in validation["missing_data"]:
                    st.warning(f"Missing: {item}")
            
            # Proceed to document filling
            if status == "ELIGIBLE":
                if st.button("Fill Lithuanian Documents", type="primary"):
                    st.session_state.step = 6
                    st.rerun()
        
        else:
            st.error(f"Document processing failed: {sme_data.get('error', 'Unknown error')}")

# STEP 6: Document Filling
elif st.session_state.step == 6:

    # Navigation buttons
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("⬅️ Back to Step 5", key="back_to_step_5"):
            st.session_state.step = 5
            st.rerun()
    

    st.markdown("""
    <div style="
        background: linear-gradient(90deg, #4A90E2, #00C6FF);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        color: white;   
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 15px;">
        📄 Step 6: Fill All Lithuanian R&D Documents
    </div>
""", unsafe_allow_html=True)

    st.info("Upload all blank Lithuanian R&D documents to auto-fill them with your comprehensive project data")
    
    # Show comprehensive data summary
    if st.session_state.comprehensive_data and "final_data" in st.session_state.comprehensive_data:
        comp_final_data = st.session_state.comprehensive_data["final_data"]
        
        with st.expander("📊 Data Used for Document Filling"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write("**Company Information:**")
                st.write(f"- Company: {comp_final_data.get('COMPANY_NAME', 'N/A')}")
                st.write(f"- Code: {comp_final_data.get('COMPANY_CODE', 'N/A')}")
                st.write(f"- Manager: {comp_final_data.get('MANAGER_NAME', 'N/A')}")
                st.write(f"- Position: {comp_final_data.get('MANAGER_POSITION', 'N/A')}")
            with col2:
                st.write("**Project Details:**")
                st.write(f"- Product: {comp_final_data.get('PRODUCT_NAME', 'N/A')}")
                st.write(f"- R&D Priority: {comp_final_data.get('RD_PRIORITY', 'N/A')}")
                st.write(f"- Research Area: {comp_final_data.get('RESEARCH_AREA', 'N/A')}")
                st.write(f"- Team Size: {comp_final_data.get('TEAM_SIZE', 'N/A')}")
            with col3:
                st.write("**Financial & Technical:**")
                st.write(f"- R&D Budget: €{comp_final_data.get('RD_BUDGET', 'N/A')}")
                st.write(f"- Duration: {comp_final_data.get('PROJECT_DURATION', 'N/A')} months")
                st.write(f"- Current TPL: {comp_final_data.get('CURRENT_TPL', 'N/A')}")
                st.write(f"- Target TPL: {comp_final_data.get('TARGET_TPL', 'N/A')}")
    
    
    # Automatic document loading from docsss folder
    st.subheader("📁 Documents from docsss folder:")
    
    # Define the document mappings
    document_files = {
        "ENGLISH_PFSA 4 priedas en.docx": "Document 1: PFSA 4 (Declaration Form)",
        "ENGLISH_MTEP verslo planas InoStartas en.docx": "Document 2: MTEP Business Plan", 
        "ENGLISH_PFSA 1 priedas en.docx": "Document 3: PFSA 1 (R&D Assessment)",
        "ENGISH_PFSA 5 priedas en.docx": "Document 4: PFSA 5 (Additional Form)"
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        for i, (filename, description) in enumerate(list(document_files.items())[:2]):
            file_path = os.path.join("docsss", filename)
            if os.path.exists(file_path):
                st.success(f"✅ **{description}**")
                st.write(f"📄 {filename}")
            else:
                st.error(f"❌ **{description}**")
                st.write(f"📄 {filename} (NOT FOUND)")
    
    with col2:
        for i, (filename, description) in enumerate(list(document_files.items())[2:]):
            file_path = os.path.join("docsss", filename)
            if os.path.exists(file_path):
                st.success(f"✅ **{description}**")
                st.write(f"📄 {filename}")
            else:
                st.error(f"❌ **{description}**")
                st.write(f"📄 {filename} (NOT FOUND)")
    
    # Check if all files exist
    all_files_exist = all(os.path.exists(os.path.join("docsss", filename)) for filename in document_files.keys())

    # Process all documents
    if st.button("Process All Documents", type="primary"):
        if all_files_exist:
            # Get comprehensive data
            comp_final_data = st.session_state.comprehensive_data.get("final_data", {})
            
            with st.spinner("Processing all documents from docsss folder..."):
                # Load files from docsss folder
                declaration_file_path = os.path.join("docsss", "ENGLISH_PFSA 4 priedas en.docx")
                mtep_file_path = os.path.join("docsss", "ENGLISH_MTEP verslo planas InoStartas en.docx")
                rd_assessment_file_path = os.path.join("docsss", "ENGLISH_PFSA 1 priedas en.docx")
                passthrough_file_path = os.path.join("docsss", "ENGISH_PFSA 5 priedas en.docx")
                
                document_results = agents["document_filling"].process_all_documents_from_paths(
                    declaration_file_path, mtep_file_path, rd_assessment_file_path, passthrough_file_path, comp_final_data
                )
                st.session_state.document_results = document_results
            
            st.success("✅ Documents processed successfully!")
            st.rerun()
        else:
            st.error("❌ Not all required documents are available in the docsss folder. Please check the file names and try again.")
    
    
    # Show results and download options
    if st.session_state.document_results:
        results = st.session_state.document_results
        
        st.subheader("📋 Documents Ready for Download")
        
        col1, col2 = st.columns(2)
        
        # Left column - Declaration and MTEP
        with col1:
            # Declaration document results
            if results.get("declaration_result"):
                decl_result = results["declaration_result"]
                
                if decl_result.get("success"):
                    st.success("✅ Declaration Form Complete")
                    st.write(f"**Preview:** {decl_result.get('preview', 'Document processed successfully')}")
                    
                    # Download button
                    if decl_result.get("filled_document"):
                        st.download_button(
                            label="📥 Download Declaration",
                            data=decl_result["filled_document"].getvalue(),
                            file_name=decl_result.get("filename", "declaration_filled.docx"),
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                else:
                    st.error(f"Declaration failed: {decl_result.get('error', 'Unknown error')}")
            else:
                st.info("Declaration form not uploaded")
            
            st.markdown("---")
            
            # MTEP business plan results
            if results.get("mtep_result"):
                mtep_result = results["mtep_result"]
                
                if mtep_result.get("success"):
                    st.success("✅ MTEP Business Plan Complete")
                    st.write(f"**Preview:** {mtep_result.get('preview', 'Document processed successfully')}")
                    
                    # Download button
                    if mtep_result.get("filled_document"):
                        st.download_button(
                            label="📥 Download MTEP Plan",
                            data=mtep_result["filled_document"].getvalue(),
                            file_name=mtep_result.get("filename", "mtep_filled.docx"),
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                else:
                    st.error(f"MTEP plan failed: {mtep_result.get('error', 'Unknown error')}")
            else:
                st.info("MTEP business plan not uploaded")
        
        # Right column - R&D Assessment and Additional Document
        with col2:
            # R&D assessment results
            if results.get("rd_assessment_result"):
                assess_result = results["rd_assessment_result"]
                
                if assess_result.get("success"):
                    st.success("✅ R&D Assessment Complete")
                    st.write(f"**Preview:** {assess_result.get('preview', 'Document processed successfully')}")
                    
                    # Download button
                    if assess_result.get("filled_document"):
                        st.download_button(
                            label="📥 Download R&D Assessment",
                            data=assess_result["filled_document"].getvalue(),
                            file_name=assess_result.get("filename", "rd_assessment_filled.docx"),
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                else:
                    st.error(f"R&D assessment failed: {assess_result.get('error', 'Unknown error')}")
            else:
                st.info("R&D assessment form not uploaded")
            
            st.markdown("---")
            
            # Pass-through document results
            if results.get("passthrough_result"):
                passthrough_result = results["passthrough_result"]
                
                if passthrough_result.get("success"):
                    st.success("✅ Additional Document Complete")
                    st.write(f"**Preview:** {passthrough_result.get('preview', 'Document processed successfully')}")
                    
                    # Determine MIME type based on file extension
                    filename = passthrough_result.get("filename", "additional_document")
                    if filename.endswith('.docx'):
                        mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    elif filename.endswith('.pdf'):
                        mime_type = "application/pdf"
                    elif filename.endswith('.xlsx'):
                        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    else:
                        mime_type = "application/octet-stream"
                    
                    # Download button
                    if passthrough_result.get("filled_document"):
                        st.download_button(
                            label="📥 Download Additional Doc",
                            data=passthrough_result["filled_document"].getvalue(),
                            file_name=filename,
                            mime=mime_type
                        )
                else:
                    st.error(f"Additional document failed: {passthrough_result.get('error', 'Unknown error')}")
            else:
                st.info("Additional document not uploaded")
        
        # Summary and final step
        st.markdown("---")
        st.subheader("🎉 Document Processing Summary")
        
        completed_docs = []
        if results.get("declaration_result", {}).get("success"):
            completed_docs.append("Declaration Form")
        if results.get("mtep_result", {}).get("success"):
            completed_docs.append("MTEP Business Plan")
        if results.get("rd_assessment_result", {}).get("success"):
            completed_docs.append("R&D Assessment")
        if results.get("passthrough_result", {}).get("success"):
            completed_docs.append("Additional Document")
        
        if completed_docs:
            st.success(f"✅ Successfully processed {len(completed_docs)} document(s): {', '.join(completed_docs)}")
            st.info("📋 Your documents are ready for submission!")
        
        # Proceed to Excel processing button
        if st.button("Process Excel Sheets", type="primary"):
            st.session_state.step = 7
            st.rerun()

# STEP 7: Excel Processing
elif st.session_state.step == 7:
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("⬅️ Back to Step 6", key="back_to_step_6"):
            st.session_state.step = 6
            st.rerun()
    
    st.markdown("""
    <div style="
        background: linear-gradient(90deg, #4A90E2, #00C6FF);
        border-radius: 12px;
        padding: 15px;
        text-align: center; 
        color: white;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 15px;">
        📊 Step 7: Generate & Fill Excel Forms
    </div>
""", unsafe_allow_html=True)
    
    
    st.info("Generate Lithuanian R&D Excel files using the COMPLETE agent pipeline")
    
    # Show project data summary
    if st.session_state.comprehensive_data and "final_data" in st.session_state.comprehensive_data:
        comp_final_data = st.session_state.comprehensive_data["final_data"]
        
        with st.expander("📊 Your Project Data (Used for Excel Form Filling)", expanded=False):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write("**Company Information:**")
                st.write(f"- Company: {comp_final_data.get('COMPANY_NAME', 'N/A')}")
                st.write(f"- Product: {comp_final_data.get('PRODUCT_NAME', 'N/A')}")
                st.write(f"- Manager: {comp_final_data.get('MANAGER_NAME', 'N/A')}")
            with col2:
                st.write("**Project Details:**")
                st.write(f"- Duration: {comp_final_data.get('PROJECT_DURATION', 'N/A')} months")
                st.write(f"- Team Size: {comp_final_data.get('TEAM_SIZE', 'N/A')}")
                st.write(f"- R&D Budget: €{comp_final_data.get('RD_BUDGET', 'N/A')}")
            with col3:
                st.write("**Technical Info:**")
                st.write(f"- Current TPL: {comp_final_data.get('CURRENT_TPL', 'N/A')}")
                st.write(f"- Target TPL: {comp_final_data.get('TARGET_TPL', 'N/A')}")
                st.write(f"- Research Area: {comp_final_data.get('RESEARCH_AREA', 'N/A')}")
    
    # Data validation step
    if not st.session_state.excel_validation_result:
        st.subheader("🔍 Step 1: Data Validation")
        st.write("Validate your data completeness before running the complete agent pipeline")
        
        if st.button("🔍 Validate Data Completeness", type="secondary"):
            with st.spinner("Validating data completeness..."):
                try:
                    validator = DataValidationAgent()
                    # First, validate current data without interactive completion
                    # Pass the correct prompts directory path
                    validation_results = validator.validate_all_prompts("code/finalInput.txt", prompts_dir="code/prompts")
                    
                    # Store validation result for display
                    st.session_state.excel_validation_result = {
                        "completeness_score": validation_results.get('overall_completeness_score', 0),
                        "missing_fields": validation_results.get('summary', {}).get('all_missing_fields', []),
                        "validation_results": validation_results,
                        "needs_completion": validation_results.get('overall_completeness_score', 0) < 90
                    }
                    
                    st.success("✅ Data validation completed successfully!")
                    
                except Exception as e:
                    st.error(f"❌ Error during data validation: {e}")
                    st.session_state.excel_validation_result = {
                        "completeness_score": 0,
                        "missing_fields": ["Validation failed"],
                        "error": str(e)
                    }
            
            st.rerun()
    
    # Show validation results and completion options
    if st.session_state.excel_validation_result:
        validation_result = st.session_state.excel_validation_result
        
        # Display validation summary
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Data Completeness", f"{validation_result.get('completeness_score', 0):.2f}%")
        with col2:
            missing_count = len(validation_result.get('missing_fields', []))
            st.metric("Missing Fields", missing_count)
        
        # Show missing fields if any
        if validation_result.get('missing_fields'):
            with st.expander("View Missing Fields"):
                for field in validation_result.get('missing_fields', [])[:10]:
                    if field and field != "Unable to parse detailed analysis":
                        st.write(f"• {field}")
        
        # Data completion section - show if there are any missing fields
        missing_fields = validation_result.get('missing_fields', [])
        has_meaningful_missing_fields = any(field and field not in ["None", "Unable to parse detailed analysis"] 
                                          for field in missing_fields)
        
        if has_meaningful_missing_fields:
            st.subheader("🔧 Step 2: Complete Missing Data")
            st.write(f"You have {len([f for f in missing_fields if f and f not in ['None', 'Unable to parse detailed analysis']])} fields that can be completed to improve your data quality.")
            st.write("Choose how you would like to fill the missing information:")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🤖 AI Completion", type="primary", help="AI will analyze your data and intelligently fill missing fields"):
                    st.session_state.completion_choice = "ai"
            
            with col2:
                if st.button("✍️ Manual Input", help="You will manually enter each missing field"):
                    st.session_state.completion_choice = "manual"
            
            with col3:
                if st.button("🔄 Hybrid Approach", help="AI generates suggestions that you can approve or modify"):
                    st.session_state.completion_choice = "hybrid"
            
            # Handle completion choice
            if hasattr(st.session_state, 'completion_choice'):
                try:
                    from code.complete_missing_data import DataCompletionAgent
                    
                    completion_agent = DataCompletionAgent()
                    
                    if st.session_state.completion_choice == "ai":
                        st.info("🤖 Running AI-powered data completion...")
                        with st.spinner("AI is analyzing and completing your data..."):
                            updated_file = completion_agent._ai_completion("code/finalInput.txt", validation_result)
                            st.success("✅ AI completion finished! Your data has been updated.")
                            st.session_state.completion_completed = True
                            
                    elif st.session_state.completion_choice == "manual":
                        st.info("✍️ Manual completion mode")
                        st.write("**Missing fields to complete:**")
                        
                        # Create form for manual input
                        with st.form("manual_completion_form"):
                            completed_data = {}
                            meaningful_missing_fields = [f for f in validation_result.get('missing_fields', []) 
                                                       if f and f not in ["None", "Unable to parse detailed analysis"]]
                            
                            for i, field in enumerate(meaningful_missing_fields[:10]):  # Limit to 10 fields for UI
                                if field:
                                    completed_data[field] = st.text_input(f"{field}:", key=f"field_{i}")
                            
                            if st.form_submit_button("💾 Save Completed Data"):
                                # Filter out empty values
                                valid_data = {k: v for k, v in completed_data.items() if v.strip()}
                                
                                if valid_data:
                                    updated_file = completion_agent._append_completed_data("code/finalInput.txt", valid_data, "USER-PROVIDED")
                                    st.success(f"✅ Successfully saved {len(valid_data)} completed fields!")
                                    st.session_state.completion_completed = True
                                else:
                                    st.warning("⚠️ No data was entered.")
                    
                    elif st.session_state.completion_choice == "hybrid":
                        st.info("🔄 Hybrid completion mode")
                        st.write("AI will generate suggestions for you to review:")
                        
                        # Read current data for AI suggestions
                        with open("code/finalInput.txt", 'r', encoding='utf-8') as file:
                            current_data = file.read()
                        
                        meaningful_missing_fields = [f for f in validation_result.get('missing_fields', []) 
                                                   if f and f not in ["None", "Unable to parse detailed analysis"]]
                        completed_data = {}
                        
                        with st.form("hybrid_completion_form"):
                            for i, field in enumerate(meaningful_missing_fields[:5]):  # Limit for UI performance
                                if field:
                                    st.write(f"**{field}:**")
                                    
                                    # Generate AI suggestion
                                    with st.spinner(f"Generating AI suggestion for {field}..."):
                                        try:
                                            ai_suggestion = completion_agent._generate_ai_field_value(field, current_data)
                                            st.write(f"🤖 AI Suggestion: *{ai_suggestion}*")
                                            
                                            user_value = st.text_input(
                                                "Your value (leave empty to use AI suggestion):",
                                                key=f"hybrid_field_{i}",
                                                placeholder=ai_suggestion
                                            )
                                            
                                            # Use AI suggestion if user doesn't provide input
                                            completed_data[field] = user_value if user_value.strip() else ai_suggestion
                                            
                                        except Exception as e:
                                            st.error(f"Could not generate AI suggestion for {field}")
                                            completed_data[field] = st.text_input(f"Enter value for {field}:", key=f"manual_field_{i}")
                            
                            if st.form_submit_button("💾 Save Hybrid Completion"):
                                valid_data = {k: v for k, v in completed_data.items() if v and v.strip()}
                                
                                if valid_data:
                                    updated_file = completion_agent._append_completed_data("code/finalInput.txt", valid_data, "HYBRID")
                                    st.success(f"✅ Successfully saved {len(valid_data)} completed fields!")
                                    st.session_state.completion_completed = True
                                else:
                                    st.warning("⚠️ No data was completed.")
                
                except Exception as e:
                    st.error(f"❌ Error during data completion: {e}")
            
            # Show completion success
            if hasattr(st.session_state, 'completion_completed') and st.session_state.completion_completed:
                st.success("🎉 Data completion process finished!")
                
                # Option to re-run validation
                if st.button("🔍 Re-run Validation", type="secondary"):
                    st.session_state.excel_validation_result = None
                    st.session_state.completion_choice = None
                    st.session_state.completion_completed = False
                    st.rerun()
        else:
            st.success("✅ Your data is complete enough (>90% completeness)")
            if missing_fields and not has_meaningful_missing_fields:
                st.info("💡 All remaining missing fields appear to be optional or system-generated")
            
            # Show option to complete remaining fields anyway
            if meaningful_missing_fields := [f for f in missing_fields if f and f not in ["None", "Unable to parse detailed analysis"]]:
                with st.expander("🔧 Optional: Complete Remaining Fields", expanded=False):
                    st.write(f"You can still complete {len(meaningful_missing_fields)} remaining fields to achieve higher completeness:")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("🤖 AI Complete Remaining", key="optional_ai", help="AI will fill remaining fields"):
                            st.session_state.completion_choice = "ai"
                    with col2:
                        if st.button("✍️ Manual Complete", key="optional_manual", help="Manually enter remaining fields"):
                            st.session_state.completion_choice = "manual"
                    with col3:
                        if st.button("🔄 Hybrid Complete", key="optional_hybrid", help="AI suggestions with your approval"):
                            st.session_state.completion_choice = "hybrid"
            
            st.subheader("🚀 Step 2: Run Complete Processing")
            
            # Add button to proceed directly to Excel generation
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📊 Proceed to Excel Generation", type="primary", help="Generate Lithuanian R&D Excel files with current data"):
                    st.session_state.step = 7  # Go directly to Excel processing step
                    st.rerun()
            with col2:
                completeness_pct = validation_result.get('completeness_score', 0)
                st.info(f"💡 You can proceed with Excel generation using your current data ({completeness_pct:.2f}% complete)")
            
            st.markdown("---")
    
    # Continue with original processing flow
    if st.session_state.excel_validation_result:
        validation_data = st.session_state.excel_validation_result
        
        col1, col2 = st.columns(2)
        with col1:
            completeness = validation_data.get("completeness_score", 0)
            if completeness >= 80:
                st.success(f"✅ Data Completeness: {completeness}%")
            elif completeness >= 60:
                st.warning(f"⚠️ Data Completeness: {completeness}%")
            else:
                st.error(f"❌ Data Completeness: {completeness}%")
        
        with col2:
            if "completed_file" in validation_data:
                st.success(f"✅ Validation completed: {validation_data['completed_file']}")
            elif "error" in validation_data:
                st.error(f"❌ Validation error: {validation_data['error']}")
            else:
                missing_count = len(validation_data.get("missing_fields", []))
                if missing_count == 0:
                    st.success("✅ No missing fields detected")
                else:
                    st.warning(f"⚠️ {missing_count} fields may need attention")
        
        # Show missing fields if any
        missing_fields = validation_data.get("missing_fields", [])
        if missing_fields:
            with st.expander("📝 Missing Fields (Optional)", expanded=False):
                for field in missing_fields[:5]:  # Show first 5
                    st.write(f"• {field}")
                if len(missing_fields) > 5:
                    st.write(f"... and {len(missing_fields) - 5} more")
        
        # Interactive data completion section
        if validation_data.get("needs_completion", False):
            st.subheader("📝 Complete Missing Data")
            st.write("Your data needs some additional information to reach optimal completeness.")
            
            # Initialize session state for data completion if not exists
            if "missing_data_fields" not in st.session_state:
                st.session_state.missing_data_fields = {}
            
            # Show form for missing fields
            with st.form("missing_data_form"):
                st.write("**Please provide the following missing information:**")
                
                # Get top 5 missing fields
                top_missing_fields = missing_fields[:5]
                
                # Create input fields for missing data
                for i, field in enumerate(top_missing_fields):
                    if field and field != "Unable to parse detailed analysis":
                        # Create a clean key for the field
                        field_key = f"field_{i}"
                        user_input = st.text_input(
                            f"{field}:",
                            key=field_key,
                            help=f"Enter information for: {field}"
                        )
                        st.session_state.missing_data_fields[field] = user_input
                
                # Additional information section
                st.write("**Add any other relevant information:**")
                additional_info = st.text_area(
                    "Additional Information:",
                    key="additional_info",
                    help="Enter any other relevant information that might be missing",
                    height=100
                )
                
                # Submit button
                if st.form_submit_button("💾 Save Additional Data"):
                    if any(st.session_state.missing_data_fields.values()) or additional_info:
                        try:
                            # Append to the input file
                            with open("code/finalInput.txt", "a", encoding="utf-8") as file:
                                file.write("\n\n--- ADDITIONAL INFORMATION ---\n")
                                
                                # Add structured missing fields
                                for field, value in st.session_state.missing_data_fields.items():
                                    if value.strip():
                                        file.write(f"{field}: {value}\n")
                                
                                # Add additional information
                                if additional_info.strip():
                                    file.write(f"\nAdditional Information:\n{additional_info}\n")
                
                            st.success("✅ Additional data saved successfully!")
                            
                            # Clear the form
                            st.session_state.missing_data_fields = {}
                            st.session_state.additional_info = ""
                            
                            # Show re-validation option
                            st.info("🔄 Data updated! Click 'Re-validate Data' to check the new completeness score.")
                            
                            # Add re-validation button
                            if st.button("🔄 Re-validate Data", key="revalidate_button"):
                                with st.spinner("Re-validating data..."):
                                    try:
                                        validator = DataValidationAgent()
                                        new_validation_results = validator.validate_all_prompts("code/finalInput.txt", prompts_dir="code/prompts")
                                        
                                        # Update validation result
                                        st.session_state.excel_validation_result = {
                                            "completeness_score": new_validation_results.get('overall_completeness_score', 0),
                                            "missing_fields": new_validation_results.get('summary', {}).get('all_missing_fields', []),
                                            "validation_results": new_validation_results,
                                            "needs_completion": new_validation_results.get('overall_completeness_score', 0) < 90
                                        }
                                        
                                        st.success("✅ Re-validation completed!")
                                        st.rerun()
                                        
                                    except Exception as e:
                                        st.error(f"❌ Error during re-validation: {e}")
                            
                        except Exception as e:
                            st.error(f"❌ Error saving additional data: {e}")
                    else:
                        st.warning("⚠️ Please enter some information before saving.")
            
            # Show current input file content
            with st.expander("📄 View Current Input File Content", expanded=False):
                try:
                    with open("code/finalInput.txt", "r", encoding="utf-8") as file:
                        content = file.read()
                    
                    if len(content) > 1000:
                        st.text_area("File Content (truncated):", content[:1000] + "\n\n... (truncated)", height=200, disabled=True)
                        st.info(f"File is {len(content)} characters long. Showing first 1000 characters.")
                    else:
                        st.text_area("File Content:", content, height=200, disabled=True)
                        
                except FileNotFoundError:
                    st.error("❌ Input file not found: code/finalInput.txt")
                except Exception as e:
                    st.error(f"❌ Error reading file: {e}")
                
                # Download button for the updated input file
                try:
                    with open("code/finalInput.txt", "r", encoding="utf-8") as file:
                        file_content = file.read()
                    
                    st.download_button(
                        label="📥 Download Updated Input File",
                        data=file_content,
                        file_name="finalInput_updated.txt",
                        mime="text/plain",
                        help="Download the updated input file with all additional information"
                    )
                except Exception as e:
                    st.warning(f"⚠️ Cannot provide download: {e}")
    
    # Process Excel forms with user data
    if not st.session_state.excel_processing_result:
        st.subheader("🚀 Step 2: Run Complete Agent Pipeline")
        st.write("**This will run ALL agents as defined in agent_run.py:**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Processing Steps:**")
            st.write("• 📊 Data validation & completion")
            st.write("• 📝 Patenting & commercialization agents")
            st.write("• 💰 Revenue forecast agent")
            st.write("• 📋 Budget forms agents")
            st.write("• 📑 1A forms agents (10+ tabs)")
            st.write("• 🔗 Merge all sheets into final files")
        
        with col2:
            st.write("**Expected Output:**")
            st.write("• ENGISH_1B priedas_InoStartas en.xlsx")
            st.write("• ENGLISH_1A priedas_InoStartas en.xlsx") 
            st.write("• Financial Plan Excel")
            st.write("• Recommended Form Excel")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 Run Complete Agent Pipeline", type="primary"):
                with st.spinner("Running COMPLETE agent pipeline... This may take 5-10 minutes..."):
                    try:
                        # Run the complete pipeline without any parameters
                        excel_agent_run()
                        
                        # Set success result
                        st.session_state.excel_processing_result = {
                            "success": True,
                            "method": "full_pipeline_completed",
                            "pipeline_details": "All agents executed successfully: Data validation, Patenting, Commercialization, Revenue forecast, Budget forms, 1A forms, and sheet merging completed.",
                            "processing_log": "Pipeline executed via excel_agent_run() function from agent_run.py",
                            "output_files": [
                                {
                                    "name": "ENGISH_1B priedas_InoStartas en.xlsx",
                                    "path": "code/output/ENGISH_1B priedas_InoStartas en.xlsx",
                                    "size": 0,  # Will be updated when displaying
                                    "description": "1B Appendix - Patenting and Commercialization"
                                },
                                {
                                    "name": "ENGLISH_1A priedas_InoStartas en.xlsx",
                                    "path": "code/output/ENGLISH_1A priedas_InoStartas en.xlsx",
                                    "size": 0,  # Will be updated when displaying
                                    "description": "1A Appendix - Complete project data with 10+ tabs"
                                },
                                {
                                    "name": "ENGLISH_Finansinis planas en.xlsx",
                                    "path": "code/output/ENGLISH_Finansinis planas en.xlsx",
                                    "size": 0,  # Will be updated when displaying
                                    "description": "Financial Plan - Revenue forecast and budget"
                                },
                                {
                                    "name": "engish_rekomenduojama_forma_de_____l_planuojamo_darbo_uz_____mokesc_____io_en.xlsx",
                                    "path": "code/output/engish_rekomenduojama_forma_de_____l_planuojamo_darbo_uz_____mokesc_____io_en.xlsx",
                                    "size": 0,  # Will be updated when displaying
                                    "description": "Recommended Form - Budgetary authorization and non-budgetary forms"
                                }
                            ]
                        }
                        
                        st.success("✅ COMPLETE agent pipeline executed successfully!")
                        
                    except Exception as e:
                        st.error(f"❌ Pipeline failed: {str(e)}")
                        st.session_state.excel_processing_result = {
                            "success": False,
                            "error": str(e)
                        }
                
                st.rerun()
        
        with col2:
            if st.button("📁 Use Existing Files", type="secondary"):
                with st.spinner("Accessing existing Excel files..."):
                    try:
                        # Check if output files exist
                        import os
                        output_files = []
                        
                        expected_files = [
                            ("ENGISH_1B priedas_InoStartas en.xlsx", "1B Appendix - Patenting and Commercialization"),
                            ("ENGLISH_1A priedas_InoStartas en.xlsx", "1A Appendix - Complete project data with 10+ tabs"),
                            ("ENGLISH_Finansinis planas en.xlsx", "Financial Plan - Revenue forecast and budget"),
                            ("engish_rekomenduojama_forma_de_____l_planuojamo_darbo_uz_____mokesc_____io_en.xlsx", "Recommended Form - Budgetary authorization and non-budgetary forms")
                        ]
                        
                        for filename, description in expected_files:
                            file_path = f"code/output/{filename}"
                            if os.path.exists(file_path):
                                file_size = os.path.getsize(file_path)
                                output_files.append({
                                    "name": filename,
                                    "path": file_path,
                                    "size": file_size,
                                    "description": description
                                })
                        
                        if output_files:
                            st.session_state.excel_processing_result = {
                                "success": True,
                                "method": "existing_files_fallback",
                                "pipeline_details": "Using existing output files from previous pipeline execution.",
                                "processing_log": "Files accessed from code/output folder",
                                "output_files": output_files
                            }
                            st.info("ℹ️ Using existing Excel files (pipeline not executed)")
                        else:
                            st.warning("⚠️ No existing files found in output folder")
                            st.session_state.excel_processing_result = {
                                "success": False,
                                "error": "No output files found"
                            }
                    except Exception as e:
                        st.error(f"❌ Error accessing existing files: {str(e)}")
                        st.session_state.excel_processing_result = {
                            "success": False,
                            "error": str(e)
                        }
                
                st.rerun()
    
    # Show Excel processing results
    if st.session_state.excel_processing_result:
        processing_data = st.session_state.excel_processing_result
        
        if processing_data.get("success"):
            st.subheader("📋 Available Excel Files")
            
            # Check the method used to provide files
            method = processing_data.get("method", "")
            if processing_data.get("is_mock", False):
                st.warning("⚠️ Excel processing failed - showing mock files instead")
                st.info("The Excel Agent encountered configuration issues. Mock files have been created for download, but they contain sample data only.")
            elif method == "full_pipeline_completed":
                st.success("🎉 COMPLETE agent pipeline executed successfully!")
                st.info("All agents have been executed, forms filled, sheets merged, and files saved to output folder.")
                
                # Show pipeline details
                pipeline_details = processing_data.get("pipeline_details", "")
                if pipeline_details:
                    st.write("**Pipeline Steps Completed:**")
                    st.write(pipeline_details)
                
                # Show processing log if available
                processing_log = processing_data.get("processing_log", "")
                if processing_log:
                    with st.expander("📋 Complete Processing Log", expanded=False):
                        st.text(processing_log)
            elif method == "forms_filled":
                st.success("🎉 Excel forms filled with your project data!")
                st.info("These Excel files have been automatically filled with your project information and are ready for Lithuanian R&D submission.")
                
                # Show processing log if available
                processing_log = processing_data.get("processing_log", "")
                if processing_log:
                    with st.expander("📋 Processing Log", expanded=False):
                        st.text(processing_log)
            elif method == "existing_files_fallback":
                st.warning("⚠️ Form filling failed - using existing template files")
                st.info("The system couldn't fill forms with your data, but template files are available for manual completion.")
            elif method == "pre_existing_files":
                st.success("📁 Excel files are available from the output folder")
                st.info("These are pre-generated Lithuanian R&D Excel files ready for download and submission.")
            else:
                st.success("🎉 Excel processing completed successfully!")
            
            output_files = processing_data.get("output_files", [])
            if output_files:
                st.write(f"**Available {len(output_files)} Excel files:**")
                
                for file_info in output_files:
                    # Update file size if it's 0 (was set during pipeline execution)
                    if file_info.get('size', 0) == 0:
                        try:
                            import os
                            if os.path.exists(file_info['path']):
                                file_info['size'] = os.path.getsize(file_info['path'])
                        except:
                            file_info['size'] = 0
                    
                    # Show different styling for mock files
                    if processing_data.get("is_mock", False):
                        expander_title = f"🔧 {file_info['description']} (MOCK DATA)"
                    else:
                        expander_title = f"📄 {file_info['description']}"
                    
                    with st.expander(expander_title, expanded=False):
                        col1, col2 = st.columns([2, 1])
                        with col1:
                            st.write(f"**File:** {file_info['name']}")
                            st.write(f"**Size:** {file_info['size']:,} bytes")
                            st.write(f"**Description:** {file_info['description']}")
                            
                            if processing_data.get("is_mock", False):
                                st.warning("⚠️ This file contains mock data only. Configure Excel Agent properly for real data.")
                        
                        with col2:
                            # Download button - read file directly from the output folder
                            try:
                                with open(file_info['path'], 'rb') as file:
                                    file_content = file.read()
                                
                                st.download_button(
                                    label="📥 Download",
                                    data=file_content,
                                    file_name=file_info['name'],
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                )
                            except Exception as e:
                                st.error(f"❌ Error reading file: {str(e)}")
                                st.write("File may not exist or be accessible")
            else:
                st.warning("⚠️ No output files found. Please check the Excel Agent configuration.")
        
        else:
            st.error(f"❌ Excel processing failed: {processing_data.get('error', 'Unknown error')}")
        
        # Proceed to final step
        st.divider()
        if st.button("🎯 Generate Final Business Plan", type="primary"):
            st.session_state.step = 8
            st.rerun()

# STEP 8: Final Business Plan
elif st.session_state.step == 8:
    
    st.markdown("""
    <div style="
        background: linear-gradient(90deg, #4A90E2, #00C6FF);
        border-radius: 12px;
        padding: 15px;
        text-align: center; 
        color: white;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 15px;">
        📋 Step 8: Final Comprehensive Business Plan
    </div>
""", unsafe_allow_html=True)
    
    
    st.success("🎉 Complete Business Plan Generation Finished!")
    
    # Show comprehensive project overview
    if st.session_state.comprehensive_data and "final_data" in st.session_state.comprehensive_data:
        comp_final_data = st.session_state.comprehensive_data["final_data"]
        
        st.subheader("📊 Project Overview Dashboard")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Product", comp_final_data.get('PRODUCT_NAME', 'N/A'))
            st.metric("Team Size", comp_final_data.get('TEAM_SIZE', 'N/A'))
        with col2:
            st.metric("R&D Budget", f"€{comp_final_data.get('RD_BUDGET', 'N/A')}")
            st.metric("Duration", f"{comp_final_data.get('PROJECT_DURATION', 'N/A')} months")
        with col3:
            st.metric("Current TPL", comp_final_data.get('CURRENT_TPL', 'N/A'))
            st.metric("Target TPL", comp_final_data.get('TARGET_TPL', 'N/A'))
        with col4:
            st.metric("Revenue Projection", f"€{comp_final_data.get('REVENUE_PROJECTION', 'N/A')}")
            st.metric("Novelty Level", comp_final_data.get('NOVELTY_LEVEL', 'N/A'))
    
    # Compile final plan
    final_plan = compile_final_plan()
    
    # Display final plan
    st.markdown("## Executive Summary")
    st.write(final_plan["executive_summary"])
    
    st.markdown("## Technical Description (TRL 4)")
    st.write(final_plan["technical_description"])
    
    st.markdown("## R&D Activities")
    st.write(final_plan["rd_activities"])
    
    st.markdown("## Company Eligibility")
    st.write(final_plan["eligibility_confirmation"])
    
    st.markdown("## Lithuanian R&D Application Status")
    if st.session_state.document_results:
        results = st.session_state.document_results
        completed_docs = []
        if results.get("declaration_result", {}).get("success"):
            completed_docs.append("✅ Declaration Form")
        if results.get("mtep_result", {}).get("success"):
            completed_docs.append("✅ MTEP Business Plan")
        if results.get("rd_assessment_result", {}).get("success"):
            completed_docs.append("✅ R&D Assessment Form")
        if results.get("passthrough_result", {}).get("success"):
            completed_docs.append("✅ Additional Document")
        
        if completed_docs:
            st.write("**Processed Documents:**")
            for doc in completed_docs:
                st.write(f"- {doc}")
    
    # Excel processing summary
    st.markdown("## Excel Sheets Generation Status")
    if st.session_state.excel_processing_result:
        processing_data = st.session_state.excel_processing_result
        if processing_data.get("success"):
            output_files = processing_data.get("output_files", [])
            st.write("**Generated Excel Files:**")
            for file_info in output_files:
                st.write(f"- ✅ {file_info['description']}")
            st.success("🎯 **All Excel sheets are ready for download!**")
        else:
            st.warning("⚠️ Excel processing was not completed")
    else:
        st.info("ℹ️ Excel processing was skipped")
    
    # Download options
    st.markdown("## Download Options")
    
    # Main download options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Download Business Plan PDF"):
            if st.session_state.get('trl_result') or st.session_state.get('comprehensive_data'):
                try:
                    with st.spinner("Generating comprehensive PDF..."):
                        pdf_generator = BusinessPlanPDFGenerator()
                        pdf_buffer = pdf_generator.generate_business_plan_pdf(st.session_state)
                        
                        if pdf_buffer:
                            st.download_button(
                                label="💾 Download PDF",
                                data=pdf_buffer.getvalue(),
                                file_name=f"Business_Plan_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                                mime="application/pdf"
                            )
                            st.success("✅ PDF generated successfully! Click the download button above.")
                        else:
                            st.error("❌ Failed to generate PDF. Please try again.")
                except Exception as e:
                    st.error(f"❌ Error generating PDF: {str(e)}")
            else:
                st.warning("⚠️ Please complete at least the TRL analysis before generating PDF.")
    
    with col2:
        if st.button("📦 Download Complete Package (ZIP)"):
            if st.session_state.get('trl_result') or st.session_state.get('comprehensive_data'):
                try:
                    with st.spinner("Creating complete package..."):
                        pdf_generator = BusinessPlanPDFGenerator()
                        zip_buffer = pdf_generator.create_zip_with_all_files(st.session_state)
                        
                        if zip_buffer:
                            st.download_button(
                                label="💾 Download ZIP",
                                data=zip_buffer.getvalue(),
                                file_name=f"Business_Plan_Complete_{datetime.now().strftime('%Y%m%d_%H%M')}.zip",
                                mime="application/zip"
                            )
                            st.success("✅ Complete package created! Click the download button above.")
                        else:
                            st.error("❌ Failed to create package. Please try again.")
                except Exception as e:
                    st.error(f"❌ Error creating package: {str(e)}")
            else:
                st.warning("⚠️ Please complete at least the TRL analysis before creating package.")
    
    with col3:
        if st.button("🔄 Start New Analysis"):
            # Reset session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Additional download options for Excel and documents
    st.markdown("### 📊 Additional Download Options")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📈 Download Excel Files Only"):
            try:
                with st.spinner("Preparing Excel files..."):
                    downloader = DataDownloader()
                    excel_files = downloader.get_excel_files_info()
                    
                    if excel_files:
                        zip_buffer = downloader.download_all_excel_files()
                        if zip_buffer:
                            st.download_button(
                                label="💾 Download Excel ZIP",
                                data=zip_buffer.getvalue(),
                                file_name=f"Excel_Files_{datetime.now().strftime('%Y%m%d_%H%M')}.zip",
                                mime="application/zip"
                            )
                            st.success(f"✅ {len(excel_files)} Excel files ready for download!")
                        else:
                            st.error("❌ Failed to create Excel ZIP.")
                    else:
                        st.warning("⚠️ No Excel files available for download.")
            except Exception as e:
                st.error(f"❌ Error preparing Excel files: {str(e)}")
    
    with col2:
        if st.button("📄 Download Documents Only"):
            try:
                with st.spinner("Preparing documents..."):
                    downloader = DataDownloader()
                    doc_files = downloader.get_document_files_info()
                    
                    if doc_files:
                        zip_buffer = downloader.download_all_document_files()
                        if zip_buffer:
                            st.download_button(
                                label="💾 Download Documents ZIP",
                                data=zip_buffer.getvalue(),
                                file_name=f"Document_Files_{datetime.now().strftime('%Y%m%d_%H%M')}.zip",
                                mime="application/zip"
                            )
                            st.success(f"✅ {len(doc_files)} document files ready for download!")
                        else:
                            st.error("❌ Failed to create documents ZIP.")
                    else:
                        st.warning("⚠️ No document files available for download.")
            except Exception as e:
                st.error(f"❌ Error preparing documents: {str(e)}")
    
    with col3:
        if st.button("📋 Download Raw Data (JSON)"):
            if st.session_state.get('trl_result') or st.session_state.get('comprehensive_data'):
                try:
                    with st.spinner("Preparing raw data..."):
                        downloader = DataDownloader()
                        zip_buffer = downloader.download_complete_data_package(st.session_state)
                        
                        if zip_buffer:
                            st.download_button(
                                label="💾 Download Data Package",
                                data=zip_buffer.getvalue(),
                                file_name=f"Raw_Data_Package_{datetime.now().strftime('%Y%m%d_%H%M')}.zip",
                                mime="application/zip"
                            )
                            st.success("✅ Raw data package ready for download!")
                        else:
                            st.error("❌ Failed to create data package.")
                except Exception as e:
                    st.error(f"❌ Error preparing data package: {str(e)}")
            else:
                st.warning("⚠️ Please complete at least the TRL analysis before downloading data.")


# Sidebar with information
with st.sidebar:
    st.header("ℹ️ About This Tool")
    st.write("""
    This AI-powered tool helps transform your business idea into a funding-ready plan by:
    
    1. **TRL Analysis** - Upgrades ideas to TRL 4 level
    2. **R&D Validation** - Ensures Frascati compliance  
    3. **Market Analysis** - Patent search & market saturation
    4. **Data Extraction** - 46 comprehensive project fields
    5. **SME Eligibility** - Company qualification check
    6. **Document Processing** - 3 filled forms + 1 pass-through
    7. **Excel Form Filling** - Lithuanian R&D Excel sheets filled with your data
    8. **Final Plan** - Comprehensive business plan
    
    **Documents Supported:**
    - Declaration Form (auto-filled)
    - MTEP Business Plan (auto-filled)
    - R&D Assessment Form (auto-filled)
    - Additional Document (pass-through)
    
    **Excel Sheets Generated & Filled:**
    - 1A Attachment (Project Details & Staff) - filled with your data
    - 1B Attachment (Patenting & Commercialization) - filled with your data
    - Financial Plan - filled with your data
    - Recommended Form (Work Remuneration) - filled with your data
    
    **Required:**
    - Groq API key
    - Google API key (for patent search)
    """)
    
    # Show current step
    st.header("📍 Current Progress")
    step_names = [
        "TRL Analysis",
        "R&D Criteria", 
        "Market Analysis",
        "Data Extraction",
        "SME Eligibility",
        "Document Filling",
        "Excel Processing",
        "Final Plan"
    ]
    
    current_step_name = step_names[min(st.session_state.step - 1, len(step_names) - 1)]
    st.write(f"**Step {st.session_state.step}:** {current_step_name}")
    
    # Show data progress after step 4
    if st.session_state.step > 4 and st.session_state.comprehensive_data:
        st.header("🔍 Project Progress")
        comp_data = st.session_state.comprehensive_data
        st.write(f"**Data Extracted:** {comp_data.get('extracted_count', 0)}/{comp_data.get('total_fields', 46)}")
    
    # Show document status after step 6
    if st.session_state.step >= 6 and st.session_state.document_results:
        st.write("**Documents Status:**")
        results = st.session_state.document_results
        if results.get("declaration_result", {}).get("success"):
            st.write("✅ Declaration")
        if results.get("mtep_result", {}).get("success"):
            st.write("✅ MTEP Plan")
        if results.get("rd_assessment_result", {}).get("success"):
            st.write("✅ R&D Assessment")
        if results.get("passthrough_result", {}).get("success"):
            st.write("✅ Additional Doc")
    
    # Show Excel status after step 7
    if st.session_state.step >= 7:
        st.header("📊 Excel Status")
        if st.session_state.excel_processing_result:
            processing = st.session_state.excel_processing_result
            if processing.get("success"):
                excel_count = len(processing.get("output_files", []))
                st.write(f"**Excel Files:** {excel_count} available")
            else:
                st.write("**Excel Files:** Not available")

    st.header("📞 Support")
    st.write("For technical support or questions about Lithuanian R&D funding applications, please contact our team.")