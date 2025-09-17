# API Documentation

## 🔌 FRA Atlas MVP API Reference

### 📋 Overview

The FRA Atlas MVP is currently a frontend-only application, but this documentation outlines the API structure that would support the full production system. This serves as a blueprint for backend development and integration planning.

### 🏗️ Planned API Architecture

#### **RESTful API Design**
- **Base URL**: `https://api.fra-atlas.gov.in/v1`
- **Authentication**: JWT-based authentication with role-based access
- **Response Format**: JSON with consistent error handling
- **Rate Limiting**: 1000 requests per hour per user
- **API Versioning**: URL-based versioning for backward compatibility

### 🗺️ Geospatial Data APIs

#### **FRA Claims Endpoint**

##### **GET /api/v1/claims**
Retrieve FRA claim boundaries and metadata

```http
GET /api/v1/claims?state=odisha&status=approved&limit=100&offset=0
Authorization: Bearer <jwt_token>
```

**Query Parameters:**
- `state` (string): Filter by state code (odisha, mp, tripura, telangana)
- `district` (string): Filter by district name
- `status` (string): approved, pending, review, rejected
- `limit` (integer): Number of results (max 1000)
- `offset` (integer): Pagination offset
- `bbox` (string): Bounding box filter (west,south,east,north)

**Response:**
```json
{
  "type": "FeatureCollection",
  "metadata": {
    "total_count": 1247,
    "returned_count": 100,
    "page": 1,
    "has_more": true
  },
  "features": [
    {
      "type": "Feature",
      "id": "OD_2023_001",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[85.0, 20.0], [85.1, 20.0], [85.1, 20.1], [85.0, 20.1], [85.0, 20.0]]]
      },
      "properties": {
        "claim_id": "OD_2023_001",
        "village": "Kendrapada Village",
        "district": "Kendrapada",
        "state": "Odisha",
        "status": "approved",
        "area_hectares": 15.67,
        "families_count": 23,
        "claim_date": "2023-03-15T00:00:00Z",
        "approval_date": "2023-08-20T10:30:00Z",
        "approving_officer": "Block Development Officer",
        "created_at": "2023-03-15T14:30:00Z",
        "updated_at": "2023-08-20T10:30:00Z"
      }
    }
  ]
}
```

##### **GET /api/v1/claims/{claim_id}**
Retrieve specific claim details

```http
GET /api/v1/claims/OD_2023_001
Authorization: Bearer <jwt_token>
```

**Response:**
```json
{
  "claim_id": "OD_2023_001",
  "status": "approved",
  "timeline": [
    {
      "stage": "submitted",
      "date": "2023-03-15T14:30:00Z",
      "officer": "Village Secretary"
    },
    {
      "stage": "under_review",
      "date": "2023-04-02T09:15:00Z",
      "officer": "Forest Rights Committee"
    },
    {
      "stage": "approved",
      "date": "2023-08-20T10:30:00Z",
      "officer": "Block Development Officer"
    }
  ],
  "documents": [
    {
      "type": "application_form",
      "url": "/documents/OD_2023_001_application.pdf",
      "uploaded_at": "2023-03-15T14:30:00Z"
    }
  ],
  "community_details": {
    "tribe_name": "Khond",
    "village_head": "Ramesh Majhi",
    "total_families": 23,
    "primary_livelihood": "Forest produce collection"
  }
}
```

##### **POST /api/v1/claims**
Submit new FRA claim

```http
POST /api/v1/claims
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "village": "New Village Name",
  "district": "Kendrapada",
  "state": "Odisha",
  "area_hectares": 20.5,
  "families_count": 30,
  "tribe_name": "Khond",
  "geometry": {
    "type": "Polygon",
    "coordinates": [[[85.0, 20.0], [85.1, 20.0], [85.1, 20.1], [85.0, 20.1], [85.0, 20.0]]]
  },
  "supporting_documents": ["doc1_id", "doc2_id"]
}
```

