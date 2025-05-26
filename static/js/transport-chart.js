document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('transportChart').getContext('2d');
    
    // Данные для диаграммы (можно заменить на реальные из API)
    const transportData = {
        labels: ['Метро', 'Автобусы', 'Трамваи', 'МЦД', 'Велосипеды', 'Такси'],
        datasets: [{
            data: [45, 25, 10, 12, 5, 3],
            backgroundColor: [
                '#e74c3c',
                '#3498db',
                '#f1c40f',
                '#2ecc71',
                '#9b59b6',
                '#e67e22'
            ],
            borderWidth: 1
        }]
    };

    new Chart(ctx, {
        type: 'doughnut',
        data: transportData,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'right',
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.label}: ${context.raw}%`;
                        }
                    }
                }
            }
        }
    });
});