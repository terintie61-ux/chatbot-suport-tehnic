// ============================================
// BAZĂ DE DATE EXTINSĂ CU 42 DE REȚETE
// ============================================
const RECIPES_DATABASE = [
    // Angel Food Cakes
    { id: 1, name: "Angel Food Cake", category: "desert", difficulty: "medium", prep_time: 10, cook_time: 39, total_time: "49 min", cuisine: "european, french", tastes: "sweet", dietary: ["nut_free", "halal", "kosher"], is_vegan: false, is_vegetarian: true, is_gluten_free: false, is_dairy_free: false, health_score: 58, health_level: "moderate", description: "Prăjitură pufoasă din albușuri, ușoară și aerată, specifică bucătăriei americane." },
    { id: 2, name: "Mock Angel Food Cake", category: "desert", difficulty: "medium", prep_time: 15, cook_time: 24, total_time: "39 min", cuisine: "european, french", tastes: "sweet", dietary: ["halal", "kosher"], is_vegan: false, is_vegetarian: true, is_gluten_free: false, is_dairy_free: false, health_score: 50, health_level: "moderate", description: "Varianta rapidă a clasicului angel food cake, perfectă pentru orice ocazie." },
    { id: 3, name: "Heavenly Raspberry Dessert", category: "desert", difficulty: "medium", prep_time: 15, cook_time: 42, total_time: "57 min", cuisine: "european, french", tastes: "sweet, sour", dietary: ["gluten_free", "nut_free", "halal", "kosher"], is_vegan: false, is_vegetarian: false, is_gluten_free: true, is_dairy_free: false, health_score: 50, health_level: "moderate", description: "Prăjitură răcoritoare cu zmeură și gelatină, perfectă pentru vară." },
    // Antipasti
    { id: 4, name: "Stuffed Cherry Peppers", category: "internațional", difficulty: "medium", prep_time: 11, cook_time: 28, total_time: "39 min", cuisine: "mediterranean", tastes: "sweet, savory", dietary: ["gluten_free", "nut_free"], is_vegan: false, is_vegetarian: true, is_gluten_free: true, is_dairy_free: false, health_score: 72, health_level: "moderate", description: "Ardei cherry umpluți cu prosciutto și brânză provolone, marinați în ulei de măsline." },
    { id: 5, name: "Mediterranean Flatbread", category: "rapid", difficulty: "medium", prep_time: 17, cook_time: 32, total_time: "49 min", cuisine: "mediterranean", tastes: "sweet, savory", dietary: ["gluten_free", "nut_free", "halal", "kosher"], is_vegan: false, is_vegetarian: true, is_gluten_free: true, is_dairy_free: false, health_score: 84, health_level: "healthy", description: "Lipie mediteraneană cu roșii, măsline Kalamata, ceapă roșie și brânză feta." },
    { id: 6, name: "Best Caprese Skewers", category: "rapid", difficulty: "easy", prep_time: 10, cook_time: 14, total_time: "24 min", cuisine: "italian, mediterranean", tastes: "sweet, savory", dietary: ["gluten_free", "nut_free", "halal", "kosher"], is_vegan: false, is_vegetarian: true, is_gluten_free: true, is_dairy_free: false, health_score: 76, health_level: "moderate", description: "Frigărui cu mozzarella, roșii cherry și busuioc - aperitiv rapid și elegant." },
    // Bagels
    { id: 7, name: "Real Homemade Bagels", category: "tradițional", difficulty: "hard", prep_time: 22, cook_time: 111, total_time: "133 min", cuisine: "american", tastes: "sweet, savory", dietary: ["halal", "kosher"], is_vegan: false, is_vegetarian: true, is_gluten_free: false, is_dairy_free: true, health_score: 54, health_level: "moderate", description: "Bagel autentic fiert înainte de coacere, textură perfectă și gust autentic." },
    { id: 8, name: "Everything Bagel Grilled Cheese", category: "rapid", difficulty: "medium", prep_time: 14, cook_time: 49, total_time: "63 min", cuisine: "american", tastes: "savory", dietary: ["gluten_free", "nut_free", "halal", "kosher"], is_vegan: false, is_vegetarian: true, is_gluten_free: true, is_dairy_free: false, health_score: 70, health_level: "moderate", description: "Sandwich cu brânză topită pe bagel cu susan, mac și usturoi." },
    // Baked Beans
    { id: 9, name: "Baked Butter Beans", category: "tradițional", difficulty: "medium", prep_time: 19, cook_time: 51, total_time: "70 min", cuisine: "american", tastes: "savory", dietary: ["gluten_free", "nut_free", "halal", "kosher"], is_vegan: false, is_vegetarian: true, is_gluten_free: true, is_dairy_free: false, health_score: 70, health_level: "moderate", description: "Fasole cu cârnat afumat, ardei și ceapă, coaptă la cuptor." },
    { id: 10, name: "Million Dollar Baked Beans", category: "tradițional", difficulty: "hard", prep_time: 24, cook_time: 67, total_time: "91 min", cuisine: "american", tastes: "sweet, savory", dietary: ["gluten_free", "nut_free"], is_vegan: false, is_vegetarian: false, is_gluten_free: true, is_dairy_free: true, health_score: 52, health_level: "moderate", description: "Fasole coptă premium cu bacon, cârnat și caramelizată cu zahăr brun." },
    // Beef Stews
    { id: 11, name: "Savory Apple Cider Beef Stew", category: "internațional", difficulty: "hard", prep_time: 24, cook_time: 48, total_time: "72 min", cuisine: "french", tastes: "sweet, savory", dietary: ["nut_free", "halal", "kosher"], is_vegan: false, is_vegetarian: false, is_gluten_free: false, is_dairy_free: true, health_score: 80, health_level: "healthy", description: "Tocanță de vită cu cidru de mere, mere proaspete și legume." },
    { id: 12, name: "Green Chile Stew", category: "internațional", difficulty: "medium", prep_time: 21, cook_time: 68, total_time: "89 min", cuisine: "mexican", tastes: "spicy, savory", dietary: ["gluten_free", "nut_free"], is_vegan: false, is_vegetarian: false, is_gluten_free: true, is_dairy_free: true, health_score: 80, health_level: "healthy", description: "Tocanță mexicană cu ardei iute verzi și cartofi." },
    // Beef Stroganoff
    { id: 13, name: "Simple Hamburger Stroganoff", category: "rapid", difficulty: "medium", prep_time: 23, cook_time: 58, total_time: "81 min", cuisine: "russian", tastes: "savory", dietary: ["gluten_free", "nut_free", "halal", "kosher"], is_vegan: false, is_vegetarian: false, is_gluten_free: true, is_dairy_free: false, health_score: 46, health_level: "unhealthy", description: "Versiune rapidă a stroganoff-ului cu carne tocată și smântână." },
    { id: 14, name: "Classic Beef Stroganoff", category: "internațional", difficulty: "hard", prep_time: 27, cook_time: 72, total_time: "99 min", cuisine: "russian", tastes: "sweet, savory", dietary: ["nut_free", "kosher"], is_vegan: false, is_vegetarian: false, is_gluten_free: false, is_dairy_free: false, health_score: 60, health_level: "moderate", description: "Stroganoff clasic cu carne de vită, ciuperci și smântână." },
    // Beef Tenderloin
    { id: 15, name: "Individual Beef Wellingtons", category: "avansat", difficulty: "hard", prep_time: 19, cook_time: 72, total_time: "91 min", cuisine: "french", tastes: "savory", dietary: ["gluten_free", "nut_free", "halal", "kosher"], is_vegan: false, is_vegetarian: false, is_gluten_free: true, is_dairy_free: false, health_score: 68, health_level: "moderate", description: "Mușchi de vită învelit în aluat foietaj, cu ciuperci și prosciutto." },
    { id: 16, name: "Grilled Beef Tenderloin", category: "avansat", difficulty: "hard", prep_time: 17, cook_time: 190, total_time: "207 min", cuisine: "american", tastes: "savory", dietary: ["gluten_free", "nut_free", "halal", "kosher"], is_vegan: false, is_vegetarian: false, is_gluten_free: true, is_dairy_free: true, health_score: 76, health_level: "moderate", description: "Mușchi de vită la grătar cu crustă de ierburi, usturoi și piper." },
    // Rețete tradiționale românești
    { id: 17, name: "Pizza Margherita", category: "internațional", difficulty: "medium", prep_time: 20, cook_time: 25, total_time: "45 min", cuisine: "italian", tastes: "savory", dietary: ["nut_free"], is_vegan: false, is_vegetarian: true, is_gluten_free: false, is_dairy_free: false, health_score: 70, health_level: "moderate", description: "Pizza clasică cu roșii San Marzano, mozzarella di bufala și busuioc proaspăt." },
    { id: 18, name: "Sarmale în foi de varză", category: "tradițional", difficulty: "hard", prep_time: 60, cook_time: 120, total_time: "180 min", cuisine: "românească", tastes: "savory", dietary: ["nut_free", "halal", "kosher"], is_vegan: false, is_vegetarian: false, is_gluten_free: true, is_dairy_free: true, health_score: 65, health_level: "moderate", description: "Sarmale tradiționale românești cu carne tocată, orez și cimbru." },
    { id: 19, name: "Clătite franțuzești", category: "rapid", difficulty: "easy", prep_time: 10, cook_time: 10, total_time: "20 min", cuisine: "french", tastes: "sweet", dietary: ["nut_free"], is_vegan: false, is_vegetarian: true, is_gluten_free: false, is_dairy_free: false, health_score: 55, health_level: "moderate", description: "Clătite subțiri și elastice, perfecte pentru umpluturi dulci sau sărate." },
    { id: 20, name: "Cozonac cu nucă și cacao", category: "tradițional", difficulty: "hard", prep_time: 120, cook_time: 50, total_time: "170 min", cuisine: "românească", tastes: "sweet", dietary: ["nut_free"], is_vegan: false, is_vegetarian: true, is_gluten_free: false, is_dairy_free: false, health_score: 52, health_level: "moderate", description: "Cozonac pufos cu umplutură de nucă și cacao, specific sărbătorilor." },
    { id: 21, name: "Ciorbă de burtă", category: "tradițional", difficulty: "medium", prep_time: 60, cook_time: 180, total_time: "240 min", cuisine: "românească", tastes: "savory, sour", dietary: ["nut_free"], is_vegan: false, is_vegetarian: false, is_gluten_free: true, is_dairy_free: false, health_score: 58, health_level: "moderate", description: "Ciorbă tradițională românească cu burtă de vită și smântână." },
    { id: 22, name: "Risotto cu ciuperci porcini", category: "internațional", difficulty: "medium", prep_time: 15, cook_time: 20, total_time: "35 min", cuisine: "italian", tastes: "savory, umami", dietary: ["gluten_free", "nut_free"], is_vegan: false, is_vegetarian: true, is_gluten_free: true, is_dairy_free: false, health_score: 75, health_level: "healthy", description: "Risotto cremos cu ciuperci porcini și parmezan." },
    { id: 23, name: "Papanași cu smântână", category: "desert", difficulty: "medium", prep_time: 20, cook_time: 20, total_time: "40 min", cuisine: "românească", tastes: "sweet", dietary: ["nut_free"], is_vegan: false, is_vegetarian: true, is_gluten_free: false, is_dairy_free: false, health_score: 48, health_level: "moderate", description: "Papanași prăjiți cu brânză de vaci, serviți cu smântână și dulceață." },
    { id: 24, name: "Mămăligă cu brânză și ou", category: "tradițional", difficulty: "easy", prep_time: 10, cook_time: 15, total_time: "25 min", cuisine: "românească", tastes: "savory", dietary: ["gluten_free", "nut_free"], is_vegan: false, is_vegetarian: true, is_gluten_free: true, is_dairy_free: false, health_score: 70, health_level: "moderate", description: "Mămăligă tradițională cu brânză telemea și ou ochi." },
    { id: 25, name: "Paste Carbonara", category: "internațional", difficulty: "medium", prep_time: 10, cook_time: 10, total_time: "20 min", cuisine: "italian", tastes: "savory, umami", dietary: ["nut_free"], is_vegan: false, is_vegetarian: false, is_gluten_free: false, is_dairy_free: false, health_score: 65, health_level: "moderate", description: "Paste carbonara autentice cu guanciale, pecorino și ouă (fără smântână)." },
    { id: 26, name: "Salată de vinete", category: "tradițional", difficulty: "easy", prep_time: 20, cook_time: 30, total_time: "50 min", cuisine: "românească", tastes: "savory", dietary: ["gluten_free", "vegan", "vegetarian"], is_vegan: true, is_vegetarian: true, is_gluten_free: true, is_dairy_free: true, health_score: 85, health_level: "healthy", description: "Salată de vinete coapte, cu ceapă și ulei." },
    { id: 27, name: "Cheesecake New York", category: "desert", difficulty: "medium", prep_time: 30, cook_time: 60, total_time: "90 min", cuisine: "american", tastes: "sweet, sour", dietary: ["nut_free"], is_vegan: false, is_vegetarian: true, is_gluten_free: false, is_dairy_free: false, health_score: 52, health_level: "moderate", description: "Cheesecake cremos cu blat de digestiv și aromă de lămâie." },
    { id: 28, name: "Hummus cremos", category: "rapid", difficulty: "easy", prep_time: 10, cook_time: 0, total_time: "10 min", cuisine: "libaneză", tastes: "savory", dietary: ["gluten_free", "vegan", "vegetarian", "nut_free", "halal", "kosher"], is_vegan: true, is_vegetarian: true, is_gluten_free: true, is_dairy_free: true, health_score: 85, health_level: "healthy", description: "Humus cremos din năut, tahini, lămâie și usturoi." },
    { id: 29, name: "Lasagna clasică", category: "internațional", difficulty: "medium", prep_time: 30, cook_time: 50, total_time: "80 min", cuisine: "italian", tastes: "savory, umami", dietary: ["nut_free"], is_vegan: false, is_vegetarian: false, is_gluten_free: false, is_dairy_free: false, health_score: 62, health_level: "moderate", description: "Lasagna cu sos bolognese, bechamel și parmezan." },
    { id: 30, name: "Tiramisu autentic", category: "desert", difficulty: "medium", prep_time: 30, cook_time: 10, total_time: "40 min", cuisine: "italian", tastes: "sweet", dietary: ["nut_free"], is_vegan: false, is_vegetarian: true, is_gluten_free: false, is_dairy_free: false, health_score: 48, health_level: "moderate", description: "Tiramisu cu mascarpone, cafea și pișcoturi." },
    { id: 31, name: "Brioche pufoasă", category: "desert", difficulty: "medium", prep_time: 30, cook_time: 120, total_time: "150 min", cuisine: "french", tastes: "sweet", dietary: ["nut_free"], is_vegan: false, is_vegetarian: true, is_gluten_free: false, is_dairy_free: false, health_score: 55, health_level: "moderate", description: "Brioche pufoasă cu unt și ouă, textură aerată." },
    { id: 32, name: "Gulaș unguresc", category: "internațional", difficulty: "medium", prep_time: 25, cook_time: 75, total_time: "100 min", cuisine: "maghiară", tastes: "spicy, savory", dietary: ["gluten_free", "nut_free"], is_vegan: false, is_vegetarian: false, is_gluten_free: true, is_dairy_free: true, health_score: 72, health_level: "moderate", description: "Gulaș tradițional cu carne de vită, cartofi și boia." },
    { id: 33, name: "Fasole bătută", category: "tradițional", difficulty: "easy", prep_time: 15, cook_time: 30, total_time: "45 min", cuisine: "românească", tastes: "savory", dietary: ["gluten_free", "vegan", "vegetarian"], is_vegan: true, is_vegetarian: true, is_gluten_free: true, is_dairy_free: true, health_score: 82, health_level: "healthy", description: "Fasole bătută cu ceapă și usturoi." },
    { id: 34, name: "Cordon bleu de pui", category: "internațional", difficulty: "medium", prep_time: 20, cook_time: 20, total_time: "40 min", cuisine: "franceză", tastes: "savory", dietary: ["nut_free"], is_vegan: false, is_vegetarian: false, is_gluten_free: false, is_dairy_free: false, health_score: 58, health_level: "moderate", description: "Piept de pui umplut cu șuncă și cașcaval, pane." },
    { id: 35, name: "Supă cremă de dovleac", category: "rapid", difficulty: "easy", prep_time: 10, cook_time: 20, total_time: "30 min", cuisine: "internațional", tastes: "sweet, savory", dietary: ["gluten_free", "vegetarian"], is_vegan: false, is_vegetarian: true, is_gluten_free: true, is_dairy_free: false, health_score: 78, health_level: "healthy", description: "Supă cremă de dovleac cu ghimbir și smântână." },
    { id: 36, name: "Pâine de casă cu maia", category: "tradițional", difficulty: "hard", prep_time: 30, cook_time: 210, total_time: "240 min", cuisine: "românească", tastes: "savory", dietary: ["vegan", "vegetarian", "nut_free"], is_vegan: true, is_vegetarian: true, is_gluten_free: false, is_dairy_free: true, health_score: 68, health_level: "moderate", description: "Pâine artizanală cu maia, coaptă în vas de fontă." },
    // Rețete suplimentare
    { id: 37, name: "Tocăniță de vită", category: "tradițional", difficulty: "medium", prep_time: 20, cook_time: 100, total_time: "120 min", cuisine: "românească", tastes: "savory", dietary: ["nut_free", "gluten_free"], is_vegan: false, is_vegetarian: false, is_gluten_free: true, is_dairy_free: true, health_score: 75, health_level: "healthy", description: "Tocăniță tradițională de vită cu cartofi și condimente." },
    { id: 38, name: "Plăcintă cu mere", category: "desert", difficulty: "easy", prep_time: 15, cook_time: 40, total_time: "55 min", cuisine: "românească", tastes: "sweet", dietary: ["nut_free"], is_vegan: false, is_vegetarian: true, is_gluten_free: false, is_dairy_free: false, health_score: 60, health_level: "moderate", description: "Plăcintă clasică cu mere și scorțișoară." },
    { id: 39, name: "Mici (mititei) de casă", category: "tradițional", difficulty: "medium", prep_time: 30, cook_time: 60, total_time: "90 min", cuisine: "românească", tastes: "savory, spicy", dietary: ["gluten_free", "nut_free"], is_vegan: false, is_vegetarian: false, is_gluten_free: true, is_dairy_free: true, health_score: 55, health_level: "moderate", description: "Mititei tradiționali românești, copți pe grătar." },
    { id: 40, name: "Baklava cu nucă", category: "desert", difficulty: "hard", prep_time: 40, cook_time: 80, total_time: "120 min", cuisine: "turcească", tastes: "sweet", dietary: ["nut_free"], is_vegan: false, is_vegetarian: true, is_gluten_free: false, is_dairy_free: true, health_score: 45, health_level: "unhealthy", description: "Baklava crocantă cu nucă și sirop de zahăr." },
    { id: 41, name: "Crap la cuptor cu legume", category: "tradițional", difficulty: "medium", prep_time: 20, cook_time: 45, total_time: "65 min", cuisine: "românească", tastes: "savory", dietary: ["gluten_free", "nut_free"], is_vegan: false, is_vegetarian: false, is_gluten_free: true, is_dairy_free: true, health_score: 82, health_level: "healthy", description: "Carp copt la cuptor cu legume proaspete." },
    { id: 42, name: "Friptură de porc cu sos de vin", category: "internațional", difficulty: "medium", prep_time: 15, cook_time: 55, total_time: "70 min", cuisine: "franceză", tastes: "savory", dietary: ["nut_free"], is_vegan: false, is_vegetarian: false, is_gluten_free: false, is_dairy_free: false, health_score: 65, health_level: "moderate", description: "Ceafă de porc cu sos demi-glace și vin roșu." }
];

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
// VARIABILE GLOBALE
// ============================================
let currentFilter = 'all';
let isApiOnline = false;
let isWaitingForResponse = false;

