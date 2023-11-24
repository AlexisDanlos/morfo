import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pandas import DataFrame
import random, boto3
from botocore.exceptions import NoCredentialsError
import io

def upload_to_s3(local_file, bucket, s3_path):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(local_file, bucket, s3_path)
        print(f"File uploaded to {bucket}/{s3_path}")
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials not available")

def generate_images():
    images = []

    for i in range(5):
        batch = []
        for j in range(5):
            image = np.random.randint(0, 255, size=(256, 512, 3), dtype=np.uint8)
            batch.append(image)
        images.append(batch)

    return images

def check_overlap(x1, y1, x2, y2, x3, y3, x4, y4):
    if (x1 > x4 or x3 > x2):
        return False
    if (y1 > y4 or y3 > y2):
        return False
    return True

def generate_squares(images):
    for i in range(5):
        for j in range(5):
            x1 = random.randint(0, 412)
            y1 = random.randint(0, 156)
            x2 = x1 + 100
            y2 = y1 + 100
            x3 = random.randint(0, 412)
            y3 = random.randint(0, 156)
            x4 = x3 + 100
            y4 = y3 + 100
            while check_overlap(x1, y1, x2, y2, x3, y3, x4, y4):
                x1 = random.randint(0, 412)
                y1 = random.randint(0, 156)
                x2 = x1 + 100
                y2 = y1 + 100
                x3 = random.randint(0, 412)
                y3 = random.randint(0, 156)
                x4 = x3 + 100
                y4 = y3 + 100
            images[i][j][y1:y2, x1:x2] = [255, 255, 255]
            images[i][j][y3:y4, x3:x4] = [0, 0, 0]

def random_crop(images):
    for i in range(5):
        for j in range(5):
            x1 = random.randint(0, 312)
            y1 = random.randint(0, 56)
            x2 = x1 + 200
            y2 = y1 + 200
            images[i][j] = images[i][j][y1:y2, x1:x2]

def calculate_average(images):
    black_std = [0 for i in range(len(images))]
    white_std = [0 for i in range(len(images))]
    black_average = [[] for i in range(len(images))]
    white_average = [[] for i in range(len(images))]

    for i in range(len(images)):
        for j in range(len(images[i])):
            black_average[i].append(np.mean(images[i][j] == [0, 0, 0]))
            black_std[i] += np.std(images[i][j] == [0, 0, 0])
            white_average[i].append(np.mean(images[i][j] == [255, 255, 255]))
            white_std[i] += np.std(images[i][j] == [255, 255, 255])
        black_std[i] /= 5
        white_std[i] /= 5
    for i in range(len(black_average)):
        black_average[i] = np.mean(black_average[i])
        white_average[i] = np.mean(white_average[i])
    return white_average, white_std, black_average, black_std

def store_data(white_average, white_std, black_average, black_std):
    batch_ids = [f'batch_{i}' for i in range(5)]
    df = DataFrame({'batch_id': batch_ids, 'white_avg': white_average, 'white_std': white_std, 'black_avg': black_average, 'black_std': black_std})
    buffer = io.BytesIO()
    df.to_parquet(buffer, index=False)
    upload_to_s3(buffer, 'raw', 'test/test.parquet')

if __name__ == "__main__":
    images = generate_images()
    generate_squares(images)
    random_crop(images)
    calculate_average(images)
    white_average, white_std, black_average, black_std = calculate_average(images)
    store_data(white_average, white_std, black_average, black_std)

    # show images
    # fig, axs = plt.subplots(5, 5)
    # for i in range(5):
    #     for j in range(5):
    #         axs[i, j].imshow(images[i][j])
    #         axs[i, j].axis('off')
    # plt.show()