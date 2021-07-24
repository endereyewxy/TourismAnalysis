var dom = document.getElementById("map1");
var myChart = echarts.init(dom);
var app = {};

var option;


// $.getJSON('/static/data/flights.json', function(data) {

// function getAirportCoord(idx) {
//     return [data.airports[idx][3], data.airports[idx][4]];
// }

// var routes = data.routes.map(function (airline) {
//     return [
//         getAirportCoord(airline[1]),
//         getAirportCoord(airline[2])
//     ];
// });

myChart.setOption({
    backgroundColor: '#000',
    globe: {
        baseTexture: '/static/images/min_world.topo.bathy.jpg',
        heightTexture: '/static/images/bathymetry_bw_composite.jpg',
        globeRadius: 80,
        shading: 'lambert',

        light: {
            ambient: {
                intensity: 0.4
            },
            main: {
                intensity: 0.4
            }
        },

        viewControl: {
            autoRotate: true,
            projection: 'orthographic',
            orthographicSize: 160, //控制地图大小
            maxOrthographicSize: 160,
            minOrthographicSize: 160,
            animation: true,
            // alpha:60,
            // beta:10,
            animationDurationUpdate: 10

            // autoRotateSpeed:5
        },
    },
    // series: {
    //
    //     type: 'lines3D',
    //
    //     coordinateSystem: 'globe',
    //
    //     blendMode: 'lighter',
    //
    //     lineStyle: {
    //         width: 1,
    //         color: 'rgb(50, 50, 150)',
    //         opacity: 0.1
    //     },
    //
    //     data: routes
    // }
});
// });

if (option && typeof option === 'object') {
    myChart.setOption(option);
}
