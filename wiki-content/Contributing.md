# Contributing

## 🤝 Contributing to FRA Atlas MVP

Thank you for your interest in contributing to the **FRA Atlas MVP**! This project aims to revolutionize Forest Rights Act implementation and forest conservation through technology. Your contributions can make a real difference for tribal communities and environmental protection.

### 🌟 Ways to Contribute

#### **🐛 Bug Reports**
- Found a bug? Help us improve by reporting it
- Use clear, descriptive titles and detailed reproduction steps
- Include browser information, error messages, and screenshots

#### **💡 Feature Requests**
- Suggest new features that would benefit communities or administrators
- Consider sustainability, scalability, and real-world impact
- Provide use cases and implementation ideas

#### **📝 Documentation**
- Improve existing documentation or create new guides
- Help with translations for regional languages
- Create tutorials and best practices

#### **💻 Code Contributions**
- Fix bugs and implement new features
- Improve performance and accessibility
- Add tests and enhance code quality

#### **🎨 Design & UX**
- Improve user interface design
- Enhance accessibility for diverse user groups
- Create better mobile experiences

### 🚀 Getting Started

#### **1. Set Up Development Environment**

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR-USERNAME/fra-atlas-mvp.git
cd fra-atlas-mvp

# Add upstream remote
git remote add upstream https://github.com/UltraBot05/fra-atlas-mvp.git

# Create development branch
git checkout -b feature/your-feature-name
```

#### **2. Development Workflow**

```bash
# Keep your fork updated
git fetch upstream
git checkout master
git merge upstream/master

# Create feature branch
git checkout -b feature/amazing-feature

# Make your changes
# Test thoroughly

# Commit with descriptive message
git add .
git commit -m "feat: add amazing feature for community empowerment"

# Push to your fork
git push origin feature/amazing-feature

# Create Pull Request on GitHub
```

### 📋 Contribution Guidelines

#### **Code Standards**

##### **JavaScript Guidelines**
- Use **ES6+ modern syntax** (const/let, arrow functions, async/await)
- Follow **camelCase** naming convention
- Add **JSDoc comments** for functions and classes
- Keep functions **small and focused** (single responsibility)
- Use **meaningful variable names**

**Example:**
```javascript
/**
 * Updates dashboard statistics with animation
 * @param {Object} newStats - Statistics object with counts
 * @param {boolean} animate - Whether to animate the update
 */
async function updateDashboardStats(newStats, animate = true) {
    const statsContainer = document.getElementById('dashboard-stats');
    
    if (animate) {
        await animateCounterUpdate(statsContainer, newStats);
    } else {
        renderStatsDirectly(statsContainer, newStats);
    }
}
```

##### **CSS Guidelines**
- Use **CSS custom properties** (variables) for consistency
- Follow **BEM methodology** for class naming
- Ensure **mobile-first responsive design**
- Maintain **accessibility standards** (WCAG 2.1)
- Use **semantic HTML** elements

**Example:**
```css
/* Use CSS custom properties */
:root {
    --primary-color: #2d5016;
    --secondary-color: #4CAF50;
    --border-radius: 8px;
}

/* BEM naming convention */
.dashboard__stat-card {
    background: var(--primary-color);
    border-radius: var(--border-radius);
    padding: 1rem;
}

.dashboard__stat-card--highlighted {
    box-shadow: 0 4px 12px rgba(45, 80, 22, 0.2);
}
```

##### **HTML Guidelines**
- Use **semantic HTML5** elements
- Ensure **accessibility** with proper ARIA labels
- Maintain **progressive enhancement**
- Include **proper meta tags** for SEO

#### **Git Commit Guidelines**

Follow **Conventional Commits** specification:

```bash
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
```bash
feat(map): add satellite layer toggle functionality
fix(dashboard): resolve statistics update animation bug
docs(api): update endpoint documentation with examples
style(css): improve mobile responsive layout
refactor(components): extract reusable modal component
test(map): add unit tests for NDVI calculation
chore(deps): update Leaflet.js to latest version
```

### 🧪 Testing Guidelines

#### **Manual Testing Checklist**

##### **Cross-Browser Testing**
- [ ] Chrome (latest 2 versions)
- [ ] Firefox (latest 2 versions)
- [ ] Edge (latest 2 versions)
- [ ] Safari (latest 2 versions)

##### **Device Testing**
- [ ] Desktop (1920x1080, 1366x768)
- [ ] Tablet (768x1024, 1024x768)
- [ ] Mobile (375x667, 414x896)

##### **Functionality Testing**
- [ ] Map loads correctly with all layers
- [ ] FRA boundaries display and are clickable
- [ ] NDVI overlays work properly
- [ ] Dashboard statistics update correctly
- [ ] Issue reporting form validates and submits
- [ ] All buttons and controls are responsive

##### **Accessibility Testing**
- [ ] Keyboard navigation works
- [ ] Screen reader compatibility
- [ ] Color contrast meets WCAG standards
- [ ] Focus indicators are visible
- [ ] Alt text for images

