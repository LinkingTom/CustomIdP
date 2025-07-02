#!/usr/bin/env python3
"""
Demo script to test the User Directory API endpoints

This script demonstrates all the CRUD operations for users and teams.
Run this after starting the FastAPI server to test the API.

Usage:
    python demo_api.py
"""

import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_user_endpoints():
    print("🧪 Testing User Endpoints")
    print("=" * 50)
    
    # Test data
    user1 = {
        "email": "john.DOE@example.com",  # Will be normalized to lowercase
        "name": "John Doe",
        "roles": ["admin", "user"],
        "teams": ["engineering", "management"]
    }
    
    user2 = {
        "email": "jane.smith@example.com",
        "name": "Jane Smith",
        "roles": ["user"],
        "teams": ["engineering"]
    }
    
    print("\n1️⃣ Creating users...")
    
    # Create user 1
    response = requests.post(f"{BASE_URL}/users", json=user1)
    if response.status_code == 201:
        print(f"✅ Created user: {response.json()['email']}")
    else:
        print(f"❌ Failed to create user: {response.text}")
    
    # Create user 2
    response = requests.post(f"{BASE_URL}/users", json=user2)
    if response.status_code == 201:
        print(f"✅ Created user: {response.json()['email']}")
    else:
        print(f"❌ Failed to create user: {response.text}")
    
    # Try to create duplicate user (should fail)
    response = requests.post(f"{BASE_URL}/users", json=user1)
    if response.status_code == 409:
        print("✅ Correctly rejected duplicate user")
    else:
        print(f"❌ Should have rejected duplicate user: {response.text}")
    
    print("\n2️⃣ Getting all users...")
    response = requests.get(f"{BASE_URL}/users")
    if response.status_code == 200:
        users = response.json()
        print(f"✅ Retrieved {len(users)} users")
        for user in users:
            print(f"   - {user['email']} ({user['name']})")
    else:
        print(f"❌ Failed to get users: {response.text}")
    
    print("\n3️⃣ Getting specific user...")
    # Note: email is case-insensitive
    response = requests.get(f"{BASE_URL}/users/JOHN.DOE@EXAMPLE.COM")
    if response.status_code == 200:
        user = response.json()
        print(f"✅ Retrieved user: {user['email']} (case-insensitive lookup)")
    else:
        print(f"❌ Failed to get user: {response.text}")
    
    print("\n4️⃣ Updating user (PUT)...")
    updated_user = {
        "email": "john.doe@example.com",
        "name": "John Doe Updated",
        "roles": ["admin", "user", "moderator"],
        "teams": ["engineering"]
    }
    response = requests.put(f"{BASE_URL}/users/john.doe@example.com", json=updated_user)
    if response.status_code == 200:
        user = response.json()
        print(f"✅ Updated user: {user['name']}")
        print(f"   Roles: {user['roles']}")
    else:
        print(f"❌ Failed to update user: {response.text}")
    
    print("\n5️⃣ Partially updating user (PATCH)...")
    partial_update = {
        "roles": ["admin", "super-user"],
        "teams": ["engineering", "leadership"]
    }
    response = requests.patch(f"{BASE_URL}/users/john.doe@example.com", json=partial_update)
    if response.status_code == 200:
        user = response.json()
        print(f"✅ Partially updated user: {user['email']}")
        print(f"   New roles: {user['roles']}")
        print(f"   New teams: {user['teams']}")
    else:
        print(f"❌ Failed to partially update user: {response.text}")
    
    print("\n6️⃣ Deleting user...")
    response = requests.delete(f"{BASE_URL}/users/jane.smith@example.com")
    if response.status_code == 204:
        print("✅ Deleted user successfully")
    else:
        print(f"❌ Failed to delete user: {response.text}")
    
    # Verify deletion
    response = requests.get(f"{BASE_URL}/users/jane.smith@example.com")
    if response.status_code == 404:
        print("✅ Confirmed user was deleted")
    else:
        print(f"❌ User should have been deleted: {response.text}")


def test_team_endpoints():
    print("\n\n🧪 Testing Team Endpoints")
    print("=" * 50)
    
    # Test data
    team1 = {
        "name": "Engineering",
        "description": "Software development team",
        "user_emails": ["john.doe@example.com", "alice@example.com"]
    }
    
    team2 = {
        "name": "Marketing",
        "description": "Marketing and communications team",
        "user_emails": ["bob@example.com"]
    }
    
    print("\n1️⃣ Creating teams...")
    
    # Create team 1
    response = requests.post(f"{BASE_URL}/teams", json=team1)
    if response.status_code == 201:
        team = response.json()
        print(f"✅ Created team: {team['name']} (ID: {team['id']})")
        team1_id = team['id']
    else:
        print(f"❌ Failed to create team: {response.text}")
        return
    
    # Create team 2
    response = requests.post(f"{BASE_URL}/teams", json=team2)
    if response.status_code == 201:
        team = response.json()
        print(f"✅ Created team: {team['name']} (ID: {team['id']})")
        team2_id = team['id']
    else:
        print(f"❌ Failed to create team: {response.text}")
        return
    
    print("\n2️⃣ Getting all teams...")
    response = requests.get(f"{BASE_URL}/teams")
    if response.status_code == 200:
        teams = response.json()
        print(f"✅ Retrieved {len(teams)} teams")
        for team in teams:
            print(f"   - {team['name']}: {team['description']}")
    else:
        print(f"❌ Failed to get teams: {response.text}")
    
    print("\n3️⃣ Getting specific team...")
    response = requests.get(f"{BASE_URL}/teams/{team1_id}")
    if response.status_code == 200:
        team = response.json()
        print(f"✅ Retrieved team: {team['name']}")
        print(f"   Members: {team['user_emails']}")
    else:
        print(f"❌ Failed to get team: {response.text}")
    
    print("\n4️⃣ Updating team...")
    updated_team = {
        "name": "Engineering",
        "description": "Full-stack development team",
        "user_emails": ["john.doe@example.com", "alice@example.com", "charlie@example.com"]
    }
    response = requests.put(f"{BASE_URL}/teams/{team1_id}", json=updated_team)
    if response.status_code == 200:
        team = response.json()
        print(f"✅ Updated team: {team['name']}")
        print(f"   Description: {team['description']}")
        print(f"   Members: {team['user_emails']}")
    else:
        print(f"❌ Failed to update team: {response.text}")
    
    print("\n5️⃣ Deleting team...")
    response = requests.delete(f"{BASE_URL}/teams/{team2_id}")
    if response.status_code == 204:
        print("✅ Deleted team successfully")
    else:
        print(f"❌ Failed to delete team: {response.text}")


def test_health_endpoint():
    print("🧪 Testing Health Endpoint")
    print("=" * 50)
    
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        health = response.json()
        print(f"✅ Health check: {health['status']}")
        print(f"   Message: {health['message']}")
    else:
        print(f"❌ Health check failed: {response.text}")


def main():
    print("🚀 User Directory API Demo")
    print("=" * 50)
    print("Make sure the FastAPI server is running on http://localhost:8000")
    print("Start it with: python main.py")
    print()
    
    # Test if server is running
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("❌ Server is not responding. Please start the server first.")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Please start the server first.")
        return
    
    # Run all tests
    test_health_endpoint()
    test_user_endpoints()
    test_team_endpoints()
    
    print("\n\n🎉 Demo completed!")
    print("=" * 50)
    print("API Documentation available at: http://localhost:8000/docs")
    print("Alternative docs at: http://localhost:8000/redoc")


if __name__ == "__main__":
    main() 