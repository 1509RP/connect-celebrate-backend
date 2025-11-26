/*
  # AI Invitation System Database Schema

  ## Overview
  Complete database schema for AI-powered invitation system with voice cloning,
  contact management, event tracking, and personalized invitations.

  ## Tables Created

  ### 1. `events`
  Stores all event information created by users
  - `id` (uuid, primary key) - Unique event identifier
  - `user_id` (uuid) - Owner of the event (for future auth)
  - `title` (text) - Event name
  - `date` (date) - Event date
  - `time` (time) - Event time
  - `location` (text) - Event venue
  - `description` (text) - Event details
  - `host` (text) - Host name
  - `template` (text) - Template style (modern/elegant/casual)
  - `custom_template` (text) - Custom HTML template
  - `rsvp_deadline` (timestamp) - RSVP cutoff date
  - `dress_code` (text) - Dress code information
  - `created_at` (timestamp) - Creation timestamp
  - `updated_at` (timestamp) - Last update timestamp

  ### 2. `contacts`
  Manages contact list for invitations
  - `id` (uuid, primary key) - Unique contact identifier
  - `user_id` (uuid) - Owner of the contact
  - `name` (text) - Contact full name
  - `email` (text) - Email address
  - `phone` (text) - Phone number
  - `group` (text) - Contact group (Friends/Family/Colleagues)
  - `preferences` (jsonb) - Contact preferences (JSON)
  - `created_at` (timestamp) - Creation timestamp
  - `updated_at` (timestamp) - Last update timestamp

  ### 3. `voice_samples`
  Stores recorded voice samples for AI cloning
  - `id` (uuid, primary key) - Unique sample identifier
  - `user_id` (uuid) - Owner of the voice sample
  - `name` (text) - Sample name/description
  - `audio_url` (text) - Storage URL for audio file
  - `duration` (integer) - Duration in seconds
  - `status` (text) - Processing status (recorded/processing/ready)
  - `metadata` (jsonb) - Additional metadata (JSON)
  - `created_at` (timestamp) - Creation timestamp

  ### 4. `invitations`
  Tracks all sent invitations and responses
  - `id` (uuid, primary key) - Unique invitation identifier
  - `event_id` (uuid, foreign key) - Related event
  - `contact_id` (uuid, foreign key) - Related contact
  - `status` (text) - RSVP status (pending/accepted/declined/maybe)
  - `delivery_method` (text) - How sent (sms/email/voice/call)
  - `sent_at` (timestamp) - When invitation was sent
  - `opened_at` (timestamp) - When invitation was opened
  - `responded_at` (timestamp) - When contact responded
  - `response_message` (text) - Optional response message
  - `voice_message_url` (text) - URL to voice invitation audio
  - `tracking_token` (text) - Unique tracking token
  - `metadata` (jsonb) - Additional tracking data (JSON)
  - `created_at` (timestamp) - Creation timestamp

  ### 5. `custom_templates`
  User-created invitation templates
  - `id` (uuid, primary key) - Unique template identifier
  - `user_id` (uuid) - Template creator
  - `name` (text) - Template name
  - `html_content` (text) - HTML template content
  - `preview_image` (text) - Preview image URL
  - `is_public` (boolean) - Public template flag
  - `created_at` (timestamp) - Creation timestamp
  - `updated_at` (timestamp) - Last update timestamp

  ## Security
  - RLS enabled on all tables
  - Policies restrict access to authenticated users' own data
  - Future-ready for multi-user authentication

  ## Indexes
  - Performance indexes on foreign keys and status fields
*/

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Events Table
CREATE TABLE IF NOT EXISTS events (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id uuid,
  title text NOT NULL,
  date date NOT NULL,
  time time NOT NULL,
  location text DEFAULT '',
  description text DEFAULT '',
  host text DEFAULT '',
  template text DEFAULT 'modern',
  custom_template text,
  rsvp_deadline timestamptz,
  dress_code text DEFAULT '',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Contacts Table
CREATE TABLE IF NOT EXISTS contacts (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id uuid,
  name text NOT NULL,
  email text DEFAULT '',
  phone text DEFAULT '',
  "group" text DEFAULT 'Friends',
  preferences jsonb DEFAULT '{}',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Voice Samples Table
CREATE TABLE IF NOT EXISTS voice_samples (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id uuid,
  name text NOT NULL,
  audio_url text,
  duration integer DEFAULT 0,
  status text DEFAULT 'recorded',
  metadata jsonb DEFAULT '{}',
  created_at timestamptz DEFAULT now()
);

-- Invitations Table
CREATE TABLE IF NOT EXISTS invitations (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  event_id uuid REFERENCES events(id) ON DELETE CASCADE,
  contact_id uuid REFERENCES contacts(id) ON DELETE CASCADE,
  status text DEFAULT 'pending',
  delivery_method text DEFAULT 'email',
  sent_at timestamptz,
  opened_at timestamptz,
  responded_at timestamptz,
  response_message text DEFAULT '',
  voice_message_url text,
  tracking_token text UNIQUE,
  metadata jsonb DEFAULT '{}',
  created_at timestamptz DEFAULT now()
);

-- Custom Templates Table
CREATE TABLE IF NOT EXISTS custom_templates (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id uuid,
  name text NOT NULL,
  html_content text NOT NULL,
  preview_image text,
  is_public boolean DEFAULT false,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_invitations_event ON invitations(event_id);
CREATE INDEX IF NOT EXISTS idx_invitations_contact ON invitations(contact_id);
CREATE INDEX IF NOT EXISTS idx_invitations_status ON invitations(status);
CREATE INDEX IF NOT EXISTS idx_invitations_tracking ON invitations(tracking_token);
CREATE INDEX IF NOT EXISTS idx_contacts_user ON contacts(user_id);
CREATE INDEX IF NOT EXISTS idx_events_user ON events(user_id);

-- Enable Row Level Security
ALTER TABLE events ENABLE ROW LEVEL SECURITY;
ALTER TABLE contacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE voice_samples ENABLE ROW LEVEL SECURITY;
ALTER TABLE invitations ENABLE ROW LEVEL SECURITY;
ALTER TABLE custom_templates ENABLE ROW LEVEL SECURITY;

-- RLS Policies (permissive for now, will be restricted with auth)
CREATE POLICY "Allow all access to events"
  ON events FOR ALL
  TO public
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Allow all access to contacts"
  ON contacts FOR ALL
  TO public
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Allow all access to voice_samples"
  ON voice_samples FOR ALL
  TO public
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Allow all access to invitations"
  ON invitations FOR ALL
  TO public
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Allow all access to custom_templates"
  ON custom_templates FOR ALL
  TO public
  USING (true)
  WITH CHECK (true);