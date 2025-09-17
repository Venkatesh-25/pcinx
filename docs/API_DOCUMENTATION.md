# 🔌 FRA Atlas DSS - API Documentation

## Overview
This document outlines the planned API architecture for the FRA Atlas Decision Support System. The current MVP uses client-side processing; this API design supports the POC and production phases.

## Base URL
```
Production: https://api.fra-atlas.gov.in/v1
Development: http://localhost:5000/api/v1
MVP: Static files (no backend required)
```

## Authentication
```http
POST /auth/login
Content-Type: application/json

{
  "username": "official@odisha.gov.in",
  "password": "secure_password",
  "role": "state_official"
}

Response:
{
  "access_token": "jwt_token_here",
  "user": {
    "id": "user123",
    "role": "state_official",
    "permissions": ["view_claims", "export_reports"],
    "jurisdiction": "odisha"
  }
}
```

## FRA Claims API

### Get Claims
```http
GET /claims?state={state}&status={status}&limit={limit}&offset={offset}

Parameters:
- state: odisha, mp, tripura, telangana
- status: approved, pending, rejected, under_review
- limit: 1-100 (default: 50)
- offset: pagination offset

Response:
{
  "total": 1458,
  "claims": [
    {
      "claim_id": "CFR-2024-OD-101",
      "village_name": "Khandagiri",
      "district": "Khurda",
      "state": "Odisha",
      "area_hectares": 245.6,
      "status": "Approved",
      "approval_date": "2024-03-15",
      "claimant_families": 127,
      "rights_type": "Community Forest Rights",
      "geometry": {...},
      "monitoring": {
        "ndvi_baseline": 0.75,
        "last_monitored": "2025-09-15",
        "alert_level": "High",
        "deforestation_detected": true
      }
    }
  ]
}
```

### Get Single Claim
```http
GET /claims/{claim_id}

Response:
{
  "claim_id": "CFR-2024-OD-101",
  "details": {...},
  "history": [
    {
      "date": "2024-01-15",
      "action": "application_submitted",
      "actor": "community_representative",
      "notes": "Initial application with GPS survey"
    }
  ],
  "documents": [
    {
      "type": "gps_survey",
      "url": "/documents/survey_CFR-2024-OD-101.pdf",
      "uploaded_date": "2024-01-15"
    }
  ]
}
```

## Satellite Monitoring API

### Get NDVI Data
```http
GET /monitoring/ndvi/{claim_id}?start_date={start}&end_date={end}

Parameters:
- start_date: YYYY-MM-DD
- end_date: YYYY-MM-DD

Response:
{
  "claim_id": "CFR-2024-OD-101",
  "temporal_data": [
    {
      "date": "2025-01-10",
      "ndvi_mean": 0.74,
      "ndvi_std": 0.12,
      "cloud_cover": 5,
      "data_quality": "good"
    }
  ],
  "alerts": [
    {
      "date": "2025-09-10",
      "alert_type": "deforestation",
      "severity": "high",
      "area_affected_ha": 12.5,
      "confidence": 0.89
    }
  ]
}
```

### Trigger Monitoring
```http
POST /monitoring/analyze
Content-Type: application/json

{
  "claim_ids": ["CFR-2024-OD-101", "IFR-2024-OD-102"],
  "priority": "high",
  "notify": true
}

Response:
{
  "job_id": "job_12345",
  "status": "queued",
  "estimated_completion": "2025-09-15T14:30:00Z"
}
```

## Alerts API

### Get Alerts
```http
GET /alerts?state={state}&severity={severity}&status={status}

Response:
{
  "total": 15,
  "alerts": [
    {
      "alert_id": "alert_456",
      "claim_id": "CFR-2024-OD-101",
      "type": "deforestation",
      "severity": "high",
      "detected_date": "2025-09-15T08:30:00Z",
      "area_affected": 12.5,
      "confidence_score": 0.89,
      "status": "open",
      "assigned_to": "forest_officer_123",
      "location": {
        "coordinates": [85.8150, 20.2980],
        "description": "Northern boundary of claim area"
      }
    }
  ]
}
```

### Update Alert Status
```http
PATCH /alerts/{alert_id}
Content-Type: application/json

{
  "status": "investigating",
  "assigned_to": "forest_officer_456",
  "notes": "Field team dispatched for verification"
}
```

## Reports API

### Generate Report
```http
POST /reports/generate
Content-Type: application/json

{
  "type": "claim_summary",
  "filters": {
    "state": "odisha",
    "date_range": {
      "start": "2025-01-01",
      "end": "2025-09-15"
    }
  },
  "format": "pdf",
  "include_maps": true
}

Response:
{
  "report_id": "report_789",
  "status": "generating",
  "download_url": "/reports/download/report_789.pdf",
  "expires_at": "2025-09-22T00:00:00Z"
}
```

## WebSocket Events
```javascript
// Real-time updates
const ws = new WebSocket('wss://api.fra-atlas.gov.in/ws');

// Subscribe to updates
ws.send(JSON.stringify({
  type: 'subscribe',
  channels: ['alerts', 'claim_updates'],
  filters: { state: 'odisha' }
}));

// Receive real-time notifications
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type === 'new_alert') {
    updateDashboard(data.alert);
  }
};
```

## Rate Limiting
- **Free Tier**: 100 requests/hour
- **Government**: 10,000 requests/hour
- **Satellite Processing**: 50 analysis jobs/day

## Error Responses
```json
{
  "error": {
    "code": "INVALID_CLAIM_ID",
    "message": "Claim ID not found in database",
    "details": {
      "claim_id": "CFR-2024-INVALID",
      "suggestion": "Check claim ID format: CFR-YYYY-ST-NNN"
    }
  }
}
```

## SDK Examples

### Python
```python
import fra_atlas_sdk

client = fra_atlas_sdk.Client(api_key='your_key')
claims = client.claims.list(state='odisha', status='pending')
ndvi_data = client.monitoring.get_ndvi('CFR-2024-OD-101')
```

### JavaScript
```javascript
import FRAAtlas from 'fra-atlas-js';

const client = new FRAAtlas({ apiKey: 'your_key' });
const claims = await client.claims.list({ state: 'odisha' });
const alerts = await client.alerts.list({ severity: 'high' });
```

---
**Future Implementation | Team Green Guardians | SIH 2025**
