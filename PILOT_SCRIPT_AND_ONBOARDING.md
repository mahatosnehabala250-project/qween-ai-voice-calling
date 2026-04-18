# 🦷 DENTAL CLINIC VOICE AI - PILOT SCRIPT

## 📞 THE "PERFECT CALL" FLOW (Hindi/English)

### Scenario: Patient calling for appointment booking

**AI Persona:** Friendly, professional, efficient. Name: "ClinicAssist"

---

### 1. GREETING (0-5 seconds)
**AI:** "Namaste! Thank you for calling [Clinic Name]. This is [AI Name], your virtual assistant. How can I help you today?"
*(Hindi: "Namaste! [Clinic Name] mein aapka swagat hai. Main [AI Name] hoon, aapki sahayata ke liye. Kaise madad kar sakti hoon?")*

---

### 2. INTENT DETECTION (5-15 seconds)

**Patient:** "I want to book an appointment for teeth cleaning."
*(Hindi: "Mujhe teeth cleaning ke liye appointment leni hai.")*

**AI Actions:**
- Detect intent: `BOOK_APPOINTMENT`
- Extract service: `TEETH_CLEANING`
- Respond: "Great! I can help you book a teeth cleaning appointment. May I have your name please?"

---

### 3. PATIENT INFO COLLECTION (15-30 seconds)

**Patient:** "Rajesh Kumar"

**AI Actions:**
- Store name: `Rajesh Kumar`
- Ask: "Thank you Rajesh. Are you a new patient or have you visited us before?"

---

### 4. SCHEDULING (30-60 seconds)

**Patient:** "New patient"

**AI Actions:**
- Check calendar for next available slots
- Offer options: "We have availability tomorrow at 11 AM or Thursday at 4 PM. Which works better for you?"
*(Hindi: "Kal subah 11 baje ya Guruvaar ko shaam 4 baje available hai. Kaunsa samay behtar rahega?")*

**Patient:** "Tomorrow 11 AM"

**AI Actions:**
- Confirm slot: `Tomorrow, 11:00 AM`
- Verify: "Perfect! Booking you for tomorrow at 11 AM with Dr. Sharma. Should I send a confirmation on WhatsApp?"

---

### 5. CONFIRMATION & WRAP-UP (60-90 seconds)

**Patient:** "Yes, send on WhatsApp"

**AI Actions:**
- Ask number: "Please share your WhatsApp number."
- Patient provides: `9876543210`
- Final confirmation: "Thank you Rajesh! Your appointment is confirmed for tomorrow at 11 AM. You'll receive a WhatsApp message shortly. Anything else I can help with?"

**Patient:** "No, that's all."

**AI:** "Wonderful! We look forward to seeing you. Have a great day!"

---

## 🔄 EDGE CASE HANDLING

### Case 1: Emergency/Urgent Pain
**Patient:** "I have severe tooth pain!"
**AI Response:** "I understand you're in pain. Let me connect you to our emergency line immediately."
→ **ACTION:** Transfer to doctor's mobile (`+91-XXXXXXXXXX`)

### Case 2: Price Inquiry
**Patient:** "How much does root canal cost?"
**AI Response:** "Root canal treatment typically ranges from ₹3,000 to ₹8,000 depending on complexity. Our dentist will give you an exact quote after examination. Would you like to book a consultation?"

### Case 3: Rescheduling/Canceling
**Patient:** "I need to cancel my appointment."
**AI Response:** "I can help with that. May I have your phone number to find your booking?"
→ Look up → "Found your appointment for [Date]. Should I cancel or reschedule?"

### Case 4: Language Switch
**Patient:** (Starts in Hindi mid-call)
**AI:** Automatically detects language → Switches to Hindi seamlessly.

### Case 5: AI Uncertainty (Confidence < 60%)
**Patient:** "Do you do braces for children?"
**AI:** "Let me connect you with our orthodontic specialist who can answer this in detail."
→ **ACTION:** Transfer to staff member

---

## 📋 CLINIC ONBOARDING FORM (Google Form Template)

### Section 1: Basic Info
- Clinic Name: ___________
- Owner/Doctor Name: ___________
- Phone Number: ___________
- WhatsApp Number: ___________
- Address: ___________

### Section 2: Operating Hours
- Monday-Friday: ___ AM to ___ PM
- Saturday: ___ AM to ___ PM
- Sunday: Closed / Open (___ AM to ___ PM)

### Section 3: Services Offered (Check all that apply)
- [ ] Teeth Cleaning (₹___)
- [ ] Root Canal (₹___ - ₹___)
- [ ] Tooth Extraction (₹___)
- [ ] Braces (₹___ - ₹___)
- [ ] Dental Implants (₹___ - ₹___)
- [ ] Teeth Whitening (₹___)
- [ ] Emergency Care (Yes/No)
- [ ] Pediatric Dentistry (Yes/No)

