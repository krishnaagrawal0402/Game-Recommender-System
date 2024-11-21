import sqlite3
import hashlib
import streamlit as st

class UserAuthentication:
    @staticmethod
    def hash_password(password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def register_user(username, password, name, age, cognitive_impairment, platforms):
        """Register a new user in the database"""
        conn = sqlite3.connect('game_recommendations.db')
        cursor = conn.cursor()
        
        hashed_password = UserAuthentication.hash_password(password)
        
        try:
            cursor.execute('''
            INSERT INTO users 
            (username, password, name, age, cognitive_impairment, preferred_platforms) 
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, hashed_password, name, age, cognitive_impairment, platforms))
            
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    @staticmethod
    def login_user(username, password):
        """Validate user login credentials"""
        conn = sqlite3.connect('game_recommendations.db')
        cursor = conn.cursor()
        
        hashed_password = UserAuthentication.hash_password(password)
        
        cursor.execute('''
        SELECT * FROM users 
        WHERE username = ? AND password = ?
        ''', (username, hashed_password))
        
        user = cursor.fetchone()
        conn.close()
        
        return user is not None