// ============================================
// FUNCȚII AJUTĂTOARE
// ============================================
function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

function getDifficultyBadge(difficulty) {
    const difficultyMap = {
        'easy': { class: 'difficulty-easy', icon: '🟢', text: 'Ușor' },
        'medium': { class: 'difficulty-medium', icon: '🟡', text: 'Mediu' },
        'hard': { class: 'difficulty-hard', icon: '🔴', text: 'Avansat' }
    };
    const d = difficultyMap[difficulty.toLowerCase()] || { class: 'difficulty-medium', icon: '🟡', text: 'Mediu' };
    return `<span class="card-badge ${d.class}"><i class="fas fa-chart-line"></i> ${d.text}</span>`;
}

function getTimeBadge(recipe) {
    return `<span class="card-badge time"><i class="far fa-clock"></i> ${recipe.total_time} (${recipe.prep_time}' + ${recipe.cook_time}')</span>`;
}

function getDietaryBadges(recipe) {
    let badges = '';
    if (recipe.is_vegan) badges += `<span class="card-badge vegan"><i class="fas fa-leaf"></i> Vegan</span>`;
    else if (recipe.is_vegetarian) badges += `<span class="card-badge vegetarian"><i class="fas fa-seedling"></i> Vegetarian</span>`;
    if (recipe.is_gluten_free) badges += `<span class="card-badge gluten-free"><i class="fas fa-wheat-slash"></i> Fără gluten</span>`;
    if (recipe.is_dairy_free) badges += `<span class="card-badge dairy-free"><i class="fas fa-cheese"></i> Fără lactoză</span>`;
    if (recipe.dietary && recipe.dietary.includes('nut_free')) badges += `<span class="card-badge nut-free"><i class="fas fa-seedling"></i> Fără nuci</span>`;
    if (recipe.health_score >= 75) badges += `<span class="card-badge healthy"><i class="fas fa-heartbeat"></i> Sănătos</span>`;
    return badges;
}

