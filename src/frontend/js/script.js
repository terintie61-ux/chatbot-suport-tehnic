/**
 * BUCĂTĂRIA ACADEMICĂ - SCRIPT PRINCIPAL
 * Integrare completă cu API-ul dezvoltat de Vasilache Dumitru
 * Model clasificare intenții cu acuratețe 95.56%
 * Autor: Implementare profesională cu experiență academică
 * Versiune: 2.0.0
 */

// ============================================
// CONFIGURARE API
// ============================================
const API_BASE_URL = 'http://localhost:5000';
const API_ENDPOINTS = {
    health: `${API_BASE_URL}/health`,
    chat: `${API_BASE_URL}/chat`,
    chatTest: `${API_BASE_URL}/chat/test`,
    stats: `${API_BASE_URL}/stats`
};

// ============================================
// BAZĂ DE DATE RETETE (36 DE REŢETE)
// ============================================
const RECIPES_DATABASE = [
    { id: 1, name: "Pizza Margherita", category: "internațional", difficulty: "mediu", time: "45 min", desc: "Roșii San Marzano, mozzarella di bufala, busuioc proaspăt, aluat cu fermentație lentă.", tags: "italian, clasic" },
    { id: 2, name: "Sarmale în foi de varză", category: "tradițional", difficulty: "avansat", time: "180 min", desc: "Carne tocată porc-vită, orez, cimbru, foi de varză murată, afumătură." },
    { id: 3, name: "Clătite franțuzești", category: "rapid", difficulty: "ușor", time: "20 min", desc: "Făină, ouă, lapte, esență de vanilie. Subțiri și elastice." },
    { id: 4, name: "Cozonac cu nucă și cacao", category: "tradițional", difficulty: "avansat", time: "210 min", desc: "Aluat pufos dospit dublu, umplutură de nucă măcinată, cacao, rom." },
    { id: 5, name: "Ciorbă de burtă", category: "tradițional", difficulty: "mediu", time: "240 min", desc: "Burtă de vită, zarzavat, smântână, ou, oțet, leuștean." },
    { id: 6, name: "Risotto cu ciuperci porcini", category: "internațional", difficulty: "mediu", time: "35 min", desc: "Orez arborio, șampioane, vin alb, parmezan, unt." },
    { id: 7, name: "Papanași cu smântână", category: "desert", difficulty: "mediu", time: "40 min", desc: "Brânză de vaci, griș, ouă, prăjiți, serviți cu dulceață de afine." },
    { id: 8, name: "Mămăligă cu brânză și ou", category: "tradițional", difficulty: "ușor", time: "25 min", desc: "Mălai, apă, sare, brânză telemea, unt." },
    { id: 9, name: "Paste Carbonara", category: "internațional", difficulty: "mediu", time: "20 min", desc: "Guanciale, pecorino, ouă, piper negru, fără smântână." },
    { id: 10, name: "Salată de vinete", category: "tradițional", difficulty: "ușor", time: "50 min", desc: "Vinete coapte, ceapă, ulei, lămâie." },
    { id: 11, name: "Cheesecake New York", category: "desert", difficulty: "mediu", time: "90 min", desc: "Blat digestive, cremă brânză, ouă, smântână, coajă lămâie." },
    { id: 12, name: "Tocăniță de vită", category: "internațional", difficulty: "mediu", time: "120 min", desc: "Carne de vită, ceapă, boia, piure roșii, cartofi." },
    { id: 13, name: "Plăcintă cu mere", category: "desert", difficulty: "ușor", time: "55 min", desc: "Foi foietaj, mere, scorțișoară, zahăr." },
    { id: 14, name: "Friptură de porc cu sos de vin", category: "internațional", difficulty: "mediu", time: "70 min", desc: "Ceafă de porc, vin roșu, cimbru, sos demi-glace." },
    { id: 15, name: "Mici (mititei) de casă", category: "tradițional", difficulty: "mediu", time: "90 min", desc: "Carne vită-oaie, usturoi, cimbru, bicarbonat." },
    { id: 16, name: "Supă cremă de dovleac", category: "rapid", difficulty: "ușor", time: "30 min", desc: "Dovleac, morcov, ghimbir, smântână, semințe." },
    { id: 17, name: "Crap la cuptor cu legume", category: "tradițional", difficulty: "mediu", time: "65 min", desc: "Crap, ceapă, ardei, roșii, vin alb." },
    { id: 18, name: "Gulaș unguresc", category: "internațional", difficulty: "mediu", time: "100 min", desc: "Vită, cartofi, boia dulce, chimen, ardei." },
    { id: 19, name: "Baklava cu nucă", category: "desert", difficulty: "avansat", time: "120 min", desc: "Foi de plăcintă, nucă, sirop de zahăr cu miere." },
    { id: 20, name: "Fasole bătută", category: "tradițional", difficulty: "ușor", time: "45 min", desc: "Fasole boabe, ceapă, ulei, căței usturoi." },
    { id: 21, name: "Piept de pui la grătar", category: "rapid", difficulty: "ușor", time: "25 min", desc: "Pui marinat cu lămâie, rozmarin, usturoi." },
    { id: 22, name: "Tiramisu autentic", category: "desert", difficulty: "mediu", time: "40 min", desc: "Mascarpone, cafea, pișcoturi, ouă, cacao." },
    { id: 23, name: "Piure de cartofi trufat", category: "rapid", difficulty: "ușor", time: "25 min", desc: "Cartofi, unt, ulei trufe, parmezan." },
    { id: 24, name: "Cordon bleu de pui", category: "internațional", difficulty: "mediu", time: "40 min", desc: "Piept de pui, șuncă, cașcaval, pesmet." },
    { id: 25, name: "Orez cu legume (pilaf)", category: "rapid", difficulty: "ușor", time: "35 min", desc: "Orez, ardei, morcov, mazăre, turmeric." },
    { id: 26, name: "Colivă tradițională", category: "desert", difficulty: "mediu", time: "80 min", desc: "Grâu fiert, nucă, zahăr, scorțișoară, pesmet." },
    { id: 27, name: "Ciorbă de perișoare", category: "tradițional", difficulty: "mediu", time: "75 min", desc: "Chiftele mici din carne, orez, supă de legume, leuștean." },
    { id: 28, name: "Hummus cremos", category: "rapid", difficulty: "ușor", time: "10 min", desc: "Năut, tahini, lămâie, usturoi, ulei măsline." },
    { id: 29, name: "Lasagna clasică", category: "internațional", difficulty: "mediu", time: "80 min", desc: "Sos bolognese, bechamel, foi lasagna, parmezan." },
    { id: 30, name: "Pâine de casă cu maia", category: "tradițional", difficulty: "avansat", time: "240 min", desc: "Făină, apă, maia, sare, coacere în vas de fontă." },
    { id: 31, name: "Gratin de cartofi dauphinois", category: "internațional", difficulty: "mediu", time: "60 min", desc: "Cartofi, smântână, usturoi, nucșoară, brânză." },
    { id: 32, name: "Budincă de orez", category: "desert", difficulty: "ușor", time: "45 min", desc: "Orez, lapte, scorțișoară, zahăr, stafide." },
    { id: 33, name: "Salată de boeuf", category: "tradițional", difficulty: "mediu", time: "90 min", desc: "Vită fiartă, legume, maioneză, muraături." },
    { id: 34, name: "Macaroons (franceze)", category: "desert", difficulty: "avansat", time: "90 min", desc: "Făină de migdale, albuș, zahăr, umplutură ganache." },
    { id: 35, name: "Tacos de vită", category: "rapid", difficulty: "ușor", time: "20 min", desc: "Carne tocată condimentată, tortilla, salsa, avocado." },
    { id: 36, name: "Brioche pufoasă", category: "desert", difficulty: "mediu", time: "150 min", desc: "Făină T45, ouă, unt, lapte, dospire lentă." }
];

