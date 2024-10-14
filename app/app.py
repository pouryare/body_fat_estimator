import streamlit as st
import joblib
import pandas as pd
import os

# Set page config (must be the first Streamlit command)
st.set_page_config(page_title="Body Fat Estimator", page_icon="❤️", layout="wide")

# Load the model
@st.cache_resource
def load_model():
    model_path = os.path.join(os.getcwd(), 'lr.joblib')
    return joblib.load(model_path)

model = load_model()

# Title
st.title("Body Fat Estimator")

# Sidebar with summary information
st.sidebar.header("About This Estimator")
st.sidebar.markdown("""
This tool estimates body fat percentage using key body measurements. 
It's based on a study of 252 men and uses multiple regression techniques.

Key measurements used:
1. Body density
2. Abdomen circumference
3. Chest circumference
4. Weight
5. Hip circumference

For more detailed information, click the 'Learn More' button below.
""")

# Main content
col1, col2 = st.columns([3, 2])

with col1:
    st.header("Enter Your Measurements")

    density = st.number_input("Density determined from underwater weighing (g/cm³)", min_value=0.0, max_value=2.0, value=1.0, step=0.001)
    abdomen = st.number_input("Abdomen Circumference (cm)", min_value=0.0, max_value=200.0, value=90.0, step=0.1)
    chest = st.number_input("Chest Circumference (cm)", min_value=0.0, max_value=200.0, value=100.0, step=0.1)
    weight = st.number_input("Weight (lbs)", min_value=0.0, max_value=500.0, value=150.0, step=0.1)
    hip = st.number_input("Hip Circumference (cm)", min_value=0.0, max_value=200.0, value=95.0, step=0.1)

    if st.button("Estimate Body Fat Percentage"):
        input_features = pd.DataFrame([[density, abdomen, chest, weight, hip]], 
                                      columns=['Density', 'Abdomen', 'Chest', 'Weight', 'Hip'])
        prediction = model.predict(input_features)[0].round(2)
        st.success(f"Estimated Body Fat Percentage: {prediction}%")

with col2:
    st.header("Understanding Body Fat Percentage")
    st.markdown("""
    General guide to body fat percentages:
    - **Essential fat:** 2-5% (men), 10-13% (women)
    - **Athletes:** 6-13% (men), 14-20% (women)
    - **Fitness:** 14-17% (men), 21-24% (women)
    - **Average:** 18-24% (men), 25-31% (women)
    - **Obese:** 25%+ (men), 32%+ (women)

    Note: This is a general guide. Individual health can vary.
    """)

# Detailed information (hidden by default)
detailed_info = """
### More Details on Body Fat Estimation

The body fat percentage is estimated using body density. The body is assumed to consist of lean tissue and fat tissue.

Key equations:
- D = 1/[(A/a) + (B/b)]
- B = (1/D)*[ab/(a-b)] - [b/(a-b)]
- Body Fat % = 495/D - 450

Where:
- D = Body Density (gm/cm³)
- A = proportion of lean body tissue
- B = proportion of fat tissue
- a = density of lean body tissue (1.10 gm/cm³)
- b = density of fat tissue (0.90 gm/cm³)

### References

1. Bailey, C. (1994). Smart Exercise: Burning Fat, Getting Fit.
2. Behnke, A.R. and Wilmore, J.H. (1974). Evaluation and Regulation of Body Build and Composition.
3. Siri, W.E. (1956). Gross composition of the body.
4. Katch, F. and McArdle, W. (1977). Nutrition, Weight Control, and Exercise.
5. Wilmore, J. (1976). Athletic Training and Physical Fitness: Physiological Principles of the Conditioning Process.

This estimator is based on the study by K.W. Penrose, A.G. Nelson, and A.G. Fisher, 
published in Medicine and Science in Sports and Exercise, vol. 17, no. 2, April 1985.
"""

if st.button("Learn More"):
    st.markdown(detailed_info)

# Footer
st.markdown("---")
st.markdown("Developed with ❤️by Pourya")