function getHealthScoreCircle(score) {
    const circumference = 138;
    const offset = circumference - (circumference * score) / 100;
    const color = score >= 75 ? '#4CAF50' : (score >= 50 ? '#FF9800' : '#F44336');
    return `
        <div class="health-score-circle">
            <svg viewBox="0 0 50 50">
                <circle cx="25" cy="25" r="22" stroke="#e0e0e0" stroke-width="3" fill="none" />
                <circle cx="25" cy="25" r="22" stroke="${color}" stroke-width="3" fill="none" stroke-dasharray="${circumference}" stroke-dashoffset="${offset}" />
            </svg>
            <span>${score}</span>
        </div>
    `;
}

function matchesFilter(recipe, filter) {
    if (filter === 'all') return true;
    if (filter === 'vegan') return recipe.is_vegan === true;
    if (filter === 'gluten-free') return recipe.is_gluten_free === true;
    if (filter === 'healthy') return recipe.health_score >= 75;
    if (filter === 'italian') return recipe.cuisine && recipe.cuisine.toLowerCase().includes('italian');
    if (filter === 'romanesc') return recipe.cuisine && recipe.cuisine.toLowerCase().includes('românească');
    return recipe.category === filter;
}

function renderRecipes() {
    const grid = document.getElementById('recipesGrid');
    if (!grid) return;
    const filtered = RECIPES_DATABASE.filter(recipe => matchesFilter(recipe, currentFilter));
    if (filtered.length === 0) {
        grid.innerHTML = '<div style="grid-column:1/-1; text-align:center; padding:3rem;">Nu există rețete în această secțiune academică</div>';
        return;
    }
    grid.innerHTML = filtered.map(recipe => `
        <div class="recipe-card" data-recipe-id="${recipe.id}" data-recipe-name="${recipe.name.replace(/'/g, "\\'")}">
            ${getHealthScoreCircle(recipe.health_score)}
            <div class="card-img"><i class="fas fa-utensils" style="opacity:0.7"></i></div>
            <div class="card-content">
                <div class="recipe-time-header"><div class="title">${escapeHtml(recipe.name)}</div></div>
                <div class="recipe-cuisine"><i class="fas fa-globe"></i> ${recipe.cuisine.split(',')[0]}</div>
                <div class="recipe-meta">${getTimeBadge(recipe)} ${getDifficultyBadge(recipe.difficulty)}</div>
                <div class="description">${escapeHtml(recipe.description)}</div>
                <div class="card-badges">${getDietaryBadges(recipe)}</div>
                <div class="badge">${recipe.category}</div>
            </div>
        </div>
    `).join('');
}

