# TourismAnalysis
重庆大学毕业实习大数据项目

## 接口规范

### 爬虫与后端

爬虫使用SQLite数据库向后端提交原始数据，该数据库中的表描述如下：

#### stories

该表描述游记实体。

| 字段       | 类型 | 描述       | 备注                               |
| ---------- | ---- | ---------- | ---------------------------------- |
| stid       | int  | 游记编号   | 主键，与原始网站中编号规则保持一致 |
| cost       | int  | 人均消费   | 单位：元                           |
| auth       | str  | 作者用户名 |                                    |
| relp       | str  | 参与者关系 |                                    |
| title      | str  | 标题       |                                    |
| date_start | str  | 开始日期   | 格式：YYYY-mm-dd                   |
| date_count | int  | 持续时间   | 单位：天                           |
| text_count | int  | 正文字数   |                                    |
| pict_count | int  | 图片数量   |                                    |
| cmmt_count | int  | 评论数量   |                                    |
| like_count | int  | 点赞数量   |                                    |
| view_count | int  | 浏览数量   |                                    |

#### scenics

该表描述景点实体。

| 字段 | 类型 | 描述     | 备注                               |
| ---- | ---- | -------- | ---------------------------------- |
| scid | int  | 景点编号 | 主键，与原始网站中编号规则保持一致 |
| name | str  | 景点名称 |                                    |
| city | int  | 所属城市 |                                    |

虽然称为景点，但该实体也会描述诸如酒店、机场等其它地点。

#### cities

该表描述城市实体。

| 字段 | 类型 | 描述     | 备注                               |
| ---- | ---- | -------- | ---------------------------------- |
| ctid | int  | 城市编号 | 主键，与原始网站中编号规则保持一致 |
| name | str  | 城市名称 |                                    |
| prov | str  | 所属省份 | 国外城市统一属于“国外”省份         |

#### visits

该表描述游记中提及景点和城市的情况。

| 字段  | 类型 | 描述                       | 备注         |
| ----- | ---- | -------------------------- | ------------ |
| vstid | int  | 对应游记编号               | 游记表的外键 |
| index | int  | 游记中的出现次序，从零开始 |              |
| vscid | int  | 对应景点编号               | 景点表的外键 |
| vctid | int  | 对应城市编号               | 城市表的外键 |

字段`vstid`和`index`为该表的复合主键，字段`vscid`和`vctid`有且只有一个非空。

#### how_to

该表描述游记的玩法标签。

| 字段  | 类型 | 描述         | 备注         |
| ----- | ---- | ------------ | ------------ |
| hstid | int  | 对应游记编号 | 游记表的外键 |
| h_tag | str  | 标签内容     |              |

### 后端与前端

#### 错误代码说明

| 错误代码 | 解释     |
| -------- | -------- |
| 100      | 无错误   |
| 101      | 参数错误 |

#### 出行人数


##### 简要描述

- 月份平均出行人数

##### 请求URL
- ` /api/month_and_people/ `

##### 请求方式

- GET

##### 参数

| 参数名 | 必选 | 类型 | 说明                                 |
| ------ | ---- | ---- | ------------------------------------ |
| year1  | 是   | int  | year1=2021，获取2021年的每月出行人数 |
| year2  | 是   | int  | year2=2018，获取2018年的每月出行人数 |



##### 返回示例

``` json
{
    "error_code": 100,
    "data": [{
        "year" : 2021,
        "month_and_people" : [{
            "month": 12,
            "people_num": 2345,    
        }]
    }]
}
```

##### 返回参数说明 

| 参数名           | 类型  | 说明                               |
| :--------------- | :---- | ---------------------------------- |
| year             | int   | 年                                 |
| month_and_people | list  | 包含12个元素，月份及其每月出行人数 |
| month            | int   | 月份（按升序）                     |
| people_num       | float | 对应月份的出行人数                 |

#### 人均消费


##### 简要描述

- 获取人物对应的人均消费

##### 请求URL
- ` /api/relp_avg_cost/ `
##### 请求方式
- GET

##### 返回示例 

``` json
{
    "error_code": 100,
    "data": [{
        "relp":"闺蜜",
        "relp_avg_cost": 2345.12
    }]
}
```

##### 返回参数说明 

| 参数名        | 类型   | 说明                                         |
| :------------ | :----- | -------------------------------------------- |
| relp          | string | 人物关系                                     |
| relp_avg_cost | float  | 对应的人物关系的每天的人均消费，保留两位小数 |

##### 其他说明

返回的数据不要包含 name = Null 的数据

#### 人物


##### 简要描述

