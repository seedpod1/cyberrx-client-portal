# CyberRX Client Portal

**Business information collection portal for SeedPod Cyber insurance assessments**

---

## 🎯 Purpose

This portal allows end-clients to complete the business information portion of their cyber insurance assessment after their MSP has completed the technical security evaluation.

## ✨ Key Features

- ✅ **No password required** - Direct access via unique link
- ✅ **Auto-populated fields** - Client info pre-filled from MSP assessment
- ✅ **Simplified interface** - Only business information, no technical questions
- ✅ **Mobile-friendly** - Responsive design for any device
- ✅ **Automatic submission** - Results sent to SeedPod team
- ✅ **Email confirmation** - Client receives confirmation upon completion

---

## 📋 What Clients Complete

This portal collects business information only:

### 👤 Contact Information
- First Name (auto-filled)
- Last Name (auto-filled)
- Email Address (auto-filled)
- MSP Company Name (auto-filled)
- Organization Name (auto-filled)

### 🏢 Business Information
- Organization Address
- Website URL
- NAICS Industry Code
- Total Employees
- Annual Revenue
- Year Established

### 🛡️ Cyber Insurance Information
- Current cyber insurance status (Yes/No)
- If yes: Policy details, limits, carrier

### ⚠️ Loss History
- Ransomware attacks
- Data breaches
- Business email compromise
- Wire fraud
- Claims history

### 🔐 Authentication Procedures
- Multi-factor authentication usage
- Password policy details
- Wire transfer validation procedures

---

## 🔗 Integration with MSP Assessment

### How Clients Access This Portal

1. **MSP completes technical assessment** in MSP Assessment app
2. **MSP enters client information:**
   - Client Name: "Jane Smith"
   - Client Email: "jane@acme.com"
   - Organization Name: "Acme Corp"
3. **System sends email to client** with unique link:
   ```
   https://client-portal.railway.app?
     msp_name=ABC+Technology
     &client_name=Jane+Smith
     &client_email=jane@acme.com
     &organization=Acme+Corp
   ```
4. **Client clicks link** → Form opens with information pre-filled
5. **Client completes and submits** → Data sent to SeedPod

### Auto-Population from URL

The portal automatically reads these parameters:

| URL Parameter | Populates Field |
|---------------|-----------------|
| `client_name` | First Name + Last Name |
| `client_email` | Email Address |
| `msp_name` | MSP Company Name |
| `organization` | Organization Name |

**Example:**
- URL param: `client_name=Jane+Smith`
- Auto-fills: First Name: "Jane", Last Name: "Smith"

---

## 🚫 What's NOT in This Portal

This portal intentionally excludes all technical security questions:

❌ Security Controls Assessment  
❌ Patch Management  
❌ EDR/Antivirus Status  
❌ Email Filtering  
❌ Backup Procedures  
❌ Network Security  
❌ SIEM/Log Management  
❌ All other technical MSP questions  

**Why?** These are completed by the MSP in the MSP Assessment app.

---

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Purpose | Example |
|----------|----------|---------|---------|
| `SENDGRID_API_KEY` | Yes | Email confirmation | `SG.xxx...` |
| `PORT` | Auto | Application port | `8080` |

**Note:** Unlike MSP Assessment, this portal does NOT need:
- ~~`CLIENT_PORTAL_URL`~~ (not applicable)
- ~~`CLIENT_ACCESS_KEY`~~ (no password required)

### Railway Deployment

Configured for Railway with:
- **Procfile**: `streamlit run client_portal_form.py`
- **railway.json**: Deployment settings
- **.streamlit/config.toml**: Streamlit configuration
- **requirements.txt**: Python dependencies

---

## 📦 Files

