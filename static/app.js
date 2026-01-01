const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const browseBtn = document.getElementById('browseBtn');
const fileList = document.getElementById('fileList');
const uploadBtn = document.getElementById('uploadBtn');

// Ranking Elements
const toggleRankBtn = document.getElementById('toggleRankBtn');
const rankingSection = document.getElementById('rankingSection');
const closeRankBtn = document.getElementById('closeRankBtn');
const jdInput = document.getElementById('jdInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const rankResults = document.getElementById('rankResults');
const resultsList = document.getElementById('resultsList');

// Table Elements
const resumeTableBody = document.getElementById('resumeTableBody');

let selectedFiles = [];

// --- Init ---
fetchResumes();

// --- Event Listeners ---

// 1. Ranking Toggle
toggleRankBtn.addEventListener('click', () => {
    rankingSection.classList.remove('hidden');
    jdInput.focus();
});

closeRankBtn.addEventListener('click', () => {
    rankingSection.classList.add('hidden');
});

// 2. Drag & Drop
dropZone.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.classList.add('dragover'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    handleFiles(e.dataTransfer.files);
});

browseBtn.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', (e) => handleFiles(e.target.files));

function handleFiles(files) {
    const newFiles = Array.from(files).filter(file => file.type === 'application/pdf');
    selectedFiles = [...selectedFiles, ...newFiles];
    updateFileList();
    uploadBtn.disabled = selectedFiles.length === 0;
}

function updateFileList() {
    fileList.innerHTML = selectedFiles.map(file => `
        <div class="file-item">
            <span>${file.name}</span>
            <span>${(file.size / 1024 / 1024).toFixed(2)} MB</span>
        </div>
    `).join('');
}

// 3. Upload Action
uploadBtn.addEventListener('click', async () => {
    uploadBtn.disabled = true;
    uploadBtn.textContent = 'Uploading...';

    try {
        const formData = new FormData();
        selectedFiles.forEach(file => formData.append('files', file));

        const res = await fetch('/api/v1/resumes/upload', { method: 'POST', body: formData });
        if (!res.ok) throw new Error('Upload failed');

        // Success
        selectedFiles = []; // Clear queue
        updateFileList();
        fetchResumes(); // Refresh Table
        alert("Upload successful! Resumes added to repository.");

    } catch (err) {
        alert(err.message);
    } finally {
        uploadBtn.disabled = selectedFiles.length === 0;
        uploadBtn.textContent = 'Upload Files';
    }
});

// 4. Analyze Action
jdInput.addEventListener('input', () => {
    analyzeBtn.disabled = jdInput.value.trim().length === 0;
});

analyzeBtn.addEventListener('click', async () => {
    analyzeBtn.disabled = true;
    analyzeBtn.textContent = 'Analyzing...';

    try {
        const res = await fetch('/api/v1/resumes/rank', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ jd: jdInput.value })
        });

        if (!res.ok) throw new Error('Analysis failed');

        const data = await res.json();
        displayRankingResults(data.results);

    } catch (err) {
        alert(err.message);
    } finally {
        analyzeBtn.disabled = false;
        analyzeBtn.textContent = 'Analyze & Rank';
    }
});

function displayRankingResults(results) {
    rankResults.classList.remove('hidden');
    resultsList.innerHTML = results.map(r => {
        let matchClass = r.score >= 80 ? 'high-match' : '';
        return `
            <div class="result-card">
                <div class="result-info">
                    <h3>${r.metadata.filename}</h3>
                    <p style="color: #94a3b8; font-size: 0.9rem">Match Score</p>
                </div>
                <div class="score-badge ${matchClass}">
                    ${r.score}%
                </div>
            </div>
        `;
    }).join('');
}


// --- Functions ---
async function fetchResumes() {
    try {
        const res = await fetch('/api/v1/resumes/');
        if (!res.ok) return;
        const resumes = await res.json();
        renderTable(resumes);
    } catch (e) {
        console.error("Failed to fetch resumes", e);
    }
}

function renderTable(resumes) {
    resumeTableBody.innerHTML = resumes.map(r => {
        const safeParse = (str) => { try { return JSON.parse(str) || [] } catch { return [] } };
        const experience = safeParse(r.experience);
        const skills = safeParse(r.skills);

        return `
            <tr>
                <td>
                    <div style="font-weight: 500; color: #f1f5f9;">${r.filename}</div>
                    <div class="summary-preview">${r.summary || 'No summary parsed'}</div>
                </td>
                <td>
                    <div style="font-size: 0.85rem; color: #cbd5e1; margin-bottom: 0.5rem">
                        ${experience.length > 0 ? experience.slice(0, 1).join(', ') + '...' : 'No experience listed'}
                    </div>
                    <div class="tags">
                        ${skills.slice(0, 3).map(s => `<span class="tag">${s}</span>`).join('')}
                        ${skills.length > 3 ? `<span class="tag">+${skills.length - 3}</span>` : ''}
                    </div>
                </td>
                <td style="color: #94a3b8; font-size: 0.9rem;">
                    ${new Date(r.created_at).toLocaleDateString()}
                </td>
                <td>
                    <button class="icon-btn" title="View Details">👁️</button>
                    <button class="icon-btn" title="Delete">🗑️</button>
                </td>
            </tr>
        `;
    }).join('');
}
