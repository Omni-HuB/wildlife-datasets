import os
import numpy as np
import datetime
from matplotlib import pyplot as plt
from PIL import Image

# Visualisation utils
def bbox_segmentation(bbox, theta=0):    
    segmentation = [bbox[0], bbox[1], bbox[0]+bbox[2], bbox[1], bbox[0]+bbox[2], bbox[1]+bbox[3], bbox[0], bbox[1]+bbox[3], bbox[0], bbox[1]]
    if theta != 0:
        rot_matrix = np.array([[np.cos(theta), np.sin(theta)], [-np.sin(theta), np.cos(theta)]])
        center = np.array([bbox[0]+bbox[2]/2, bbox[1]+bbox[3]/2])
        segmentation = (np.reshape(segmentation, (-1,2)) - center) @ rot_matrix + center
        segmentation = np.reshape(segmentation, (segmentation.size,))
        segmentation = list(segmentation)
    return segmentation

def segmentation_bbox(segmentation):
    x = segmentation[0::2]
    y = segmentation[1::2]
    x_min = np.min(x)
    x_max = np.max(x)
    y_min = np.min(y)
    y_max = np.max(y)
    return [x_min, y_min, x_max-x_min, y_max-y_min]

def is_annotation_bbox(ann, bbox, theta=0, tol=0):
    bbox_ann = bbox_segmentation(bbox, theta)
    if len(ann) == len(bbox_ann):
        for x, y in zip(ann, bbox_ann):
            if abs(x-y) > tol:
                return False
    else:
        return False
    return True

def plot_image(img):
    fig, ax = plt.subplots()
    ax.imshow(img)
    plt.show()

def plot_segmentation(img, segmentation):
    if not np.isnan(segmentation).all():
        fig, ax = plt.subplots()
        ax.imshow(img)
        ax.plot(segmentation[0::2], segmentation[1::2], '--', linewidth=5, color='firebrick')
        plt.show()

def plot_bbox_segmentation(df, root, n):
    if 'bbox' not in df.columns and 'segmentation' not in df.columns:
        for i in range(n):
            img = Image.open(os.path.join(root, df['path'][i]))
            plot_image(img)
    if 'bbox' in df.columns:
        df_red = df[~df['bbox'].isnull()]
        if 'bbox_theta' in df.columns:
            df_red1 = df_red[df_red['bbox_theta'] != 0]
            for i in range(n):
                img = Image.open(os.path.join(root, df_red1['path'].iloc[i]))
                segmentation = bbox_segmentation(df_red1['bbox'].iloc[i], df_red1['bbox_theta'].iloc[i])
                plot_segmentation(img, segmentation)

            df_red2 = df_red[df_red['bbox_theta'] == 0]
            for i in range(n):
                img = Image.open(os.path.join(root, df_red2['path'].iloc[i]))
                segmentation = bbox_segmentation(df_red2['bbox'].iloc[i], df_red2['bbox_theta'].iloc[i])
                plot_segmentation(img, segmentation)
        else:
            for i in range(n):
                img = Image.open(os.path.join(root, df_red['path'].iloc[i]))
                segmentation = bbox_segmentation(df_red['bbox'].iloc[i])
                plot_segmentation(img, segmentation)
    if 'segmentation' in df.columns:
        df_red = df[~df['segmentation'].isnull()]
        for i in range(n):
            segmentation = df_red['segmentation'].iloc[i]
            if type(segmentation) == str:
                img = Image.open(os.path.join(root, df_red['path'].iloc[i]))
                plot_image(img)
                img = Image.open(os.path.join(root, segmentation))
                plot_image(img)
            else:
                img = Image.open(os.path.join(root, df_red['path'].iloc[i]))
                segmentation = df_red['segmentation'].iloc[i]
                plot_segmentation(img, segmentation)

def plot_grid(df, root, n_rows=5, n_cols=8, offset=10, img_min=100, rotate=True):
    idx = np.random.permutation(len(df))[:n_rows*n_cols]

    ratios = []
    for k in idx:
        file_path = os.path.join(root, df['path'][k])
        im = Image.open(file_path)
        ratios.append(im.size[0] / im.size[1])

    ratio = np.median(ratios)
    if ratio > 1:    
        img_w, img_h = int(img_min*ratio), int(img_min)
    else:
        img_w, img_h = int(img_min), int(img_min/ratio)

    im_grid = Image.new('RGB', (n_cols*img_w + (n_cols-1)*offset, n_rows*img_h + (n_rows-1)*offset))

    for i in range(n_rows):
        for j in range(n_cols):
            k = n_cols*i + j
            file_path = os.path.join(root, df['path'][idx[k]])

            im = Image.open(file_path)
            if rotate and ((ratio > 1 and im.size[0] < im.size[1]) or (ratio < 1 and im.size[0] > im.size[1])):
                im = im.transpose(Image.ROTATE_90)
            im.thumbnail((img_w,img_h))

            pos_x = j*img_w + j*offset
            pos_y = i*img_h + i*offset        
            im_grid.paste(im, (pos_x,pos_y))
    display(im_grid) # TODO: remove display

def display_statistics(df, root, plot_images=True, display_dataframe=True, n=2):
    df_red = df.loc[df['identity'] != 'unknown', 'identity']
    df_red.value_counts().reset_index(drop=True).plot()
        
    if 'unknown' in list(df['identity'].unique()):
        n_identity = len(df.identity.unique()) - 1
    else:
        n_identity = len(df.identity.unique())
    print(f"Number of identitites          {n_identity}")
    print(f"Number of all animals          {len(df)}")
    print(f"Number of identified animals   {sum(df['identity'] != 'unknown')}")    
    print(f"Number of unidentified animals {sum(df['identity'] == 'unknown')}")
    if 'video' in df.columns:
        print(f"Number of videos               {len(df[['identity', 'video']].drop_duplicates())}")
    if 'date' in df.columns:
        span_years = compute_span(df) / (60*60*24*365.25)
        if span_years > 1:
            print(f"Images span                    %1.1f years" % (span_years))
        elif span_years / 12 > 1:
            print(f"Images span                    %1.1f months" % (span_years * 12))
        else:
            print(f"Images span                    %1.0f days" % (span_years * 365.25))
    if plot_images:
        plot_bbox_segmentation(df, root, n)
        plot_grid(df, root)
    if display_dataframe:
        display(df)  # TODO: remove display

def get_dates(dates, frmt):
    return np.array([datetime.datetime.strptime(date, frmt) for date in dates])

def compute_span(df):
    df = df.loc[~df['date'].isnull()]
    dates = get_dates(df['date'].str[:10], '%Y-%m-%d')
    identities = df['identity'].unique()
    span = -np.inf
    for identity in identities:
        idx = df['identity'] == identity
        span = np.maximum(span, (max(dates[idx]) - min(dates[idx])).total_seconds())    
    return span