#### **Automated Testing (Future)**
```javascript
// Example test structure for future implementation
describe('MapManager', () => {
    test('should load GeoJSON data correctly', async () => {
        const mapManager = new MapManager('test-map');
        await mapManager.loadStateData('odisha');
        expect(mapManager.fraLayers.size).toBeGreaterThan(0);
    });
    
    test('should generate NDVI overlay', () => {
        const ndviData = mapManager.generateNDVIOverlay('current');
        expect(ndviData).toBeDefined();
        expect(ndviData.type).toBe('FeatureCollection');
    });
});
```

### 🌍 Community Focus

#### **Cultural Sensitivity**
- **Respect tribal traditions** and forest-dependent communities
- **Use inclusive language** in all communications
- **Consider digital literacy levels** in design decisions
- **Support multilingual accessibility**

#### **Environmental Responsibility**
- **Optimize for low-bandwidth** connections in rural areas
- **Minimize resource usage** for mobile devices
- **Consider offline functionality** for remote locations
- **Promote sustainable technology practices**

### 📚 Documentation Standards

#### **Code Documentation**
```javascript
/**
 * Manages FRA claim boundary visualization and interaction
 * @class MapManager
 * @description Handles all map-related functionality including
 * layer management, user interactions, and data visualization
 */
class MapManager {
    /**
     * Initialize map with default settings
     * @param {string} containerId - DOM element ID for map container
     * @param {Object} options - Configuration options
     * @param {number} options.zoom - Initial zoom level (default: 6)
     * @param {Array} options.center - Initial center coordinates [lat, lng]
     */
    constructor(containerId, options = {}) {
        // Implementation
    }
}
```

#### **README Updates**
When adding new features, update relevant documentation:
- Feature descriptions in main README
- Installation instructions if dependencies change
- Usage examples for new functionality
- Configuration options

### 🏆 Recognition

#### **Contributor Recognition**
- Contributors will be listed in project README
- Significant contributions recognized in release notes
- Opportunity to present at conferences and communities
- Co-authorship on research papers and publications

#### **Impact Tracking**
Your contributions help:
- **Tribal communities** access their forest rights
- **Environmental conservation** through early detection
- **Government efficiency** in claim processing
- **Digital inclusion** for marginalized communities

### 📋 Issue Templates

#### **Bug Report Template**
```markdown
**Bug Description**
Clear description of the issue

**Steps to Reproduce**
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

**Expected Behavior**
What you expected to happen

**Screenshots**
Add screenshots if applicable

**Environment**
- Browser: [e.g. Chrome 91]
- Device: [e.g. iPhone X]
- OS: [e.g. iOS 14.6]
```

#### **Feature Request Template**
```markdown
**Feature Summary**
Brief description of the feature

**Problem Statement**
What problem does this solve?

**Proposed Solution**
Detailed description of the proposed feature

**Community Impact**
How does this benefit tribal communities or conservation?

**Implementation Ideas**
Technical suggestions for implementation
```

### 🔗 Resources

#### **Helpful Links**
- **Leaflet.js Documentation**: [https://leafletjs.com/reference.html](https://leafletjs.com/reference.html)
- **Forest Rights Act 2006**: [Official Documentation](https://tribal.nic.in/fra.aspx)
- **Satellite Data Sources**: [ESA Sentinel Hub](https://www.sentinel-hub.com/)
- **NDVI Calculation**: [Remote Sensing Guide](https://earthobservatory.nasa.gov/features/MeasuringVegetation)

#### **Communication Channels**
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Pull Request Reviews**: Code collaboration
- **Wiki Updates**: Documentation improvements

### 🎯 Contribution Ideas

#### **Beginner-Friendly Tasks**
- [ ] Improve error messages for better user experience
- [ ] Add tooltips to explain technical terms
- [ ] Enhance mobile responsive design
- [ ] Fix cross-browser compatibility issues
- [ ] Update documentation with examples

#### **Intermediate Tasks**
- [ ] Implement data caching for better performance
- [ ] Add keyboard navigation support
- [ ] Create automated form validation
- [ ] Build component test suite
- [ ] Add accessibility improvements

#### **Advanced Tasks**
- [ ] Integrate real satellite data APIs
- [ ] Implement offline functionality
- [ ] Build backend API endpoints
- [ ] Add machine learning predictions
- [ ] Create mobile app version

### 📞 Getting Help

#### **Need Assistance?**
- **Documentation**: Check existing wiki pages first
- **Search Issues**: Look for similar questions or problems
- **Ask Questions**: Create new issue with question label
- **Join Discussions**: Participate in GitHub Discussions

#### **Mentorship**
- New contributors welcome and encouraged
- Maintainers available to guide through first contributions
- Code review process designed to be educational
- Pair programming sessions available for complex features

---

**Together, we can build technology that empowers communities, protects forests, and creates a sustainable future. Every contribution matters! 🌿🤝**

*Thank you for being part of the FRA Atlas community!*