import os
configs = [
    "--config 'configs/baseline.py' ",

    "--config 'configs/img_seg.py' ", 
    "--config 'configs/img_full.py' ",

    "--config 'configs/augment_none.py' ",
    "--config 'configs/augment_basic.py' ",

    "--config 'configs/features_model_top.py' ",
    "--config 'configs/features_model_left.py' ",
    "--config 'configs/features_model_topleft.py' ",
    "--config 'configs/features_model_right.py' ",
    "--config 'configs/features_model_topright.py' ",
    "--config 'configs/features_onehot.py' ",

    "--config 'configs/train_full_lr03.py' ",
    "--config 'configs/train_full_lr04.py' ",
    "--config 'configs/train_only_last-lr04.py' ",
    "--config 'configs/train_only_last_lr03.py' ", 
    "--config 'configs/train_pretrain_lr03.py' ",
    "--config 'configs/train_pretrain_lr04.py' ",  

    "--config 'configs/sample_20.py' ", 
    "--config 'configs/sample_40.py' ", 
    "--config 'configs/sample_60.py' ", 
    "--config 'configs/sample_80.py' ", 

   ]

for c in configs:
    os.system(f"sbatch train.sh {c}")
