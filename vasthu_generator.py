import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# --- 1. CONFIGURATION & VASTU RULES (Cacheable Resources) ---

# @st.cache_resource is typically used for ML models/heavy objects, but can be used 
# here to ensure constants are loaded only once, improving app startup time slightly.
@st.cache_resource
def get_vastu_constants():
    """Defines Vastu constants and rules, cached as a resource."""
    ROOM_RULES = {
        'Kitchen': 'SE',
        'Master Bedroom': 'SW',
        'Pooja Room': 'NE',
        'Toilet': 'NW'
    }
    MIN_DIMS = {
        'Kitchen': (10, 8),
        'Master Bedroom': (12, 14),
        'Pooja Room': (6, 6),
        'Toilet': (5, 7),
        'Bedroom 2': (10, 10),
        'Bedroom 3': (10, 10),
        'Living Room': (15, 12)
    }
    return ROOM_RULES, MIN_DIMS

ROOM_RULES, MIN_DIMS = get_vastu_constants()

# --- 2. PLAN GENERATION ALGORITHM (Cacheable Data) ---

# @st.cache_data ensures this function only re-runs if any of its arguments change, 
# significantly speeding up Streamlit's inherent re-run cycle when no inputs are altered.
@st.cache_data
def generate_plan_options(plot_width, plot_length, facing_direction, num_bhk):
    """
    Generates two Vastu-compliant room placement options based on plot size and rules.
    This logic is computationally simple, but caching prevents redundant execution.
    """
    plans = []
    
    # 1. Define the plot center
    center_x, center_y = plot_width / 2, plot_length / 2
    
    # --- Option 1: Traditional Focus ---
    plan_data_1 = {}
    plan_data_1['Master Bedroom'] = (plot_width * 0.25, plot_length * 0.25, MIN_DIMS['Master Bedroom'], 'SW') 
    plan_data_1['Kitchen'] = (plot_width * 0.75, plot_length * 0.25, MIN_DIMS['Kitchen'], 'SE') 
    plan_data_1['Pooja Room'] = (plot_width * 0.75, plot_length * 0.75, MIN_DIMS['Pooja Room'], 'NE') 
    plan_data_1['Toilet'] = (plot_width * 0.25, plot_length * 0.75, MIN_DIMS['Toilet'], 'NW') 
    plan_data_1['Bedroom 2'] = (plot_width * 0.50, plot_length * 0.75, MIN_DIMS['Bedroom 2'], 'N') 
    plan_data_1['Living Room'] = (center_x, plot_length * 0.50, MIN_DIMS['Living Room'], 'Center/E')
    if num_bhk == 3:
        plan_data_1['Bedroom 3'] = (plot_width * 0.50, plot_length * 0.25, MIN_DIMS['Bedroom 3'], 'S') 

    plans.append({'title': "Option 1: Traditional Layout", 'data': plan_data_1})
    
    # --- Option 2: High Flexibility (Contrasting Option) ---
    plan_data_2 = {}
    plan_data_2['Master Bedroom'] = (plot_width * 0.25, plot_length * 0.25, MIN_DIMS['Master Bedroom'], 'SW') 
    plan_data_2['Kitchen'] = (plot_width * 0.75, plot_length * 0.75, MIN_DIMS['Kitchen'], 'NE-DEFECT') 
    plan_data_2['Pooja Room'] = (plot_width * 0.75, plot_length * 0.25, MIN_DIMS['Pooja Room'], 'SE') 
    plan_data_2['Toilet'] = (plot_width * 0.25, plot_length * 0.75, MIN_DIMS['Toilet'], 'NW') 
    plan_data_2['Bedroom 2'] = (plot_width * 0.50, plot_length * 0.75, MIN_DIMS['Bedroom 2'], 'N') 
    plan_data_2['Living Room'] = (center_x, plot_length * 0.50, MIN_DIMS['Living Room'], 'Center/E')
    if num_bhk == 3:
        plan_data_2['Bedroom 3'] = (plot_width * 0.50, plot_length * 0.25, MIN_DIMS['Bedroom 3'], 'S')
        
    plans.append({'title': "Option 2: High Flexibility (Check for Dosha)", 'data': plan_data_2})
    
    return plans

