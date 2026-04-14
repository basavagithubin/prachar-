#!/usr/bin/env bash
# This file is used by Render.com for deployment

gunicorn candidate_management.wsgi:application --bind 0.0.0.0:$PORT
