# MSP Cybersecurity Assessment Tool

## Overview
Comprehensive cybersecurity risk assessment tool for Managed Service Providers.

## Local Development Setup
1. Clone repository
2. Create virtual environment: `python -m venv venv`
3. Activate environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and add your SendGrid API key
6. Add logo file: `seedpod_logo.png`
7. Run application: `streamlit run comprehensive_msp_assessment.py`

## Deployment
Deployed automatically to Azure App Service via Azure DevOps pipelines.

## Team
- SeedPod Cyber Development Team
