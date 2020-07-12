import pandas as pd

class CohortAnalyser:

    def __init__(self, target, cohort_type, cohort_range, date_range):
        self._target = target
        self._cohort_type= cohort_type
        self._cohort_range = cohort_range
        self._date_range = date_range

    def analyse(self, data):
        results = []

        df = pd.read_excel(f"storage/{data['token']}/data/{data['filename']}", sheet_name=1)

        # group data by cohort range (need `Sale Date`)
        if self._cohort_range == 'month':
            df['OrderPeriod'] = df['Sale Date'].apply(lambda x: x.strftime('%Y-%m'))

        else:
            raise ValueError(f'Unknown cohort range {self._cohort_range}')

        # group by cohort type (need `Client ID`)
        if self._cohort_type == 'JoinMonth':
            df = df.join(
                df.groupby(by='Client ID')['OrderPeriod'].min().rename('JoinMonth'),
                on='Client ID'
            )

        else:
            raise ValueError(f'Unknown cohort type {self._cohort_type}')

        # join groups  (needs `Item name`, Item Total`)
        cohorts = df.groupby(['JoinMonth', 'OrderPeriod']).aggregate({
                'Client ID': pd.Series.nunique,
                'Item name': pd.Series.count,
                'Item Total': pd.Series.sum
        }).rename(columns={
                'Client ID': 'TotalClients',
                'Item name': 'TotalOrders',
                'Item Total': 'Revenue'})

        # sorting
        cohorts = cohorts.join(
            cohorts.groupby(level=0).cumcount().rename('CohortPeriod')
        )

        # cohort size
        cohorts = cohorts.reset_index().join(
            cohorts.groupby(level=0)['TotalClients'].first().rename('CohortSize'),
            on='JoinMonth'
        )

        # retention
        cohorts['Retention'] = (cohorts['TotalClients'] / cohorts['CohortSize'] * 100).round()

        cohort_size_by_JoinMonth = cohorts.groupby('JoinMonth')['CohortSize'].first()

        results.append({
            "name": "graph.json",
            "title": "Приток пользователей",
            "x": cohort_size_by_JoinMonth.index.tolist(),
            "xlabel": "Дата первого посещения",
            "y": cohort_size_by_JoinMonth.values.tolist(),
            "ylabel": "Размер когорты"
        })

        return results
