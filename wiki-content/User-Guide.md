# User Guide

## 🎮 Complete User Manual for FRA Atlas MVP

Welcome to the comprehensive user guide for the **FRA Atlas Decision Support System**. This guide covers all features and functionality available in the application.

### 🎯 Getting Started

#### **Accessing the Application**
- **Online**: Visit [https://ultrabot05.github.io/fra-atlas-mvp/](https://ultrabot05.github.io/fra-atlas-mvp/)
- **Local**: Open `index.html` or `index-modular.html` in your web browser

#### **First Time User Flow**
1. **Loading**: Application loads with progress indicator
2. **Map Display**: Interactive map appears with default view of India
3. **Dashboard**: Right sidebar shows live statistics and controls
4. **Legend**: Bottom-left corner explains map symbols and colors

### 🗺️ Interactive Map Features

#### **Basic Navigation**
- **Pan**: Click and drag to move around the map
- **Zoom**: Use mouse wheel or +/- buttons to zoom in/out
- **Reset View**: Click "Reset View" button to return to default position

#### **Map Controls**
- **Zoom Controls**: Located in top-left corner of map
- **Full Screen**: Toggle full-screen mode for better visibility
- **Layer Controls**: Switch between different map layers

#### **FRA Claim Boundaries**
- **Visual Display**: Orange polygon outlines show FRA claim boundaries
- **Click Interaction**: Click any boundary to view detailed information
- **Popup Details**: Shows claim ID, village, district, status, area, and families

##### Example Popup Information:
```
🏛️ Claim Details
Claim ID: OD_2023_001
Village: Kendrapada Village
District: Kendrapada
State: Odisha
Status: Approved ✅
Area: 15.67 hectares
Families: 23
Applied: March 15, 2023
Approved: August 20, 2023
```

#### **State Coverage**
The application currently demonstrates data for 4 Indian states:

| State | Region | Focus Area | Sample Claims |
|-------|--------|------------|---------------|
| **🌊 Odisha** | Eastern Coast | Mangrove conservation, coastal communities | 15+ sample boundaries |
| **🏔️ Madhya Pradesh** | Central India | Dense forest areas, tribal communities | 12+ sample boundaries |
| **🌿 Tripura** | Northeast | Biodiversity hotspot, indigenous rights | 8+ sample boundaries |
| **🌾 Telangana** | South Central | Deccan plateau, rural development | 10+ sample boundaries |

### 🛰️ Satellite Monitoring System

#### **NDVI Analysis Controls**

##### **January 2025 (Baseline) Button**
- **Purpose**: Shows healthy vegetation baseline from January 2025
- **Visual**: Green overlay indicating high NDVI values (healthy forests)
- **Use Case**: Compare against current conditions to detect changes

##### **September 2025 (Current) Button**
- **Purpose**: Displays current vegetation health analysis
- **Visual**: Color-coded overlay showing vegetation changes
- **Alert System**: Red areas indicate potential deforestation (NDVI < 0.3)

##### **Reset View Button**
- **Purpose**: Removes all NDVI overlays and returns to base map
- **Use Case**: Clear view for boundary analysis or navigation

#### **NDVI Color Legend**
| Color | NDVI Range | Interpretation |
|-------|------------|----------------|
| 🟢 **Dark Green** | 0.6 - 1.0 | Healthy, dense vegetation |
| 🟡 **Light Green** | 0.3 - 0.6 | Moderate vegetation cover |
| 🔴 **Red** | 0.0 - 0.3 | **DEFORESTATION ALERT** |
| 🔵 **Blue** | N/A | Water bodies |

#### **Temporal Comparison Workflow**
1. **View Baseline**: Click "January 2025 (Baseline)" to see healthy forest state
2. **Compare Current**: Click "September 2025 (Current)" to see recent changes
3. **Identify Issues**: Look for red areas indicating forest loss
4. **Take Action**: Use information for decision-making or reporting

### 📊 Dashboard Analytics

#### **Real-Time Statistics Section**

##### **Claim Status Metrics**
- **Approved**: Green counter showing successfully processed claims
- **Pending**: Yellow counter for claims awaiting review
- **Under Review**: Orange counter for claims in evaluation process
- **Rejected**: Red counter for declined claims

##### **Live Updates Feature**
- **Auto-Refresh**: Statistics update automatically every 30 seconds
- **Status Indicator**: "Real-time monitoring active" message
- **Change Animation**: Smooth counting animations for number updates

#### **Community Impact Metrics**

##### **Families Protected**
- **Current Count**: 8,542 tribal families with secured rights
- **Significance**: Represents successful FRA implementation impact
- **Growth Tracking**: Numbers increase as new claims are approved

##### **Hectares Secured**
- **Current Area**: 24,156 hectares of protected forest land
- **Environmental Impact**: Quantifies conservation success
- **Visualization**: Links to map boundaries showing secured areas

#### **System Analytics Section**

##### **Coverage Information**
- **States Monitored**: 4 states (Odisha, MP, Tripura, Telangana)
- **Last Update**: Shows time since last data refresh
- **NDVI Threshold**: 0.3 threshold for deforestation alerts
- **Spatial Resolution**: 10m Sentinel-2 satellite imagery

#### **Alert System**

##### **Deforestation Alerts**
- **Visual Indicator**: Red warning triangle with alert count
- **Example**: "3 new alerts in Telangana region"
- **Action Required**: Immediate investigation and response needed
- **Priority System**: Color-coded by severity level

### 📱 Issue Reporting System

#### **Accessing the Report Modal**
- **Button Location**: "Report Issue" button in dashboard controls
- **Button Color**: Red gradient indicating urgent action capability
- **Icon**: Exclamation circle indicating alert/warning function

#### **Report Form Categories**

##### **Issue Type Selection** (Required)
- **Illegal Deforestation**: Unauthorized cutting of forest trees
- **Forest Encroachment**: Illegal occupation of forest land
- **Unauthorized Mining**: Illegal extraction activities in forest areas
- **Waste Dumping**: Illegal disposal of waste in forest regions
- **Other Environmental Violation**: Any other environmental concerns

#### **Personal Information Section**

##### **Reporter Details** (Required)
- **Your Name**: Full name of person filing the report
- **Phone Number**: Contact number for follow-up (optional)
- **Validation**: Name must be 2-50 characters, letters and spaces only

##### **Location Information** (Required)
- **Location/Village**: Specific village or area name
- **District**: Administrative district where issue occurred
- **GPS Coordinates**: Optional precise location (format: lat, lng)

#### **Issue Description** (Required)
- **Detailed Description**: Comprehensive explanation of the environmental issue
- **Minimum Length**: At least 10 characters required
- **Maximum Length**: Up to 1000 characters allowed
- **Guidance**: Include when noticed, estimated area affected, other relevant details

#### **Form Validation**
- **Real-time Validation**: Fields validated as you type
- **Required Field Indicators**: Red asterisks (*) show mandatory fields
- **Error Messages**: Clear feedback for invalid inputs
- **Submission Check**: All required fields must be completed

#### **Submission Process**
1. **Fill Form**: Complete all required fields with accurate information
2. **Validation**: System checks all inputs for correctness
3. **Submit**: Click "Submit Report" button to send
4. **Confirmation**: Success message confirms report submission
5. **Processing**: Report enters system for official review

### 🎛️ Control Panel Features

#### **Export Functionality**
- **Generate Report Button**: Green gradient button for data export
- **Report Types**: Statistical summaries, maps, analysis data
- **Format Options**: PDF reports, data exports, map images
- **Use Case**: Documentation for presentations or official reporting

#### **System Status Indicators**

##### **Header Status Bar**
- **Live Monitoring**: Shows real-time system operational status
- **Database Connection**: "4 States Connected" indicates data availability
- **System Status**: Green circle with "System Online" shows operational health

#### **Professional UI Elements**

##### **Loading States**
- **Initial Loading**: Animated spinner with "Loading FRA Atlas..." message
- **Processing Actions**: Secondary loading indicator for form submissions
- **Progressive Loading**: Smooth transitions between application states

##### **Responsive Design**
- **Desktop View**: Full sidebar with complete dashboard
- **Tablet View**: Collapsible sidebar for better map visibility
- **Mobile View**: Bottom sheet layout optimized for touch interaction

### 🎯 Advanced Usage Scenarios

#### **Scenario 1: Investigating Deforestation Alert**
1. **Notice Alert**: Dashboard shows "3 new alerts in Telangana region"
2. **Navigate to Region**: Pan and zoom to Telangana state on map
3. **Enable NDVI**: Click "September 2025 (Current)" button
4. **Identify Problem Areas**: Look for red zones indicating forest loss
5. **Get Details**: Click on affected FRA boundaries for claim information
6. **Document Issue**: Use "Report Issue" if additional violations found
7. **Generate Report**: Export findings for official documentation

#### **Scenario 2: Community Rights Verification**
1. **Locate Community**: Search for specific village or district
2. **View Boundaries**: Click FRA claim boundaries to see approval status
3. **Check Timeline**: Review application and approval dates in popup
4. **Verify Coverage**: Confirm protected area matches community needs
5. **Monitor Health**: Use NDVI analysis to ensure forest protection
6. **Report Changes**: Submit reports if new issues arise

#### **Scenario 3: Administrative Oversight**
1. **Review Statistics**: Monitor dashboard for overall system performance
2. **Track Progress**: Observe trends in approval/rejection rates
3. **Identify Bottlenecks**: Look for high pending counts requiring attention
4. **Geographic Analysis**: Use map to identify regional patterns
5. **Export Data**: Generate reports for stakeholder meetings
6. **Set Priorities**: Focus resources on high-alert regions

### 🔧 Troubleshooting & Tips

#### **Common Issues**

##### **Map Not Loading**
- **Solution**: Check internet connection for map tiles
- **Alternative**: Refresh page if loading stalls
- **Browser**: Try different browser if issues persist

##### **Slow Performance**
- **Solution**: Close other browser tabs to free memory
- **Optimization**: Use Chrome or Firefox for best performance
- **Hardware**: Enable hardware acceleration in browser settings

##### **Mobile Display Issues**
- **Solution**: Rotate device to landscape mode for better map viewing
- **Touch**: Use two-finger gestures for map zoom and pan
- **Sidebar**: Tap dashboard areas to expand/collapse sections

#### **Pro Tips for Effective Usage**

##### **Navigation Efficiency**
- **Bookmarks**: Bookmark specific map locations for quick access
- **Zoom Levels**: Use appropriate zoom for your analysis needs
- **Layer Management**: Toggle overlays on/off to focus on specific data

##### **Data Analysis**
- **Temporal Comparison**: Always compare baseline vs current NDVI
- **Cross-Reference**: Use popup data with NDVI analysis for complete picture
- **Documentation**: Take screenshots of important findings

##### **Reporting Best Practices**
- **Accuracy**: Provide precise location information
- **Detail**: Include comprehensive description of issues
- **Follow-up**: Note contact information for official response
- **Evidence**: Take photos if reporting from field (upload separately)

### 📞 Support & Assistance

#### **Getting Help**
- **Documentation**: Refer to other wiki sections for specific topics
- **Technical Issues**: Report bugs via GitHub Issues
- **Feature Requests**: Submit enhancement suggestions
- **Community**: Join discussions for user collaboration

#### **Training Resources**
- **Video Tutorials**: Planned for future releases
- **Training Workshops**: Available for institutional users
- **Documentation Updates**: Regular improvements based on user feedback

---

**Master the FRA Atlas MVP with this comprehensive guide and contribute to forest conservation and community empowerment! 🌿🎯**