import pandas as pd
import json
from util.redis_connector import RedisConnection

class SpecificAnalytics:

    DISCUSSION_GROUP_CACHE_PREFIX = "discussion_group:"
    INITIAL_DISCUSSION_GROUP_METRICS = {'num_followers': 1, 'num_threads': 0}

    def __init__(self):
        self.k = None

    def store_discussion_group_metrics(self, id):
        redis_connection = RedisConnection.get_connection()
        value = SpecificAnalytics.INITIAL_DISCUSSION_GROUP_METRICS
        redis_connection.hmset(SpecificAnalytics.DISCUSSION_GROUP_CACHE_PREFIX + str(id), value)

    def getDiscussionGroupsMetrics(self, discussion_groups):
        discussion_groups = pd.DataFrame(discussion_groups, columns=['id', 'name', 'description', 'university_name'])
        redis_connection = RedisConnection.get_connection()
        relevant_keys = SpecificAnalytics.compose_discussion_group_cache_keys(discussion_groups['id'])

        redis_pipeline = RedisConnection.get_pipeline(redis_connection)

        for _ in relevant_keys:
            redis_pipeline.hgetall(_)

        values = redis_pipeline.execute()

        core_values = [_ if (_ is not None) else SpecificAnalytics.INITIAL_DISCUSSION_GROUP_METRICS for _ in values]

        metrics_df = pd.DataFrame(core_values)
        discussion_groups_metrics = pd.concat([discussion_groups, metrics_df], axis=1)

        return discussion_groups_metrics.to_dict('records')

    @classmethod
    def compose_discussion_group_cache_keys(cls, group_ids):
        cache_keys = [(SpecificAnalytics.DISCUSSION_GROUP_CACHE_PREFIX + str(_)) for _ in group_ids]
        return cache_keys