def plot_plan(ax, plan_data, plot_w, plot_l, title):
    """Draws the 2D floor plan using Matplotlib (not cached)."""
    
    ax.add_patch(plt.Rectangle((0, 0), plot_w, plot_l, edgecolor='black', facecolor='#f0f2f6', linewidth=2))
    
    for room, (x_pos, y_pos, dims, zone) in plan_data.items():
        w, l = dims
        
        # Color coding logic
        is_compliant = room in ROOM_RULES and ROOM_RULES[room] == zone
        is_defect = 'DEFECT' in zone or (room in ROOM_RULES and not is_compliant and 'DEFECT' not in zone)
        
        if is_compliant:
            color = '#4CAF50' # Green
        elif is_defect:
            color = '#F44336' # Red
        else:
            color = '#2196F3' # Blue
        
        rect = plt.Rectangle((x_pos - w/2, y_pos - l/2), w, l, edgecolor='black', facecolor=color, alpha=0.6, linewidth=1)
        ax.add_patch(rect)
        
        ax.text(x_pos, y_pos, f"{room}\n({zone})", ha='center', va='center', fontsize=9, color='white', fontweight='bold')

    ax.set_xlim(0, plot_w)
    ax.set_ylim(0, plot_l)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_aspect('equal', adjustable='box')
    ax.axis('off') 

# --- 3. STREAMLIT FRONT-END (FIXED & OPTIMIZED) ---

def generate_and_store_plans(plot_w, plot_l, facing, num_bhk):
    """
    Function called by the button click. Implements the loading transition.
    """
    # UX Enhancement: Start Loading State Transition
    with st.spinner('Calculating and optimizing Vastu layouts...'):
        # Simulate processing delay for visual effect
        time.sleep(1) 
        
        # 1. Generate plans (calls the cached function)
        st.session_state['plans'] = generate_plan_options(plot_w, plot_l, facing, num_bhk)
        st.session_state['last_run'] = True 
        
    st.toast('Layouts Generated Successfully!', icon='🏠') # Instant success feedback

def main():
    # Initialize session state markers if they don't exist
    if 'last_run' not in st.session_state:
        st.session_state['last_run'] = False
    
    st.set_page_config(page_title="e.VastuLeap Plan Generator", layout="wide")
    st.title("e.VastuLeap: Rule-Based Vastu Plan Generator 🏠")
    st.markdown("Enter your plot dimensions and requirements to generate Vastu-compliant layout options using algorithmic principles.")
    st.divider()

    col_input, col_info = st.columns([1, 1])

    with col_input:
        st.subheader("Your Requirements:")
        
        # Widgets are bound to variables (using keys)
        plot_w = st.number_input("Plot Width (ft)", min_value=10, value=30, step=5, key='width')
        plot_l = st.number_input("Plot Length (ft)", min_value=10, value=40, step=5, key='length')
        facing = st.selectbox("House Facing Direction", ["East", "North", "West", "South"], key='facing')
        num_bhk = st.selectbox("Number of Bedrooms (BHK)", [2, 3], key='bhk')
        
        # Button calls the function with current widget values
        st.button(
            "Generate Vastu Plans", 
            use_container_width=True, 
            type="primary",
            on_click=generate_and_store_plans, 
            args=(plot_w, plot_l, facing, num_bhk)
        )
        
    with col_info:
        st.subheader("Key Vastu Principles")
        st.markdown(f"""
        The generator prioritizes these rules:
        * **Kitchen:** **{ROOM_RULES['Kitchen']}** (Fire element)
        * **Master Bed:** **{ROOM_RULES['Master Bedroom']}** (Stability, Grounding)
        * **Pooja Room:** **{ROOM_RULES['Pooja Room']}** (Purity, Divine energy)
        * **Plot Shape:** Assumes a square/rectangular plot for simplicity.
        """)

    st.divider()
    
    # Display logic runs only if 'last_run' is True (i.e., button was clicked)
    if st.session_state.get('last_run'):
        
        plans = st.session_state.get('plans', [])
        
        if plans:
            st.subheader("Generated Layout Options")
            cols = st.columns(2)
            
            for i, plan in enumerate(plans):
                with cols[i]:
                    fig, ax = plt.subplots(figsize=(6, 6))
                    plot_plan(ax, plan['data'], plot_w, plot_l, plan['title'])
                    st.pyplot(fig)
                    
                    # Display detailed placement
                    st.markdown(f"**Details for {plan['title']}:**")
                    for room, (_, _, _, zone) in plan['data'].items():
                        # Check against Ideal Vastu Zone
                        is_compliant = room in ROOM_RULES and ROOM_RULES[room] == zone
                        is_defect = 'DEFECT' in zone or (room in ROOM_RULES and not is_compliant and 'DEFECT' not in zone)
                        
                        if is_compliant:
                            st.success(f"**{room}:** Placed Compliantly in {zone} {u'\u2714'}") 
                        elif is_defect:
                            st.error(f"**{room}:** Defect Detected! Should be in {ROOM_RULES.get(room, 'N/A')} {u'\u2718'}") 
                        else:
                            st.info(f"**{room}:** Placed in {zone} (Neutral Zone) {u'\u2714'}")

            # st.success is moved inside the generation function via st.toast
        else:
            st.error("Could not generate plans for the given constraints. Try different dimensions.")
            
    else:
        st.info("Click 'Generate Vastu Plans' to see the layouts.")

if __name__ == "__main__":
    main()