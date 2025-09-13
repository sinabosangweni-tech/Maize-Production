import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import io
import time
import base64

# Page configuration
st.set_page_config(
    page_title="Maize Production Predictor",
    page_icon="🌽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E8B57;
        text-align: center;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #3CB371;
        border-bottom: 2px solid #3CB371;
        padding-bottom: 0.5rem;
    }
    .feature-card {
        background-color: #F5F5F5;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .urgent {
        background-color: #FFE4E1;
        border-left: 5px solid #FF4500;
    }
</style>
""", unsafe_allow_html=True)

# App title
st.markdown('<h1 class="main-header">🌽 Maize Production Prediction System</h1>', unsafe_allow_html=True)

# In-memory storage for messages
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Production Prediction", "Farmer Communication", "Model Analysis"])

# Load sample data
@st.cache_data
def load_sample_data():
    features = ['AREA.PLTD', 'MAIZE.YLD', 'FOOD.PROD.INX', 'CPI.INX.10', 'LAND.CER.HA', 
                'CER.PROD.MT', 'SE.TOT.PERC', 'FERT.CONS.KG_HA', 'CFW.TOT.PERC', 
                'ANS.PEM.DMG.PERC', 'HHO.PPT.MM', 'X0NV.AGR.TOTL.ZS', 'FWW.AGRI.PERC', 
                'SHS.PPT.MM', 'REMIT.COST.PERC', 'LUB.PPT.MM', 'MZ.PPT.MM']
    
    # Create sample data for demonstration
    np.random.seed(42)
    data = {}
    for feature in features:
        if 'PPT' in feature:
            data[feature] = np.random.uniform(50, 200, 100)
        elif 'PERC' in feature:
            data[feature] = np.random.uniform(0, 100, 100)
        elif feature == 'MAIZE.YLD':
            data[feature] = np.random.uniform(1.5, 4.5, 100)
        elif feature == 'AREA.PLTD':
            data[feature] = np.random.uniform(1000, 5000, 100)
        else:
            data[feature] = np.random.uniform(10, 500, 100)
    
    return pd.DataFrame(data)

sample_data = load_sample_data()

# Model prediction function
def predict_production(input_data):
    """Make a production prediction based on input features"""
    prediction = (
        0.4 * input_data.get('AREA.PLTD', 0) +
        0.3 * input_data.get('MAIZE.YLD', 0) +
        0.1 * input_data.get('CER.PROD.MT', 0) +
        0.05 * input_data.get('FERT.CONS.KG_HA', 0) +
        0.05 * input_data.get('MZ.PPT.MM', 0) +
        np.random.normal(0, 50)  # Add some randomness
    )
    
    return max(0, prediction)  # Ensure non-negative prediction

def explain_prediction(input_data):
    """Generate explanation for a prediction"""
    # Calculate feature contributions (simplified)
    contributions = {
        'AREA.PLTD': 0.4 * input_data.get('AREA.PLTD', 0),
        'MAIZE.YLD': 0.3 * input_data.get('MAIZE.YLD', 0),
        'CER.PROD.MT': 0.1 * input_data.get('CER.PROD.MT', 0),
        'FERT.CONS.KG_HA': 0.05 * input_data.get('FERT.CONS.KG_HA', 0),
        'MZ.PPT.MM': 0.05 * input_data.get('MZ.PPT.MM', 0)
    }
    
    return contributions

if page == "Dashboard":
    st.markdown('<h2 class="sub-header">Dashboard Overview</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Predicted Production", "2,450 MT", "5%")
    
    with col2:
        st.metric("Current Yield", "3.2 MT/Ha", "2%")
    
    with col3:
        st.metric("Planted Area", "3,200 Ha", "3%")
    
    # Recent predictions chart
    st.subheader("Production Trends")
    trend_data = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'Production': [2100, 2250, 2350, 2450, 2500, 2550],
        'Prediction': [2200, 2300, 2400, 2450, 2550, 2600]
    })
    
    st.line_chart(trend_data.set_index('Month'))
    
    # Feature importance
    st.subheader("Top Influential Features")
    feature_importance = pd.DataFrame({
        'Feature': ['AREA.PLTD', 'MAIZE.YLD', 'FOOD.PROD.INX', 'CPI.INX.10', 'LAND.CER.HA'],
        'Importance': [0.37, 0.23, 0.21, 0.18, 0.16]
    })
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Importance', y='Feature', data=feature_importance, ax=ax)
    ax.set_title('Feature Importance for Production Prediction')
    st.pyplot(fig)

elif page == "Production Prediction":
    st.markdown('<h2 class="sub-header">Production Prediction</h2>', unsafe_allow_html=True)
    
    st.info("Adjust the feature values below to get a production prediction")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        area_pltd = st.slider('Area Planted (Ha)', 1000, 5000, 3200)
        maize_yld = st.slider('Maize Yield (MT/Ha)', 1.5, 4.5, 3.2)
        food_prod_inx = st.slider('Food Production Index', 80, 120, 100)
    
    with col2:
        cpi_inx = st.slider('Consumer Price Index', 80, 120, 100)
        land_cer_ha = st.slider('Land for Cereals (Ha)', 1000, 5000, 3200)
        cer_prod_mt = st.slider('Cereal Production (MT)', 2000, 6000, 4000)
    
    with col3:
        fert_cons = st.slider('Fertilizer Consumption (Kg/Ha)', 50, 200, 120)
        precipitation = st.slider('Precipitation (mm)', 50, 200, 120)
        temp = st.slider('Average Temperature (°C)', 20, 30, 25)
    
    if st.button('Predict Production'):
        with st.spinner('Making prediction...'):
            # Create input data
            input_data = {
                'AREA.PLTD': area_pltd,
                'MAIZE.YLD': maize_yld,
                'FOOD.PROD.INX': food_prod_inx,
                'CPI.INX.10': cpi_inx,
                'LAND.CER.HA': land_cer_ha,
                'CER.PROD.MT': cer_prod_mt,
                'FERT.CONS.KG_HA': fert_cons,
                'MZ.PPT.MM': precipitation
            }
            
            # Make prediction
            prediction = predict_production(input_data)
            
            st.success(f"Predicted Production: {prediction:.2f} MT")
            
            # Show explanation
            st.subheader("Prediction Explanation")
            explanation = explain_prediction(input_data)
            
            expl_df = pd.DataFrame.from_dict(explanation, orient='index', columns=['Contribution'])
            expl_df = expl_df.sort_values('Contribution', ascending=False)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            colors = ['green' if x > 0 else 'red' for x in expl_df['Contribution']]
            ax.barh(expl_df.index, expl_df['Contribution'], color=colors)
            ax.set_xlabel('Contribution to Prediction')
            ax.set_title('Feature Contributions to Production Prediction')
            st.pyplot(fig)

elif page == "Farmer Communication":
    st.markdown('<h2 class="sub-header">Farmer Communication Portal</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Send Message", "Message History", "Officer Dashboard"])
    
    with tab1:
        st.subheader("Send Message to Extension Officer")
        
        farmer_id = st.text_input("Farmer ID")
        message_type = st.selectbox("Message Type", ["Pest Issue", "Growth Update", "Soil Problem", "General Inquiry"])
        priority = st.selectbox("Priority", ["Normal", "Urgent"])
        
        # Voice recording (simulated in Colab)
        st.write("Voice Message Recording")
        if st.button("Start Recording"):
            st.info("Recording... (simulated in demo)")
            time.sleep(2)
            st.success("Recording complete!")
        
        # Photo upload
        uploaded_photo = st.file_uploader("Upload Field Photo", type=['jpg', 'jpeg', 'png'])
        if uploaded_photo is not None:
            image = Image.open(uploaded_photo)
            st.image(image, caption="Uploaded Field Photo", use_column_width=True)
        
        # Additional details
        additional_info = st.text_area("Additional Details")
        
        if st.button("Send Message"):
            if not farmer_id:
                st.error("Please enter your Farmer ID")
            else:
                # Save the message
                message_data = {
                    'farmer_id': farmer_id,
                    'type': message_type,
                    'priority': priority,
                    'photo': uploaded_photo is not None,
                    'message': additional_info,
                    'timestamp': pd.Timestamp.now()
                }
                
                st.session_state.messages.append(message_data)
                st.success("Message sent successfully!")
    
    with tab2:
        st.subheader("Message History")
        
        # Display message history
        messages = st.session_state.messages
        
        if not messages:
            st.info("No messages yet.")
        else:
            for msg in messages:
                urgency_class = "urgent" if msg['priority'] == 'Urgent' else ""
                st.markdown(f"""
                <div class="feature-card {urgency_class}">
                    <strong>{msg['type']}</strong> ({msg['priority']}) - {msg['timestamp']}
                    <p>{msg['message']}</p>
                    <small>Farmer ID: {msg['farmer_id']}</small>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        st.subheader("Extension Officer Dashboard")
        st.info("This view is for extension officers to monitor farmer messages")
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            filter_priority = st.selectbox("Filter by Priority", ["All", "Normal", "Urgent"])
        with col2:
            filter_type = st.selectbox("Filter by Type", ["All", "Pest Issue", "Growth Update", "Soil Problem", "General Inquiry"])
        
        # Display filtered messages
        filtered_messages = st.session_state.messages.copy()
        
        if filter_priority != "All":
            filtered_messages = [m for m in filtered_messages if m['priority'] == filter_priority]
        
        if filter_type != "All":
            filtered_messages = [m for m in filtered_messages if m['type'] == filter_type]
        
        if not filtered_messages:
            st.info("No messages match your filters.")
        else:
            for msg in filtered_messages:
                urgency_class = "urgent" if msg['priority'] == 'Urgent' else ""
                st.markdown(f"""
                <div class="feature-card {urgency_class}">
                    <strong>{msg['type']}</strong> ({msg['priority']}) - {msg['timestamp']}
                    <p>{msg['message']}</p>
                    <small>Farmer ID: {msg['farmer_id']}</small>
                    <div style="margin-top: 10px;">
                        <button style="background-color: #4CAF50; color: white; border: none; padding: 5px 10px; border-radius: 4px;">Respond</button>
                        <button style="background-color: #f44336; color: white; border: none; padding: 5px 10px; border-radius: 4px; margin-left: 5px;">Mark as Resolved</button>
                    </div>
                </div>
                """, unsafe_allow_html=True)

