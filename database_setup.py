import sqlite3
import pandas as pd

def create_database():
    """Create SQLite database for game recommendations"""
    conn = sqlite3.connect('game_recommendations.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT,
        name TEXT,
        age INTEGER,
        cognitive_impairment TEXT,
        preferred_platforms TEXT
    )
    ''')
    
    # Create games table with comprehensive tagging
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY,
        name TEXT,
        difficulty_level TEXT,
        platforms TEXT,
        cognitive_focus TEXT,
        description TEXT,
        min_age INTEGER,
        max_age INTEGER
    )
    ''')
    
    # Sample game data
    sample_games = [
        ('Memory Match', 'Easy', 'Web,Mobile', 'Memory', 'Classic memory game', 5, 80),
        ('Puzzle Quest', 'Medium', 'PC,Tablet', 'Problem Solving', 'Complex puzzle solving', 10, 70),
        ('Word Builder', 'Hard', 'Mobile,Web', 'Language', 'Advanced word construction game', 15, 75),
        # Add more sample games
    ]
    
    cursor.executemany('''
    INSERT OR IGNORE INTO games 
    (name, difficulty_level, platforms, cognitive_focus, description, min_age, max_age) 
    VALUES (?,?,?,?,?,?,?)
    ''', sample_games)
    
    conn.commit()
    conn.close()

def get_game_recommendations(user_preferences):
    """Match game recommendations based on user preferences"""
    conn = sqlite3.connect('game_recommendations.db')
    
    # Build dynamic query based on user preferences
    query = "SELECT * FROM games WHERE 1=1 "
    params = []
    
    if user_preferences.get('difficulty'):
        query += " AND difficulty_level = ? "
        params.append(user_preferences['difficulty'])
    
    if user_preferences.get('platform'):
        query += " AND platforms LIKE ? "
        params.append(f"%{user_preferences['platform']}%")
    
    if user_preferences.get('cognitive_focus'):
        query += " AND cognitive_focus = ? "
        params.append(user_preferences['cognitive_focus'])
    
    cursor = conn.cursor()
    cursor.execute(query, params)
    
    recommendations = cursor.fetchall()
    conn.close()
    
    return recommendations

# Initialize database
create_database()