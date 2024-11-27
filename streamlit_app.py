import streamlit as st
from db_utils import DatabaseManager
import json
from datetime import datetime
import random

# Initialize database manager
db = DatabaseManager()

def accessible_ui_styles():
    st.markdown("""
    <style>
    .stApp {
        background-color: black;
    }
    body {
        font-family: 'Arial', sans-serif;
        font-size: 18px;
        line-height: 1.6;
    }
    .stMarkdown, .stTitle {
        color: #2C3E50;
    }
    .stButton>button {
        background-color: #3498DB;
        color: white;
        font-size: 18px;
        padding: 10px 20px;
        border-radius: 10px;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #2980B9;
    }
    .stTextInput>div>div>input {
        font-size: 18px;
        padding: 10px;
        border-radius: 8px;
        border: 2px solid #BDC3C7;
    }
    .stSelectbox>div>div>select {
        font-size: 18px;
        padding: 10px;
        border-radius: 8px;
    }
    .game-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .profile-section {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

def safe_json_loads(json_str, default=None):
    """
    Safely load JSON string or return the object if it's already a list.

    Args:
        json_str (str or list): JSON string to parse or a list.
        default (any, optional): Default value to return if parsing fails. Defaults to None.

    Returns:
        Parsed JSON or default value
    """
    if isinstance(json_str, list):  # Return as-is if it's already a list
        return json_str
    if not json_str or json_str == '[]' or json_str == '{}':
        return default or []
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return default or []


def display_game_card(game):
    st.markdown(f"""
    <div class="game-card">
        <h3>{game['title']}</h3>
        <p><strong>Difficulty:</strong> {game['difficulty']}</p>
        <p><strong>Platform:</strong> {game['platform']}</p>
        <p><strong>Cognitive Focus:</strong> {game['cognitive_focus']}</p>
        <p>{game['description']}</p>
    </div>
    """, unsafe_allow_html=True)

def get_game_recommendations(user_preferences):
    # Sample game database - in production, this would come from a real database
    sample_games = [
        {
            "title": "Memory Match",
            "difficulty": "Easy",
            "platform": "Web",
            "cognitive_focus": "Memory",
            "description": "A classic memory matching game with customizable difficulty levels."
        },
        {
            "title": "Word Adventure",
            "difficulty": "Medium",
            "platform": "Mobile",
            "cognitive_focus": "Language",
            "description": "Interactive word-finding game that helps improve vocabulary and language skills."
        },
        {
            "title": "Pattern Master",
            "difficulty": "Hard",
            "platform": "PC",
            "cognitive_focus": "Problem Solving",
            "description": "Complex pattern recognition game with progressive difficulty levels."
        }
    ]
    return sample_games

def profile_page(username):
    user_data = db.get_user_data(username)
    if user_data:
        st.markdown("### My Profile")

        # Personal Information
        st.markdown("""
        <div class="profile-section">
            <h4>Personal Information</h4>
        </div>
        """, unsafe_allow_html=True)
        cols = st.columns(2)
        with cols[0]:
            st.write(f"**Name:** {user_data['full_name']}")
            st.write(f"**Age:** {user_data['age']}")
            st.write(f"**Gender:** {user_data['gender']}")
        with cols[1]:
            st.write(f"**Contact:** {user_data['contact_info']}")
            st.write(f"**Caregiver:** {user_data['primary_caregiver']}")

        # Cognitive Profile
        st.markdown("""
        <div class="profile-section">
            <h4>Cognitive Profile</h4>
        </div>
        """, unsafe_allow_html=True)
        cols = st.columns(2)
        with cols[0]:
            st.write(f"**Memory Challenge Level:** {user_data['memory_challenge_severity']}/10")
            st.write(f"**Focus Difficulty:** {user_data['focus_difficulty']}/10")
            st.write(f"**Navigation Ability:** {user_data['navigation_ability']}/10")
        with cols[1]:
            st.write(f"**Language Difficulties:** {user_data['language_difficulties']}")
            st.write(f"**Daily Problems:** {user_data['everyday_problems']}")
            st.write(f"**Memory Issues:** {user_data['remembering_info']}")

        # Game Preferences
        st.markdown("""
        <div class="profile-section">
            <h4>Gaming Preferences</h4>
        </div>
        """, unsafe_allow_html=True)

        leisure_devices = safe_json_loads(user_data.get('leisure_devices', '[]'))
        cognitive_focus_areas = safe_json_loads(user_data.get('cognitive_focus_areas', '[]'))

        cols = st.columns(2)
        with cols[0]:
            st.write(f"**Preferred Devices:** {', '.join(leisure_devices)}")
            st.write(f"**Daily Gaming Time:** {user_data['time_spent']} hours")
            st.write(f"**Gameplay Style:** {user_data['gameplay_preference']}")
        with cols[1]:
            st.write(f"**Multiplayer:** {user_data['multiplayer_interaction']}")
            st.write(f"**Progress Tracking:** {user_data['progress_tracking']}")
            st.write(f"**Game Type:** {user_data['game_preferences_type']}")

def game_recommendations_page(username):
    user_data = db.get_user_data(username)
    if user_data:
        st.markdown("### Game Recommendations")

        # Filters for recommendations
        st.markdown("#### Customize Your Recommendations")
        cols = st.columns(3)
        with cols[0]:
            difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])
        with cols[1]:
            platform = st.selectbox("Platform", ["All"] + safe_json_loads(user_data.get('leisure_devices', '[]')))
        with cols[2]:
            # Use safe_json_loads to handle both lists and JSON strings
            cognitive_focus = st.selectbox(
                "Cognitive Focus",
                ["All"] + safe_json_loads(user_data.get('cognitive_focus_areas', '[]'))
            )

        # Get and display recommendations
        games = get_game_recommendations(user_data)

        # Filter games based on user selection
        if platform != "All":
            games = [g for g in games if g['platform'] == platform]
        if cognitive_focus != "All":
            games = [g for g in games if g['cognitive_focus'] == cognitive_focus]

        # Display games
        if games:
            for game in games:
                display_game_card(game)
        else:
            st.info("No games match your current filters. Try adjusting your selections.")



# Add other pages (e.g., login_signup_page) as necessary.

def login_signup_page():
    st.title("Welcome to the Game Recommendation System")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.markdown("### Login to Your Account")
        login_username = st.text_input("Username", key="login_username", help="Enter your username")
        login_password = st.text_input("Password", type="password", key="login_password", help="Enter your password")
        
        if st.button("Login", help="Click to log into your account"):
            if login_username and login_password:
                if db.verify_user(login_username, login_password):
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = login_username
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
            else:
                st.error("Please enter both username and password.")
    
    with tab2:
        st.markdown("### Create Your Account")
        
        # Basic account information
        username = st.text_input("Username", key="signup_username", help="Choose a unique username")
        password = st.text_input("Password", type="password", key="signup_password", help="Choose a strong password")
        
        # Personal Information
        with st.expander("Personal Information", expanded=True):
            full_name = st.text_input("Full Name", help="Enter your full name")
            age = st.number_input("Age", min_value=5, max_value=100, help="Your current age")
            gender = st.selectbox("Gender", ["Select", "Male", "Female", "Other"], help="Select your gender")
            contact_info = st.text_input("Contact Information (Optional)", help="Enter your contact information")
            primary_caregiver = st.text_input("Primary Caregiver (If Applicable)", help="Enter caregiver's name")

        # Memory and Cognitive Challenges
        with st.expander("Memory and Cognitive Challenges", expanded=True):
            memory_challenge_severity = st.slider("Rate the severity of your memory challenges:", 1, 10, 5)
            focus_difficulty = st.slider("How often do you have difficulty focusing?", 1, 10, 5)
            everyday_problems = st.radio("Do you struggle with solving everyday problems?", ["Yes", "No"])
            remembering_info = st.radio("Do you have difficulty remembering new information?", ["Yes", "No"])
            navigation_ability = st.slider("Rate your ability to navigate new environments:", 1, 10, 5)
            language_difficulties = st.radio("Do you experience language difficulties?", ["Yes", "No"])

        # Physical Limitations and Device Usability
        with st.expander("Physical Limitations and Device Usability", expanded=True):
            physical_limitations = st.radio("Do you have any physical limitations that might affect game interaction?", ["Yes", "No"])
            physical_details = st.text_area("Please provide details:") if physical_limitations == "Yes" else None
            
            device_usability = st.radio("Can you easily use devices (computer, tablet, gaming console)?", ["Yes", "No"])
            leisure_devices = st.multiselect("Which devices do you use for leisure activities?", 
                                           ["Computer", "Tablet", "Gaming Console", "Mobile"])

        # Game Preferences
        with st.expander("Game Preferences", expanded=True):
            game_preferences = st.text_input("What type of games do you enjoy or think you'd enjoy?")
            time_spent = st.slider("How much time do you spend on games daily (hours)?", 0, 24, 1)
            gameplay_preference = st.radio("Do you prefer fast-paced or slow-paced gameplay?", ["Fast-paced", "Slow-paced"])
            multiplayer_interaction = st.radio("Do you enjoy games with multiplayer interaction?", ["Yes", "No"])
            
            accommodations_needed = st.radio("Do you need any accommodations (e.g. larger text, voice commands)?", ["Yes", "No"])
            accommodations_details = st.text_area("Please provide accommodation details:") if accommodations_needed == "Yes" else None
            
            visual_hearing_impairments = st.radio("Do you have visual or hearing impairments?", ["Yes", "No"])
            impairments_details = st.text_area("Please provide impairment details:") if visual_hearing_impairments == "Yes" else None
            
            frustrating_game_mechanics = st.text_input("Any game mechanics that you find frustrating?")

        # Cognitive Goals
        with st.expander("Cognitive Goals and Experiences", expanded=True):
            cognitive_focus_areas = st.multiselect("Which cognitive abilities do you want to focus on improving?",
                                                 ["Memory", "Attention", "Problem Solving", "Language", "Spatial Skills"])
            ideal_game_description = st.text_area("Describe your ideal game for cognitive rehabilitation.")
            desired_outcomes = st.text_area("What outcomes do you want from playing rehabilitation games?")
            
            previous_experience = st.radio("Have you tried cognitive rehabilitation games before?", ["Yes", "No"])
            games_tried = st.text_input("Which games have you tried?") if previous_experience == "Yes" else None
            enjoyed_aspects = st.text_area("What aspects did you enjoy?") if previous_experience == "Yes" else None
            difficulties = st.text_area("What did you find difficult?") if previous_experience == "Yes" else None
            
            game_preferences_type = st.radio("Do you prefer games with:", ["Single-player", "Multiplayer", "Both"])
            game_values = st.text_input("What do you value most in a game?")
            progress_tracking = st.selectbox("How do you want your progress tracked?", 
                                          ["Visual graphs", "Daily summaries", "No tracking", "Other"])

        if st.button("Sign Up"):
            if not username or not password:
                st.error("Username and password are required.")
            elif gender == "Select":
                st.error("Please select a gender.")
            else:
                user_data = {
                    "full_name": full_name,
                    "age": age,
                    "gender": gender,
                    "contact_info": contact_info,
                    "primary_caregiver": primary_caregiver,
                    "memory_challenge_severity": memory_challenge_severity,
                    "focus_difficulty": focus_difficulty,
                    "everyday_problems": everyday_problems,
                    "remembering_info": remembering_info,
                    "navigation_ability": navigation_ability,
                    "language_difficulties": language_difficulties,
                    "physical_limitations": physical_limitations,
                    "physical_details": physical_details,
                    "device_usability": device_usability,
                    "leisure_devices": leisure_devices,
                    "game_preferences": game_preferences,
                    "time_spent": time_spent,
                    "gameplay_preference": gameplay_preference,
                    "multiplayer_interaction": multiplayer_interaction,
                    "accommodations_needed": accommodations_needed,
                    "accommodations_details": accommodations_details,
                    "visual_hearing_impairments": visual_hearing_impairments,
                    "impairments_details": impairments_details,
                    "frustrating_game_mechanics": frustrating_game_mechanics,
                    "cognitive_focus_areas": cognitive_focus_areas,
                    "ideal_game_description": ideal_game_description,
                    "desired_outcomes": desired_outcomes,
                    "previous_experience": previous_experience,
                    "games_tried": games_tried,
                    "enjoyed_aspects": enjoyed_aspects,
                    "difficulties": difficulties,
                    "game_preferences_type": game_preferences_type,
                    "game_values": game_values,
                    "progress_tracking": progress_tracking
                }
                
                success, message = db.create_user(username, password, user_data)
                if success:
                    st.success(message)
                    st.info("Please proceed to login with your new account.")
                else:
                    st.error(message)

def profile_page(username):
    user_data = db.get_user_data(username)
    if user_data:
        st.markdown("### My Profile")
        
        # Personal Information
        st.markdown("""
        <div class="profile-section">
            <h4>Personal Information</h4>
        </div>
        """, unsafe_allow_html=True)
        cols = st.columns(2)
        with cols[0]:
            st.write(f"**Name:** {user_data['full_name']}")
            st.write(f"**Age:** {user_data['age']}")
            st.write(f"**Gender:** {user_data['gender']}")
        with cols[1]:
            st.write(f"**Contact:** {user_data['contact_info']}")
            st.write(f"**Caregiver:** {user_data['primary_caregiver']}")

        # Cognitive Profile
        st.markdown("""
        <div class="profile-section">
            <h4>Cognitive Profile</h4>
        </div>
        """, unsafe_allow_html=True)
        cols = st.columns(2)
        with cols[0]:
            st.write(f"**Memory Challenge Level:** {user_data['memory_challenge_severity']}/10")
            st.write(f"**Focus Difficulty:** {user_data['focus_difficulty']}/10")
            st.write(f"**Navigation Ability:** {user_data['navigation_ability']}/10")
        with cols[1]:
            st.write(f"**Language Difficulties:** {user_data['language_difficulties']}")
            st.write(f"**Daily Problems:** {user_data['everyday_problems']}")
            st.write(f"**Memory Issues:** {user_data['remembering_info']}")

        # Game Preferences
        st.markdown("""
        <div class="profile-section">
            <h4>Gaming Preferences</h4>
        </div>
        """, unsafe_allow_html=True)
        cols = st.columns(2)
        with cols[0]:
            st.write(f"**Preferred Devices:** {', '.join(user_data['leisure_devices'])}")
            st.write(f"**Daily Gaming Time:** {user_data['time_spent']} hours")
            st.write(f"**Gameplay Style:** {user_data['gameplay_preference']}")
        with cols[1]:
            st.write(f"**Multiplayer:** {user_data['multiplayer_interaction']}")
            st.write(f"**Progress Tracking:** {user_data['progress_tracking']}")
            st.write(f"**Game Type:** {user_data['game_preferences_type']}")

def game_recommendations_page(username):
    user_data = db.get_user_data(username)
    if user_data:
        st.markdown("### Game Recommendations")
        
        # Filters for recommendations
        st.markdown("#### Customize Your Recommendations")
        cols = st.columns(3)
        with cols[0]:
            difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])
        with cols[1]:
            platform = st.selectbox("Platform", ["All"] + user_data['leisure_devices'])

        with cols[2]:
            cognitive_focus = st.selectbox("Cognitive Focus", 
                                         ["All"] + safe_json_loads(user_data['cognitive_focus_areas']))
        
        # Get and display recommendations
        games = get_game_recommendations(user_data)
        
        # Filter games based on user selection
        if platform != "All":
            games = [g for g in games if g['platform'] == platform]
        if cognitive_focus != "All":
            games = [g for g in games if g['cognitive_focus'] == cognitive_focus]
        
        # Display games
        if games:
            for game in games:
                display_game_card(game)
        else:
            st.info("No games match your current filters. Try adjusting your selections.")

def main():
    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    
    accessible_ui_styles()
    
    if not st.session_state["logged_in"]:
        login_signup_page()
    else:
        # Sidebar navigation
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", ["Home", "My Profile", "Game Recommendations"])
        
        # Logout button
        if st.sidebar.button("Logout"):
            st.session_state["logged_in"] = False
            st.session_state["username"] = None
            st.rerun()
        
        # Main content based on navigation
        if page == "Home":
            st.title(f"Welcome back, {st.session_state['username']}!")
            
            # Quick stats
            cols = st.columns(3)
            with cols[0]:
                st.metric(label="Games Played", value="12")  # Replace with actual data
            with cols[1]:
                st.metric(label="Hours Played", value="24")  # Replace with actual data
            with cols[2]:
                st.metric(label="Cognitive Score", value="85")  # Replace with actual data
            
            # Recent activity
            st.markdown("### Recent Activity")
            st.markdown("""
            <div class="game-card">
                <p>🎮 Played Memory Match - 30 minutes ago</p>
                <p>🏆 New high score in Pattern Master!</p>
                <p>📈 Completed daily cognitive assessment</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Daily recommendations
            st.markdown("### Today's Recommended Games")
            games = get_game_recommendations({})[:2]  # Get top 2 games
            for game in games:
                display_game_card(game)
                
            # Daily cognitive tip
            st.markdown("### Daily Cognitive Tip")
            tips = [
                "Take regular breaks during gaming sessions to maintain focus.",
                "Try varying difficulty levels to challenge yourself appropriately.",
                "Mix different types of games to exercise various cognitive skills.",
                "Set specific goals for each gaming session."
            ]
            st.info(random.choice(tips))
            
        elif page == "My Profile":
            profile_page(st.session_state["username"])
            
            # Add profile editing functionality
            if st.button("Edit Profile"):
                st.session_state["editing_profile"] = True
            
            if st.session_state.get("editing_profile", False):
                st.markdown("### Edit Profile")
                # Add profile editing form here
                pass
            
        elif page == "Game Recommendations":
            game_recommendations_page(st.session_state["username"])

def update_user_progress(username, game_data):
    """Update user's gaming progress and statistics"""
    try:
        # Get current user data
        user_data = db.get_user_data(username)
        
        # Update progress
        if 'progress' not in user_data:
            user_data['progress'] = []
        
        # Add new progress entry
        progress_entry = {
            'timestamp': datetime.now().isoformat(),
            'game': game_data['game_name'],
            'score': game_data['score'],
            'duration': game_data['duration'],
            'difficulty': game_data['difficulty']
        }
        user_data['progress'].append(progress_entry)
        
        # Update user statistics
        if 'statistics' not in user_data:
            user_data['statistics'] = {
                'total_games_played': 0,
                'total_time_played': 0,
                'average_score': 0,
                'favorite_games': {}
            }
        
        stats = user_data['statistics']
        stats['total_games_played'] += 1
        stats['total_time_played'] += game_data['duration']
        
        # Update favorite games
        if game_data['game_name'] in stats['favorite_games']:
            stats['favorite_games'][game_data['game_name']] += 1
        else:
            stats['favorite_games'][game_data['game_name']] = 1
        
        # Save updated user data
        db.update_user_data(username, user_data)
        return True, "Progress updated successfully"
    except Exception as e:
        return False, f"Error updating progress: {str(e)}"

def generate_progress_report(username):
    """Generate a detailed progress report for the user"""
    user_data = db.get_user_data(username)
    if not user_data or 'progress' not in user_data:
        return None
    
    report = {
        'games_played': len(user_data['progress']),
        'total_time': sum(p['duration'] for p in user_data['progress']),
        'average_score': sum(p['score'] for p in user_data['progress']) / len(user_data['progress']),
        'favorite_games': user_data['statistics']['favorite_games'],
        'recent_progress': user_data['progress'][-5:],  # Last 5 games
        'cognitive_improvement': calculate_cognitive_improvement(user_data['progress'])
    }
    return report

def calculate_cognitive_improvement(progress_data):
    """Calculate cognitive improvement metrics based on user progress"""
    # Implementation would analyze trends in user performance
    # and return improvement metrics for different cognitive areas
    pass

if __name__ == "__main__":
    main()