// DOM Elements
const searchForm = document.getElementById('search-form');
const searchQuery = document.getElementById('search-query');
const searchBtn = document.getElementById('search-btn');
const resultLimit = document.getElementById('result-limit');
const loading = document.getElementById('loading');
const resultsContainer = document.getElementById('results-container');
const results = document.getElementById('results');
const resultCount = document.getElementById('result-count');
const noResults = document.getElementById('no-results');
const errorContainer = document.getElementById('error-container');
const errorMessage = document.getElementById('error-message');
const statusBadge = document.getElementById('status-badge');
const sampleQueries = document.querySelectorAll('.sample-query');

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    checkStatus();
    setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
    searchForm.addEventListener('submit', handleSearch);
    
    sampleQueries.forEach(btn => {
        btn.addEventListener('click', function() {
            searchQuery.value = this.dataset.query;
            handleSearch(new Event('submit'));
        });
    });
}

// Check Qdrant database status
async function checkStatus() {
    try {
        const response = await fetch('/status');
        const data = await response.json();
        
        if (data.status === 'healthy') {
            statusBadge.className = 'badge bg-success';
            statusBadge.innerHTML = `<i class="fas fa-check-circle"></i> Connected (${data.document_count} documents)`;
        } else {
            statusBadge.className = 'badge bg-danger';
            statusBadge.innerHTML = `<i class="fas fa-times-circle"></i> Connection Error`;
        }
    } catch (error) {
        statusBadge.className = 'badge bg-danger';
        statusBadge.innerHTML = `<i class="fas fa-times-circle"></i> Offline`;
    }
}

// Handle search form submission
async function handleSearch(event) {
    event.preventDefault();
    
    const query = searchQuery.value.trim();
    const limit = parseInt(resultLimit.value);
    
    if (!query) {
        showError('Please enter a search query');
        return;
    }
    
    hideAllContainers();
    showLoading();
    
    try {
        const response = await fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                limit: limit
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Search failed');
        }
        
        hideLoading();
        displayResults(data);
        
    } catch (error) {
        hideLoading();
        showError(error.message);
    }
}

// Display search results
function displayResults(data) {
    if (data.results.length === 0) {
        noResults.classList.remove('d-none');
        return;
    }
    
    resultCount.textContent = `${data.total} results for "${data.query}"`;
    
    const resultsHTML = data.results.map((result, index) => {
        const score = (result.score * 100).toFixed(1);
        const text = result.data.text || result.data.text_content || 'No description available';
        
        return `
            <div class="result-item p-3">
                <div class="d-flex justify-content-between align-items-start mb-2">
                    <div class="d-flex align-items-center">
                        <span class="badge bg-light text-dark me-2">#${index + 1}</span>
                        <span class="score-badge">${score}% match</span>
                    </div>
                    <small class="text-muted">
                        <i class="fas fa-building"></i> Property
                    </small>
                </div>
                <div class="property-text">
                    ${highlightSearchTerms(text, data.query)}
                </div>
                ${result.data.id ? `<small class="text-muted mt-2 d-block">ID: ${result.data.id}</small>` : ''}
            </div>
        `;
    }).join('');
    
    results.innerHTML = resultsHTML;
    resultsContainer.classList.remove('d-none');
}

// Highlight search terms in results
function highlightSearchTerms(text, query) {
    if (!query || !text) return text;
    
    const terms = query.toLowerCase().split(/\s+/).filter(term => term.length > 2);
    let highlightedText = text;
    
    terms.forEach(term => {
        const regex = new RegExp(`(${escapeRegex(term)})`, 'gi');
        highlightedText = highlightedText.replace(regex, '<span class="highlight">$1</span>');
    });
    
    return highlightedText;
}

// Escape special regex characters
function escapeRegex(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// Show loading state
function showLoading() {
    loading.classList.remove('d-none');
    searchBtn.disabled = true;
    searchBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Searching...';
}

// Hide loading state
function hideLoading() {
    loading.classList.add('d-none');
    searchBtn.disabled = false;
    searchBtn.innerHTML = '<i class="fas fa-search"></i> Search';
}

// Show error message
function showError(message) {
    errorMessage.textContent = message;
    errorContainer.classList.remove('d-none');
}

// Hide all result containers
function hideAllContainers() {
    resultsContainer.classList.add('d-none');
    noResults.classList.add('d-none');
    errorContainer.classList.add('d-none');
}

// Auto-focus search input
searchQuery.focus();