import streamlit as st
from utils import rerun

def landing_page():
    st.set_page_config(
        page_title="Medicare Plus - Professional Healthcare Platform",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Manrope:wght@300;400;500;600;700;800&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Hide Streamlit elements */
    header, #MainMenu, footer, .stDeployButton {
        visibility: hidden !important;
        height: 0 !important;
    }
    
    /* Enhanced background with animated gradient */
    .stApp {
        background: linear-gradient(-45deg, #667eea, #764ba2, #6B73FF, #9A9CE3);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        min-height: 100vh;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Floating elements animation */
    .floating-shapes {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1;
    }
    
    .shape {
        position: absolute;
        opacity: 0.1;
        animation: float 20s infinite linear;
    }
    
    .shape1 {
        top: 10%;
        left: 10%;
        width: 80px;
        height: 80px;
        background: white;
        border-radius: 50%;
        animation-delay: 0s;
    }
    
    .shape2 {
        top: 20%;
        right: 10%;
        width: 60px;
        height: 60px;
        background: white;
        border-radius: 10px;
        animation-delay: 5s;
    }
    
    .shape3 {
        bottom: 20%;
        left: 15%;
        width: 100px;
        height: 100px;
        background: white;
        border-radius: 30px;
        animation-delay: 10s;
    }
    
    .shape4 {
        bottom: 10%;
        right: 20%;
        width: 40px;
        height: 40px;
        background: white;
        border-radius: 50%;
        animation-delay: 15s;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    /* Navigation Bar */
    .navbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 80px;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0 5%;
        z-index: 1000;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    .logo {
        display: flex;
        align-items: center;
        gap: 12px;
        font-family: 'Manrope', sans-serif;
        font-weight: 800;
        font-size: 24px;
        color: #1e293b;
    }
    
    .logo-icon {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 18px;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    /* Main content */
    .main-content {
        padding-top: 80px;
        max-width: 1400px;
        margin: 0 auto;
        position: relative;
        z-index: 2;
    }
    
    /* Hero Section */
    .hero {
        padding: 120px 5% 100px;
        text-align: center;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 30px;
        margin: 40px 5%;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    }
    
    .hero::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.2) 0%, transparent 50%),
                    radial-gradient(circle at 70% 70%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
        pointer-events: none;
    }
    
    .hero-content {
        position: relative;
        z-index: 2;
        max-width: 800px;
        margin: 0 auto;
    }
    
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(255, 255, 255, 0.2);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 32px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .hero-title {
        font-family: 'Manrope', sans-serif;
        font-size: 64px;
        font-weight: 800;
        line-height: 1.1;
        color: white;
        margin-bottom: 24px;
        letter-spacing: -0.02em;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .hero-subtitle {
        font-size: 20px;
        color: rgba(255, 255, 255, 0.9);
        line-height: 1.6;
        margin-bottom: 48px;
        font-weight: 400;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    .hero-stats {
        display: flex;
        justify-content: center;
        gap: 64px;
        flex-wrap: wrap;
        margin-bottom: 48px;
    }
    
    .stat {
        text-align: center;
        background: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .stat-number {
        font-family: 'Manrope', sans-serif;
        font-size: 32px;
        font-weight: 800;
        color: white;
        display: block;
        margin-bottom: 8px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .stat-label {
        font-size: 14px;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 500;
    }
    
    /* Features Section */
    .features {
        padding: 120px 5%;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        margin: 40px 5%;
        border-radius: 30px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    }
    
    .section-header {
        text-align: center;
        margin-bottom: 80px;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .section-title {
        font-family: 'Manrope', sans-serif;
        font-size: 48px;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 16px;
        letter-spacing: -0.02em;
    }
    
    .section-subtitle {
        font-size: 18px;
        color: #64748b;
        line-height: 1.6;
    }
    
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
        gap: 32px;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 40px;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover::before {
        transform: scaleX(1);
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
        border-color: #3b82f6;
    }
    
    .feature-icon {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 24px;
        font-size: 32px;
        color: white;
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
    }
    
    .feature-title {
        font-family: 'Manrope', sans-serif;
        font-size: 24px;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 12px;
    }
    
    .feature-description {
        font-size: 16px;
        color: #64748b;
        line-height: 1.6;
        margin-bottom: 20px;
    }
    
    .feature-link {
        color: #3b82f6;
        text-decoration: none;
        font-weight: 600;
        font-size: 14px;
        display: inline-flex;
        align-items: center;
        gap: 4px;
        transition: all 0.3s ease;
        padding: 8px 16px;
        border-radius: 8px;
        background: rgba(59, 130, 246, 0.1);
    }
    
    .feature-link:hover {
        color: #2563eb;
        background: rgba(59, 130, 246, 0.2);
        transform: translateX(4px);
    }
    
    /* Trust Section */
    .trust {
        padding: 120px 5%;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        margin: 40px 5%;
        border-radius: 30px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    }
    
    .trust-content {
        max-width: 1200px;
        margin: 0 auto;
        text-align: center;
    }
    
    .trust-logos {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 64px;
        margin-bottom: 64px;
        flex-wrap: wrap;
        opacity: 0.8;
    }
    
    .trust-logo {
        font-size: 28px;
        color: white;
        background: rgba(255, 255, 255, 0.1);
        padding: 15px 25px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .trust-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 32px;
        margin-bottom: 80px;
    }
    
    .trust-item {
        text-align: center;
        background: rgba(255, 255, 255, 0.1);
        padding: 32px;
        border-radius: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .trust-item:hover {
        transform: translateY(-4px);
        background: rgba(255, 255, 255, 0.2);
    }
    
    .trust-icon {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 24px;
        font-size: 32px;
        color: white;
        box-shadow: 0 8px 24px rgba(16, 185, 129, 0.3);
    }
    
    .trust-title {
        font-family: 'Manrope', sans-serif;
        font-size: 20px;
        font-weight: 700;
        color: white;
        margin-bottom: 8px;
    }
    
    .trust-desc {
        font-size: 14px;
        color: rgba(255, 255, 255, 0.8);
        line-height: 1.6;
    }
    
    /* CTA Section */
    .cta {
        padding: 120px 5%;
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        text-align: center;
        color: white;
        margin: 40px 5%;
        border-radius: 30px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
    }
    
    .cta-title {
        font-family: 'Manrope', sans-serif;
        font-size: 48px;
        font-weight: 800;
        margin-bottom: 16px;
        letter-spacing: -0.02em;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .cta-subtitle {
        font-size: 18px;
        opacity: 0.9;
        margin-bottom: 48px;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
        padding: 24px 48px !important;
        border-radius: 15px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 12px 32px rgba(59, 130, 246, 0.4) !important;
        width: auto !important;
        max-width: 350px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 16px 40px rgba(59, 130, 246, 0.5) !important;
    }
    
    /* Footer */
    .footer {
        padding: 80px 5% 40px;
        background: rgba(30, 41, 59, 0.95);
        backdrop-filter: blur(20px);
        color: white;
        margin: 40px 5%;
        border-radius: 30px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
    }
    
    .footer-content {
        max-width: 800px;
        margin: 0 auto;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 48px;
        margin-bottom: 48px;
    }
    
    .footer-section h3 {
        font-family: 'Manrope', sans-serif;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 16px;
        color: white;
    }
    
    .footer-section p,
    .footer-section a {
        color: #94a3b8;
        text-decoration: none;
        line-height: 1.6;
        font-size: 14px;
    }
    
    .footer-section a:hover {
        color: white;
    }
    
    .footer-bottom {
        border-top: 1px solid #334155;
        padding-top: 32px;
        text-align: center;
        color: #64748b;
        font-size: 14px;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .navbar {
            padding: 0 20px;
        }
        
        .hero, .features, .trust, .cta, .footer {
            margin: 20px;
            padding: 60px 20px;
        }
        
        .hero-title {
            font-size: 40px;
        }
        
        .hero-subtitle {
            font-size: 18px;
        }
        
        .hero-stats {
            gap: 32px;
        }
        
        .section-title {
            font-size: 36px;
        }
        
        .features-grid {
            grid-template-columns: 1fr;
        }
        
        .trust-grid {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Floating background shapes
    st.markdown("""
    <div class="floating-shapes">
        <div class="shape shape1"></div>
        <div class="shape shape2"></div>
        <div class="shape shape3"></div>
        <div class="shape shape4"></div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation (Sign In button removed)
    st.markdown("""
    <div class="navbar">
        <div class="logo">
            <div class="logo-icon">⚕️</div>
            <span>Medicare Plus</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Main Content
    st.markdown('<div class="main-content">', unsafe_allow_html=True)

    # Hero Section (buttons removed, start button moved up)
    st.markdown("""
    <div class="hero">
        <div class="hero-content">
            <div class="hero-badge">
                <span>🏆</span>
                <span>Trusted by 50,000+ patients nationwide</span>
            </div>
            <h1 class="hero-title">Healthcare Made Simple & Accessible</h1>
            <p class="hero-subtitle">
                Connect with certified doctors and order prescription medicines from the comfort of your home. Available 24/7 across India.
            </p>
    """, unsafe_allow_html=True)

    # Start button moved up (right after subtitle)
    if st.button("🚀 Start Your Healthcare Journey", key="start_button"):
        st.session_state["current_page"] = "login"
        rerun(st)

    st.markdown("""
            <div class="hero-stats">
                <div class="stat">
                    <span class="stat-number">50,000+</span>
                    <span class="stat-label">Happy Patients</span>
                </div>
                <div class="stat">
                    <span class="stat-number">500+</span>
                    <span class="stat-label">Expert Doctors</span>
                </div>
                <div class="stat">
                    <span class="stat-number">15,000+</span>
                    <span class="stat-label">Medicines Available</span>
                </div>
                <div class="stat">
                    <span class="stat-number">24/7</span>
                    <span class="stat-label">Customer Support</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Features Section
    st.markdown("""
    <div class="features">
        <div class="section-header">
            <h2 class="section-title">Complete Healthcare Solutions</h2>
            <p class="section-subtitle">
                Everything you need for your health and wellness, delivered with care and precision by our team of healthcare professionals.
            </p>
        </div>
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">🩺</div>
                <h3 class="feature-title">Online Doctor Consultations</h3>
                <p class="feature-description">
                    Connect with certified doctors through video calls, voice calls, or chat. Get medical advice, prescriptions, and follow-up care from specialists across all medical fields.
                </p>
                <a href="#" class="feature-link">Book consultation →</a>
            </div>
            <div class="feature-card">
                <div class="feature-icon">💊</div>
                <h3 class="feature-title">Prescription Medicine Delivery</h3>
                <p class="feature-description">
                    Order prescription and over-the-counter medicines online. Upload your prescription, verify with our pharmacists, and get medicines delivered to your doorstep.
                </p>
                <a href="#" class="feature-link">Order medicines →</a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Trust Section
    st.markdown("""
    <div class="trust">
        <div class="trust-content">
            <div class="trust-logos">
                <div class="trust-logo">🏛️ MCI</div>
                <div class="trust-logo">🛡️ ISO 27001</div>
                <div class="trust-logo">⚖️ HIPAA</div>
                <div class="trust-logo">🔒 SSL</div>
            </div>
            <div class="trust-grid">
                <div class="trust-item">
                    <div class="trust-icon">🛡️</div>
                    <h3 class="trust-title">Secure & Confidential</h3>
                    <p class="trust-desc">Your health data is encrypted and stored securely with enterprise-grade security measures.</p>
                </div>
                <div class="trust-item">
                    <div class="trust-icon">✅</div>
                    <h3 class="trust-title">Licensed Professionals</h3>
                    <p class="trust-desc">All doctors and pharmacists are verified, licensed, and registered with respective medical councils.</p>
                </div>
                <div class="trust-item">
                    <div class="trust-icon">🚚</div>
                    <h3 class="trust-title">Fast Delivery</h3>
                    <p class="trust-desc">Same-day delivery in major cities with temperature-controlled logistics for medicines.</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # CTA Section
    st.markdown("""
    <div class="cta">
        <h2 class="cta-title">Ready to Transform Your Healthcare Experience?</h2>
        <p class="cta-subtitle">
            Join thousands of satisfied patients who trust Medicare Plus for their healthcare needs. Start your journey to better health today.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="footer">
        <div class="footer-content">
            <div class="footer-section">
                <h3>Contact</h3>
                <p>📞 +91 1800-123-4567</p>
                <p>📧 support@medicareplus.com</p>
                <p>🏥 24/7 Emergency Helpline</p>
                <p>💬 Live Chat Available</p>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2024 Medicare Plus. All rights reserved. | Licensed Healthcare Provider | Registered with Medical Council of India</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