### 🛰️ Satellite Monitoring APIs

#### **NDVI Analysis Endpoint**

##### **GET /api/v1/satellite/ndvi**
Retrieve NDVI analysis for specified area and time

```http
GET /api/v1/satellite/ndvi?bbox=85.0,20.0,85.5,20.5&date=2025-09-15&resolution=10m
Authorization: Bearer <jwt_token>
```

**Query Parameters:**
- `bbox` (string): Bounding box (west,south,east,north)
- `date` (string): Analysis date (YYYY-MM-DD)
- `resolution` (string): 10m, 20m, 60m
- `cloud_threshold` (integer): Maximum cloud cover percentage (default: 20)

**Response:**
```json
{
  "analysis_id": "ndvi_20250915_001",
  "bbox": [85.0, 20.0, 85.5, 20.5],
  "date": "2025-09-15",
  "resolution": "10m",
  "cloud_cover": 15.2,
  "statistics": {
    "mean_ndvi": 0.45,
    "std_ndvi": 0.23,
    "min_ndvi": -0.1,
    "max_ndvi": 0.89,
    "forest_area_km2": 145.7,
    "deforested_area_km2": 3.2
  },
  "tiles": {
    "base_url": "https://tiles.fra-atlas.gov.in/ndvi/{z}/{x}/{y}.png",
    "style": "ndvi_color_ramp"
  },
  "alerts": [
    {
      "alert_id": "DEFOR_001",
      "location": [85.234, 20.456],
      "severity": "high",
      "ndvi_change": -0.4,
      "area_affected_hectares": 2.3
    }
  ]
}
```

##### **GET /api/v1/satellite/change-detection**
Temporal change analysis between two dates

```http
GET /api/v1/satellite/change-detection?bbox=85.0,20.0,85.5,20.5&start_date=2025-01-15&end_date=2025-09-15
Authorization: Bearer <jwt_token>
```

### 📊 Analytics APIs

#### **Dashboard Statistics**

##### **GET /api/v1/analytics/dashboard**
Retrieve dashboard statistics

```http
GET /api/v1/analytics/dashboard?state=all&timeframe=30d
Authorization: Bearer <jwt_token>
```

**Response:**
```json
{
  "claim_statistics": {
    "total_claims": 1458,
    "approved": 1247,
    "pending": 156,
    "under_review": 43,
    "rejected": 12,
    "approval_rate": 85.5
  },
  "community_impact": {
    "families_protected": 8542,
    "hectares_secured": 24156,
    "average_claim_size": 16.57
  },
  "performance_metrics": {
    "average_processing_time_days": 127,
    "sla_compliance_rate": 78.2,
    "pending_over_sla": 23
  },
  "alerts": {
    "total_active": 7,
    "deforestation": 3,
    "encroachment": 2,
    "mining": 1,
    "dumping": 1
  },
  "last_updated": "2025-09-15T10:30:00Z"
}
```

##### **GET /api/v1/analytics/trends**
Historical trends and time-series data

```http
GET /api/v1/analytics/trends?metric=approvals&timeframe=12m&granularity=month
Authorization: Bearer <jwt_token>
```

### 📱 Community Reporting APIs

#### **Issue Reporting**

##### **POST /api/v1/reports**
Submit environmental issue report

```http
POST /api/v1/reports
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "issue_type": "deforestation",
  "reporter_name": "Local Community Member",
  "reporter_phone": "+919876543210",
  "location": "Village Name",
  "district": "District Name",
  "state": "State Name",
  "coordinates": [85.234, 20.456],
  "description": "Observed illegal tree cutting in forest area near village",
  "severity": "high",
  "estimated_area_hectares": 2.5,
  "photos": ["photo1_id", "photo2_id"],
  "reported_date": "2025-09-15T14:30:00Z"
}
```

