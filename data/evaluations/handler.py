from data.const import PostType
from data.evaluations.metric_based import (
    post_type_by_category,
    refs_by_post_type
)
import sys

class EvaluationHandler:
    def __init__(self, df, content_index, s3_path):
        self.df = df
        self.content_index = content_index
        self.s3_path = s3_path
        self.eval_results = {}

    def check_metric(self, metric_result, category):
        if not metric_result == 1:
            post_type = post_type_by_category.get(category, PostType.DELAY)
            refs = refs_by_post_type.get(post_type, [])
            self.eval_results["eval_metric_rouge1_reason"] = f"문장에 {', '.join(refs)}가 포함되지 않았습니다."
            print(f"Fail (Metric keyword: {metric_result})")
            self._update_dataframe(self.eval_results)
            sys.exit(1)

    def check_qgqa_eval(self, date_comparison, line_comparison):
        if not date_comparison or not line_comparison:
            print(f"Fail (QGQA Eval): ", self.eval_results)
            self._update_dataframe(self.eval_results)
            sys.exit(1)

    def check_geval_eval(self, geval_results):
        # 임계값 사전 정의
        thresholds = {
            'Consistency': 5,  # Consistency는 4 이하가 문제
            'Human_Likeness': 3,
            'Coherence': 3,
            'Blog': 3,
            'Fluency': 3
        }
        failed_fields = {
            key: False
            for key, result in geval_results.items()
            if result['score'] < thresholds.get(key, 3)
        }
        print("Fields that did not meet the criteria:", failed_fields)

        if len(failed_fields):
            self.eval_results["eval_geval_failed_reason"] = f"{', '.join(failed_fields.keys())}"
            print(f"Fail (GEVAL Eval): ", self.failed_fields.keys())
            self._update_dataframe(self.eval_results)
            sys.exit(1)

    def _update_dataframe(self, eval_results):
        for key, value in eval_results.items():
            self.df.at[self.content_index, key] = value
        self.df.to_csv(self.s3_path, index=False)
        print(f"*** Data saved to {self.s3_path} ***")
