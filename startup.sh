#!/bin/bash
python -m streamlit run client_audit_form.py --server.port $PORT --server.address 0.0.0.0 --server.headless true --server.enableCORS false
