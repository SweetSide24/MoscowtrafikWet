document.addEventListener('DOMContentLoaded', function() {
    // Инициализация карты (без API ключа)
    const mapElement = document.getElementById('map');
    
    // Здесь можно добавить логику для статичной карты
    // или использовать OpenStreetMap без ключа API
    mapElement.innerHTML = `
        <iframe 
            width="100%" 
            height="100%" 
            frameborder="0" 
            scrolling="no" 
            marginheight="0" 
            marginwidth="0" 
            src="https://www.openstreetmap.org/export/embed.html?bbox=37.3696,55.5815,37.8709,55.8322&layer=mapnik&marker=55.751244,37.618423">
        </iframe>
    `;
});