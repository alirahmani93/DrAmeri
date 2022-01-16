import datetime
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from cv2 import cv2
# from tensorflow.keras.preprocessing import image_dataset_from_directory
# from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
# from tensorflow.keras.preprocessing import image

from app.models import Output

u = datetime.datetime.timestamp(datetime.datetime.now())


def DETECTING(SourceInputImageDir, M_WindowShape, C_WindowShape):
    z = 0
    t = datetime.datetime.now()

    # print("t1",t)
    z = t

    M_NetDir = 'app/CNN.h5'
    C_NetDir = 'app/CNN.h5'
    ResultDir_C = 'output'
    TemplatePachDir = 'temp'
    ResultDir_M = 'output'
    ResultDir_M_C = 'output'

    imtest = cv2.imread(SourceInputImageDir, 1)
    model = keras.models.load_model(M_NetDir)
    d = imtest[:, :, 1]
    [a, b] = d.shape
    d = imtest
    ZeroPachesNumber = 0
    NonZeroPachesNumber = 0
    k = 0
    WindowShape = M_WindowShape
    M = np.int(a / WindowShape)
    N = np.int(b / WindowShape)
    M_M = M
    N_M = N
    PatchPosition_M = np.zeros((M, N))
    # print("t2",t)
    z += t - z
    for i in range(M):
        for j in range(N):
            CNNFeedPic = d[i * WindowShape:i * WindowShape + WindowShape, j * WindowShape:j * WindowShape + WindowShape]
            p = CNNFeedPic.sum()
            if p == 0:
                ZeroPachesNumber = ZeroPachesNumber + 1
            else:
                im = Image.fromarray(CNNFeedPic)
                im.save(TemplatePachDir + f'/1-{u}.png')
                [img_height, img_width] = [160, 160]
                img = keras.preprocessing.image.load_img(TemplatePachDir + f'/1-{u}.png',
                                                         target_size=(img_height, img_width))
                img_array = keras.preprocessing.image.img_to_array(img)
                img_array = tf.expand_dims(img_array, 0)
                predictions = model.predict(img_array)
                Tempimage = plt.imread(TemplatePachDir + f'/1-{u}.png')
                if predictions[0].sum() > 0:
                    PatchPosition_M[i, j] = 1
                    k = k + 1
                    cv2.rectangle(imtest, (j * WindowShape, i * WindowShape),
                                  (j * WindowShape + WindowShape, i * WindowShape + WindowShape), (0, 0, 255),
                                  thickness=10, lineType=cv2.LINE_8)
                    cv2.putText(imtest, "M", (j * WindowShape, i * WindowShape), cv2.FONT_HERSHEY_SIMPLEX, 2,
                                (0, 0, 255), 5)
    im = Image.fromarray(imtest)
    Out_M_Image = im
    # im.save(ResultDir_M+'/1.png')
    # print("t3",datetime.datetime.now())
    z += t - z

    imtest = cv2.imread(SourceInputImageDir, 1)
    CalcIm = imtest
    model = keras.models.load_model(C_NetDir)
    WindowShape = C_WindowShape
    M = np.int(a / WindowShape)
    N = np.int(b / WindowShape)
    M_C = M
    N_C = N
    PatchPosition_C = np.zeros((M, N))
    i = 0
    j = 0
    for i in range(M):
        for j in range(N):
            CNNFeedPic = CalcIm[i * WindowShape:i * WindowShape + WindowShape,
                         j * WindowShape:j * WindowShape + WindowShape]
            p = CNNFeedPic.sum()
            if p == 0:
                ZeroPachesNumber = ZeroPachesNumber + 1
            else:
                im = Image.fromarray(CNNFeedPic)
                im.save(TemplatePachDir + f'/2-{u}.png')
                [img_height, img_width] = [160, 160]
                img = keras.preprocessing.image.load_img(TemplatePachDir + f'/2-{u}.png',
                                                         target_size=(img_height, img_width))
                img_array = keras.preprocessing.image.img_to_array(img)
                img_array = tf.expand_dims(img_array, 0)
                predictions = model.predict(img_array)
                Tempimage = plt.imread(TemplatePachDir + f'/2-{u}.png')
                if predictions[0].sum() > 0:
                    PatchPosition_C[i, j] = 1
                    k = k + 1
                    cv2.rectangle(CalcIm, (i * WindowShape, j * WindowShape),
                                  (i * WindowShape + WindowShape, j * WindowShape + WindowShape), (0, 255, 0),
                                  thickness=10, lineType=cv2.LINE_8)
                    cv2.putText(CalcIm, "C", (j * WindowShape, i * WindowShape), cv2.FONT_HERSHEY_SIMPLEX, 2,
                                (0, 255, 0), 5)
    im = Image.fromarray(CalcIm)
    Out_C_Image = im
    # im.save(ResultDir_C+'/2.png')
    # print("t4",datetime.datetime.now())
    z += t - z

    M_C_Im = imtest
    WindowShape = M_WindowShape
    for i in range(M_M):
        for j in range(N_M):
            if PatchPosition_M[i, j] == 1:
                cv2.rectangle(M_C_Im, (i * WindowShape, j * WindowShape),
                              (i * WindowShape + WindowShape, j * WindowShape + WindowShape), (0, 0, 255), thickness=10,
                              lineType=cv2.LINE_8)
                cv2.putText(M_C_Im, "M", (j * WindowShape, i * WindowShape), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),
                            5)
    i = 0
    j = 0
    WindowShape = C_WindowShape
    for i in range(M_C):
        for j in range(N_C):
            if PatchPosition_C[i, j] == 1:
                cv2.rectangle(M_C_Im, (i * WindowShape, j * WindowShape),
                              (i * WindowShape + WindowShape, j * WindowShape + WindowShape), (0, 255, 0), thickness=10,
                              lineType=cv2.LINE_8)
                cv2.putText(M_C_Im, "C", (j * WindowShape, i * WindowShape), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0),
                            5)
    im = Image.fromarray(M_C_Im)
    Out_M_C_Image = im
    # im.save(ResultDir_M_C+'/3.png')
    # print("t5",datetime.datetime.now())
    z += t - z
    # print("z: " , z)
    return Out_C_Image, Out_M_Image, Out_M_C_Image


def save_to_output(input, c_res, m_res, cm_res):
    c_res.save(f'Output/c{input.id}.jpg')
    m_res.save(f'Output/m{input.id}.jpg')
    cm_res.save(f'Output/cm{input.id}.jpg')
    Output.objects.create(
        input_ids=input,
        Cimage=f'Output/c{input.id}.jpg',
        Mimage=f'Output/m{input.id}.jpg',
        CMimage=f'Output/cm{input.id}.jpg'
    )
