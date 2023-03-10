import unittest
import pandas as pd
from .utils import load_datasets
from wildlife_datasets import datasets, splits

dataset_names = [
    datasets.IPanda50,
    datasets.MacaqueFaces,
]

tol = 0.1
dfs = load_datasets(dataset_names)

class TestTimeSplits(unittest.TestCase):
    def test_df(self):
        self.assertGreaterEqual(len(dfs), 1)
    
    def test_time_proportion(self):
        for df in dfs:
            if 'date' not in df.columns:
                self.assertRaises(Exception, splits.TimeProportionSplit, df)
            else:
                splitter = splits.TimeProportionSplit(df)
                idx_train, idx_test = splitter.split()
                df_train = df.loc[idx_train]
                df_test = df.loc[idx_test]

                split_type = splits.recognize_time_split(df_train, df_test)
                self.assertEqual(split_type, 'time-proportion')

    def test_time_cutoff(self):
        for df in dfs:
            if 'date' not in df.columns:
                self.assertRaises(Exception, splits.TimeCutoffSplit, df)
            else:
                years = pd.to_datetime(df['date']).apply(lambda x: x.year)
                splitter = splits.TimeCutoffSplit(df)
                idx_train, idx_test = splitter.split(max(years))
                df_train = df.loc[idx_train]
                df_test = df.loc[idx_test]

                split_type = splits.recognize_time_split(df_train, df_test)
                self.assertEqual(split_type, 'time-cutoff')
                
    def test_resplit_random(self):
        for df in dfs:
            if 'date' not in df.columns:
                self.assertRaises(Exception, splits.TimeProportionSplit, df)
            else:
                splitter = splits.TimeProportionSplit(df)
                idx_train1, idx_test1 = splitter.split()
                idx_train2, idx_test2 = splitter.resplit_random(idx_train1, idx_test1)
                
                df_train1 = df.loc[idx_train1]
                df_test1 = df.loc[idx_test1]
                df_train2 = df.loc[idx_train2]
                df_test2 = df.loc[idx_test2]

                self.assertEqual(set(df_train1['identity']), set(df_train2['identity']))
                self.assertEqual(set(df_test1['identity']), set(df_test2['identity']))
                for id in set(df_train1['identity']):
                    self.assertEqual(len(df_train1['identity']==id), len(df_train2['identity']==id))
                for id in set(df_test1['identity']):
                    self.assertEqual(len(df_test1['identity']==id), len(df_test2['identity']==id))


if __name__ == '__main__':
    unittest.main()
