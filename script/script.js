function graficar() {
    var region1 = document.getElementById("region1").value;
    var region2 = document.getElementById("region2").value;

    fetch('/graficar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            region1: region1,
            region2: region2
        })
    })
    .then(response => response.json())
    .then(data => {
        var ctx = document.getElementById('grafica').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: data.datasets
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    })
    .catch(error => console.error('Error:', error));
}