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

    // Inicializar el tercer gráfico
    const chart3 = echarts.init(document.getElementById('grafico3'));
    chart3.setOption(chartData.chart3);
    };

window.addEventListener('load', async () => {
    await initCharts();
});
