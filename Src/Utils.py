
import numpy as np
import pygame
import tensorflow as tf
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D
from tensorflow.keras.layers import LeakyReLU
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam


def get_shape(layer, input_shape=False):
    one_dim_orientation = 'z'
    if input_shape:
        layer_shape = layer.input_shape
    else:
        layer_shape = layer.output_shape

    if isinstance(layer_shape, tuple):
        shape = list(layer_shape)
    elif isinstance(layer_shape, list) and len(layer_shape) == 1:  # drop dimension for non seq. models
        shape = layer_shape[0]
        if isinstance(shape, tuple):
            shape = list(shape)
    else:
        raise RuntimeError(f"not supported tensor shape {layer_shape}")

    shape = shape[1:]
    if len(shape) == 1:
        if one_dim_orientation in ['x', 'y', 'z']:
            shape = list((1, ) * "xyz".index(one_dim_orientation) + tuple(shape))
        else:
            raise ValueError(f"unsupported orientation: {one_dim_orientation}")

    if shape[2] == 73728:
        shape[2] = shape[2]/1000
    else:
        shape[2] = shape[2] / np.log(shape[2])
    # print(layer.name, layer.__class__.__name__, shape, "input_shape" if input else "output_shape")
    return shape


def move_camera(x_camera, y_camera, z_camera):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

            if event.key == pygame.K_a:
                x_camera = 0.8

            elif event.key == pygame.K_d:
                x_camera = -0.8

            elif event.key == pygame.K_w:
                z_camera = 0.8

            elif event.key == pygame.K_s:
                z_camera = -0.8

            elif event.key == pygame.K_LSHIFT:
                y_camera = -0.8

            elif event.key == pygame.K_LCTRL:
                y_camera = 0.8

        elif event.type == pygame.KEYUP:

            if event.key == pygame.K_a and x_camera > 0:
                x_camera = 0

            elif event.key == pygame.K_d and x_camera < 0:
                x_camera = 0

            elif event.key == pygame.K_w and z_camera > 0:
                z_camera = 0

            elif event.key == pygame.K_s and z_camera < 0:
                z_camera = 0

            elif event.key == pygame.K_LSHIFT and y_camera < 0:
                y_camera = 0

            elif event.key == pygame.K_LCTRL and y_camera > 0:
                y_camera = 0

    return x_camera, y_camera, z_camera


def get_model():
    # model = load_model("model_GTSRB_train1_val1_02//cp-0057.ckpt")

    # model = tf.keras.applications.VGG16(
    #     include_top=True,
    #     weights="imagenet",
    #     input_tensor=None,
    #     input_shape=None,
    #     pooling=None,
    #     classes=1000,
    #     classifier_activation="softmax",
    # )

    model, _ = create_model(10, 28, 3)
    return model


def create_model(class_count, img_size, channels):

    model_logits = Sequential()

    model_logits.add(Conv2D(128, (5, 5), input_shape=(img_size, img_size, channels), name='layer_conv1'))
    # model_logits.add(LeakyReLU(alpha=0.01))
    # model_logits.add(BatchNormalization())
    # model_logits.add(Dropout(0.5))

    # model_logits.add(Conv2D(196, (2, 2), name='layer_conv2'))
    # model_logits.add(LeakyReLU(alpha=0.01))
    # model_logits.add(Conv2D(196, (2, 2), name='layer_conv3'))
    # model_logits.add(LeakyReLU(alpha=0.01))
    # model_logits.add(Conv2D(196, (5, 5), name='layer_conv4'))
    # model_logits.add(LeakyReLU(alpha=0.01))
    # model_logits.add(MaxPooling2D(pool_size=(2, 2)))
    # model_logits.add(BatchNormalization())
    # model_logits.add(Dropout(0.5))

    # model_logits.add(Conv2D(256, (2, 2), name='layer_conv5'))
    # model_logits.add(LeakyReLU(alpha=0.01))
    # model_logits.add(Conv2D(256, (2, 2), name='layer_conv6'))
    # model_logits.add(LeakyReLU(alpha=0.01))
    # model_logits.add(Conv2D(256, (2, 2), name='layer_conv7'))
    # model_logits.add(LeakyReLU(alpha=0.01))
    # model_logits.add(MaxPooling2D(pool_size=(2, 2)))
    # model_logits.add(BatchNormalization())
    # model_logits.add(Dropout(0.5))

    model_logits.add(Flatten())
    # model_logits.add(LeakyReLU(alpha=0.0))
    model_logits.add(Dense(384))
    model_logits.add(LeakyReLU(alpha=0.0))
    model_logits.add(Dropout(0.5))

    model_logits.add(Dense(class_count))

    output = Activation('softmax')(model_logits.output)

    model = tf.keras.Model(model_logits.inputs, output)

    opt = Adam(learning_rate=0.0005)
    model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
    return model, model_logits