elif page == "Model Analysis":
    st.markdown('<h2 class="sub-header">Model Analysis & Insights</h2>', unsafe_allow_html=True)
    
    st.subheader("SHAP Analysis Results")
    st.write("""
    The SHAP analysis reveals the most important features influencing maize production predictions:
    """)
    
    # SHAP summary plot (simulated)
    features = ['AREA.PLTD', 'MAIZE.YLD', 'FOOD.PROD.INX', 'CPI.INX.10', 'LAND.CER.HA',
               'CER.PROD.MT', 'SE.TOT.PERC', 'FERT.CONS.KG_HA', 'CFW.TOT.PERC']
    shap_values = [0.37, 0.23, -0.21, -0.18, 0.16, 0.15, 0.13, 0.12, 0.07]
    
    fig, ax = plt.subplots(figsize=(10, 8))
    y_pos = np.arange(len(features))
    colors = ['green' if x > 0 else 'red' for x in shap_values]
    ax.barh(y_pos, shap_values, color=colors)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(features)
    ax.set_xlabel('SHAP Value (Impact on Model Output)')
    ax.set_title('Feature Importance based on SHAP Values')
    st.pyplot(fig)
    
    st.subheader("LIME Explanation for a Sample Prediction")
    st.write("""
    LIME explains individual predictions by highlighting the most influential features:
    """)
    
    # Sample LIME explanation
    sample_prediction = {
        'features': ['AREA.PLTD', 'MAIZE.YLD', 'FERT.CONS.KG_HA', 'CPI.INX.10', 'MZ.PPT.MM'],
        'values': [3200, 3.2, 120, 105, 120],
        'contributions': [1280, 960, 60, -189, 60]
    }
    
    lime_df = pd.DataFrame(sample_prediction)
    lime_df = lime_df.sort_values('contributions', key=abs, ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['green' if x > 0 else 'red' for x in lime_df['contributions']]
    ax.barh(lime_df['features'], lime_df['contributions'], color=colors)
    ax.set_xlabel('Contribution to Prediction')
    ax.set_title('LIME Explanation for a Sample Prediction')
    st.pyplot(fig)
    
    st.subheader("Model Performance Metrics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("RMSE", "30.45", "-26.6%")
    
    with col2:
        st.metric("MAE", "8.86", "-55.8%")
    
    with col3:
        st.metric("R² Score", "0.98", "+1.9%")

if __name__ == "__main__":
    # This is needed for Streamlit to run properly
    pass