```
cyberrx-client-portal/
├── client_portal_form.py      # Main application (simplified)
├── seedpod_logo.png           # SeedPod branding
├── requirements.txt           # Python dependencies
├── Procfile                   # Railway start command
├── railway.json               # Railway configuration
├── .streamlit/
│   └── config.toml           # Streamlit settings
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

---

## 🛠️ Local Development

### Prerequisites
- Python 3.11+
- pip package manager

### Setup

```bash
# Clone repository
git clone https://github.com/seedpod1/cyberrx-client-portal.git
cd cyberrx-client-portal

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SENDGRID_API_KEY="your_key_here"

# Run application
streamlit run client_portal_form.py
```

### Local Testing with URL Parameters

Test auto-population locally:
```
http://localhost:8501?
  msp_name=Test+MSP
  &client_name=John+Doe
  &client_email=john@test.com
  &organization=Test+Company
```

---

## 📊 Workflow

```
┌─────────────────────────────────────────────────┐
│  Client receives email from MSP                 │
│  Subject: "Complete Your Client Information"   │
└─────────────────┬───────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────┐
│  Client clicks link in email                    │
│  https://client-portal.railway.app?params       │
└─────────────────┬───────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────┐
│  Portal opens with pre-filled information:      │
│  ✅ First Name: "Jane"                          │
│  ✅ Last Name: "Smith"                          │
│  ✅ Email: "jane@acme.com"                      │
│  ✅ MSP Name: "ABC Technology"                  │
│  ✅ Organization: "Acme Corp"                   │
└─────────────────┬───────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────┐
│  Client completes remaining fields:             │
│  • Address, NAICS, Revenue, Employees           │
│  • Cyber insurance status                       │
│  • Loss history                                 │
│  • Authentication procedures                    │
└─────────────────┬───────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────┐
│  Client clicks "Submit"                         │
│  • Data validated                               │
│  • CSV generated                                │
│  • Email sent to support@seedpodcyber.com       │
│  • Confirmation shown to client                 │
└─────────────────────────────────────────────────┘
```

---

## 🎨 Branding

- **Primary Color**: #009D4F (SeedPod Green)
- **Secondary Color**: #013220 (Dark Green)
- **Logo**: seedpod_logo.png (400px width)
- **Page Title**: "Client Business Information"
- **Subtitle**: "Cyber Insurance Assessment - Client Portion"

---

## 🔒 Security Features

### Access Control
- **No password required** - Simplified for clients
- **Unique URLs** - Each link contains client-specific parameters
- **One-time use concept** - Links sent privately via email
- **HTTPS enforced** - All traffic encrypted via Railway

### Why No Password?

1. **Better user experience** - One less step for clients
2. **Higher completion rates** - Fewer drop-offs
3. **Secure enough** - URL is private and contains unique identifiers
4. **Similar to "magic links"** - Common authentication pattern

### Privacy
- Client data submitted via HTTPS
- No data stored in browser
- Results emailed securely to SeedPod team
- No cookies or tracking

---

## 📱 Responsive Design

Optimized for all devices:
- ✅ Desktop computers (1920x1080+)
- ✅ Laptops (1366x768+)
- ✅ Tablets (iPad, Android)
- ✅ Mobile phones (iPhone, Android)

Form layout adapts automatically to screen size.

---

## 🐛 Troubleshooting

### Fields Not Pre-filling

**Symptom**: Client name, email, MSP name appear empty

**Check:**
1. **URL in email** - Should have parameters like `?client_name=John+Doe`
2. **Browser URL bar** - Verify parameters are present after clicking
3. **Browser console** - Check for JavaScript errors (F12)

**Fix:**
- MSP Assessment must pass parameters correctly
- Ensure updated MSP Assessment code is deployed
- Verify MSP selected "Split Assessment" mode

### Form Submission Fails

**Symptom**: Error when clicking Submit

**Solutions:**
1. Check `SENDGRID_API_KEY` is set in Railway
2. Verify all required fields are completed
3. Check Railway logs for detailed error
4. Ensure SendGrid account is active

### Email Not Received

**Symptom**: Client submitted but no email at SeedPod

**Check:**
1. SendGrid dashboard for send status
2. Spam/junk folders
3. Railway logs for submission confirmation
4. Verify sender email is verified in SendGrid

### Logo Not Displaying

**Symptom**: Shows "SeedPod CYBER" text instead of logo

**Solution:**
```bash
# Ensure logo file is in repository
ls seedpod_logo.png

