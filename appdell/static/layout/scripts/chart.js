const getChartData = async () => {
    try {
        const response = await fetch('/get_chart/');
        if (!response.ok) throw new Error('Error al cargar los datos de los gráficos');
        return await response.json();
    } catch (ex) {
        console.error('Error:', ex.message);
    }
};

const initCharts = async () => {
    const chartData = await getChartData();

    // Inicializar el primer gráfico
    const chart1 = echarts.init(document.getElementById('grafico1'));

    // Configuración del tooltip para el gráfico 1
    chartData.chart1.tooltip = {
        trigger: 'axis', // Muestra el tooltip al pasar sobre el eje
        formatter: function(params) {
            const index = params[0].dataIndex; // Índice del punto actual
            const tooltipDetails = chartData.chart1.tooltip_data[index]; // Detalles enviados desde Django

            let tooltipContent = `<strong>${tooltipDetails.fecha}</strong><br/>`;
            tooltipContent += `Aceptados: ${tooltipDetails.aceptados}<br/>`;
            tooltipContent += `Rechazados: ${tooltipDetails.rechazados}<br/>`;
            tooltipContent += `Total: ${tooltipDetails.total}<br/>`;

            return tooltipContent;
        }
    };

    chart1.setOption(chartData.chart1);

    // Inicializar el segundo gráfico
    const chart2 = echarts.init(document.getElementById('grafico2'));
    chart2.setOption(chartData.chart2);

    // Inicializar el tercer gráfico (nuevo gráfico de líneas para solicitudes por fecha)
    const chart3 = echarts.init(document.getElementById('grafico3'));

    chartData.chart3.tooltip = {
        trigger: 'axis', // Tooltip dinámico al pasar sobre un punto en el eje X
        formatter: function(params) {
            let tooltipContent = `<strong>${params[0].name}</strong><br/>`; // Fecha
            params.forEach(param => {
                tooltipContent += `${param.seriesName}: ${param.value}<br/>`; // Carrera y valor
            });
            return tooltipContent;
        }
    };

    chart3.setOption(chartData.chart3);

    // Inicializar el cuarto gráfico (nuevo gráfico circular para porcentaje por carrera)
    const chart4 = echarts.init(document.getElementById('grafico4'));

    chartData.chart4.tooltip = {
        trigger: 'item', // Tooltip dinámico al pasar sobre un segmento del gráfico circular
        formatter: '{a} <br/>{b}: {c} ({d}%)' // Carrera, valor y porcentaje
    };

    chart4.setOption(chartData.chart4);
};

window.addEventListener('load', async () => {
    await initCharts();
});
