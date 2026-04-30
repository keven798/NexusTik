import React, { useState, useEffect } from 'react';
import ReactECharts from 'echarts-for-react';
import { mockVideoData, mockLiveData, overviewData } from './utils/mockData';

function App() {
  const [activeTab, setActiveTab] = useState('overview');
  const [videoData, setVideoData] = useState(mockVideoData);
  const [liveData, setLiveData] = useState(mockLiveData);

  // 格式化数字
  const formatNumber = (num) => {
    if (num >= 10000) {
      return (num / 10000).toFixed(1) + '万';
    }
    return num.toLocaleString();
  };

  // 概览卡片组件
  const OverviewCard = ({ title, value, subtitle, icon, color }) => (
    <div className="douyin-card neon-glow">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-douyin-textSecondary text-sm mb-1">{title}</p>
          <h3 className="text-2xl font-bold gradient-text">{value}</h3>
          <p className="text-douyin-textSecondary text-xs mt-1">{subtitle}</p>
        </div>
        <div className="text-3xl" style={{ color }}>{icon}</div>
      </div>
    </div>
  );

  // 销售趋势图配置
  const getTrendOption = () => {
    const dates = [...new Set(videoData.map(v => v.publishDate))].sort();
    const dailyData = dates.map(date => {
      const dayVideos = videoData.filter(v => v.publishDate === date);
      return {
        date,
        plays: dayVideos.reduce((sum, v) => sum + v.playCount, 0),
        orders: dayVideos.reduce((sum, v) => sum + v.orderCount, 0)
      };
    });

    return {
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'axis',
        backgroundColor: '#161823',
        borderColor: '#FE2C55',
        textStyle: { color: '#fff' }
      },
      legend: {
        data: ['播放量', '成交单数'],
        textStyle: { color: '#fff' }
      },
      grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
      xAxis: {
        type: 'category',
        data: dailyData.map(d => d.date),
        axisLine: { lineStyle: { color: '#8A8B91' } },
        axisLabel: { color: '#8A8B91' }
      },
      yAxis: [
        {
          type: 'value',
          name: '播放量',
          axisLine: { lineStyle: { color: '#25F4EE' } },
          axisLabel: { color: '#25F4EE' },
          splitLine: { lineStyle: { color: '#1F1F1F' } }
        },
        {
          type: 'value',
          name: '成交单数',
          axisLine: { lineStyle: { color: '#FE2C55' } },
          axisLabel: { color: '#FE2C55' },
          splitLine: { show: false }
        }
      ],
      series: [
        {
          name: '播放量',
          type: 'line',
          data: dailyData.map(d => d.plays),
          smooth: true,
          lineStyle: { color: '#25F4EE', width: 3 },
          itemStyle: { color: '#25F4EE' },
          areaStyle: {
            color: {
              type: 'linear',
              x: 0, y: 0, x2: 0, y2: 1,
              colorStops: [
                { offset: 0, color: 'rgba(37, 244, 238, 0.3)' },
                { offset: 1, color: 'rgba(37, 244, 238, 0.05)' }
              ]
            }
          }
        },
        {
          name: '成交单数',
          type: 'bar',
          yAxisIndex: 1,
          data: dailyData.map(d => d.orders),
          itemStyle: {
            color: {
              type: 'linear',
              x: 0, y: 0, x2: 0, y2: 1,
              colorStops: [
                { offset: 0, color: '#FE2C55' },
                { offset: 1, color: '#ff6b8a' }
              ]
            }
          }
        }
      ]
    };
  };

  // 类别分布图配置
  const getCategoryOption = () => {
    const categoryData = {};
    videoData.forEach(v => {
      if (!categoryData[v.category]) {
        categoryData[v.category] = { plays: 0, orders: 0 };
      }
      categoryData[v.category].plays += v.playCount;
      categoryData[v.category].orders += v.orderCount;
    });

    return {
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'item',
        backgroundColor: '#161823',
        borderColor: '#FE2C55',
        textStyle: { color: '#fff' }
      },
      legend: {
        orient: 'vertical',
        right: '10%',
        textStyle: { color: '#fff' }
      },
      series: [
        {
          name: '播放量分布',
          type: 'pie',
          radius: ['40%', '70%'],
          center: ['40%', '50%'],
          data: Object.entries(categoryData).map(([name, data]) => ({
            name,
            value: data.plays
          })),
          itemStyle: {
            borderRadius: 8,
            borderColor: '#000',
            borderWidth: 2
          },
          label: {
            color: '#fff'
          }
        }
      ]
    };
  };

  // 直播数据图配置
  const getLiveOption = () => {
    const sortedLives = [...liveData].sort((a, b) => b.gmv - a.gmv).slice(0, 10);

    return {
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'axis',
        backgroundColor: '#161823',
        borderColor: '#FE2C55',
        textStyle: { color: '#fff' }
      },
      grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
      xAxis: {
        type: 'value',
        axisLine: { lineStyle: { color: '#8A8B91' } },
        axisLabel: { color: '#8A8B91' },
        splitLine: { lineStyle: { color: '#1F1F1F' } }
      },
      yAxis: {
        type: 'category',
        data: sortedLives.map(l => l.title).reverse(),
        axisLine: { lineStyle: { color: '#8A8B91' } },
        axisLabel: { color: '#fff' }
      },
      series: [
        {
          name: 'GMV',
          type: 'bar',
          data: sortedLives.map(l => l.gmv).reverse(),
          itemStyle: {
            color: {
              type: 'linear',
              x: 0, y: 0, x2: 1, y2: 0,
              colorStops: [
                { offset: 0, color: '#25F4EE' },
                { offset: 1, color: '#FE2C55' }
              ]
            }
          }
        }
      ]
    };
  };

  return (
    <div className="min-h-screen bg-black">
      {/* 头部导航 */}
      <header className="bg-douyin-darkGray border-b border-douyin-primary/20 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-douyin-primary to-douyin-secondary flex items-center justify-center">
                <span className="text-white font-bold text-lg">抖</span>
              </div>
              <div>
                <h1 className="text-xl font-bold gradient-text">抖音电商数据分析</h1>
                <p className="text-xs text-douyin-textSecondary">短视频与直播数据可视化平台</p>
              </div>
            </div>
            
            <nav className="flex space-x-1">
              {[
                { id: 'overview', label: '数据概览', icon: '📊' },
                { id: 'videos', label: '视频分析', icon: '🎬' },
                { id: 'lives', label: '直播分析', icon: '📺' }
              ].map(tab => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`px-4 py-2 rounded-lg flex items-center space-x-2 transition-all ${
                    activeTab === tab.id
                      ? 'bg-douyin-primary text-white neon-glow'
                      : 'text-douyin-textSecondary hover:text-white hover:bg-douyin-lightGray'
                  }`}
                >
                  <span>{tab.icon}</span>
                  <span>{tab.label}</span>
                </button>
              ))}
            </nav>
          </div>
        </div>
      </header>

      {/* 主内容区 */}
      <main className="max-w-7xl mx-auto px-4 py-6">
        {activeTab === 'overview' && (
          <div className="space-y-6 animate-slide-in">
            {/* KPI 概览 */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <OverviewCard
                title="总播放量"
                value={formatNumber(overviewData.totalPlayCount)}
                subtitle="较上月 +15.8%"
                icon="▶️"
                color="#25F4EE"
              />
              <OverviewCard
                title="总点赞数"
                value={formatNumber(overviewData.totalLikeCount)}
                subtitle="较上月 +12.3%"
                icon="❤️"
                color="#FE2C55"
              />
              <OverviewCard
                title="成交订单"
                value={formatNumber(overviewData.totalOrderCount)}
                subtitle="转化率 3.25%"
                icon="🛒"
                color="#FFD700"
              />
              <OverviewCard
                title="总GMV"
                value={`¥${formatNumber(overviewData.totalGMV)}`}
                subtitle="客单价 ¥206"
                icon="💰"
                color="#00FF88"
              />
            </div>

            {/* 图表区域 */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2 douyin-card">
                <h3 className="text-lg font-semibold mb-4 gradient-text">📈 播放与成交趋势</h3>
                <ReactECharts option={getTrendOption()} style={{ height: '350px' }} />
              </div>
              
              <div className="douyin-card">
                <h3 className="text-lg font-semibold mb-4 gradient-text">🥧 内容类别分布</h3>
                <ReactECharts option={getCategoryOption()} style={{ height: '350px' }} />
              </div>
            </div>

            {/* 直播数据 */}
            <div className="douyin-card">
              <h3 className="text-lg font-semibold mb-4 gradient-text">📺 直播GMV排行 TOP 10</h3>
              <ReactECharts option={getLiveOption()} style={{ height: '400px' }} />
            </div>
          </div>
        )}

        {activeTab === 'videos' && (
          <div className="space-y-6 animate-slide-in">
            <div className="douyin-card">
              <h3 className="text-lg font-semibold mb-4 gradient-text">🎬 视频数据明细</h3>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-douyin-primary/20">
                      <th className="text-left py-3 px-4 text-douyin-textSecondary">视频ID</th>
                      <th className="text-left py-3 px-4 text-douyin-textSecondary">标题</th>
                      <th className="text-right py-3 px-4 text-douyin-textSecondary">播放量</th>
                      <th className="text-right py-3 px-4 text-douyin-textSecondary">点赞</th>
                      <th className="text-right py-3 px-4 text-douyin-textSecondary">成交</th>
                      <th className="text-right py-3 px-4 text-douyin-textSecondary">转化率</th>
                    </tr>
                  </thead>
                  <tbody>
                    {videoData.slice(0, 10).map((video, index) => (
                      <tr key={video.videoId} className="border-b border-douyin-lightGray/50 hover:bg-douyin-lightGray/30">
                        <td className="py-3 px-4 text-douyin-secondary">{video.videoId}</td>
                        <td className="py-3 px-4">{video.title}</td>
                        <td className="py-3 px-4 text-right">{formatNumber(video.playCount)}</td>
                        <td className="py-3 px-4 text-right text-douyin-primary">{formatNumber(video.likeCount)}</td>
                        <td className="py-3 px-4 text-right">{video.orderCount}</td>
                        <td className="py-3 px-4 text-right">
                          <span className={`px-2 py-1 rounded text-xs ${
                            parseFloat(video.conversionRate) > 3 
                              ? 'bg-green-500/20 text-green-400' 
                              : 'bg-yellow-500/20 text-yellow-400'
                          }`}>
                            {video.conversionRate}%
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'lives' && (
          <div className="space-y-6 animate-slide-in">
            <div className="douyin-card">
              <h3 className="text-lg font-semibold mb-4 gradient-text">📺 直播数据明细</h3>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-douyin-primary/20">
                      <th className="text-left py-3 px-4 text-douyin-textSecondary">直播ID</th>
                      <th className="text-left py-3 px-4 text-douyin-textSecondary">标题</th>
                      <th className="text-right py-3 px-4 text-douyin-textSecondary">时长(分)</th>
                      <th className="text-right py-3 px-4 text-douyin-textSecondary">峰值在线</th>
                      <th className="text-right py-3 px-4 text-douyin-textSecondary">GMV</th>
                      <th className="text-right py-3 px-4 text-douyin-textSecondary">订单数</th>
                    </tr>
                  </thead>
                  <tbody>
                    {liveData.slice(0, 10).map((live) => (
                      <tr key={live.liveId} className="border-b border-douyin-lightGray/50 hover:bg-douyin-lightGray/30">
                        <td className="py-3 px-4 text-douyin-secondary">{live.liveId}</td>
                        <td className="py-3 px-4">{live.title}</td>
                        <td className="py-3 px-4 text-right">{live.duration}</td>
                        <td className="py-3 px-4 text-right">{formatNumber(live.maxOnline)}</td>
                        <td className="py-3 px-4 text-right text-douyin-primary">¥{formatNumber(live.gmv)}</td>
                        <td className="py-3 px-4 text-right">{live.orderCount}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