# If missing, add it
git add seedpod_logo.png
git commit -m "Add SeedPod logo"
git push origin main
```

---

## 🔄 Updates & Deployment

### Deploy Changes

```bash
# Make changes to client_portal_form.py
git add client_portal_form.py
git commit -m "Description of changes"
git push origin main
```

Railway automatically deploys in ~2 minutes.

### Important: File Naming

This portal uses `client_portal_form.py` (not `client_audit_form.py`)

If you rename the file, update:
- **Procfile**: Change filename in start command
- **railway.json**: Update `startCommand`

---

## 📈 Analytics & Tracking

### UTM Parameters

While the portal doesn't require UTM tracking, it preserves UTM parameters passed from MSP Assessment:

- `utm_source` - Traffic source (e.g., msp_assessment)
- `utm_medium` - Medium (e.g., email)
- `utm_campaign` - Campaign name (e.g., client_completion)

These are included in CSV exports for attribution analysis.

### Metrics to Track

From Railway/SendGrid dashboards:
- Completion rate (emails sent vs. submitted)
- Average time to complete
- Drop-off points
- Error rates

---

## 💡 Best Practices for MSPs

When sending clients to this portal:

1. **Explain the process** - Tell clients to expect an email
2. **Check spam** - Clients should check junk folders
3. **Use work email** - Better deliverability than personal emails
4. **Set expectations** - 10-15 minutes to complete
5. **Be available** - Clients may have questions

### Sample Email to Client

```
Subject: Complete Your Cyber Insurance Assessment

Hi [Client Name],

Your MSP partner [MSP Name] has completed the technical security 
portion of your cyber insurance assessment. 

To complete the process, please click the link below to provide 
some basic business information about your organization (10-15 minutes):

[LINK TO PORTAL]

The form has been pre-filled with your contact information. You'll 
need to provide:
- Business details (address, industry, size)
- Cyber insurance status
- Brief security history

If you have any questions, contact us at support@seedpodcyber.com

Thank you,
The SeedPod Cyber Team
```

---

## 📞 Support

- **Email**: support@seedpodcyber.com
- **MSP Support**: partners@seedpodcyber.com
- **Documentation**: https://docs.seedpodcyber.com
- **Repository**: https://github.com/seedpod1/cyberrx-client-portal

---

## 🔗 Related Applications

- **MSP Assessment**: https://github.com/seedpod1/cyberrx-assessment
- **SeedPod Website**: https://seedpodcyber.com

---

## 📄 License

Proprietary - SeedPod Cyber LLC. All rights reserved.

---

## 🏢 About SeedPod Cyber

SeedPod Cyber makes cyber insurance accessible for SMBs through technology-driven underwriting and MSP partnerships.

**Key Stats:**
- 1.3% loss ratio (industry: 40-45%)
- API-driven underwriting
- Real-time security monitoring
- MSP-first distribution model

**Learn More**: https://seedpodcyber.com

---

**Version**: 2.0  
**Last Updated**: January 2026  
**Maintained by**: SeedPod Cyber Development Team

---

## 🎯 Quick Reference

### For Clients
- ✅ No account needed
- ✅ No password to remember
- ✅ Information pre-filled
- ✅ 10-15 minutes to complete
- ✅ Mobile-friendly

### For MSPs
- ✅ Automatically sends client email
- ✅ Client info pre-populated
- ✅ No manual follow-up needed
- ✅ Email confirmation when complete
- ✅ Reduces friction in workflow

### For SeedPod Team
- ✅ Complete data (technical + business)
- ✅ CSV exports for analysis
- ✅ UTM tracking for attribution
- ✅ Automated workflow
- ✅ High completion rates