// ============================================
// VARIABILE GLOBALE
// ============================================
let currentFilter = 'all';
let isApiOnline = false;
let isWaitingForResponse = false;
let currentTypingTimeout = null;

// ============================================
// FUNCȚII DE RANDARE RETETE
// ============================================
function renderRecipes() {
    const grid = document.getElementById('recipesGrid');
    if (!grid) return;
    
    const filtered = currentFilter === 'all' 
        ? RECIPES_DATABASE 
        : RECIPES_DATABASE.filter(r => r.category === currentFilter);
    
    if (filtered.length === 0) {
        grid.innerHTML = '<div style="grid-column:1/-1; text-align:center; padding:3rem;">Nu există rețete în această secțiune academică</div>';
        return;
    }
    
    grid.innerHTML = filtered.map(recipe => `
        <div class="recipe-card" data-recipe-id="${recipe.id}" data-recipe-name="${recipe.name.replace(/'/g, "\\'")}">
            <div class="card-img">
                <i class="fas fa-utensils" style="opacity:0.7"></i>
            </div>
            <div class="card-content">
                <div class="title">${escapeHtml(recipe.name)}</div>
                <div class="recipe-meta">
                    <span><i class="far fa-clock"></i> ${recipe.time}</span>
                    <span><i class="fas fa-chart-line"></i> ${recipe.difficulty}</span>
                </div>
                <div class="description">${escapeHtml(recipe.desc)}</div>
                <div class="badge">${recipe.category}</div>
            </div>
        </div>
    `).join('');
}

