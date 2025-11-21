-- ============================================================================
-- Supabase Table Schema for Facebook Hashtag Trends
-- ============================================================================
-- This matches your actual Supabase schema
-- Run this SQL in your Supabase SQL Editor if table doesn't exist
-- ============================================================================

CREATE TABLE IF NOT EXISTS public.facebook (
  id BIGSERIAL NOT NULL,
  platform TEXT NOT NULL DEFAULT 'Facebook'::text,
  topic_hashtag TEXT NOT NULL,
  engagement_score DOUBLE PRECISION NULL,
  sentiment_polarity DOUBLE PRECISION NULL,
  sentiment_label TEXT NULL,
  posts BIGINT NULL,
  views BIGINT NULL,
  metadata JSONB NULL,
  scraped_at TIMESTAMPTZ NULL DEFAULT NOW(),
  version_id UUID NOT NULL,
  CONSTRAINT facebook_pkey PRIMARY KEY (id)
) TABLESPACE pg_default;

-- Create indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_facebook_scraped_at ON public.facebook USING btree (scraped_at) TABLESPACE pg_default;
CREATE INDEX IF NOT EXISTS idx_facebook_version_id ON public.facebook USING btree (version_id) TABLESPACE pg_default;
CREATE INDEX IF NOT EXISTS idx_facebook_hashtag ON public.facebook USING btree (topic_hashtag) TABLESPACE pg_default;
CREATE INDEX IF NOT EXISTS idx_facebook_engagement_score ON public.facebook USING btree (engagement_score DESC) TABLESPACE pg_default;
CREATE INDEX IF NOT EXISTS idx_facebook_metadata_category ON public.facebook USING gin ((metadata->>'category')) TABLESPACE pg_default;

-- Enable Row Level Security (RLS)
ALTER TABLE public.facebook ENABLE ROW LEVEL SECURITY;

-- Create policy to allow all operations (adjust based on your security needs)
CREATE POLICY IF NOT EXISTS "Allow all operations" ON public.facebook
  FOR ALL
  USING (true)
  WITH CHECK (true);

-- Add comments
COMMENT ON TABLE public.facebook IS 'Stores Facebook hashtag trending data scraped by facebook_scraper';
COMMENT ON COLUMN public.facebook.version_id IS 'UUID identifier for each scraping run';
COMMENT ON COLUMN public.facebook.metadata IS 'JSON object containing category, trending_score, likes, comments, shares, etc.';
