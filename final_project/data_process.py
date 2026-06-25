# data_process.py
import pandas as pd
import numpy as np
import random

def generate_data():
    cities = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '南京']
    categories = ['咖啡店', '奶茶店', '火锅店', '便利店', '电影院', '健身房']

    comments_pool = [
        '环境很好', '服务态度差', '价格实惠', '位置偏僻', 
        '口味一般', '强烈推荐', '卫生堪忧', '性价比高', 
        '非常喜欢', '再也不来了', '氛围不错', '停车方便'
    ]
    

    city_sentiment_bias = {
        '北京': -0.05, '上海': 0.1,  '广州': 0.15, '深圳': 0.05,
        '杭州': 0.2,   '成都': 0.25, '武汉': -0.1, '南京': 0.0
    }
    
    data = []
    for _ in range(1000):
        city = random.choice(cities)
        

        lat_base = {'北京': 39.9, '上海': 31.2, '广州': 23.1, '深圳': 22.5, '杭州': 30.2, '成都': 30.6, '武汉': 30.5, '南京': 32.0}
        lng_base = {'北京': 116.4, '上海': 121.4, '广州': 113.2, '深圳': 114.0, '杭州': 120.1, '成都': 104.0, '武汉': 114.3, '南京': 118.7}
        
        lat = lat_base[city] + np.random.normal(0, 0.2)
        lng = lng_base[city] + np.random.normal(0, 0.2)
        category = random.choice(categories)
        rating = round(random.uniform(3.0, 5.0), 1)
        comment = random.choice(comments_pool)
        
        data.append({
            'name': f"{city}{category}{random.randint(1,100)}店",
            'city': city,
            'category': category,
            'latitude': lat,
            'longitude': lng,
            'rating': rating,
            'comment': comment
        })
    return pd.DataFrame(data)

def preprocess_data(df):
    df = df.dropna()
    
 
    city_bias = {
        '北京': 0.05, '上海': 0.15, '广州': 0.2, '深圳': 0.1,
        '杭州': 0.25, '成都': 0.3, '武汉': 0.0, '南京': 0.1
    }
    
    def get_sentiment_simple(city, text):
        base_score = 0.5 
        good_words = ['好', '推荐', '实惠', '方便', '喜欢', '不错', '棒']
        bad_words = ['差', '贵', '偏僻', '堪忧', '再也不来', '差评']
        
        for word in good_words:
            if word in text:
                base_score += 0.2
                break 
        for word in bad_words:
            if word in text:
                base_score -= 0.2
                break 
        
 
        base_score += city_bias.get(city, 0)
        

        final_score = base_score + random.uniform(-0.05, 0.05)
        return round(max(0, min(1, final_score)), 3)
    
    df['sentiment_score'] = df.apply(lambda row: get_sentiment_simple(row['city'], row['comment']), axis=1)
    
    return df