// ============================================
// FUNCȚII AJUTĂTOARE
// ============================================
function escapeHtml(str) {
    if (!str) return '';
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

function updateApiStatus(status, message) {
    const indicator = document.querySelector('.status-indicator');
    const statusText = document.getElementById('statusText');
    
    if (!indicator || !statusText) return;
    
    indicator.classList.remove('online', 'offline', 'checking');
    
    switch(status) {
        case 'online':
            indicator.classList.add('online');
            statusText.textContent = message || 'API conectat · model SVM activ';
            isApiOnline = true;
            break;
        case 'offline':
            indicator.classList.add('offline');
            statusText.textContent = message || 'API offline · mod de rezervă activ';
            isApiOnline = false;
            break;
        default:
            indicator.classList.add('checking');
            statusText.textContent = message || 'Verificare conexiune...';
            isApiOnline = false;
    }
}

// ============================================
// CONEXIUNE API - VERIFICARE STARE
// ============================================
async function checkApiHealth() {
    updateApiStatus('checking', 'Verificare conexiune API...');
    
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 5000);
        
        const response = await fetch(API_ENDPOINTS.health, {
            method: 'GET',
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (response.ok) {
            const data = await response.json();
            const modelStatus = data.model_incarcat ? 'model activ' : 'model indisponibil';
            updateApiStatus('online', `API conectat · ${modelStatus}`);
            console.log('[API] Stare sănătate:', data);
        } else {
            updateApiStatus('offline', `API indisponibil (status ${response.status})`);
        }
    } catch (error) {
        console.warn('[API] Eroare conexiune:', error.message);
        updateApiStatus('offline', 'API indisponibil · mod de rezervă activ');
    }
}

// ============================================
// COMUNICARE CU API-UL PENTRU CHAT
// ============================================
async function sendMessageToApi(message) {
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 15000);
        
        const response = await fetch(API_ENDPOINTS.chat, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ mesaj: message }),
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (response.ok) {
            const data = await response.json();
            return { success: true, data };
        } else {
            return { success: false, error: `HTTP ${response.status}` };
        }
    } catch (error) {
        console.warn('[API] Eroare request chat:', error.message);
        return { success: false, error: error.message };
    }
}

// ============================================
// GENERARE RĂSPUNS FALLBACK (MOD DE REZERVĂ)
// ============================================
function getFallbackResponse(question) {
    const q = question.toLowerCase();
    
    // Matrice semantică extinsă
    const patterns = [
        { keywords: ['pizza', 'cum se face'], response: "Pizza clasică necesită: 500g făină, 300ml apă, 7g drojdie, 10g sare. Frământați 10 minute, dospire 2 ore, coacere 12 minute la 250°C." },
        { keywords: ['clătite', 'ingrediente'], response: "Clătite: 2 ouă, 250ml lapte, 125g făină, 2 linguri ulei, 15g zahăr. Omogenizați, prăjiți în tigaie unsă." },
        { keywords: ['cozonac', 'timp', 'coace'], response: "Cozonacul se coace la 170°C timp de 45-50 minute. Verificați cu scobitoarea." },
        { keywords: ['sarmale', 'timp'], response: "Sarmalele se fierb la foc mic 2-2.5 ore, în funcție de mărime." },
        { keywords: ['înlocuitor', 'ouă'], response: "Înlocuitor pentru ou: 1 lingură semințe de in măcinate + 3 linguri apă, sau 50g piure de mere." },
        { keywords: ['papanasi'], response: "Papanasi: 500g brânză de vaci, 2 ouă, 100g făină, 50g griș. Se fierb 5-7 minute, apoi se prăjesc." },
        { keywords: ['mămăligă'], response: "Mămăligă: 1L apă, 10g sare, 300g mălai. Turnați mălaiul în ploaie, amestecați 15 minute." },
        { keywords: ['salut', 'bună'], response: "Bună ziua. Vă stau la dispoziție pentru orice întrebare culinară." },
        { keywords: ['mulțumesc', 'mersi'], response: "Cu plăcere! Vă invit să consultați arhiva de rețete." }
    ];
    
    for (const pattern of patterns) {
        if (pattern.keywords.every(kw => q.includes(kw))) {
            return pattern.response;
        }
    }
    
    return "Vă rugăm să reformulați întrebarea. Puteți întreba despre rețete din lista laterală, timpi de preparare, înlocuitori sau tehnici culinare fundamentale.";
}

