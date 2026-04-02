document.addEventListener('DOMContentLoaded', () => {
    
    // Elements for form 1 (Shorten)
    const shortenForm = document.getElementById('shorten-form');
    const originalUrlInput = document.getElementById('original-url');
    const shortenResult = document.getElementById('shorten-result');
    const shortUrlLink = document.getElementById('short-url-link');
    const copyBtn = document.getElementById('copy-btn');
    
    // Elements for form 2 (Analytics)
    const analyticsForm = document.getElementById('analytics-form');
    const shortIdInput = document.getElementById('short-id-input');
    const analyticsResult = document.getElementById('analytics-result');
    const statTotalClicks = document.getElementById('stat-total-clicks');
    const clickHistory = document.getElementById('click-history');

    shortenForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const urlToShorten = originalUrlInput.value.trim();
        if (!urlToShorten) return;

        try {
            const response = await fetch('/api/shorten', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: urlToShorten })
            });

            if (response.ok) {
                const data = await response.json();
                shortUrlLink.href = data.short_url;
                shortUrlLink.textContent = data.short_url;
                shortenResult.classList.remove('hidden');
                originalUrlInput.value = '';
            } else {
                alert('Failed to shorten URL. Make sure it is a valid HTTP URL.');
            }
        } catch (error) {
            console.error(error);
            alert('A network error occurred.');
        }
    });

    copyBtn.addEventListener('click', () => {
        navigator.clipboard.writeText(shortUrlLink.textContent).then(() => {
            const originalText = copyBtn.textContent;
            copyBtn.textContent = 'Copied!';
            setTimeout(() => { copyBtn.textContent = originalText; }, 2000);
        });
    });

    analyticsForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const shortId = shortIdInput.value.trim();
        if (!shortId) return;

        try {
            const response = await fetch(`/api/analytics/${shortId}`);

            if (response.ok) {
                const data = await response.json();
                statTotalClicks.textContent = data.total_clicks;
                
                clickHistory.innerHTML = '';
                if (data.clicks.length === 0) {
                    clickHistory.innerHTML = '<div class="history-item"><span>No clicks yet.</span></div>';
                } else {
                    data.clicks.forEach(click => {
                        const date = new Date(click.clicked_at).toLocaleString();
                        const ip = click.ip_address || "Unknown IP";
                        clickHistory.insertAdjacentHTML('beforeend', `
                            <div class="history-item">
                                <div>Click at <strong>${date}</strong></div>
                                <span>${ip}</span>
                            </div>
                        `);
                    });
                }
                
                analyticsResult.classList.remove('hidden');
            } else {
                alert('Analytics not found for that ID.');
            }
        } catch (error) {
            console.error(error);
            alert('A network error occurred fetching analytics.');
        }
    });
});
