import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import base64
import shutil
from pathlib import Path

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Digital Financial Corruption Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Initialize Session State
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'auth_page' not in st.session_state:
    st.session_state.auth_page = 'login'
if 'username' not in st.session_state:
    st.session_state.username = ''
if 'dataset_uploaded' not in st.session_state:
    st.session_state.dataset_uploaded = False
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None

# --- AUTO-COPY BACKGROUND IMAGES ---

src_login = Path(r"C:\Users\Likith.N\.gemini\antigravity-ide\brain\6067dd5a-2ea1-4a0b-8801-75dd660b2346\login_background_1780286848893.png")
src_dash = Path(r"C:\Users\Likith.N\.gemini\antigravity-ide\brain\785b0cb5-90e0-46f0-baf0-bade78638b9b\dashboard_background_1780300527259.png")

dest_dir = Path("assets")
dest_dir.mkdir(exist_ok=True)

dest_login = dest_dir / "login_bg.png"
dest_dash = dest_dir / "dashboard_bg.png"

# Copy the generated backgrounds from the brain folder
if src_login.exists():
    try:
        shutil.copy(src_login, dest_login)
    except Exception:
        pass

if src_dash.exists():
    try:
        shutil.copy(src_dash, dest_dash)
    except Exception:
        pass

# --- BACKGROUND IMAGE BASE64 ENCODING ---
@st.cache_data
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

bg_style = "background-color: #080c14;"
bg_image_file = "assets/dashboard_bg.png" if st.session_state.authenticated else "assets/login_bg.png"
bg_image_path = Path(bg_image_file)

if bg_image_path.exists():
    try:
        bin_str = get_base64_of_bin_file(str(bg_image_path))
        # Applied a dynamic dark linear gradient overlay for clean premium aesthetics and high readability
        # Login page uses a slightly more transparent overlay to show off the visual asset, while the dashboard is darker for readability.
        opacity = 0.88 if st.session_state.authenticated else 0.68
        bg_style = f"""
            background-image: linear-gradient(rgba(8, 12, 20, {opacity}), rgba(8, 12, 20, {opacity})), url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        """
    except Exception:
        pass