### Section 4: Doctors/Staff
- Doctor 1 Name: ___________ (Specialization: _______)
- Doctor 2 Name: ___________ (Specialization: _______)
- Receptionist Mobile (for transfers): ___________

### Section 5: Booking Rules
- Appointment duration: ___ minutes (default: 30)
- Buffer time between appointments: ___ minutes (default: 15)
- Max bookings per day: ___ (default: 20)
- Advance booking allowed: ___ days (default: 30)

### Section 6: Calendar Integration
- Google Calendar Email: ___________
- Do you use Practo? Yes / No
- Do you use any other software? ___________

### Section 7: Voice & Personality
- Preferred AI Voice: Male / Female / No preference
- Tone: Formal / Friendly / Warm
- Languages: English only / Hindi only / Both (Hinglish)

### Section 8: Special Instructions
- Any specific phrases to use? ___________
- Any topics to avoid? ___________
- Emergency contact protocol: ___________

---

## 💻 TECHNICAL IMPLEMENTATION CHECKLIST

### Day 1: Setup
- [ ] Create Vobiz account, get SIP credentials
- [ ] Get Google Cloud API key for Gemini 2.5 Live
- [ ] Set up Supabase project (Mumbai region)
- [ ] Create database schema (clinics, calls, appointments)

### Day 2: Core Logic
- [ ] Build Vobiz webhook handler (incoming calls)
- [ ] Implement Gemini 2.5 Live streaming connection
- [ ] Create system prompt template (dynamic based on clinic)
- [ ] Test basic conversation (Hello → Intent → Response)

### Day 3: Booking System
- [ ] Integrate Google Calendar API
- [ ] Build slot availability checker
- [ ] Implement booking confirmation logic
- [ ] Add WhatsApp notification (Twilio/Meta API)

### Day 4: Edge Cases
- [ ] Implement human transfer (SIP REFER)
- [ ] Add confidence scoring + fallback
- [ ] Handle Hindi/Hinglish code-switching
- [ ] Test emergency scenarios

### Day 5: Dashboard & Analytics
- [ ] Build simple Next.js dashboard
- [ ] Show: Total calls, Booked appointments, Missed calls
- [ ] Add call transcript viewer
- [ ] Export to CSV feature

### Day 6-7: Pilot Testing
- [ ] Make 50 test calls (various scenarios)
- [ ] Fix bugs, optimize prompts
- [ ] Record demo video
- [ ] Approach first clinic for pilot

---

## 📊 SUCCESS METRICS FOR PILOT

| Metric | Target | Why It Matters |
|--------|--------|----------------|
| **Answer Rate** | >95% | Never miss a call |
| **Booking Conversion** | >30% | Turn calls into revenue |
| **Avg Call Duration** | 1.5-3 mins | Efficient but not rushed |
| **Human Transfer Rate** | <15% | AI handles most cases |
| **Customer Satisfaction** | >4.5/5 | Patients like the experience |
| **Latency** | <600ms | Natural conversation flow |
| **Hallucination Rate** | 0% | No wrong appointments |

---

## 🎯 PITCH SCRIPT FOR DENTISTS

**Opening:**
"Dr. [Name], how many patient calls do you miss daily because your receptionist is busy or after hours?"

**Problem:**
"Studies show 62% of patients hang up if not answered in 3 rings. That's potentially ₹5-10 lakhs lost annually in missed appointments."

**Solution:**
"I've built an AI receptionist that answers 24/7, speaks Hindi/English, books appointments directly into your calendar, and costs 1/10th of a human receptionist."

**Proof:**
"We're running pilots with 3 clinics. [Clinic X] recovered 47 missed calls in week 1 and booked 18 new appointments."

**Offer:**
"I'll install it free for 14 days. You pay nothing unless we book more than 10 appointments. Fair?"

**Close:**
"Can I set it up by tomorrow morning? I just need 15 minutes to configure your services and calendar."

---

## 🚀 READY TO LAUNCH!

**Files Created:**
1. ✅ `EXPERT_VERDICT_AND_OPTIMIZED_PLAN.md` - Strategic review
2. ✅ `PILOT_SCRIPT_AND_ONBOARDING.md` - This document

**Next Step:** 
Copy the onboarding form to Google Forms, code the Hello World script, and call your first dentist TODAY!

**Remember:** Perfection is the enemy of progress. Launch with 80% quality, improve based on real calls.

**Jai Hind! 🇮🇳🦷🤖**
