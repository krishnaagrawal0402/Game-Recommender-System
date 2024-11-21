import streamlit as st

# Custom CSS for accessibility and cognitive-friendly design
def accessible_ui_styles():
    st.markdown("""
    <style>
    /* Light, soft color palette */
    .stApp {
        background-color: #F0F4F8;  /* Soft light blue-gray background */
    }
    
    /* Large, clear typography */
    body {
        font-family: 'Arial', sans-serif;
        font-size: 18px;
        line-height: 1.6;
    }
    
    /* High contrast text */
    .stMarkdown, .stTitle {
        color: #2C3E50;  /* Dark blue-gray for readability */
    }
    
    /* Larger, more distinct buttons */
    .stButton>button {
        background-color: #3498DB;  /* Bright, clear blue */
        color: white;
        font-size: 18px;
        padding: 10px 20px;
        border-radius: 10px;
        transition: background-color 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #2980B9;  /* Slightly darker blue on hover */
    }
    
    /* Larger, clearer input fields */
    .stTextInput>div>div>input {
        font-size: 18px;
        padding: 10px;
        border-radius: 8px;
        border: 2px solid #BDC3C7;
    }
    
    /* Clear, spaced select boxes */
    .stSelectbox>div>div>select {
        font-size: 18px;
        padding: 10px;
        border-radius: 8px;
    }
    
    /* Soft, clear card-like containers */
    .reportview-container .markdown-text-container {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    /* Larger game recommendation display */
    .game-recommendation {
        background-color: #ECF0F1;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

def game_recommendation_card(game):
    """Create an accessible game recommendation card"""
    st.markdown(f"""
    <div class="game-recommendation">
        <h3>{game[1]}</h3>
        <p><strong>Difficulty:</strong> {game[2]}</p>
        <p><strong>Platforms:</strong> {game[3]}</p>
        <p><strong>Description:</strong> {game[5]}</p>
    </div>
    """, unsafe_allow_html=True)

def login_page():
    st.title("Welcome to Game Helper")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### Login to Your Account")
    
    username = st.text_input("Username", help="Enter your chosen username")
    password = st.text_input("Password", type="password", help="Enter your password")
    
    login_col1, login_col2 = st.columns(2)
    
    with login_col1:
        if st.button("Login", help="Click to log into your account"):
            # Login logic here
            pass
    
    with login_col2:
        st.markdown("[Forgot Password?](#)")

def signup_page():
    st.title("Create Your Account")
    
    # Use columns to create a more spaced, readable form
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name", help="Enter your full name")
        age = st.number_input("Age", min_value=5, max_value=100, help="Your current age")
    
    with col2:
        username = st.text_input("Username", help="Choose a unique username")
        password = st.text_input("Password", type="password", help="Create a secure password")
    
    cognitive_impairments = [
        "Memory Loss", "Attention Deficit", 
        "Language Processing", "Problem Solving"
    ]
    cognitive_impairment = st.selectbox(
        "Primary Cognitive Focus", 
        cognitive_impairments,
        help="Select the area you want to improve"
    )
    
    platforms = st.multiselect(
        "Preferred Platforms", 
        ["Web", "Mobile", "PC", "Tablet"],
        help="Select platforms you're comfortable using"
    )
    
    if st.button("Create Account", help="Click to create your account"):
        # Registration logic here
        pass

def home_page():
    st.title("Game Recommendation Center")
    
    st.markdown("""
    ### Find Games Perfect for You
    Answer a few questions to get personalized game recommendations!
    """)
    
    difficulty = st.selectbox(
        "Game Difficulty", 
        ["Easy", "Medium", "Hard"],
        help="Choose a difficulty level that suits you"
    )
    
    platform = st.selectbox(
        "Your Preferred Platform", 
        ["Web", "Mobile", "PC", "Tablet"],
        help="Select the platform you'll play on"
    )
    
    cognitive_focus = st.selectbox(
        "Skill to Improve", 
        ["Memory", "Problem Solving", "Language", "Attention"],
        help="Select the cognitive skill you want to work on"
    )
    
    if st.button("Find My Games", help="Click to get game recommendations"):
        # Recommendation logic here
        pass

def main():
    accessible_ui_styles()
    
    # Navigation
    page = st.sidebar.radio(
        "Navigate", 
        ["Login", "Sign Up", "Recommendations"],
        help="Choose a section to explore"
    )
    
    if page == "Login":
        login_page()
    elif page == "Sign Up":
        signup_page()
    else:
        home_page()

if __name__ == "__main__":
    main()