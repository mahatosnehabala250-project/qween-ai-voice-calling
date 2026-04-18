'use client';

import { useState } from 'react';
import { Phone, Mic, Calendar, BarChart3 } from 'lucide-react';

export default function Home() {
  const [isCalling, setIsCalling] = useState(false);

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900">
      {/* Header */}
      <header className="p-6 border-b border-white/10">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <h1 className="text-3xl font-bold text-white">👑 Queen Voice AI</h1>
          <nav className="space-x-6 hidden md:block">
            <a href="#dashboard" className="text-white/80 hover:text-white">Dashboard</a>
            <a href="#calls" className="text-white/80 hover:text-white">Call Logs</a>
            <a href="#settings" className="text-white/80 hover:text-white">Settings</a>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <main className="max-w-7xl mx-auto p-6">
        <div className="text-center py-20">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            AI Phone Agents for Indian Businesses
          </h2>
          <p className="text-xl text-white/80 mb-8 max-w-3xl mx-auto">
            Never miss a call. Book appointments 24/7. Speak Hindi & English fluently.
          </p>
          
          <button 
            onClick={() => setIsCalling(!isCalling)}
            className="bg-white text-purple-900 px-8 py-4 rounded-full text-lg font-semibold hover:bg-purple-100 transition flex items-center gap-3 mx-auto"
          >
            <Phone className="w-6 h-6" />
            {isCalling ? 'End Test Call' : 'Try Demo Call'}
          </button>

          {isCalling && (
            <div className="mt-8 p-6 bg-white/10 backdrop-blur-sm rounded-lg max-w-md mx-auto border border-white/20">
              <div className="flex items-center gap-4 text-white">
                <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                <span>Connected to +91 80654 81672</span>
              </div>
              <p className="mt-4 text-white/90 italic">
                "Namaste! Main Queen bol rahi hoon. Kaise help kar sakti hoon?"
              </p>
            </div>
          )}
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-6 mt-20">
          <FeatureCard 
            icon={<Mic className="w-8 h-8" />}
            title="Natural Conversations"
            description="Hindi & English support with human-like voice"
          />
          <FeatureCard 
            icon={<Calendar className="w-8 h-8" />}
            title="Auto Booking"
            description="Book appointments directly into your calendar"
          />
          <FeatureCard 
            icon={<BarChart3 className="w-8 h-8" />}
            title="Analytics Dashboard"
            description="Track calls, conversions, and ROI in real-time"
          />
        </div>

        {/* Stats Section */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-20">
          <StatCard number="500+" label="Calls Handled" />
          <StatCard number="98%" label="Answer Rate" />
          <StatCard number="<600ms" label="Response Time" />
          <StatCard number="₹0.73/min" label="Cost" />
        </div>

        {/* CTA Section */}
        <div className="mt-20 text-center">
          <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-12 border border-white/20">
            <h3 className="text-3xl font-bold text-white mb-4">Ready to Transform Your Business?</h3>
            <p className="text-white/80 mb-8 max-w-2xl mx-auto">
              Join 50+ Indian clinics using Queen Voice AI to handle calls 24/7
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="bg-white text-purple-900 px-8 py-3 rounded-lg font-semibold hover:bg-purple-100 transition">
                Start Free Trial
              </button>
              <button className="bg-transparent border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white/10 transition">
                Book Demo
              </button>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-white/10 mt-20 py-8">
        <div className="max-w-7xl mx-auto text-center text-white/60">
          <p>© 2025 Queen Voice AI. Built for India 🇮🇳</p>
          <p className="mt-2 text-sm">Powered by Vobiz, LiveKit & Gemini AI</p>
        </div>
      </footer>
    </div>
  );
}

function FeatureCard({ icon, title, description }) {
  return (
    <div className="bg-white/10 backdrop-blur-sm p-6 rounded-lg border border-white/20 hover:bg-white/20 transition">
      <div className="text-purple-300 mb-4">{icon}</div>
      <h3 className="text-xl font-semibold text-white mb-2">{title}</h3>
      <p className="text-white/70">{description}</p>
    </div>
  );
}

function StatCard({ number, label }) {
  return (
    <div className="text-center p-6 bg-white/5 rounded-lg backdrop-blur-sm border border-white/10">
      <div className="text-3xl font-bold text-purple-300 mb-2">{number}</div>
      <div className="text-white/60">{label}</div>
    </div>
  );
}