# --- CUSTOM CSS FOR GLASSMORPHIC THEME ---
st.markdown(
    f"""
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Space+Grotesk:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        .stApp {{
            {bg_style}
            color: #ecf0f1;
            font-family: 'Outfit', sans-serif;
        }}
        .glass-card {{
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            backdrop-filter: blur(12px);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        }}
        .glass-card:hover {{
            border-color: rgba(0, 242, 254, 0.35);
            box-shadow: 0 12px 40px 0 rgba(0, 242, 254, 0.12);
            transform: translateY(-2px);
        }}
        .main-header {{
            background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            font-size: 2.5rem;
            margin-bottom: 2px;
            letter-spacing: -1px;
        }}
        .subheader {{
            color: #7f8c8d;
            font-size: 1.05rem;
            font-weight: 300;
            margin-bottom: 25px;
        }}
        .metric-lbl {{
            color: #a4b0be;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            font-weight: 600;
            margin-bottom: 5px;
        }}
        .metric-val {{
            font-size: 2rem;
            font-weight: 700;
            font-family: 'Space Grotesk', sans-serif;
            color: #ffffff;
        }}
        .metric-sub {{
            font-size: 0.8rem;
            margin-top: 4px;
        }}
        section[data-testid="stSidebar"] {{
            background-color: #04060b;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }}
        h2, h3, h4 {{
            font-family: 'Space Grotesk', sans-serif;
            color: #ffffff;
        }}
        /* Style for centered auth window */
        .auth-container {{
            max-width: 450px;
            margin: 60px auto;
            padding: 30px;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 16px;
            backdrop-filter: blur(12px);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
        }}
        
        /* Top-right Sign Out Button styling */
        span#signout-trigger {{
            display: none !important;
        }}
        div.element-container:has(span#signout-trigger) {{
            display: none !important;
        }}
        div.element-container:has(span#signout-trigger) + div.element-container {{
            position: fixed;
            top: 14px;
            right: 80px;
            z-index: 999999;
            width: auto !important;
        }}
        div.element-container:has(span#signout-trigger) + div.element-container button {{
            background-color: rgba(255, 255, 255, 0.03) !important;
            color: #ecf0f1 !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 10px !important;
            padding: 5px 14px !important;
            font-size: 0.85rem !important;
            font-weight: 500 !important;
            font-family: 'Outfit', sans-serif !important;
            backdrop-filter: blur(8px) !important;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
        }}
        div.element-container:has(span#signout-trigger) + div.element-container button:hover {{
            background-color: rgba(255, 75, 92, 0.12) !important;
            color: #ff4b5c !important;
            border-color: rgba(255, 75, 92, 0.4) !important;
            box-shadow: 0 4px 20px rgba(255, 75, 92, 0.18) !important;
            transform: translateY(-1px) !important;
        }}
        div.element-container:has(span#signout-trigger) + div.element-container button:active {{
            transform: translateY(1px) !important;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- USER AUTHENTICATION DATABASE LOGIC ---
def load_users():
    path = Path("data/users.json")
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        default_admin = {
            "admin": {
                "password": "password123",
                "security_question": "What is your favorite color?",
                "security_answer": "blue"
            }
        }
        with open(path, 'w') as f:
            json.dump(default_admin, f, indent=2)
    with open(path, 'r') as f:
        return json.load(f)

def save_users(users):
    path = Path("data/users.json")
    with open(path, 'w') as f:
        json.dump(users, f, indent=2)

# Auth Page Rendering Gate
if not st.session_state.authenticated:
    users = load_users()
    
    col_left, col_center, col_right = st.columns([1.5, 2, 1.5])
    
    with col_center:
        st.markdown('<div style="height: 60px;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="main-header" style="text-align:center; font-size: 1.8rem; margin-bottom: 5px;">Digital Financial Corruption Analysis</div>', unsafe_allow_html=True)
        
        if st.session_state.auth_page == 'login':
            st.markdown('<div class="subheader" style="text-align:center; font-size: 0.9rem; margin-bottom: 25px;">Sign in to access secure dashboard</div>', unsafe_allow_html=True)
            
            with st.form("login_form"):
                user_input = st.text_input("Username").strip()
                pass_input = st.text_input("Password", type="password")
                btn_login = st.form_submit_button("Sign In", use_container_width=True)
                
                if btn_login:
                    if user_input in users and users[user_input]['password'] == pass_input:
                        st.session_state.authenticated = True
                        st.session_state.username = user_input
                        st.rerun()
                    else:
                        st.error("Invalid Username or Password")
            
            col_nav1, col_nav2 = st.columns(2)
            with col_nav1:
                if st.button("Create an Account", use_container_width=True):
                    st.session_state.auth_page = 'signup'
                    st.rerun()
            with col_nav2:
                if st.button("Forgot Password?", use_container_width=True):
                    st.session_state.auth_page = 'forgot_password'
                    st.rerun()
                    
        elif st.session_state.auth_page == 'signup':
            st.markdown('<div class="subheader" style="text-align:center; font-size: 0.9rem; margin-bottom: 25px;">Register a new analyst account</div>', unsafe_allow_html=True)
            
            with st.form("signup_form"):
                new_user = st.text_input("Choose Username").strip()
                new_pass = st.text_input("Choose Password", type="password")
                confirm_pass = st.text_input("Confirm Password", type="password")
                sec_q = st.selectbox(
                    "Select Password Recovery Question",
                    options=[
                        "What is your mother's maiden name?",
                        "What was the name of your first pet?",
                        "What city were you born in?",
                        "What was your high school name?"
                    ]
                )
                sec_a = st.text_input("Security Answer").strip().lower()
                btn_register = st.form_submit_button("Create Account", use_container_width=True)
                
                if btn_register:
                    if not new_user or not new_pass or not sec_a:
                        st.error("All fields are required")
                    elif new_user in users:
                        st.error("Username already registered")
                    elif new_pass != confirm_pass:
                        st.error("Passwords do not match")
                    else:
                        users[new_user] = {
                            "password": new_pass,
                            "security_question": sec_q,
                            "security_answer": sec_a
                        }
                        save_users(users)
                        st.success("Account created successfully! Click below to Sign In.")
                        st.session_state.auth_page = 'login'
                        st.rerun()
                
            if st.button("Back to Sign In", use_container_width=True):
                st.session_state.auth_page = 'login'
                st.rerun()
                
        elif st.session_state.auth_page == 'forgot_password':
            st.markdown('<div class="subheader" style="text-align:center; font-size: 0.9rem; margin-bottom: 25px;">Recover Account Password</div>', unsafe_allow_html=True)
            
            recover_user = st.text_input("Enter your Username").strip()
            
            if recover_user:
                if recover_user in users:
                    q = users[recover_user]['security_question']
                    st.info(f"Question: **{q}**")
                    
                    with st.form("reset_form"):
                        a_attempt = st.text_input("Enter Answer").strip().lower()
                        n_pass = st.text_input("New Password", type="password")
                        c_pass = st.text_input("Confirm New Password", type="password")
                        btn_reset = st.form_submit_button("Reset Password", use_container_width=True)
                        
                        if btn_reset:
                            if users[recover_user]['security_answer'] == a_attempt:
                                if n_pass == c_pass:
                                    if n_pass:
                                        users[recover_user]['password'] = n_pass
                                        save_users(users)
                                        st.success("Password reset completed successfully!")
                                        st.session_state.auth_page = 'login'
                                        st.rerun()
                                    else:
                                        st.error("Password cannot be empty")
                                else:
                                    st.error("Passwords do not match")
                            else:
                                st.error("Incorrect security answer")
                else:
                    st.error("Username not registered")
                
            if st.button("Back to Sign In", use_container_width=True):
                st.session_state.auth_page = 'login'
                st.rerun()
                
    st.stop()

# --- TOP-RIGHT SIGN OUT BUTTON ---
if st.session_state.authenticated:
    st.markdown('<span id="signout-trigger"></span>', unsafe_allow_html=True)
    if st.button("Sign Out", key="top_signout"):
        st.session_state.authenticated = False
        st.session_state.username = ''
        st.session_state.dataset_uploaded = False
        st.session_state.uploaded_data = None
        st.rerun()

# --- DATASET UPLOADER GATE ---
if st.session_state.authenticated and not st.session_state.dataset_uploaded:
    col_l, col_c, col_r = st.columns([1.3, 2.4, 1.3])
    
    with col_c:
        st.markdown('<div style="height: 60px;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="main-header" style="text-align:center; font-size: 1.8rem; margin-bottom: 5px;">Digital Financial Corruption Analysis</div>', unsafe_allow_html=True)
        st.markdown('<div class="subheader" style="text-align:center; font-size: 0.9rem; margin-bottom: 25px;">Please upload the transaction dataset to initialize the dashboard</div>', unsafe_allow_html=True)
        
        # Step 1: Download template
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### Step 1: Download Baseline Dataset")
        st.write("Click below to download the standard project dataset template to your local machine:")
        try:
            csv_path = Path("data/processed/india_corruption_state_wise.csv")
            if not csv_path.exists():
                csv_path = Path("C:/Users/Likith.N/.gemini/antigravity/scratch/financial-corruption-app/data/processed/india_corruption_state_wise.csv")
            with open(csv_path, 'r', encoding='utf-8') as f:
                csv_bytes = f.read().encode('utf-8')
            st.download_button(
                label="📥 Download Template (india_corruption_state_wise.csv)",
                data=csv_bytes,
                file_name="india_corruption_state_wise.csv",
                mime="text/csv",
                use_container_width=True
            )
        except Exception as file_err:
            st.error(f"Error loading template file: {file_err}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Step 2: Upload CSV uploader
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### Step 2: Upload Dataset CSV")
        uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
        
        if uploaded_file is not None:
            try:
                temp_df = pd.read_csv(uploaded_file)
                required_cols = ['State', 'Year', 'Total_Economic_Offences', 'Financial_Loss_Crores_INR', 'Conviction_Rate_Pct']
                missing_cols = [c for c in required_cols if c not in temp_df.columns]
                
                if missing_cols:
                    st.error(f"Invalid columns! Missing required fields: {', '.join(missing_cols)}")
                else:
                    region_map = {
                        'Maharashtra': 'West', 'Gujarat': 'West',
                        'Uttar Pradesh': 'North', 'Delhi': 'North', 'Punjab': 'North', 'Haryana': 'North', 'Rajasthan': 'North', 'Madhya Pradesh': 'North',
                        'Karnataka': 'South', 'Tamil Nadu': 'South', 'Andhra Pradesh': 'South', 'Telangana': 'South', 'Kerala': 'South',
                        'West Bengal': 'East', 'Bihar': 'East', 'Odisha': 'East', 'Assam': 'East'
                    }
                    temp_df['Region'] = temp_df['State'].map(region_map)
                    
                    st.session_state.uploaded_data = temp_df
                    st.session_state.dataset_uploaded = True
                    st.success("Dataset loaded successfully!")
                    st.rerun()
            except Exception as upload_err:
                st.error(f"Error reading CSV: {upload_err}")
        st.markdown('</div>', unsafe_allow_html=True)
            
    st.stop()

# --- ASSIGN DYNAMIC DATAFRAME ---
df = st.session_state.uploaded_data

# --- SIDEBAR ROUTING NAVIGATION ---
st.sidebar.title("Forensic Portal")
st.sidebar.markdown(f"User: `{st.session_state.username}`")

if st.sidebar.button("🔄 Swap Dataset", use_container_width=True):
    st.session_state.dataset_uploaded = False
    st.session_state.uploaded_data = None
    st.rerun()

# Main Navigation Selectbox (The 8 Modules)
module = st.sidebar.selectbox(
    "Select Analysis Module",
    options=[
        "1. Executive Summary",
        "2. India Choropleth Map",
        "3. Crime Typologies",
        "4. State Comparison",
        "5. Judicial Performance",
        "6. Policy Sandbox",
        "7. Money Laundering Routes",
        "8. Report Export Engine"
    ]
)

# Sidebar Filter Settings (Global context)
st.sidebar.markdown("---")
st.sidebar.markdown("### Global Filters")
min_year, max_year = int(df['Year'].min()), int(df['Year'].max())
selected_years = st.sidebar.slider("Year Range", min_year, max_year, (min_year, max_year))

all_states = sorted(df['State'].unique())
selected_states = st.sidebar.multiselect("Filter States", options=all_states, default=all_states)

# Filter Dataframe
if not selected_states:
    filtered_df = df[(df['Year'] >= selected_years[0]) & (df['Year'] <= selected_years[1])]
else:
    filtered_df = df[
        (df['State'].isin(selected_states)) &
        (df['Year'] >= selected_years[0]) &
        (df['Year'] <= selected_years[1])
    ]

# Common Metrics Calculations
total_cases = filtered_df['Total_Economic_Offences'].sum()
total_loss = filtered_df['Financial_Loss_Crores_INR'].sum()
avg_conviction = filtered_df['Conviction_Rate_Pct'].mean()
total_cyber = filtered_df['Cyber_Fraud_Cases'].sum()

# Helper to render custom metric cards
def render_metric_cards():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="glass-card"><div class="metric-lbl">Economic Offences</div><div class="metric-val">{total_cases:,}</div><div class="metric-sub" style="color:#3498db;">Registered cases</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="glass-card"><div class="metric-lbl">Financial Loss</div><div class="metric-val">₹{total_loss:,.1f} Cr</div><div class="metric-sub" style="color:#e74c3c;">Asset leakage</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="glass-card"><div class="metric-lbl">Avg Conviction Rate</div><div class="metric-val">{avg_conviction:.1f}%</div><div class="metric-sub" style="color:#2ecc71;">Judicial prosecution</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="glass-card"><div class="metric-lbl">Cyber Fraud</div><div class="metric-val">{total_cyber:,}</div><div class="metric-sub" style="color:#e67e22;">Digital-based cases</div></div>', unsafe_allow_html=True)

# ==============================================================================
# MODULE 1: EXECUTIVE SUMMARY
# ==============================================================================
if module == "1. Executive Summary":
    st.markdown('<div class="main-header">National Executive Summary</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">High-level national overview of economic offenses and prosecution statistics.</div>', unsafe_allow_html=True)
    
    render_metric_cards()
    
    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.markdown("### National Temporal Caseload Analysis")
        yearly_sums = filtered_df.groupby('Year')[['Total_Economic_Offences', 'Financial_Loss_Crores_INR']].sum().reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=yearly_sums['Year'], y=yearly_sums['Total_Economic_Offences'], name='Cases Registered', yaxis='y1', line=dict(color='#00f2fe', width=3)))
        fig.add_trace(go.Bar(x=yearly_sums['Year'], y=yearly_sums['Financial_Loss_Crores_INR'], name='Financial Loss (Cr)', yaxis='y2', opacity=0.3, marker_color='#ff5252'))
        
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(title=dict(text='Total Offences Registered', font=dict(color='#00f2fe')), tickfont=dict(color='#00f2fe')),
            yaxis2=dict(title=dict(text='Financial Loss (Crores ₹)', font=dict(color='#ff5252')), tickfont=dict(color='#ff5252'), overlaying='y', side='right'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col_right:
        st.markdown("### Strategic Analysis Report")
        st.write(
            f"Based on your selection representing years **{selected_years[0]} to {selected_years[1]}**, "
            f"India registered a cumulative total of **{total_cases:,} economic offenses** across the monitored states. "
            f"This has resulted in an estimated financial drainage of **₹{total_loss:,.2f} Crores**."
        )
        st.write(
            f"The judicial system achieved an average conviction rate of **{avg_conviction:.2f}%** in economic offences, "
            f"indicating strong variance in law enforcement effectiveness between states."
        )
        st.write(
            f"Notably, digital fraud accounts for **{(total_cyber/max(1, total_cases))*100:.1f}%** of the total crime portfolio, "
            f"demanding a structural shift from physical vigilance to digital infrastructure auditing."
        )

# ==============================================================================
# MODULE 2: INDIA CHOROPLETH MAP
# ==============================================================================
elif module == "2. India Choropleth Map":
    st.markdown('<div class="main-header">India Choropleth Map</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Interactive geographical visualization of financial losses and registered crimes across Indian states.</div>', unsafe_allow_html=True)
    
    col_map1, col_map2 = st.columns([2, 1])
    
    with col_map1:
        st.markdown("### Geographical Risk Heatmap")
        try:
            with open("data/india_states.geojson", 'r', encoding='utf-8') as f:
                india_geojson = json.load(f)
            
            # Prepare map data
            df_map = filtered_df.groupby('State')[['Financial_Loss_Crores_INR', 'Total_Economic_Offences']].mean().reset_index()
            # Map Delhi to NCT of Delhi
            df_map['State'] = df_map['State'].replace({'Delhi': 'NCT of Delhi'})
            
            fig_map = px.choropleth(
                df_map,
                geojson=india_geojson,
                featureidkey="properties.ST_NM",
                locations="State",
                color="Financial_Loss_Crores_INR",
                color_continuous_scale="Reds",
                range_color=(0, df_map['Financial_Loss_Crores_INR'].max()),
                labels={'Financial_Loss_Crores_INR': 'Avg Loss (₹ Cr)'},
                template="plotly_dark"
            )
            fig_map.update_geos(fitbounds="locations", visible=False)
            fig_map.update_layout(
                margin={"r":0,"t":0,"l":0,"b":0},
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_map, use_container_width=True)
        except Exception as map_err:
            st.error(f"Error rendering map: {map_err}")
            st.info("Check your map GeoJSON data under data/india_states.geojson.")
            
    with col_map2:
        st.markdown("### State Heat Index Ranking")
        state_ranking = filtered_df.groupby('State')[['Financial_Loss_Crores_INR', 'Total_Economic_Offences']].sum().reset_index()
        state_ranking = state_ranking.sort_values(by='Financial_Loss_Crores_INR', ascending=False)
        
        st.dataframe(
            state_ranking,
            column_config={
                "State": "State Name",
                "Financial_Loss_Crores_INR": st.column_config.NumberColumn("Total Loss (₹ Cr)", format="₹%.1f Cr"),
                "Total_Economic_Offences": st.column_config.NumberColumn("Total Cases", format="%d")
            },
            hide_index=True,
            use_container_width=True
        )

# ==============================================================================
# MODULE 3: CRIME TYPOLOGIES
# ==============================================================================
elif module == "3. Crime Typologies":
    st.markdown('<div class="main-header">Crime Typology Drilldown</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Investigating trends, velocities, and correlations of specific financial crime categories.</div>', unsafe_allow_html=True)
    
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        st.markdown("### Year-on-Year Growth comparison")
        yearly_crime = filtered_df.groupby('Year')[['Corruption_Cases', 'Cheating_Fraud_Cases', 'Forgery_Cases', 'Cyber_Fraud_Cases']].sum().reset_index()
        
        # Melt dataframe to make it easy to plot in express
        melted_df = pd.melt(
            yearly_crime, 
            id_vars=['Year'], 
            value_vars=['Corruption_Cases', 'Cheating_Fraud_Cases', 'Forgery_Cases', 'Cyber_Fraud_Cases'],
            var_name='Crime Head',
            value_name='Cases'
        )
        fig_growth = px.line(melted_df, x='Year', y='Cases', color='Crime Head', template='plotly_dark')
        fig_growth.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_growth, use_container_width=True)
        
    with col_t2:
        st.markdown("### Correlation Heatmap (Crime Categories)")
        corr_matrix = filtered_df[['Corruption_Cases', 'Cheating_Fraud_Cases', 'Forgery_Cases', 'Cyber_Fraud_Cases', 'Financial_Loss_Crores_INR']].corr()
        
        fig_corr = px.imshow(
            corr_matrix,
            text_auto=True,
            color_continuous_scale='RdBu_r',
            aspect="auto",
            template='plotly_dark'
        )
        fig_corr.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_corr, use_container_width=True)

# ==============================================================================
# MODULE 4: STATE COMPARISON
# ==============================================================================
elif module == "4. State Comparison":
    st.markdown('<div class="main-header">State-by-State Comparative Matrix</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Side-by-side benchmarking of regional corruption metrics and caseloads.</div>', unsafe_allow_html=True)
    
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        state_a = st.selectbox("Select Benchmark State (State A)", options=all_states, index=0)
    with col_sel2:
        state_b = st.selectbox("Select Comparison State (State B)", options=all_states, index=1 if len(all_states) > 1 else 0)
        
    if state_a and state_b:
        df_a = filtered_df[filtered_df['State'] == state_a].sort_values('Year')
        df_b = filtered_df[filtered_df['State'] == state_b].sort_values('Year')
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown(
                f"""
                <div class="glass-card">
                    <h3>🏛️ {state_a} Profile</h3>
                    <p><b>Average Annual Cases:</b> {int(df_a['Total_Economic_Offences'].mean()):,}</p>
                    <p><b>Average Annual Loss:</b> ₹{df_a['Financial_Loss_Crores_INR'].mean():,.1f} Cr</p>
                    <p><b>Avg Prosecution Rate:</b> {df_a['Conviction_Rate_Pct'].mean():.1f}%</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col_c2:
            st.markdown(
                f"""
                <div class="glass-card">
                    <h3>🏛️ {state_b} Profile</h3>
                    <p><b>Average Annual Cases:</b> {int(df_b['Total_Economic_Offences'].mean()):,}</p>
                    <p><b>Average Annual Loss:</b> ₹{df_b['Financial_Loss_Crores_INR'].mean():,.1f} Cr</p>
                    <p><b>Avg Prosecution Rate:</b> {df_b['Conviction_Rate_Pct'].mean():.1f}%</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        fig_compare = go.Figure()
        fig_compare.add_trace(go.Bar(x=df_a['Year'], y=df_a['Financial_Loss_Crores_INR'], name=f"{state_a} Loss (₹ Cr)", marker_color='#00f2fe'))
        fig_compare.add_trace(go.Bar(x=df_b['Year'], y=df_b['Financial_Loss_Crores_INR'], name=f"{state_b} Loss (₹ Cr)", marker_color='#ffab40'))
        
        fig_compare.update_layout(
            barmode='group',
            title="Year-on-Year Financial Loss Comparison",
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_compare, use_container_width=True)

# ==============================================================================
# MODULE 5: JUDICIAL PERFORMANCE
# ==============================================================================
elif module == "5. Judicial Performance":
    st.markdown('<div class="main-header">Judicial Performance & Prosecution Audit</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Analyzing state enforcement capability and judicial outcomes for financial corruption.</div>', unsafe_allow_html=True)
    
    col_j1, col_j2 = st.columns(2)
    
    with col_j1:
        st.markdown("### Conviction Rate vs Case Volume")
        # Aggregated state stats
        state_stats = filtered_df.groupby('State')[['Conviction_Rate_Pct', 'Total_Economic_Offences', 'Financial_Loss_Crores_INR']].mean().reset_index()
        
        fig_scatter = px.scatter(
            state_stats,
            x='Conviction_Rate_Pct',
            y='Total_Economic_Offences',
            size='Financial_Loss_Crores_INR',
            color='State',
            hover_name='State',
            template='plotly_dark',
            labels={'Conviction_Rate_Pct': 'Average Conviction Rate (%)', 'Total_Economic_Offences': 'Average Annual Cases'}
        )
        fig_scatter.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with col_j2:
        st.markdown("### Conviction Rate Chronology")
        conviction_year = filtered_df.groupby('Year')['Conviction_Rate_Pct'].mean().reset_index()
        
        fig_conv_line = px.line(
            conviction_year,
            x='Year',
            y='Conviction_Rate_Pct',
            title='National Average Conviction Trend',
            template='plotly_dark',
            line_shape='spline'
        )
        fig_conv_line.update_traces(line=dict(color='#00e676', width=4))
        fig_conv_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_conv_line, use_container_width=True)

# ==============================================================================
# MODULE 6: POLICY SANDBOX
# ==============================================================================
elif module == "6. Policy Sandbox":
    st.markdown('<div class="main-header">Compliance & Policy Simulation Sandbox</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Configure anti-corruption policy tools to run state-specific cost-benefit simulations.</div>', unsafe_allow_html=True)
    
    # 1. State Selector for Localized Baselines
    selected_sim_state = st.selectbox("Select Target State for Simulation", options=["All India"] + all_states)
    
    if selected_sim_state == "All India":
        baseline_annual_loss = total_loss / max(1.0, float(selected_years[1] - selected_years[0] + 1))
        baseline_conviction = avg_conviction
        sim_name = "All India (Average)"
    else:
        df_sim = filtered_df[filtered_df['State'] == selected_sim_state]
        if df_sim.empty:
            df_sim = df[df['State'] == selected_sim_state]
        baseline_annual_loss = df_sim['Financial_Loss_Crores_INR'].mean()
        baseline_conviction = df_sim['Conviction_Rate_Pct'].mean()
        sim_name = selected_sim_state
        
    st.markdown(f"**Baseline Profile ({sim_name}):** Annual Loss: ₹{baseline_annual_loss:.1f} Cr | Conviction Rate: {baseline_conviction:.1f}%")
    
    col_in, col_out = st.columns([1, 2])
    
    with col_in:
        st.markdown("### Policy Resource Allocation")
        v_budget = st.slider("Police & Vigilance Action Scale (Raids & Audits)", 0, 100, 0, key="pol_vig")
        v_cyber = st.slider("Corporate & Public Cyber Security Training", 0, 100, 0, key="pol_cyb")
        v_courts = st.slider("Judicial Special Courts Capacity", 0, 100, 0, key="pol_cou")
        
    with col_out:
        # Heuristic calculations
        crime_reduction = (v_budget * 0.25) + (v_cyber * 0.45)
        conviction_increase = (v_courts * 0.35) + (v_budget * 0.15)
        
        # Financial impacts
        prevented_loss = baseline_annual_loss * (crime_reduction / 100.0) * 0.85
        
        # Policy costing model:
        # Vigilance raids scale with loss size; cyber safety and courts represent capital investments
        vigilance_cost = v_budget * (0.012 * baseline_annual_loss)
        cyber_cost = v_cyber * 0.18
        court_cost = v_courts * 0.28
        total_cost = vigilance_cost + cyber_cost + court_cost
        
        net_savings = prevented_loss - total_cost
        
        st.markdown("### Cost-Benefit Evaluation")
        
        card1, card2, card3 = st.columns(3)
        with card1:
            st.markdown(f'<div class="glass-card" style="border-color:rgba(52, 152, 219, 0.4);"><div class="metric-lbl" style="color:#3498db;">Implementation Cost</div><div class="metric-val" style="color:#3498db;">₹{total_cost:.1f} Cr</div><div class="metric-sub">Budget Requirement</div></div>', unsafe_allow_html=True)
        with card2:
            st.markdown(f'<div class="glass-card" style="border-color:rgba(46, 204, 113, 0.4);"><div class="metric-lbl" style="color:#2ecc71;">Projected Savings</div><div class="metric-val" style="color:#2ecc71;">₹{prevented_loss:.1f} Cr</div><div class="metric-sub">Prevented Leakage</div></div>', unsafe_allow_html=True)
        with card3:
            border_color = "rgba(46, 204, 113, 0.4)" if net_savings >= 0 else "rgba(255, 82, 82, 0.4)"
            text_color = "#2ecc71" if net_savings >= 0 else "#ff5252"
            label = "Net Return (ROI)" if net_savings >= 0 else "Net Deficit"
            st.markdown(f'<div class="glass-card" style="border-color:{border_color};"><div class="metric-lbl" style="color:{text_color};">{label}</div><div class="metric-val" style="color:{text_color};">₹{net_savings:.1f} Cr</div><div class="metric-sub">Capital Efficiency</div></div>', unsafe_allow_html=True)

        # Plotly visual before vs after comparison
        fig_sim_bar = go.Figure()
        fig_sim_bar.add_trace(go.Bar(
            x=['Current Annual Loss', 'Projected Post-Reform Loss'],
            y=[baseline_annual_loss, max(0.0, baseline_annual_loss - prevented_loss)],
            marker_color=['#ff5252', '#00e676'],
            width=0.35
        ))
        fig_sim_bar.update_layout(
            height=260,
            margin=dict(l=20, r=20, t=10, b=20),
            yaxis_title="Loss (Crores ₹)",
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_sim_bar, use_container_width=True)
        
        st.info(
            f"**Policy Advisory Note ({sim_name}):** Scaling anti-corruption compliance by these targets yields a net budget return "
            f"of **₹{net_savings:.1f} Crores** annually. Improving special courts raises the conviction index "
            f"from **{baseline_conviction:.1f}%** to **{min(95.0, baseline_conviction + conviction_increase):.1f}%** due to streamlined prosecution."
        )

# ==============================================================================
# MODULE 7: MONEY LAUNDERING ROUTES
# ==============================================================================
elif module == "7. Money Laundering Routes":
    st.markdown('<div class="main-header">Money Laundering & Offshore Tracker</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Mapping the outflow of digital financial assets from Indian states into global offshore tax havens.</div>', unsafe_allow_html=True)
    
    sel_state = st.selectbox("Select State Source", options=all_states)
    
    if sel_state:
        st.markdown(f"### Illicit Asset Diversion Network: {sel_state}")
        
        # Build node network points in 3D
        # Build node network points
        # State node is at (0, 0)
        # Intermediaries at (1, y)
        # Havens at (2, y)
        nodes = {
            sel_state: (0, 0, '#00f2fe', 'State Origin'),
            'Singapore Corp': (1, 1, '#ffab40', 'Intermediary Shell'),
            'Mauritius Trust': (1, -1, '#ffab40', 'Tax Treaty Conduit'),
            'Dubai Holding': (1, 0, '#ffab40', 'Free Zone Asset holding'),
            'Switzerland': (2, 1.5, '#ff5252', 'Banking Haven'),
            'Cayman Islands': (2, -1.5, '#ff5252', 'Offshore Trust'),
            'British Virgin Islands': (2, 0, '#ff5252', 'Shell Corporation')
        }
        
        edges = [
            (sel_state, 'Singapore Corp'),
            (sel_state, 'Mauritius Trust'),
            (sel_state, 'Dubai Holding'),
            ('Singapore Corp', 'Switzerland'),
            ('Singapore Corp', 'British Virgin Islands'),
            ('Mauritius Trust', 'Cayman Islands'),
            ('Dubai Holding', 'British Virgin Islands'),
            ('Dubai Holding', 'Switzerland')
        ]
        
        # Build traces
        edge_x = []
        edge_y = []
        for edge in edges:
            x0, y0 = nodes[edge[0]][0], nodes[edge[0]][1]
            x1, y1 = nodes[edge[1]][0], nodes[edge[1]][1]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1.5, color='rgba(255,255,255,0.2)'),
            hoverinfo='none',
            mode='lines'
        )
        
        node_x = []
        node_y = []
        node_color = []
        node_text = []
        for name, (x, y, color, role) in nodes.items():
            node_x.append(x)
            node_y.append(y)
            node_color.append(color)
            node_text.append(f"<b>{name}</b><br>Type: {role}")
            
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=[n for n in nodes.keys()],
            textposition="top center",
            hovertext=node_text,
            marker=dict(
                color=node_color,
                size=22,
                line=dict(width=2, color='#ffffff')
            )
        )
        
        fig_net = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                template='plotly_dark',
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20, l=5, r=5, t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
        )
        st.plotly_chart(fig_net, use_container_width=True)

# ==============================================================================
# MODULE 8: REPORT EXPORT ENGINE
# ==============================================================================
elif module == "8. Report Export Engine":
    st.markdown('<div class="main-header">Automated Report Export Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Generate print-ready markdown summaries and custom CSV compilations of filtered records.</div>', unsafe_allow_html=True)
    
    st.markdown("### Preview Export Data")
    st.write(f"The export matches the active filters: **{len(filtered_df)} records** selected.")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        # CSV Downloader
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="💾 Download Filtered Dataset (CSV)",
            data=csv_data,
            file_name="filtered_corruption_data.csv",
            mime="text/csv",
            use_container_width=True
        )
    with col_e2:
        # Markdown summary report content
        report_md = f"""# Executive Forensic Report
Generated on: 2026-05-28

## Selection Summary
* **Analyzed Period:** {selected_years[0]} - {selected_years[1]}
* **States Monitored:** {len(selected_states)} states
* **Total Registered Economic Offences:** {total_cases:,}
* **Total Financial Value Lost:** ₹{total_loss:,.1f} Crores
* **Average Conviction Rate:** {avg_conviction:.1f}%
* **Total Cyber-Financial Frauds:** {total_cyber:,}
"""
        st.download_button(
            label="📄 Download Executive Summary (Markdown)",
            data=report_md,
            file_name="corruption_analysis_summary.md",
            mime="text/markdown",
            use_container_width=True
        )
        
    st.success("Data export compilation complete. Select buttons above to download assets.")
