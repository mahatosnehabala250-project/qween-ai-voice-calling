-- Vobiz Voice AI Database Schema
-- Optimized for Dental Clinics in India

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Businesses (Clinics) Table
CREATE TABLE businesses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    business_type VARCHAR(100) DEFAULT 'dental_clinic',
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(255),
    address TEXT,
    timezone VARCHAR(50) DEFAULT 'Asia/Kolkata',
    languages TEXT[] DEFAULT ARRAY['en-IN', 'hi-IN'],
    business_hours JSONB,
    escalation_phone VARCHAR(20),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Agent Configurations Table
CREATE TABLE agent_configs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID REFERENCES businesses(id) ON DELETE CASCADE,
    persona_name VARCHAR(100) DEFAULT 'Dental Assistant',
    persona_description TEXT,
    voice_id VARCHAR(100) DEFAULT 'en-US-Standard-A',
    language_code VARCHAR(20) DEFAULT 'en-IN',
    system_prompt TEXT NOT NULL,
    allowed_actions JSONB,
    escalation_rules JSONB,
    fallback_behavior VARCHAR(50) DEFAULT 'transfer_human',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Call Logs Table
CREATE TABLE call_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID REFERENCES businesses(id) ON DELETE CASCADE,
    caller_phone VARCHAR(20) NOT NULL,
    call_direction VARCHAR(20) DEFAULT 'inbound',
    call_status VARCHAR(50) DEFAULT 'completed',
    duration_seconds INTEGER,
    transcript TEXT,
    summary TEXT,
    intent_detected VARCHAR(100),
    action_taken VARCHAR(100),
    escalated_to_human BOOLEAN DEFAULT false,
    booking_created BOOLEAN DEFAULT false,
    latency_ms INTEGER,
    recording_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Appointments Table
CREATE TABLE appointments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID REFERENCES businesses(id) ON DELETE CASCADE,
    call_log_id UUID REFERENCES call_logs(id),
    patient_name VARCHAR(255) NOT NULL,
    patient_phone VARCHAR(20) NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    service_type VARCHAR(100),
    status VARCHAR(50) DEFAULT 'scheduled',
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Analytics Summary View
CREATE VIEW analytics_summary AS
SELECT 
    b.id as business_id,
    b.name as business_name,
    COUNT(cl.id) as total_calls,
    COUNT(CASE WHEN cl.booking_created = true THEN 1 END) as bookings_created,
    COUNT(CASE WHEN cl.escalated_to_human = true THEN 1 END) as human_escalations,
    AVG(cl.latency_ms) as avg_latency_ms,
    AVG(cl.duration_seconds) as avg_call_duration
FROM businesses b
LEFT JOIN call_logs cl ON b.id = cl.business_id
WHERE b.is_active = true
GROUP BY b.id, b.name;

-- Indexes for Performance
CREATE INDEX idx_call_logs_business_id ON call_logs(business_id);
CREATE INDEX idx_call_logs_created_at ON call_logs(created_at DESC);
CREATE INDEX idx_appointments_business_id ON appointments(business_id);
CREATE INDEX idx_appointments_date ON appointments(appointment_date);

-- Insert sample dental clinic
INSERT INTO businesses (name, phone, email, address, escalation_phone) 
VALUES (
    'Smile Care Dental Clinic',
    '+919876543210',
    'contact@smilecare.in',
    'MG Road, Bangalore, Karnataka',
    '+919876543211'
);

-- Insert default agent config for sample clinic
INSERT INTO agent_configs (business_id, persona_name, persona_description, system_prompt)
SELECT 
    id,
    'Dr. Priya - Dental Assistant',
    'Friendly, professional dental assistant who speaks English and Hindi',
    'You are Dr. Priya, a helpful dental assistant at Smile Care Dental Clinic. You speak both English and Hindi fluently. Your role is to: 1) Answer patient questions about dental services, 2) Book appointments based on available slots, 3) Handle emergencies by escalating to human staff, 4) Provide pricing information for common procedures. Always be empathetic and professional. If the caller is in severe pain, immediately escalate to human staff.'
FROM businesses 
WHERE name = 'Smile Care Dental Clinic';