- 获取对应人物的总游记数量

##### 请求UR
- `/api/relp_story_num/ `
##### 请求方式
- GET


##### 返回示例 

``` json
{
    "error_code": 100,
    "data": [{
        "name": "独自一人",
        "value": 234
    }]
}
```

##### 返回参数说明 

| 参数名 | 类型   | 说明                   |
| :----- | :----- | ---------------------- |
| name   | string | 人物关系               |
| value  | int    | 对应人物关系的总游记数 |

#### 游玩方式


##### 简要描述

- 游玩方式占总游记数的百分比（前n个）

##### 请求URL
- ` /api/play_way_percent_topn/ `

##### 请求方式

- GET 

##### 参数

| 参数名 | 必选 | 类型 | 说明    |
| :----- | :--- | :--- | ------- |
| num    | 是   | int  | 前num个 |


##### 返回示例 

``` json
{
    "error_code": 100,
    "data": [{
        "play_way": "摄影",
        "percent": 23,
    }]
}
```

##### 返回参数说明 

| 参数名   | 类型   | 说明                                            |
| :------- | :----- | ----------------------------------------------- |
| play_way | string | 游玩方式                                        |
| percent  | int    | 游玩方式占总游记数的百分比，如23.3%，percent=23 |


#### 行程时长


##### 简要描述

- 每月的游玩时长聚类

##### 请求URL
- ` /api/everymonth_playtime_clustering/ `
##### 请求方式
- GET

##### 返回示例 

``` json
{
    "error_code": 100,
    "data": [{
        "month": 11,
        "days": [2.2,3.4]
    }]
}
```

##### 返回参数说明 

| 参数名 | 类型         | 说明                                                         |
| :----- | :----------- | ------------------------------------------------------------ |
| month  | int          | 月份                                                         |
| days   | array[float] | 数组的长度根据聚类聚出来的点的个数确定，每个元素就是聚类点的值 |

#### 省份热度


##### 简要描述

- 获取2019至2021年的省份热度

##### 请求URL

- ` /api/prov_hot/ `
##### 请求方式
- GET


##### 返回示例 

``` json
{
    "error_code": 100,
    "data": [{
        "year": 2020,
        "prov": [{
            "name": "重庆",
            "hot": 999,
        }]
        "max":99999
    }]
}
```

##### 返回参数说明 

| 参数名 | 类型   | 说明                                           |
| :----- | :----- | ---------------------------------------------- |
| year   | int    | 年份                                           |
| prov   | list   | 省份列表                                       |
| name   | string | 省份名称                                       |
| hot    | float  | 省份热度（自定热度如何表示，如：该省出行人数） |
| max    | float  | 省份热度最大值                                 |

#### 景点热度


##### 简要描述

- 获取景点热度及其经纬度

##### 请求URL
- ` /api/spot_hot/ `
##### 请求方式
- GET


##### 返回示例 

``` json
{
    "error_code": 100,
    "data": [{
        "name": "洪崖洞",
        "longitude": 12.34,
        "latitude": 43.56,
        "hot": 123,
    }]
}
```

##### 返回参数说明 

| 参数名    | 类型   | 说明     |
| :-------- | :----- | -------- |
| name      | string | 景点名字 |
| longitude | float  | 景点经度 |
| latitude  | float  | 景点纬度 |
| hot       | float  | 景点热度 |

#### 城市人均消费


##### 简要描述

- 获取2019-2021年每个城市的每年人均消费

##### 请求URL

- ` /api/city_everypeolple_avg_cost/ `
##### 请求方式

- GET


##### 返回示例 

``` json
{
    "error_code": 100,
    "data": [{
        "year": 2020,
        "prov": [{
            "name": "重庆",
            "avg_cost": 123.55,
        }]
    }]
}
```

##### 返回参数说明 

| 参数名    | 类型   | 说明                                 |
| :-------- | :----- | ------------------------------------ |
| year      | int    | 年份                                 |
| prov_name | string | 省份名称                             |
| avg_cost  | float  | 每年这个省份的人均消费，保留两位小数 |

## 注意事项

- 请提交能通过编译的、经过充分测试的代码，至少自己手动测试一下。
- 请提交格式规范的代码，推荐使用IDE的自动格式化功能格式化代码。
- 提交信息请使用中文，描述一下本次提交实现了哪些功能。
- 已知的BUG和尚未实现的功能请使用FIXME和TODO标注。
- 代码请存放在对应的目录下，如爬虫存放在`spiders`目录下，服务器（包括后端和前端）存放在`server`目录下；提交时请在同名分支下提交。