#!/usr/bin/env python3
"""
Test Supabase Connection and Table Setup
=========================================

Run this script to verify your Supabase configuration is correct.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from supabase import create_client
except ImportError:
    print("❌ Supabase package not installed!")
    print("   Install with: pip install supabase")
    sys.exit(1)

def test_supabase():
    """Test Supabase connection and table operations"""
    
    print("=" * 80)
    print("Supabase Connection Test")
    print("=" * 80)
    print()
    
    # Check credentials
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_ANON_KEY')
    
    if not url:
        print("❌ SUPABASE_URL not found in .env file")
        print("   Add: SUPABASE_URL=https://your-project.supabase.co")
        return False
    
    if not key:
        print("❌ SUPABASE_ANON_KEY not found in .env file")
        print("   Add: SUPABASE_ANON_KEY=your-anon-key-here")
        return False
    
    print(f"✓ Found SUPABASE_URL: {url[:30]}...")
    print(f"✓ Found SUPABASE_ANON_KEY: {key[:20]}...")
    print()
    
    try:
        # Create client
        print("Connecting to Supabase...")
        supabase = create_client(url, key)
        print("✓ Connection successful!")
        print()
        
        # Test table exists
        print("Testing table 'facebook'...")
        try:
            result = supabase.table('facebook').select('id').limit(1).execute()
            print("✓ Table 'facebook' exists and is accessible")
        except Exception as e:
            if 'relation "facebook" does not exist' in str(e).lower():
                print("❌ Table 'facebook' does not exist!")
                print("   Run the SQL in 'create_supabase_table.sql' in Supabase SQL Editor")
                return False
            else:
                raise
        
        print()
        
        # Test insert
        print("Testing insert operation...")
        import uuid
        test_version_id = str(uuid.uuid4())
        test_record = {
            'platform': 'Facebook',
            'topic_hashtag': 'test_hashtag_setup',
            'engagement_score': 8.5,
            'sentiment_polarity': 0.65,
            'sentiment_label': 'positive',
            'posts': 10,
            'views': 1000,
            'version_id': test_version_id,  # UUID type in Supabase
            'scraped_at': None,  # Will use default NOW()
            'metadata': {
                'category': 'technology',
                'trending_score': 85.0,
                'avg_engagement': 100.0,
                'test': True
            }
        }
        
        response = supabase.table('facebook').insert(test_record).execute()
        print("✓ Insert successful!")
        print(f"  Inserted record ID: {response.data[0]['id']}")
        print()
        
        # Test query
        print("Testing query operation...")
        result = supabase.table('facebook')\
            .select('*')\
            .eq('version_id', test_version_id)\
            .execute()
        
        print(f"✓ Query successful! Found {len(result.data)} record(s)")
        print()
        
        # Cleanup test record
        print("Cleaning up test record...")
        supabase.table('facebook')\
            .delete()\
            .eq('version_id', test_version_id)\
            .execute()
        print("✓ Test record deleted")
        print()
        
        # Success!
        print("=" * 80)
        print("✅ ALL TESTS PASSED!")
        print("=" * 80)
        print()
        print("Your Supabase setup is correct!")
        print("The scraper will now automatically save data to Supabase.")
        print()
        
        return True
        
    except Exception as e:
        print()
        print("=" * 80)
        print("❌ ERROR")
        print("=" * 80)
        print(f"Error: {e}")
        print()
        print("Common issues:")
        print("  1. Check SUPABASE_URL is correct")
        print("  2. Check SUPABASE_ANON_KEY is correct")
        print("  3. Check table 'facebook' exists (run create_supabase_table.sql)")
        print("  4. Check RLS policies allow operations")
        print("  5. Check internet connection")
        print()
        return False

if __name__ == "__main__":
    success = test_supabase()
    sys.exit(0 if success else 1)

