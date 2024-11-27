import sqlite3
import hashlib
from typing import Dict, Optional, Tuple
import json

class DatabaseManager:
    def __init__(self, db_path: str = 'game_helper.db'):
        self.db_path = db_path
        self.init_db()

    def get_db_connection(self):
        """Create and return a database connection."""
        return sqlite3.connect(self.db_path)

    def init_db(self):
        """Initialize the database with required tables."""
        conn = self.get_db_connection()
        c = conn.cursor()
        
        # Create users table
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                age INTEGER,
                gender TEXT,
                contact_info TEXT,
                primary_caregiver TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create user_preferences table
        c.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                user_id INTEGER PRIMARY KEY,
                memory_challenge_severity INTEGER,
                focus_difficulty INTEGER,
                everyday_problems TEXT,
                remembering_info TEXT,
                navigation_ability INTEGER,
                language_difficulties TEXT,
                physical_limitations TEXT,
                physical_details TEXT,
                device_usability TEXT,
                leisure_devices TEXT,
                game_preferences TEXT,
                time_spent INTEGER,
                gameplay_preference TEXT,
                multiplayer_interaction TEXT,
                accommodations_needed TEXT,
                accommodations_details TEXT,
                visual_hearing_impairments TEXT,
                impairments_details TEXT,
                frustrating_game_mechanics TEXT,
                cognitive_focus_areas TEXT,
                ideal_game_description TEXT,
                desired_outcomes TEXT,
                previous_experience TEXT,
                games_tried TEXT,
                enjoyed_aspects TEXT,
                difficulties TEXT,
                game_preferences_type TEXT,
                game_values TEXT,
                progress_tracking TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        conn.commit()
        conn.close()

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user(self, username: str, password: str, user_data: Dict) -> Tuple[bool, str]:
        """
        Create a new user with their preferences.
        Returns: Tuple of (success: bool, message: str)
        """
        conn = self.get_db_connection()
        c = conn.cursor()
        
        try:
            # Start transaction
            conn.execute('BEGIN')
            
            # Insert into users table
            c.execute(
                'INSERT INTO users (username, password_hash, full_name, age, gender, contact_info, primary_caregiver) '
                'VALUES (?, ?, ?, ?, ?, ?, ?)',
                (username, self.hash_password(password), user_data['full_name'], user_data['age'],
                 user_data['gender'], user_data['contact_info'], user_data['primary_caregiver'])
            )
            user_id = c.lastrowid
            
            # Convert lists to JSON strings for storage
            user_prefs = user_data.copy()
            for key in ['leisure_devices', 'cognitive_focus_areas']:
                if key in user_prefs and isinstance(user_prefs[key], list):
                    user_prefs[key] = json.dumps(user_prefs[key])
            
            # Insert into user_preferences table
            c.execute('''
                INSERT INTO user_preferences (
                    user_id, memory_challenge_severity, focus_difficulty, everyday_problems,
                    remembering_info, navigation_ability, language_difficulties,
                    physical_limitations, physical_details, device_usability,
                    leisure_devices, game_preferences, time_spent, gameplay_preference,
                    multiplayer_interaction, accommodations_needed, accommodations_details,
                    visual_hearing_impairments, impairments_details, frustrating_game_mechanics,
                    cognitive_focus_areas, ideal_game_description, desired_outcomes,
                    previous_experience, games_tried, enjoyed_aspects, difficulties,
                    game_preferences_type, game_values, progress_tracking
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id, user_prefs['memory_challenge_severity'], user_prefs['focus_difficulty'],
                user_prefs['everyday_problems'], user_prefs['remembering_info'],
                user_prefs['navigation_ability'], user_prefs['language_difficulties'],
                user_prefs['physical_limitations'],
                user_prefs.get('physical_details'),
                user_prefs['device_usability'],
                user_prefs['leisure_devices'],
                user_prefs['game_preferences'],
                user_prefs['time_spent'],
                user_prefs['gameplay_preference'],
                user_prefs['multiplayer_interaction'],
                user_prefs['accommodations_needed'],
                user_prefs.get('accommodations_details'),
                user_prefs['visual_hearing_impairments'],
                user_prefs.get('impairments_details'),
                user_prefs['frustrating_game_mechanics'],
                user_prefs['cognitive_focus_areas'],
                user_prefs['ideal_game_description'],
                user_prefs['desired_outcomes'],
                user_prefs['previous_experience'],
                user_prefs.get('games_tried'),
                user_prefs.get('enjoyed_aspects'),
                user_prefs.get('difficulties'),
                user_prefs['game_preferences_type'],
                user_prefs['game_values'],
                user_prefs['progress_tracking']
            ))
            
            conn.commit()
            return True, "User created successfully"
            
        except sqlite3.IntegrityError:
            conn.rollback()
            return False, "Username already exists"
        except Exception as e:
            conn.rollback()
            return False, f"Error creating user: {str(e)}"
        finally:
            conn.close()

    def verify_user(self, username: str, password: str) -> bool:
        """Verify user credentials."""
        conn = self.get_db_connection()
        c = conn.cursor()
        
        try:
            c.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
            result = c.fetchone()
            
            if result and result[0] == self.hash_password(password):
                return True
            return False
        finally:
            conn.close()

    def get_user_data(self, username: str) -> Optional[Dict]:
        """Retrieve user data and preferences."""
        conn = self.get_db_connection()
        c = conn.cursor()
        
        try:
            c.execute('''
                SELECT u.*, up.*
                FROM users u
                LEFT JOIN user_preferences up ON u.id = up.user_id
                WHERE u.username = ?
            ''', (username,))
            
            result = c.fetchone()
            if not result:
                return None
                
            # Convert row to dictionary
            columns = [desc[0] for desc in c.description]
            user_data = dict(zip(columns, result))
            
            # Parse JSON strings back to lists
            for key in ['leisure_devices', 'cognitive_focus_areas']:
                if user_data.get(key):
                    try:
                        user_data[key] = json.loads(user_data[key])
                    except json.JSONDecodeError:
                        user_data[key] = []
                        
            return user_data
        finally:
            conn.close()

    def update_user_preferences(self, username: str, preferences: Dict) -> Tuple[bool, str]:
        """Update user preferences."""
        conn = self.get_db_connection()
        c = conn.cursor()
        
        try:
            # Start transaction
            conn.execute('BEGIN')
            
            # Get user ID
            c.execute('SELECT id FROM users WHERE username = ?', (username,))
            result = c.fetchone()
            if not result:
                return False, "User not found"
            
            user_id = result[0]
            
            # Prepare preferences for update
            prefs = preferences.copy()
            for key in ['leisure_devices', 'cognitive_focus_areas']:
                if key in prefs and isinstance(prefs[key], list):
                    prefs[key] = json.dumps(prefs[key])
            
            # Update preferences
            placeholders = ', '.join(f'{k} = ?' for k in prefs.keys())
            query = f'UPDATE user_preferences SET {placeholders} WHERE user_id = ?'
            
            c.execute(query, list(prefs.values()) + [user_id])
            conn.commit()
            
            return True, "Preferences updated successfully"
        except Exception as e:
            conn.rollback()
            return False, f"Error updating preferences: {str(e)}"
        finally:
            conn.close()