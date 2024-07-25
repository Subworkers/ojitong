from data.const import PostType
from data.evaluations.metric_based import (
    post_type_by_category,
    refs_by_post_type
***REMOVED***
import sys

class EvaluationHandler:
    def __init__(self, df, content_index, s3_path***REMOVED***:
        self.df = df
        self.content_index = content_index
        self.s3_path = s3_path
        self.eval_results = {***REMOVED***

    def check_metric(self, metric_result, category***REMOVED***:
        if not metric_result == 1:
            post_type = post_type_by_category.get(category, PostType.DELAY***REMOVED***
            refs = refs_by_post_type.get(post_type, [***REMOVED******REMOVED***
            self.eval_results["eval_metric_rouge1_reason"***REMOVED*** = f"문장에 {', '.join(refs***REMOVED******REMOVED***가 포함되지 않았습니다."
            print(f"Fail (Metric keyword: {metric_result***REMOVED******REMOVED***"***REMOVED***
            self._update_dataframe(self.eval_results***REMOVED***
            sys.exit(1***REMOVED***

    def check_qgqa_eval(self, date_comparison, line_comparison***REMOVED***:
        if not date_comparison or not line_comparison:
            print(f"Fail (QGQA Eval***REMOVED***: ", self.eval_results***REMOVED***
            self._update_dataframe(self.eval_results***REMOVED***
            sys.exit(1***REMOVED***

    def check_geval_eval(self, geval_results***REMOVED***:
        # 임계값 사전 정의
        thresholds = {
            'Consistency': 5,  # Consistency는 4 이하가 문제
            'Human_Likeness': 3,
            'Coherence': 3,
            'Blog': 3,
            'Fluency': 3
        ***REMOVED***
        failed_fields = {
            key: False
            for key, result in geval_results.items(***REMOVED***
            if result['score'***REMOVED*** < thresholds.get(key, 3***REMOVED***
        ***REMOVED***
        print("Fields that did not meet the criteria:", failed_fields***REMOVED***

        if len(failed_fields***REMOVED***:
            self.eval_results["eval_geval_failed_reason"***REMOVED*** = f"{', '.join(failed_fields.keys(***REMOVED******REMOVED******REMOVED***"
            print(f"Fail (GEVAL Eval***REMOVED***: ", self.failed_fields.keys(***REMOVED******REMOVED***
            self._update_dataframe(self.eval_results***REMOVED***
            sys.exit(1***REMOVED***

    def _update_dataframe(self, eval_results***REMOVED***:
        for key, value in eval_results.items(***REMOVED***:
            self.df.at[self.content_index, key***REMOVED*** = value
        self.df.to_csv(self.s3_path, index=False***REMOVED***
        print(f"*** Data saved to {self.s3_path***REMOVED*** ***"***REMOVED***
