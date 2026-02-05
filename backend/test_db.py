#!/usr/bin/env python3
"""
Test script to verify database connection and table creation.
"""

import asyncio
from database import engine, create_db_and_tables
from models.user import User
from models.task import Task
from sqlmodel import SQLModel, select
from sqlalchemy import text


async def test_connection():
    print("Testing database connection and creating tables...")
    
    try:
        # Create tables
        await create_db_and_tables()
        print("Tables created successfully!")
        
        # Verify connection by running a simple query
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT version();"))
            version = result.scalar()
            print(f"Connected to database. Version info: {version[:50]}...")
        
        # Check if tables exist by inspecting metadata
        from sqlalchemy import inspect
        async with engine.begin() as conn:
            insp = inspect(conn.sync_engine)
            tables = insp.get_table_names()
            print(f"Existing tables: {tables}")
            
            # Check specifically for our tables
            if 'user' in tables:
                print("✓ User table exists")
            else:
                print("✗ User table does not exist")
                
            if 'task' in tables:
                print("✓ Task table exists")
            else:
                print("✗ Task table does not exist")
        
        print("Database setup test completed successfully!")
        
    except Exception as e:
        print(f"Error during database setup: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_connection())