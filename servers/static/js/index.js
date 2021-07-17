// 柱状图1模块 完成
(function() {
  // 实例化对象
  var myChart = echarts.init(document.querySelector(".bar .chart"));
$.getJSON('/api/relp_avg_cost', function(bardata) {
  var data = [];
  var titlename = [];
  for (var key in bardata.data) {
    titlename.push(bardata.data[key].relp);
    num = Math.floor(bardata.data[key].relp_avg_cost * 100) / 100
    data.push(num);
  }

      // 指定配置和数据
  var option = {
    color: ["#2f89cf"],
    tooltip: {
      trigger: "axis",
      formatter: '{a0}:{c0}元',
      axisPointer: {
        // 坐标轴指示器，坐标轴触发有效
        type: "shadow" // 默认为直线，可选为：'line' | 'shadow'
      }
    },
    grid: {
      left: "0%",
      top: "30px",
      right: "0%",
      bottom: "4%",
      containLabel: true
    },
    xAxis: [
      {
        type: "category",
        data: titlename,
        axisTick: {
          alignWithLabel: true
        },
        axisLabel: {
          textStyle: {
            color: "rgba(255,255,255,.6)",
            fontSize: "13"
          }
        },
        axisLine: {
          show: false
        }
      }
    ],
    yAxis: [
      {
        type: "value",
        name: "元",
        nameLocation : 'end',
        nameTextStyle: {
          color: "rgba(255,255,255,.6)"
        },
        axisLabel: {
          textStyle: {
            color: "rgba(255,255,255,.6)",
            fontSize: "12"
          }
        },
        axisLine: {
          lineStyle: {
            color: "rgba(255,255,255,.1)"
            // width: 1,
            // type: "solid"
          }
        },
        splitLine: {
          lineStyle: {
            color: "rgba(255,255,255,.1)"
          }
        }
      }
    ],
    series: [
      {
        name: "人均消费",
        type: "bar",
        barWidth: "35%",
        data: data,
        itemStyle: {
          barBorderRadius: 5
        }
      }
    ]
  };

  // 把配置给实例对象
  myChart.setOption(option);
 });

  window.addEventListener("resize", function() {
    myChart.resize();
  });
})();

// 柱状堆叠图定制 完成,等数据
(function() {
  // 基于准备好的dom，初始化echarts实例
  var myChart = echarts.init(document.querySelector(".line .chart"));
  $.getJSON('/api/quarter_days', function(bardata) {
    var titlename = ['1-3天', '4-7天', '8-10天','11-15天','15天以上'];
    // 2. 指定配置和数据
    option = {
      tooltip: {
          trigger: 'axis',
          axisPointer: {            // 坐标轴指示器，坐标轴触发有效
              type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
          }
      },
      legend: {
          data: ['1-3天', '4-7天', '8-10天','11-15天','15天以上'],
          textStyle: {
            color: "rgba(255,255,255,.5)",
            fontSize: "12"
          }
      },
      grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
      },
      xAxis: [
          {
              type: 'category',
              data: ['第一季度', '第二季度', '第三季度', '第四季度'],
              axisLabel: {
                textStyle: {
                  color: "rgba(255,255,255,.6)",
                  fontSize: "13"
                }
              },
          }
      ],
      yAxis: [
        {
          type: "value",
          name: "篇",
          nameLocation : 'end',
          interval: 2000,
          nameTextStyle: {
            color: "rgba(255,255,255,.6)"
          },
          axisLabel: {
            textStyle: {
              color: "rgba(255,255,255,.6)",
              fontSize: "12"
            }
          },
          axisLine: {
            lineStyle: {
              color: "rgba(255,255,255,.1)"
              // width: 1,
              // type: "solid"
            }
          },
          splitLine: {
            lineStyle: {
              color: "rgba(255,255,255,.1)"
            }
          }
        }
      ],
      series: [
          {
              name: titlename[bardata.data[0].days-1],
              type: 'bar',
              stack: '行程时长',
              barWidth: 30,
              emphasis: {
                  focus: 'series'
              },
              data: bardata.data[0].quarter_list,
              itemStyle: {
                normal: {
                    color: '#1E90FF'
                }
            }
          },
          {
              name: titlename[bardata.data[1].days-1],
              type: 'bar',
              stack: '行程时长',
              barWidth: 30,
              emphasis: {
                  focus: 'series'
              },
              data:bardata.data[1].quarter_list,
              itemStyle: {
                normal: {
                    color: '#00BFFF'
                }
            }
          },
          {
              name: titlename[bardata.data[2].days-1],
              type: 'bar',
              stack: '行程时长',
              barWidth: 30,
              emphasis: {
                  focus: 'series'
              },
              data: bardata.data[2].quarter_list,
              itemStyle: {
                normal: {
                    color: '#87CEEB'
                }
            }
          },
          {
            name: titlename[bardata.data[3].days-1],
            type: 'bar',
            stack: '行程时长',
            barWidth: 30,
            emphasis: {
                focus: 'series'
            },
            data:  bardata.data[3].quarter_list,
            itemStyle: {
              normal: {
                  color: '#AFEEEE'
              }
          }
        },
        {
          name: titlename[bardata.data[4].days-1],
          type: 'bar',
          stack: '行程时长',
          barWidth: 30,
          emphasis: {
              focus: 'series'
          },
          data:  bardata.data[4].quarter_list,
          itemStyle: {
            normal: {
                color: '#4682B4'
            }
        }
      },
      ]
  };
    // 3. 把配置和数据给实例对象
    myChart.setOption(option);
  });

  window.addEventListener("resize", function() {
    myChart.resize();
  });
})();

