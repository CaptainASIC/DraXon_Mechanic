import asyncpg
import os
from datetime import datetime

class Database:
    def __init__(self):
        self.pool = None

    async def initialize_db(self, conn):
        """Initialize database tables and indexes"""
        # Create system_info table
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS system_info (
                user_id BIGINT PRIMARY KEY,
                os TEXT NOT NULL,
                cpu TEXT NOT NULL,
                gpu TEXT NOT NULL,
                memory TEXT NOT NULL,
                storage TEXT NOT NULL,
                keyboard TEXT,
                mouse TEXT,
                other_controllers TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create indexes
        await conn.execute('''
            CREATE INDEX IF NOT EXISTS idx_system_info_updated 
            ON system_info(updated_at)
        ''')

    async def connect(self):
        """Connect to PostgreSQL database and initialize if needed"""
        try:
            # Get database configuration from environment
            DB_USER = os.getenv('DB_USER')
            DB_PASSWORD = os.getenv('DB_PASSWORD')
            DB_NAME = os.getenv('DB_NAME')
            DB_HOST = os.getenv('DB_HOST', 'localhost')
            DB_PORT = os.getenv('DB_PORT', '5432')

            # Create connection pool
            self.pool = await asyncpg.create_pool(
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                host=DB_HOST,
                port=DB_PORT
            )

            # Initialize database structure
            async with self.pool.acquire() as conn:
                await self.initialize_db(conn)
                print("Database initialized successfully")

        except Exception as e:
            print(f"Database connection/initialization error: {str(e)}")
            raise

    async def close(self):
        """Close database connection"""
        if self.pool:
            await self.pool.close()

    async def save_system_info(self, user_id: int, os: str, cpu: str, gpu: str, memory: str, storage: str, 
                             keyboard: str = None, mouse: str = None, other_controllers: str = None):
        """Save system information to database"""
        async with self.pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO system_info 
                (user_id, os, cpu, gpu, memory, storage, keyboard, mouse, other_controllers, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                ON CONFLICT (user_id) 
                DO UPDATE SET 
                    os = $2, cpu = $3, gpu = $4, memory = $5, storage = $6,
                    keyboard = $7, mouse = $8, other_controllers = $9, updated_at = $10
            ''', user_id, os, cpu, gpu, memory, storage, keyboard, mouse, other_controllers, datetime.now())

    async def get_system_info(self, user_id: int):
        """Get system information from database"""
        async with self.pool.acquire() as conn:
            return await conn.fetchrow('''
                SELECT * FROM system_info WHERE user_id = $1
            ''', user_id)