// ============================================
// GESTIONARE MESAJE CHAT
// ============================================
function addMessage(sender, text, intent = null) {
    const container = document.getElementById('chatMessages');
    if (!container) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender === 'user' ? 'user' : 'bot'}`;
    
    const bubble = document.createElement('div');
    bubble.className = 'bubble';
    bubble.innerText = text;
    
    const meta = document.createElement('div');
    meta.className = 'meta';
    
    if (sender === 'user') {
        meta.innerText = 'dvs. · ' + new Date().toLocaleTimeString('ro-RO', { hour: '2-digit', minute: '2-digit' });
    } else {
        const modelInfo = intent ? ` · intenție: ${intent}` : '';
        meta.innerText = `asistent academic${modelInfo} · ${new Date().toLocaleTimeString('ro-RO', { hour: '2-digit', minute: '2-digit' })}`;
    }
    
    messageDiv.appendChild(bubble);
    messageDiv.appendChild(meta);
    container.appendChild(messageDiv);
    container.scrollTop = container.scrollHeight;
}

function showTypingIndicator() {
    const container = document.getElementById('chatMessages');
    if (!container) return;
    
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot';
    typingDiv.id = 'typingIndicator';
    
    const bubble = document.createElement('div');
    bubble.className = 'bubble';
    bubble.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';
    
    typingDiv.appendChild(bubble);
    container.appendChild(typingDiv);
    container.scrollTop = container.scrollHeight;
}

function hideTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) indicator.remove();
}

async function processUserMessage(message) {
    if (isWaitingForResponse) return;
    
    isWaitingForResponse = true;
    showTypingIndicator();
    
    try {
        let responseText, detectedIntent = null;
        
        if (isApiOnline) {
            const apiResponse = await sendMessageToApi(message);
            
            if (apiResponse.success && apiResponse.data) {
                responseText = apiResponse.data.raspuns || apiResponse.data.message;
                detectedIntent = apiResponse.data.intentie_detectata || null;
            } else {
                responseText = getFallbackResponse(message);
            }
        } else {
            responseText = getFallbackResponse(message);
        }
        
        hideTypingIndicator();
        addMessage('bot', responseText, detectedIntent);
        
    } catch (error) {
        console.error('[Chat] Eroare procesare:', error);
        hideTypingIndicator();
        addMessage('bot', 'Sistemul întâmpină dificultăți tehnice. Vă rugăm să reîncercați.');
    } finally {
        isWaitingForResponse = false;
    }
}

async function handleSendMessage() {
    const input = document.getElementById('userInput');
    const message = input.value.trim();
    
    if (!message || isWaitingForResponse) return;
    
    addMessage('user', message);
    input.value = '';
    
    await processUserMessage(message);
}

// ============================================
// INIȚIALIZARE ȘI EVENT LISTENERS
// ============================================
function initializeFilters() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            filterButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentFilter = btn.dataset.filter;
            renderRecipes();
        });
    });
}

function initializeSuggestions() {
    const suggestionsContainer = document.getElementById('suggestionsContainer');
    if (!suggestionsContainer) return;
    
    const suggestionsList = [
        "Cum se prepară pizza neapolitană?",
        "Ce ingrediente sunt necesare pentru clătite clasice?",
        "Timp coacere cozonac tradițional",
        "Înlocuitor pentru ouă în prăjituri",
        "Cât durează să fac sarmale?",
        "Cum se face tiramisu autentic?",
        "Tehnici pentru blat pufos de chec"
    ];
    
    suggestionsContainer.innerHTML = suggestionsList.map(suggestion => 
        `<span class="chip" data-question="${escapeHtml(suggestion)}">${escapeHtml(suggestion.substring(0, 40))}${suggestion.length > 40 ? '...' : ''}</span>`
    ).join('');
    
    document.querySelectorAll('.chip').forEach(chip => {
        chip.addEventListener('click', () => {
            const question = chip.getAttribute('data-question');
            const input = document.getElementById('userInput');
            if (input && question) {
                input.value = question;
                handleSendMessage();
            }
        });
    });
}

function initializeRecipeClicks() {
    document.addEventListener('click', (e) => {
        const card = e.target.closest('.recipe-card');
        if (card) {
            const recipeName = card.getAttribute('data-recipe-name');
            if (recipeName) {
                const input = document.getElementById('userInput');
                if (input) {
                    input.value = `Cum se prepară ${recipeName}?`;
                    handleSendMessage();
                }
            }
        }
    });
}

function initializeEventListeners() {
    const sendBtn = document.getElementById('sendBtn');
    const userInput = document.getElementById('userInput');
    
    if (sendBtn) sendBtn.addEventListener('click', handleSendMessage);
    if (userInput) {
        userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') handleSendMessage();
        });
    }
}

async function initialize() {
    renderRecipes();
    initializeFilters();
    initializeSuggestions();
    initializeRecipeClicks();
    initializeEventListeners();
    
    await checkApiHealth();
    
    // Verificare periodică a stării API (la fiecare 30 secunde)
    setInterval(checkApiHealth, 30000);
    
    console.log('[System] Bucătăria Academică - sistem inițializat cu succes');
    console.log('[System] API endpoint:', API_BASE_URL);
    console.log('[System] Model SVM acuratețe: 95.56%');
}

// Pornirea aplicației după încărcarea DOM-ului
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize);
} else {
    initialize();
}