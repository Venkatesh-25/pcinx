/**
 * Report Modal Component - Handles issue reporting functionality
 */

class ReportModal {
    constructor() {
        this.modal = document.getElementById('reportModal');
        this.form = document.getElementById('reportForm');
        this.closeBtn = document.getElementById('closeModal');
        
        this.initializeEventListeners();
    }

    /**
     * Initialize event listeners for modal
     */
    initializeEventListeners() {
        // Close button
        if (this.closeBtn) {
            this.closeBtn.addEventListener('click', () => this.hide());
        }

        // Click outside modal to close
        if (this.modal) {
            this.modal.addEventListener('click', (event) => {
                if (event.target === this.modal) {
                    this.hide();
                }
            });
        }

        // Form submission
        if (this.form) {
            this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        }

        // Escape key to close
        document.addEventListener('keydown', (event) => {
            if (event.key === 'Escape' && this.isVisible()) {
                this.hide();
            }
        });
    }

    /**
     * Show the modal
     */
    show() {
        if (this.modal) {
            this.modal.style.display = 'block';
            document.body.style.overflow = 'hidden'; // Prevent background scrolling
            
            // Focus on first input
            const firstInput = this.modal.querySelector('input, select, textarea');
            if (firstInput) {
                setTimeout(() => firstInput.focus(), 100);
            }
        }
    }

    /**
     * Hide the modal
     */
    hide() {
        if (this.modal) {
            this.modal.style.display = 'none';
            document.body.style.overflow = ''; // Restore scrolling
            this.resetForm();
        }
    }

    /**
     * Check if modal is visible
     */
    isVisible() {
        return this.modal && this.modal.style.display === 'block';
    }

    /**
     * Handle form submission
     */
    handleSubmit(event) {
        event.preventDefault();
        
        if (!this.validateForm()) {
            return;
        }

        const formData = this.collectFormData();
        this.submitReport(formData);
    }

    /**
     * Validate form data
     */
    validateForm() {
        const requiredFields = this.form.querySelectorAll('[required]');
        let isValid = true;
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                this.markFieldAsError(field);
                isValid = false;
            } else {
                this.clearFieldError(field);
            }
        });

        if (!isValid) {
            this.showError('Please fill in all required fields.');
        }

        return isValid;
    }

    /**
     * Mark field as having an error
     */
    markFieldAsError(field) {
        field.style.borderColor = '#dc3545';
        field.style.boxShadow = '0 0 0 0.2rem rgba(220, 53, 69, 0.25)';
    }

    /**
     * Clear field error styling
     */
    clearFieldError(field) {
        field.style.borderColor = '#e1e1e1';
        field.style.boxShadow = 'none';
    }

    /**
     * Collect form data
     */
    collectFormData() {
        const formData = new FormData(this.form);
        const data = {};
        
        // Convert FormData to regular object
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }

        // Add additional fields
        data.submissionTime = new Date().toISOString();
        data.reportId = 'ENV-' + Date.now().toString().slice(-6);
        
        return data;
    }

    /**
     * Submit the report
     */
    submitReport(data) {
        this.showLoading();
        
        // Simulate API submission
        setTimeout(() => {
            this.hideLoading();
            this.hide();
            this.showSuccessMessage(data.reportId);
            
            // Log for demo purposes
            console.log('📝 Report submitted:', data);
        }, 2500);
    }

    /**
     * Show loading state
     */
    showLoading() {
        const submitBtn = this.form.querySelector('.submit-btn');
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting...';
        }
    }

    /**
     * Hide loading state
     */
    hideLoading() {
        const submitBtn = this.form.querySelector('.submit-btn');
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Submit Report';
        }
    }

    /**
     * Show success message
     */
    showSuccessMessage(reportId) {
        alert(`✅ Report Submitted Successfully!\n\nYour environmental issue report has been submitted to the Forest Department.\n\nReport ID: ${reportId}\n\nExpected Response Time: 24-48 hours\n\nThank you for helping protect our forests!`);
    }

    /**
     * Show error message
     */
    showError(message) {
        // Create or update error message div
        let errorDiv = this.modal.querySelector('.error-message');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            errorDiv.style.cssText = `
                background: #ffebee;
                color: #d32f2f;
                padding: 10px;
                border-radius: 4px;
                margin-bottom: 15px;
                border-left: 4px solid #d32f2f;
            `;
            this.form.insertBefore(errorDiv, this.form.firstChild);
        }
        
        errorDiv.textContent = message;
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 5000);
    }

    /**
     * Reset form to initial state
     */
    resetForm() {
        if (this.form) {
            this.form.reset();
            
            // Clear any error styling
            const inputs = this.form.querySelectorAll('input, select, textarea');
            inputs.forEach(input => this.clearFieldError(input));
            
            // Remove error messages
            const errorDiv = this.modal.querySelector('.error-message');
            if (errorDiv && errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }
    }

    /**
     * Pre-fill form with data (useful for testing or demo)
     */
    prefillDemo() {
        const demoData = {
            issueType: 'deforestation',
            reporterName: 'Demo User',
            reporterPhone: '+91-9876543210',
            location: 'Khandagiri Village',
            district: 'Khurda',
            description: 'Noticed illegal tree cutting in the protected forest area near our village. Approximately 50 trees have been cut down in the last week.',
            coordinates: '20.2961, 85.8245'
        };

        Object.keys(demoData).forEach(key => {
            const field = this.form.querySelector(`[name="${key}"], #${key}`);
            if (field) {
                field.value = demoData[key];
            }
        });
    }
}