# Micro-learning
짧은 교육영상 컨텐츠를 서로 연결해주는 공간

## What is Microlearning?
**Microlearning**, characterized by brief, focused learning sessions typically lasting between 2 to 10 minutes, has garnered attention for its effectiveness in enhancing learner engagement and knowledge retention. Several studies have explored the impact of microlearning on educational outcomes:
    - Learner Satisfaction and Effectiveness: Research indicates that microlearning can improve student motivation by offering self-paced, accessible learning opportunities.
    - Learning Outcomes and Self-Efficacy: A study focusing on nursing students found that microlearning effectively enhanced learning outcomes and self-efficacy, particularly during internships.
    - Cognitive Load and Performance: Microlearning modules have been shown to reduce cognitive load, thereby improving knowledge retention, engagement, and overall learning outcomes.

Microlearning is a valuable educational strategy, offering concise and targeted content that aligns with learners' attention spans and cognitive capacities.

# How to get started
```
docker-compose up -build
```

## Background
스마트 교육 콘텐츠 시장의 급격한 성장 중임. YouTube와 같은 비디오 공유 플랫폼 등장은 K-MOOC와 같은 전문 온라인 플랫폼과 다르게 학습자게에 자율적으고 다양한 교육의 기회를 제공하고 있음. 

 - 교육 소외계층(저소득층 등)에게 다양한 교육기회를 제공하는 유연하고 자유로운 지식 공유 및 교육 매체
 - 학습자들이 자율적인 속도로 학습하고 사회적으로 참여가능
 - 개방적 사회적 특성으로 인해, 주제, 형식, 범위 측면에서 높은 다양성

## Limitation
하지만, 학습자는 교육영상을 검색, 필터링, 조직화하는데 상당한 지식이 필요함
- 제공되는 정보를 효과적으로 활용하기 위해서는 정작 자신에게 없는 해당 분야의 지식이 요구됨

# Create a file .env 
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=datasciencelabs

YOUTUBE_API_KEY= [YOUR_API_KEY]