// ============================================
// CONEXIUNE API
// ============================================
function updateApiStatus(status, message) {
    const indicator = document.querySelector('.status-indicator');
    const statusText = document.getElementById('statusText');
    if (!indicator || !statusText) return;
    indicator.classList.remove('online', 'offline', 'checking');
    if (status === 'online') { indicator.classList.add('online'); statusText.textContent = message || 'API conectat · model SVM activ'; isApiOnline = true; }
    else if (status === 'offline') { indicator.classList.add('offline'); statusText.textContent = message || 'API offline · mod de rezervă activ'; isApiOnline = false; }
    else { indicator.classList.add('checking'); statusText.textContent = message || 'Verificare conexiune...'; isApiOnline = false; }
}

async function checkApiHealth() {
    updateApiStatus('checking', 'Verificare conexiune API...');
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 5000);
        const response = await fetch(API_ENDPOINTS.health, { method: 'GET', signal: controller.signal });
        clearTimeout(timeoutId);
        if (response.ok) {
            const data = await response.json();
            const modelStatus = data.model_incarcat ? 'model activ' : 'model indisponibil';
            updateApiStatus('online', `API conectat · ${modelStatus}`);
        } else { updateApiStatus('offline', `API indisponibil (status ${response.status})`); }
    } catch (error) { updateApiStatus('offline', 'API indisponibil · mod de rezervă activ'); }
}

