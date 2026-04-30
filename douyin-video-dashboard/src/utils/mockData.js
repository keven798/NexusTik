// 抖音电商短视频数据模拟

export const generateMockVideoData = () => {
  const videos = [];
  const categories = ['服装', '美妆', '数码', '家居', '食品'];
  
  for (let i = 1; i <= 50; i++) {
    const playCount = Math.floor(Math.random() * 500000) + 10000;
    const likeCount = Math.floor(playCount * (Math.random() * 0.1 + 0.02));
    const commentCount = Math.floor(playCount * (Math.random() * 0.02 + 0.005));
    const shareCount = Math.floor(playCount * (Math.random() * 0.01 + 0.002));
    const favoriteCount = Math.floor(playCount * (Math.random() * 0.03 + 0.01));
    const cartClick = Math.floor(playCount * (Math.random() * 0.05 + 0.01));
    const orderCount = Math.floor(cartClick * (Math.random() * 0.3 + 0.1));
    
    videos.push({
      videoId: `DY${String(i).padStart(3, '0')}`,
      title: `视频标题 ${i} - ${categories[i % categories.length]}推荐`,
      category: categories[i % categories.length],
      publishDate: new Date(2024, Math.floor(Math.random() * 12), Math.floor(Math.random() * 28) + 1).toISOString().split('T')[0],
      playCount,
      likeCount,
      commentCount,
      shareCount,
      favoriteCount,
      cartClick,
      orderCount,
      conversionRate: ((orderCount / playCount) * 100).toFixed(2)
    });
  }
  
  return videos;
};

export const generateMockLiveData = () => {
  const lives = [];
  
  for (let i = 1; i <= 30; i++) {
    const duration = Math.floor(Math.random() * 180) + 60; // 60-240分钟
    const maxOnline = Math.floor(Math.random() * 5000) + 500;
    const avgOnline = Math.floor(maxOnline * 0.6);
    const gmv = Math.floor(Math.random() * 50000) + 5000;
    const orderCount = Math.floor(gmv / (Math.random() * 200 + 50));
    
    lives.push({
      liveId: `LIVE${String(i).padStart(3, '0')}`,
      title: `直播场次 ${i}`,
      startTime: new Date(2024, Math.floor(Math.random() * 12), Math.floor(Math.random() * 28) + 1, Math.floor(Math.random() * 12) + 8).toISOString(),
      duration,
      maxOnline,
      avgOnline,
      gmv,
      orderCount,
      avgOrderValue: (gmv / orderCount).toFixed(2),
      interactionRate: (Math.random() * 20 + 5).toFixed(2)
    });
  }
  
  return lives;
};

export const generateOverviewData = () => {
  return {
    totalPlayCount: 15800000,
    totalLikeCount: 850000,
    totalOrderCount: 12500,
    totalGMV: 2580000,
    avgConversionRate: 3.25,
    totalVideos: 156,
    totalLives: 45,
    growthRate: 15.8
  };
};

export const mockVideoData = generateMockVideoData();
export const mockLiveData = generateMockLiveData();
export const overviewData = generateOverviewData();
