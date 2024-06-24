#!/usr/bin/env sh

stripe listen --forward-to https://localhost:8000/dashboard/billing/webhooks/stripe/
