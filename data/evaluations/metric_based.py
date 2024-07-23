from rouge_score import rouge_scorer
from data.const import PostType

# PostType에 따라 참조 키워드를 설정
refs_by_post_type = {
    PostType.TIMETABLE: ["시간표 변경 일시", "변경된 시간표", "변경 이유"],
    PostType.DELAY: ["지연/사고 일시", "지연/사고 노선"],
    PostType.STRIKE: ["파업 일시", "파업 노선", "파업 이유"],
    PostType.EXTENSION: ["연장 노선"],
}
post_type_by_category = {
    "지연": PostType.DELAY,
    "연착": PostType.DELAY,
    "사고": PostType.DELAY,
    "파업": PostType.STRIKE,
    "연장": PostType.EXTENSION,
    "시간표": PostType.TIMETABLE
}

def compute_rouge_recall_per_keyword(keywords, hypothesis):
    """각 키워드에 대해 ROUGE 재현율을 계산하고 그 평균을 반환합니다."""
    matches = sum(1 for keyword in keywords if keyword in hypothesis)
    rouge_recall = matches / len(keywords)
    return rouge_recall

def evaluate_post_metric_based(category, blog_post):
    # PostType을 기반으로 참조 키워드 설정
    post_type = post_type_by_category.get(category, PostType.DELAY)
    refs = refs_by_post_type.get(post_type, [])
    
    # ROUGE Recall 계산
    recall_score = compute_rouge_recall_per_keyword(refs, blog_post)
    print(f"{category} 범주에 대한 평균 ROUGE Recall 점수: {recall_score}")
    return recall_score