**Response:**
```json
{
  "report_id": "RPT_2025_001",
  "status": "submitted",
  "tracking_number": "FRA-RPT-2025-001",
  "estimated_response_time": "48 hours",
  "assigned_officer": {
    "name": "Forest Officer Name",
    "designation": "Range Forest Officer",
    "contact": "+919876543211"
  },
  "created_at": "2025-09-15T14:30:00Z"
}
```

##### **GET /api/v1/reports/{report_id}**
Track report status

```http
GET /api/v1/reports/RPT_2025_001
Authorization: Bearer <jwt_token>
```

### 🔐 Authentication APIs

#### **User Authentication**

##### **POST /api/v1/auth/login**
User login

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "user@example.com",
  "password": "secure_password",
  "role": "community_member"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "refresh_token_here",
  "expires_in": 3600,
  "user": {
    "id": "user_123",
    "name": "User Name",
    "role": "community_member",
    "state": "Odisha",
    "district": "Kendrapada"
  }
}
```

##### **POST /api/v1/auth/refresh**
Refresh access token

```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "refresh_token_here"
}
```

### 🔧 Utility APIs

#### **File Upload**

##### **POST /api/v1/files/upload**
Upload documents or images

```http
POST /api/v1/files/upload
Authorization: Bearer <jwt_token>
Content-Type: multipart/form-data

file: [binary data]
type: document|photo
category: claim_document|report_evidence
```

#### **Geocoding**

##### **GET /api/v1/geocode**
Convert address to coordinates

```http
GET /api/v1/geocode?address=Kendrapada Village, Kendrapada, Odisha
Authorization: Bearer <jwt_token>
```

### 📝 Error Handling

#### **Standard Error Response**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input parameters",
    "details": [
      {
        "field": "state",
        "message": "State code must be one of: odisha, mp, tripura, telangana"
      }
    ],
    "request_id": "req_123456789"
  }
}
```

#### **HTTP Status Codes**
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `429` - Rate Limit Exceeded
- `500` - Internal Server Error

### 🔒 Security Considerations

#### **Authentication & Authorization**
- **JWT Tokens**: Stateless authentication with role-based access
- **API Keys**: For external integrations and monitoring systems
- **Rate Limiting**: Prevent abuse with configurable limits
- **Input Validation**: Comprehensive validation for all endpoints

#### **Data Protection**
- **HTTPS Only**: All API communication encrypted
- **Data Sanitization**: SQL injection and XSS prevention
- **Personal Data**: GDPR-compliant handling of user information
- **Audit Logging**: Complete API access logging for compliance

### 📊 Integration Examples

#### **JavaScript Frontend Integration**

```javascript
class FRAAtlasAPI {
    constructor(baseURL, apiKey) {
        this.baseURL = baseURL;
        this.apiKey = apiKey;
    }
    
    async getClaims(filters = {}) {
        const params = new URLSearchParams(filters);
        const response = await fetch(`${this.baseURL}/claims?${params}`, {
            headers: {
                'Authorization': `Bearer ${this.apiKey}`,
                'Content-Type': 'application/json'
            }
        });
        return response.json();
    }
    
    async getNDVIAnalysis(bbox, date) {
        const response = await fetch(`${this.baseURL}/satellite/ndvi?bbox=${bbox}&date=${date}`, {
            headers: {
                'Authorization': `Bearer ${this.apiKey}`
            }
        });
        return response.json();
    }
    
    async submitReport(reportData) {
        const response = await fetch(`${this.baseURL}/reports`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.apiKey}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(reportData)
        });
        return response.json();
    }
}

// Usage
const api = new FRAAtlasAPI('https://api.fra-atlas.gov.in/v1', 'your_api_key');
const claims = await api.getClaims({ state: 'odisha', status: 'approved' });
```

---

**This API documentation provides the foundation for building a comprehensive backend system to support the FRA Atlas MVP in production environments.** 🔌📊