#!/bin/usr/python
# 先通过相似度判定两个人的相似度大小，然后用每个人对物品的不同评价与其相似度的乘积，作为对物品的整体评价；
# 同时为了修正单一物品被过多评价而给整体产生的影响，通过除以所有对该物品有过评价的评论者的相似度之和。

#  A dictionary of movie critics and their ratings of a small set of movies
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 3.5},
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0,
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

from math import sqrt
from math import pow


# 使用欧几里得距离公司判断两个人的相似度大小
def euclidean_distance(prefs,person1,person2):
    si = {}
    # 获取相同的分享列表
    for item in prefs[person1]:
      if item in prefs[person2]:
        si[item] = 1

    # 列表为空时，无相同兴趣
    if len(si) == 0: return 0

    # 计算所有插值的平方和
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item],2) for item in prefs[person1] if item in prefs[person2]])
    # 欧几里得距离评价：无法修正夸大分值的情况
    # EuclideanDistance = sqrt(sum_of_squares)
    return 1/(1 + sqrt(sum_of_squares))

# 通过皮尔逊相关系数判断两个人的相似度大小
def pearson_correlation(prefs,person1,person2):
    si = {}
    # 获取相同的分享列表
    for item in prefs[person1]:
      if item in prefs[person2]:
        si[item] = 1

    n = len(si)
    # 没有共同之处，则返回0
    if n == 0:return 1

    # 所有偏好之和
    sum1 = sum([prefs[person1][item] for item in si])
    sum2 = sum([prefs[person2][item] for item in si])

    # 平方和
    sum1Sq = sum([pow(prefs[person1][item],2) for item in si])
    sum2Sq = sum([pow(prefs[person2][item],2) for item in si])

    # 乘积之和
    pSum = sum([prefs[person1][item] * prefs[person2][item] for item in si])

    # 计算皮尔逊评价值
    num = pSum -(sum1 * sum2/n)
    den = sqrt((sum1Sq - pow(sum1,2)/n) * (sum2Sq - pow(sum2,2)/n))
    if den == 0: return 0
    r = num /den
    return r

# 找出相似偏好的朋友，并对其按照相似性大小进行排名
# 从反映偏好的字典中返回最为匹配者，返回结果的个数和相似度函数均为可选参数
def topMatches(prefs,pseron,n=5,similarityMetric=pearson_correlation):
    scores = [(similarityMetric(prefs,pseron,other),other) for other in prefs if other != pseron]
    scores.sort()
    scores.reverse()
    return scores[0:n]

# 为某人推荐物品
def getRecommendations(prefs,person,similarityMetric=pearson_correlation):
    totals = {}
    simSums = {}

    for other in prefs:
      # 不和自己比较
      if other == person: continue
      sim = similarityMetric(prefs,person,other)

      # 忽略评价值为零或小于零的情况
      if sim <= 0: continue
      for item in prefs[other]:
        # 只对自己还未曾看过的电影进行评价处理
        if item not in prefs[person] or prefs[person][item] == 0:
          # 相似度 * 评价值
          totals.setdefault(item,0)
          totals[item] += prefs[other][item] * sim
          # 相似度之和
          simSums.setdefault(item,0)
          simSums[item] += sim

    # 建立归一化的列表
    rankings = [(total/simSums[item],item) for item,total in totals.items()]

    # 对返回结果进行排序
    rankings.sort()
    rankings.reverse()
    return rankings

# 将物品与人员对调
def transformPrefs(prefs):
  result ={}
  for person in prefs:
    for item in prefs[person]:
      result.setdefault(item,{})
      result[item][person] = prefs[person][item]
  return result


# 构造物品比较数据集
def calculateSimilarItems(prefs,n=10):
    # 建立字典，以给出与这些物品最为相近的所有其他物品
    result = {}

    # 以物品为中心对偏好矩阵进行倒置处理
    itemPrefs = transformPrefs(prefs)
    c = 0
    for item in itemPrefs:
    # 针对大数据集更新状态变量
      c += 1
      if c % 100 == 0:print("%d / %d" % (c,len(itemPrefs)))

      # 寻找最为相近的物品
      scores = topMatches(itemPrefs,item,n=n,similarityMetric=euclidean_distance)
      result[item] = scores
    return result

# 获得推荐
def getRecommendedItems(prefs,itemMatch,user):
    userRating = prefs[user]
    scores = {}
    totalSim = {}

    # 循环遍历与当前物品相似的物品
    for item,rating in userRating.items():
       # 循环遍历与当前物品相似的商品
      for similarity,item2 in itemMatch[item]:
        # 如果该用户已经对当前物品做过评价，则将其忽略
        if item2 in userRating:continue

        # 评价值与相似度的加权之和
        scores.setdefault(item2,0)
        scores[item2] += similarity * rating

        # 全部相似度之和
        totalSim.setdefault(item2,0)
        totalSim[item2] +=similarity

    # 将每个合计值除以加权和，求出平均值
    ranking = [(score/totalSim[item],item) for item,score in scores.items()]

    # 按最高值到最低值的顺序，返回结果
    ranking.sort()
    ranking.reverse()
    return ranking

# 基于物品的协作过滤和基于用户的协作过滤
# 在拥有大量数据集的情况下，基于物品的协作过滤能够得出更好的结论
# 而且允许将大量计算任务预先执行
if __name__ == '__main__':

  # 寻找相同爱好的评价者
  # print(topMatches(critics,"Toby"))
  # 为指定评价者推荐影片
  # print(getRecommendations(critics,"Toby"))
  # 人和物对调
  # result = transformPrefs(critics)
  # 反向寻找相同类型的影片
  # print(topMatches(result,"Superman Returns"))
  # 为影片推荐相似爱好的评论者
  # print(getRecommendations(result,"Just My Luck"))

  # 基于物品的协作过滤
  result =calculateSimilarItems(critics)
  print(result)
  # print(getRecommendedItems(critics,result,'Toby'))