async function sendMessageToApi(message) {
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 15000);
        const response = await fetch(API_ENDPOINTS.chat, {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mesaj: message }), signal: controller.signal
        });
        clearTimeout(timeoutId);
        if (response.ok) return { success: true, data: await response.json() };
        else return { success: false, error: `HTTP ${response.status}` };
    } catch (error) { return { success: false, error: error.message }; }
}

function getFallbackResponse(question) {
    const q = question.toLowerCase();
    if (q.includes('pizza') && (q.includes('cum') || q.includes('prepar'))) return "Pizza clasică necesită: 500g făină, 300ml apă, 7g drojdie, 10g sare. Frământați 10 minute, dospire 2 ore, coacere 12 minute la 250°C.";
    if (q.includes('clătite') || (q.includes('clatite'))) return "Clătite: 2 ouă, 250ml lapte, 125g făină, 2 linguri ulei, 15g zahăr. Omogenizați, prăjiți în tigaie unsă.";
    if (q.includes('cozonac')) return "Cozonacul se coace la 170°C timp de 45-50 minute. Verificați cu scobitoarea.";
    if (q.includes('sarmale')) return "Sarmalele se fierb la foc mic 2-2.5 ore, în funcție de mărime.";
    if (q.includes('înlocuitor') && q.includes('ouă')) return "Înlocuitor pentru ou: 1 lingură semințe de in măcinate + 3 linguri apă, sau 50g piure de mere.";
    if (q.includes('papanasi')) return "Papanași: 500g brânză de vaci, 2 ouă, 100g făină, 50g griș. Se fierb 5-7 minute, apoi se prăjesc.";
    if (q.includes('mămăligă') || q.includes('mamaliga')) return "Mămăligă: 1L apă, 10g sare, 300g mălai. Turnați mălaiul în ploaie, amestecați 15 minute.";
    if (q.includes('salut') || q.includes('bună')) return "Bună ziua. Vă stau la dispoziție pentru orice întrebare culinară.";
    if (q.includes('mulțumesc') || q.includes('mersi')) return "Cu plăcere! Vă invit să consultați arhiva de rețete.";
    return "Vă rugăm să reformulați întrebarea. Puteți întreba despre rețete din lista laterală, timpi de preparare, înlocuitori sau tehnici culinare fundamentale.";
}

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
    const time = new Date().toLocaleTimeString('ro-RO', { hour: '2-digit', minute: '2-digit' });
    meta.innerText = sender === 'user' ? `dvs. · ${time}` : `asistent academic${intent ? ` · intenție: ${intent}` : ''} · ${time}`;
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
            } else { responseText = getFallbackResponse(message); }
        } else { responseText = getFallbackResponse(message); }
        hideTypingIndicator();
        addMessage('bot', responseText, detectedIntent);
    } catch (error) {
        hideTypingIndicator();
        addMessage('bot', 'Sistemul întâmpină dificultăți tehnice. Vă rugăm să reîncercați.');
    } finally { isWaitingForResponse = false; }
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
// INIȚIALIZARE
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
    const suggestionsList = ["Cum se prepară pizza neapolitană?", "Ce ingrediente sunt necesare pentru clătite clasice?", "Timp coacere cozonac tradițional", "Înlocuitor pentru ouă în prăjituri", "Cât durează să fac sarmale?", "Cum se face tiramisu autentic?", "Tehnici pentru blat pufos de chec"];
    suggestionsContainer.innerHTML = suggestionsList.map(s => `<span class="chip" data-question="${escapeHtml(s)}">${escapeHtml(s.substring(0, 40))}${s.length > 40 ? '...' : ''}</span>`).join('');
    document.querySelectorAll('.chip').forEach(chip => {
        chip.addEventListener('click', () => {
            const question = chip.getAttribute('data-question');
            if (question) { document.getElementById('userInput').value = question; handleSendMessage(); }
        });
    });
}

