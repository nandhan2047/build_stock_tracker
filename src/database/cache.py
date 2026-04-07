"""
Cache management module using SQLite for local caching.
Reduces API calls and improves performance.
"""

import sys
from pathlib import Path

# Add project root to path (works in Colab & local)
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import json
import sqlite3
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from pathlib import Path

from config import DB_PATH, CACHE_EXPIRY_SECONDS
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class CacheManager:
    """Manages caching of analysis results using SQLite."""

    def __init__(self, db_path: str = str(DB_PATH)):
        """
        Initialize cache manager.

        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize database schema if needed."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Create cache table
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS cache (
                        key TEXT PRIMARY KEY,
                        data TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        expires_at TIMESTAMP NOT NULL,
                        hit_count INTEGER DEFAULT 0
                    )
                    """
                )

                # Create index on key and expires_at
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_expires_at ON cache(expires_at)"
                )

                conn.commit()
                logger.info(f"✓ Cache database initialized at {self.db_path}")

        except sqlite3.Error as e:
            logger.error(f"Database initialization error: {e}")
            raise

    def set(
        self, key: str, data: Dict[str, Any], ttl_seconds: int = CACHE_EXPIRY_SECONDS
    ) -> bool:
        """
        Store data in cache.

        Args:
            key: Cache key
            data: Data to cache (will be JSON serialized)
            ttl_seconds: Time to live in seconds

        Returns:
            True if successful
        """
        try:
            expires_at = datetime.now() + timedelta(seconds=ttl_seconds)
            data_json = json.dumps(data, default=str)  # Handle datetime serialization

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO cache (key, data, expires_at)
                    VALUES (?, ?, ?)
                    """,
                    (key, data_json, expires_at),
                )
                conn.commit()

            logger.debug(f"✓ Cached {key} (expires in {ttl_seconds}s)")
            return True

        except Exception as e:
            logger.error(f"Error caching {key}: {e}")
            return False

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve data from cache.

        Args:
            key: Cache key

        Returns:
            Cached data or None if not found or expired
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Check if key exists and hasn't expired
                cursor.execute(
                    """
                    SELECT data, hit_count FROM cache
                    WHERE key = ? AND expires_at > datetime('now')
                    """,
                    (key,),
                )

                result = cursor.fetchone()

                if result:
                    data, hit_count = result

                    # Increment hit count
                    cursor.execute(
                        "UPDATE cache SET hit_count = hit_count + 1 WHERE key = ?",
                        (key,),
                    )
                    conn.commit()

                    logger.debug(f"✓ Cache hit for {key} (hits: {hit_count + 1})")
                    return json.loads(data)
                else:
                    logger.debug(f"Cache miss for {key}")
                    return None

        except Exception as e:
            logger.error(f"Error retrieving cache for {key}: {e}")
            return None

    def delete(self, key: str) -> bool:
        """
        Delete a cache entry.

        Args:
            key: Cache key

        Returns:
            True if deleted
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM cache WHERE key = ?", (key,))
                conn.commit()

            logger.debug(f"✓ Deleted cache entry: {key}")
            return True

        except Exception as e:
            logger.error(f"Error deleting cache {key}: {e}")
            return False

    def clear_expired(self) -> int:
        """
        Delete all expired cache entries.

        Returns:
            Number of entries deleted
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM cache WHERE expires_at < datetime('now')")
                deleted_count = cursor.rowcount
                conn.commit()

            logger.info(f"✓ Cleared {deleted_count} expired cache entries")
            return deleted_count

        except Exception as e:
            logger.error(f"Error clearing expired cache: {e}")
            return 0

    def clear_all(self) -> bool:
        """
        Clear all cache entries.

        Returns:
            True if successful
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM cache")
                conn.commit()

            logger.info("✓ Cleared all cache entries")
            return True

        except Exception as e:
            logger.error(f"Error clearing all cache: {e}")
            return False

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache stats
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("SELECT COUNT(*) FROM cache")
                total_entries = cursor.fetchone()[0]

                cursor.execute(
                    "SELECT COUNT(*) FROM cache WHERE expires_at > datetime('now')"
                )
                valid_entries = cursor.fetchone()[0]

                cursor.execute("SELECT SUM(hit_count) FROM cache")
                total_hits = cursor.fetchone()[0] or 0

                cursor.execute(
                    "SELECT avg(length(data)) FROM cache"
                )
                avg_size = cursor.fetchone()[0] or 0

                return {
                    "total_entries": total_entries,
                    "valid_entries": valid_entries,
                    "expired_entries": total_entries - valid_entries,
                    "total_hits": int(total_hits),
                    "avg_entry_size_bytes": int(avg_size),
                }

        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {}


if __name__ == "__main__":
    print("\n✅ Testing Cache Manager\n")

    cache = CacheManager()

    # Test storing
    test_data = {"ticker": "AAPL", "price": 175.50, "analysis": "Test data"}
    success = cache.set("test_key", test_data, ttl_seconds=3600)
    print(f"Store test: {'✓' if success else '✗'}")

    # Test retrieving
    retrieved = cache.get("test_key")
    print(f"Retrieve test: {'✓' if retrieved else '✗'}")
    print(f"Retrieved data: {retrieved}")

    # Test expired
    cache.set("expired_key", {"test": "data"}, ttl_seconds=1)
    import time
    time.sleep(2)
    expired = cache.get("expired_key")
    print(f"Expiry test: {'✓' if expired is None else '✗'}")

    # Test stats
    stats = cache.get_stats()
    print(f"\nCache Stats:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # Cleanup
    cache.clear_all()
