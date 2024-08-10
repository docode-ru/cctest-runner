#!/bin/bash


python3 -m streamlit run cctest.py

if [ $? -eq 0 ]; then
    exit 0
else
    python -m streamlit run cctest.py
fi