function initializeRecipeClicks() {
    document.addEventListener('click', (e) => {
        const card = e.target.closest('.recipe-card');
        if (card) {
            const recipeId = parseInt(card.getAttribute('data-recipe-id'));
            const recipe = RECIPES_DATABASE.find(r => r.id === recipeId);
            if (recipe && !e.ctrlKey && !e.metaKey) {
                const input = document.getElementById('userInput');
                if (input) input.value = `Cum se prepară ${recipe.name}? Vreau detalii despre timp (${recipe.total_time}), dificultate (${recipe.difficulty}) și dacă e potrivită pentru ${recipe.is_vegan ? 'vegani' : (recipe.is_vegetarian ? 'vegetarieni' : 'toți')}.`;
                handleSendMessage();
            }
        }
    });
}

function initializeEventListeners() {
    const sendBtn = document.getElementById('sendBtn');
    const userInput = document.getElementById('userInput');
    if (sendBtn) sendBtn.addEventListener('click', handleSendMessage);
    if (userInput) userInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') handleSendMessage(); });
}

async function initialize() {
    renderRecipes();
    initializeFilters();
    initializeSuggestions();
    initializeRecipeClicks();
    initializeEventListeners();
    await checkApiHealth();
    setInterval(checkApiHealth, 30000);
    console.log('[System] Bucătăria Academică - sistem inițializat cu succes');
}

if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initialize);
else initialize();