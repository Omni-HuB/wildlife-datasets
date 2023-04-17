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
        splitter = splits.TimeProportionSplit()
        for df in dfs:
            if 'date' not in df.columns:
                splitter = splits.TimeProportionSplit()
                self.assertRaises(Exception, splitter.split, df)
            else:
                idx_train, idx_test = splitter.split(df)
                df_train = df.loc[idx_train]
                df_test = df.loc[idx_test]

                split_type = splits.recognize_time_split(df_train, df_test)
                self.assertEqual(split_type, 'time-proportion')

    def test_time_cutoff(self):
        for df in dfs:
            if 'date' not in df.columns:
                splitter = splits.TimeCutoffSplit(0)
                self.assertRaises(Exception, splitter.split, df)
            else:
                years = pd.to_datetime(df['date']).apply(lambda x: x.year)
                splitter = splits.TimeCutoffSplit(max(years))
                idx_train, idx_test = splitter.split(df)
                df_train = df.loc[idx_train]
                df_test = df.loc[idx_test]

                split_type = splits.recognize_time_split(df_train, df_test)
                self.assertEqual(split_type, 'time-cutoff')
                
    def test_resplit_random(self):
        for df in dfs:
            if 'date' not in df.columns:
                splitter = splits.TimeProportionSplit()
                self.assertRaises(Exception, splitter.split, df)
            else:
                splitter = splits.TimeProportionSplit()
                idx_train1, idx_test1 = splitter.split(df)
                idx_train2, idx_test2 = splitter.resplit_random(df, idx_train1, idx_test1)
                
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

