from skimage import io
from os import listdir
from os.path import isfile, join
import numpy as np
from skimage.transform import resize
from skimage.filters import threshold_otsu


def detect_lines(img, nb_white_pix=10):
    h = img.shape[0]
    w = img.shape[1]
    nb_white_line = 0
    found = False
    line_indices = set()

    i_start = 0

    for i in range(h):
        if found == True:
            i_start = i

        found = False
        # print("nb_white_line = ", nb_white_line, "i = ",i)
        for j in range(w):
            if img[i, j] == 0:
                nb_white_line = 0
                found = True
                break

        if found == False:
            nb_white_line = nb_white_line + 1
            if nb_white_line >= nb_white_pix:
                # draw line
                # rr, cc = line(i, 0, i, w)
                # img[(i-nb_white_line):i,0:w] = 0
                line_indices.add(i_start)
                img[i_start, 0:w] = 0
                nb_white_line = 0
        if i == (h-1) and found == False:
            img[i, 0:w] = 0
            line_indices.add(i)

    line_indices = list(line_indices)
    line_indices.sort()
    return img, line_indices


def detect_characters(img, line_indices, sep_h):
    # h = img.shape[0]
    w = img.shape[1]
    # nb_white_line = 0
    found = False
    line_drown = True
    last_col = 0

    for i in line_indices:
        if i == 0:
            continue
        if found == True:
            found = False
        last_col = 0
        for j in range(w):
            found = False
            for k in range(i-sep_h, i):
                # print("i = ", i, "  j = ", j, " k = ", k)
                if img[k, j] == 0:
                    line_drown = False
                    found = True
                    break
            if found == False:
                # print("ici j = ", j, " et i = ", i)
                if line_drown == False:
                    img[(i-sep_h):i, j] = 0
                    line_drown = True
                    # save image
                    if j > (last_col+1):
                        io.imsave("car_" + str(i) + "_" + str(j) + ".jpg",
                                  img[(i-sep_h):i, (last_col+1):j])
                        last_col = j

    return img


def digitalize_images(folder, label, max_nb_images=0):
    image_files = [f for f in listdir(folder) if isfile(join(folder, f))]
    images = []
    n_files = 0

    for f in image_files:
        if (max_nb_images != 0) and (n_files > max_nb_images):
            break

        image = io.imread(folder + "/" + f)
        image = resize(image, (64, 64), preserve_range=True)
        thresh = threshold_otsu(image)
        image = image > thresh

        shape = image.shape

        if len(shape) == 3:
            image = image[:, :, 0].reshape((shape[0]*shape[1],))

        if len(shape) == 2:
            image = image.reshape((shape[0]*shape[1],))
        n_files += 1

        images.append(list(image) + [label])

    return images


def digitalize_folder(folder, prefix_sub_folder):
    """Transforms images to csv file
    """
    path = folder + "/" + prefix_sub_folder

    # sample of zero's
    x = digitalize_images(path + "0" + str(1), 0)

    for i in range(2, 10):
        temp = digitalize_images(
            path + "0" + str(i), i)
        x = x + temp

    for i in range(10, 63):
        temp = digitalize_images(
            path + str(i), i)
        x = x + temp

    np.savetxt('train.csv', x, delimiter=';', fmt='%d')