// 饼形图定制 完成
(function() {
  // 基于准备好的dom，初始化echarts实例
  var myChart = echarts.init(document.querySelector(".pie .chart"));

  $.getJSON('/api/relp_story_num', function(piedata) {
    option = {
      tooltip: {
        trigger: "item",
        formatter: "{a} <br/>{b}: {c} ({d}%)",
        position: function(p) {
          //其中p为当前鼠标的位置
          return [p[0] + 10, p[1] - 10];
        }
      },
      legend: {
        top: "90%",
        itemWidth: 10,
        itemHeight: 10,
        data: ["独自一人", "闺蜜", "情侣", "家庭", "学生", "三五好友",  "亲子"],
        textStyle: {
          color: "rgba(255,255,255,.5)",
          fontSize: "12"
        }
      },
      series: [
        {
          name: "出行人数",
          type: "pie",
          center: ["50%", "42%"],
          radius: ["0%", "70%"],
          color: [
            "#065aab",
            "#066eab",
            "#0682ab",
            "#0696ab",
            "#06a0ab",
            "#06b4ab",
            "#06c8ab",
            "#06dcab",
            "#06f0ab"
          ],
          label: {
            normal: {
              position: 'inner',
              show : false
            }
          },
          labelLine: { show: false },
          data: piedata.data
          // data: [
          //   { value: 1, name: "独自一人" },
          //   { value: 4, name: "闺蜜" },
          //   { value: 2, name: "情侣" },
          //   { value: 2, name: "家庭" },
          //   { value: 1, name: "学生" },
          //   { value: 1, name: "三五好友" },
          //   { value: 1, name: "亲子" },
          // ]
        }
      ]
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
  });

  window.addEventListener("resize", function() {
    myChart.resize();
  });
})();
// 进度柱状图模块 完成
(function() {
  // 基于准备好的dom，初始化echarts实例
  var myChart = echarts.init(document.querySelector(".bar1 .chart"));

  // var data = [70, 34, 60, 78, 69];
  // var titlename = ["摄影", "美食", "短途周末", "深度游", "自驾"];
  var valdata = [702, 350, 610, 793, 664];
  var myColor = ["#1039E7", "#F57974", "#57D0E3", "#F8B448", "#1B78F6", "#1B78F6", "#1B78F6"];
  $.getJSON('/api/play_way_percent_topn?num=5', function(bar1data) {
    var titlename = [];
    var data = [];
    for (var key in bar1data.data) {
      titlename.push(bar1data.data[key].play_way);
      data.push(bar1data.data[key].percent);
    }

    option = {
      //图标位置
      grid: {
        top: "10%",
        left: "22%",
        bottom: "10%"
      },
      xAxis: {
        show: false
      },
      yAxis: [
        {
          show: true,
          data: titlename,
          inverse: true,
          axisLine: {
            show: false
          },
          splitLine: {
            show: false
          },
          axisTick: {
            show: false
          },
          axisLabel: {
            color: "#fff",
  
            rich: {
              lg: {
                backgroundColor: "#33911",
                color: "#fff",
                borderRadius: 15,
                // padding: 5,
                align: "center",
                width: 15,
                height: 15
              }
            }
          }
        },
        {
          show: false,
          inverse: false,
          data: valdata,
          axisLabel: {
            textStyle: {
              fontSize: 12,
              color: "#fff"
            }
          }
        }
      ],
      series: [
        {
          name: "条",
          type: "bar",
          yAxisIndex: 0,
          data: data,
          barCategoryGap: 50,
          barWidth: 15,
          itemStyle: {
            normal: {
              barBorderRadius: 20,
              color: function(params) {
                var num = myColor.length;
                return myColor[params.dataIndex % num];
              }
            }
          },
          label: {
            normal: {
              show: true,
              position: "inside",
              formatter: "{c}%"
            }
          }
        }
      ]
    };
  
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
  });
  window.addEventListener("resize", function() {
    myChart.resize();
  });
})();
// 折线图 完成
(function() {
  // 基于准备好的dom，初始化echarts实例
  var myChart = echarts.init(document.querySelector(".line1 .chart"));
  $.getJSON('/api/month_and_people?year1=2019&year2=2020', function(linedata) {
    var data1 = [];
    var data2 = [];
    var year = [];
    for (var key in linedata.data) {
      year.push(linedata.data[key].year);
    }
    for(var k in linedata.data[0].month_and_people){
      data1.push(linedata.data[0].month_and_people[k].people_num);
    }
    for(var k in linedata.data[1].month_and_people){
      data2.push(linedata.data[1].month_and_people[k].people_num);
    }
    option = {
      tooltip: {
        trigger: "axis",
        axisPointer: {
          lineStyle: {
            color: "#dddc6b"
          }
        }
      },
      legend: {
        top: "0%",
        data: ['2019年游记数量', '2020年游记数量'],
        textStyle: {
          color: "rgba(255,255,255,.5)",
          fontSize: "12"
        }
      },
      grid: {
        left: "10",
        top: "30",
        right: "10",
        bottom: "10",
        containLabel: true
      },
  
      xAxis: [
        {
          type: "category",
          boundaryGap: false,
          axisLabel: {
            textStyle: {
              color: "rgba(255,255,255,.6)",
              fontSize: 10
            }
          },
          axisLine: {
            lineStyle: {
              color: "rgba(255,255,255,.2)"
            }
          },
  
          data: [
            "1月",
            "2月",
            "3月",
            "4月",
            "5月",
            "6月",
            "7月",
            "8月",
            "9月",
            "10月",
            "11月",
            "12月"
          ]
        },
        {
          axisPointer: { show: false },
          axisLine: { show: false },
          position: "bottom",
          offset: 20
        }
      ],
  
      yAxis: [
        {
          type: "value",
          name: "篇",
          nameLocation : 'end',
          nameTextStyle: {
            color: "rgba(255,255,255,.6)"
          },
          axisTick: { show: false },
          axisLine: {
            lineStyle: {
              color: "rgba(255,255,255,.1)"
            }
          },
          axisLabel: {
            textStyle: {
              color: "rgba(255,255,255,.6)",
              fontSize: 12
            }
          },
  
          splitLine: {
            lineStyle: {
              color: "rgba(255,255,255,.1)"
            }
          }
        }
      ],
      series: [
        {
          name: year[0]+"年游记数量",
          type: "line",
          smooth: false,
          symbol: "circle",
          symbolSize: 5,
          showSymbol: false,
          lineStyle: {
            normal: {
              color: "#0184d5",
              width: 2
            }
          },
          areaStyle: {
            normal: {
              color: new echarts.graphic.LinearGradient(
                0,
                0,
                0,
                1,
                [
                  {
                    offset: 0,
                    color: "rgba(1, 132, 213, 0.4)"
                  },
                  {
                    offset: 0.8,
                    color: "rgba(1, 132, 213, 0.1)"
                  }
                ],
                false
              ),
              shadowColor: "rgba(0, 0, 0, 0.1)"
            }
          },
          itemStyle: {
            normal: {
              color: "#0184d5",
              borderColor: "rgba(221, 220, 107, .1)",
              borderWidth: 12
            }
          },
          data: data1
        },
        {
          name: year[1]+"年游记数量",
          type: "line",
          smooth: false,
          symbol: "circle",
          symbolSize: 5,
          showSymbol: false,
          lineStyle: {
            normal: {
              color: "#66CDAA",
              width: 2
            }
          },
          areaStyle: {
            normal: {
              color: new echarts.graphic.LinearGradient(
                0,
                0,
                0,
                1,
                [
                  {
                    offset: 0,
                    color: "rgba(102, 205 ,170 ,0.4)"
                  },
                  {
                    offset: 0.8,
                    color: "rgba(102, 205, 170, 0.1)"
                  }
                ],
                false
              ),
              shadowColor: "rgba(0, 0, 0, 0.1)"
            }
          },
          itemStyle: {
            normal: {
              color: "#66CDAA",
              borderColor: "rgba(102, 205, 170, .1)",
              borderWidth: 12
            }
          },
          data:data2
        }
      ]
    };
  
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
  });

  window.addEventListener("resize", function() {
    myChart.resize();
  });
})();

