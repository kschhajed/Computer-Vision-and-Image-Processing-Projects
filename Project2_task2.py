"""
 Grayscale Image Processing
(Due date: Nov. 26, 11:59 P.M., 2021)

The goal of this task is to experiment with two commonly used 
image processing techniques: image denoising and edge detection. 
Specifically, you are given a grayscale image with salt-and-pepper noise, 
which is named 'task2.png' for your code testing. 
Note that different image might be used when grading your code. 

You are required to write programs to: 
(i) denoise the image using 3x3 median filter;
(ii) detect edges in the denoised image along both x and y directions using Sobel operators (provided in line 30-32).
(iii) design two 3x3 kernels and detect edges in the denoised image along both 45° and 135° diagonal directions.
Hint: 
• Zero-padding is needed before filtering or convolution. 
• Normalization is needed before saving edge images. You can normalize image using the following equation:
    normalized_img = 255 * frac{img - min(img)}{max(img) - min(img)}

Do NOT modify the code provided to you.
You are NOT allowed to use OpenCV library except the functions we already been imported from cv2. 
You are allowed to use Numpy for basic matrix calculations EXCEPT any function/operation related to convolution or correlation. 
You should NOT use any other libraries, which provide APIs for convolution/correlation ormedian filtering. 
Please write the convolution code ON YOUR OWN. 
"""

from cv2 import imread, imwrite, imshow, IMREAD_GRAYSCALE, namedWindow, waitKey, destroyAllWindows
import numpy as np

# Sobel operators are given here, do NOT modify them.
sobel_x = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]]).astype(int)
sobel_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]]).astype(int)

def padding(img):
    padded_img = np.pad(img, pad_width=1)
    return padded_img

def filter(img):
    """
    :param img: numpy.ndarray(int), image
    :return denoise_img: numpy.ndarray(int), image, same size as the input image

    Apply 3x3 Median Filter and reduce salt-and-pepper noises in the input noise image
    """
    conv_img = np.empty(img.shape, dtype = int)
    img = padding(img)
    filter = np.ones((3,3), dtype = np.int64)
    k_h = filter.shape[0]//2
    k_w = filter.shape[1]//2
    for i in range(k_h, img.shape[0] - k_h):
        for j in range(k_w, img.shape[1] - k_w):
            prod = img[i - k_h:i + k_h + 1,j - k_w:j + k_w + 1]*filter
            conv_img[i-k_h,j-k_w] = np.median(prod)
    #print("Filtering output:", conv_img.shape)
    return conv_img


def convolve2d(img, kernel):
    """
    :param img: numpy.ndarray, image
    :param kernel: numpy.ndarray, kernel
    :return conv_img: numpy.ndarray, image, same size as the input image

    Convolves a given image (or matrix) and a given kernel.
    """
    padded_img = padding(img)
    filter = np.flip(kernel)
    conv_img = np.empty(img.shape, dtype = int)
    k_h = filter.shape[0]//2
    k_w = filter.shape[1]//2
    for i in range(k_h, padded_img.shape[0] - k_h):
        for j in range(k_w, padded_img.shape[1] - k_w):
            #prod = padded_img[i - k_h :i + k_h + 1,j - k_w:j + k_w + 1]*filter
            conv_img[i-k_h,j-k_w] =  np.sum(padded_img[i - k_h :i + k_h + 1,j - k_w:j + k_w + 1]*filter)#np.average(prod)
    #print("Convolved img: ",conv_img.shape)
    return conv_img


def edge_detect(img):
    """
    :param img: numpy.ndarray(int), image
    :return edge_x: numpy.ndarray(int), image, same size as the input image, edges along x direction
    :return edge_y: numpy.ndarray(int), image, same size as the input image, edges along y direction
    :return edge_mag: numpy.ndarray(int), image, same size as the input image, 
                      magnitude of edges by combining edges along two orthogonal directions.

    Detect edges using Sobel kernel along x and y directions.
    Please use the Sobel operators provided in line 30-32.
    Calculate magnitude of edges by combining edges along two orthogonal directions.
    All returned images should be normalized to [0, 255].
    """
    edge_x = convolve2d(img,sobel_x)
    edge_y = convolve2d(img,sobel_y)
    edge_mag = np.sqrt(np.add(np.square(edge_x),np.square(edge_y)))
    edge_x = 255*((edge_x-np.min(edge_x))/(np.max(edge_x)-np.min(edge_x)))
    edge_y = 255*((edge_y-np.min(edge_y))/(np.max(edge_y)-np.min(edge_y)))
    edge_mag = 255*((edge_mag-np.min(edge_mag))/(np.max(edge_mag)-np.min(edge_mag)))
    edge_x = edge_x.astype('uint8')
    edge_y = edge_y.astype('uint8')
    edge_mag = edge_mag.astype('uint8')
    #print("Shapes of edgex,edgey,edgemag: ",edge_x.shape, edge_y.shape, edge_mag.shape)
    return edge_x, edge_y, edge_mag


def edge_diag(img):
    """
    :param img: numpy.ndarray(int), image
    :return edge_45: numpy.ndarray(int), image, same size as the input image, edges along x direction
    :return edge_135: numpy.ndarray(int), image, same size as the input image, edges along y direction

    Design two 3x3 kernels to detect the diagonal edges of input image. Please print out the kernels you designed.
    Detect diagonal edges along 45° and 135° diagonal directions using the kernels you designed.
    All returned images should be normalized to [0, 255].
    """
    sobel_45 = np.array([[0, 1, 2], [-1, 0, 1], [-2, -1, 0]])
    sobel_135 = np.array([[-2, -1, 0], [-1, 0, 1], [0, 1, 2]])
    edge_45 = convolve2d(img, sobel_45)
    edge_135 = convolve2d(img, sobel_135)
    edge_45 = 255*((edge_45-np.min(edge_45))/(np.max(edge_45)-np.min(edge_45)))
    edge_135 = 255*((edge_135-np.min(edge_135))/(np.max(edge_135)-np.min(edge_135)))
    edge_45 = edge_45.astype('uint8')
    edge_135 = edge_135.astype('uint8')

    print("Sobel 45 filter: ", sobel_45)
    print("Soblet 135 filter: ", sobel_135)

    return edge_45, edge_135


if __name__ == "__main__":
    # noise_img = imread('task2.png', IMREAD_GRAYSCALE)
    # #print("input image: ",noise_img.shape)
    # denoise_img = filter(noise_img)
    # imwrite('results/task2_denoise.jpg', denoise_img)
    # edge_x_img, edge_y_img, edge_mag_img = edge_detect(denoise_img)
    # imwrite('results/task2_edge_x.jpg', edge_x_img)
    # imwrite('results/task2_edge_y.jpg', edge_y_img)
    # imwrite('results/task2_edge_mag.jpg', edge_mag_img)
    # edge_45_img, edge_135_img = edge_diag(denoise_img)
    # imwrite('results/task2_edge_diag1.jpg', edge_45_img)
    # imwrite('results/task2_edge_diag2.jpg', edge_135_img)
        ###### testing start #######
    print('Grading Task2:\n')
    import time
    start_time = time.time()
    thr = 10

    ################################################################
    ## original code
    noise_img = imread('task2.png', IMREAD_GRAYSCALE)
    denoise_img = filter(noise_img)
    imwrite('results/task2_denoise.png', denoise_img)
    ################################################################

    ref_denoise_img = imread('C:/Users/Kshitij/Downloads/project2_reference_results/project2_reference_results/task2_references/task2_denoise.png', IMREAD_GRAYSCALE)
    ref_denoise_img = ref_denoise_img.astype(int)
    # denoise_img_png = imread('results/task2_denoise.png', IMREAD_GRAYSCALE)
    denoise_img = denoise_img.astype(int)
    if denoise_img.shape != ref_denoise_img.shape:
        print('T2.1: Shape Inconsistent, NOT PASS')
    else:
        diff_denoise = np.sum(np.absolute(denoise_img - ref_denoise_img))
        if  diff_denoise < thr:
            print('T2.1: PASS (%d)' % diff_denoise)
        else:
            print('T2.1: Incorrect Result, NOT PASS (%d)' % diff_denoise)

    ################################################################
    ## original code
    edge_x_img, edge_y_img, edge_mag_img = edge_detect(ref_denoise_img)
    imwrite('results/task2_edge_x.png', edge_x_img)
    imwrite('results/task2_edge_y.png', edge_y_img)
    imwrite('results/task2_edge_mag.png', edge_mag_img)
    ################################################################

    ref_edge_x_img = imread('C:/Users/Kshitij/Downloads/project2_reference_results/project2_reference_results/task2_references/task2_edge_x.png', IMREAD_GRAYSCALE)
    ref_edge_y_img = imread('C:/Users/Kshitij/Downloads/project2_reference_results/project2_reference_results/task2_references/task2_edge_y.png', IMREAD_GRAYSCALE)
    ref_edge_mag_img = imread('C:/Users/Kshitij/Downloads/project2_reference_results/project2_reference_results/task2_references/task2_edge_mag.png', IMREAD_GRAYSCALE)
    edge_x_img, edge_y_img, edge_mag_img = edge_x_img.astype(int), edge_y_img.astype(int), edge_mag_img.astype(int)
    # edge_x_img_png = imread('results/task2_edge_x.png', IMREAD_GRAYSCALE)
    # edge_y_img_png = imread('results/task2_edge_y.png', IMREAD_GRAYSCALE)
    # edge_mag_img_png = imread('results/task2_edge_mag.png', IMREAD_GRAYSCALE)
    if edge_mag_img.shape != ref_edge_mag_img.shape:
            print('T2.2: Shape Inconsistent, NOT PASS')
    else:
        diff_x_x = np.sum(np.absolute(edge_x_img - ref_edge_x_img))
        diff_x_y = np.sum(np.absolute(edge_x_img - ref_edge_y_img))
        diff_y_x = np.sum(np.absolute(edge_y_img - ref_edge_x_img))
        diff_y_y = np.sum(np.absolute(edge_y_img - ref_edge_y_img))
        diff_mag = np.sum(np.absolute(edge_mag_img - ref_edge_mag_img))
        # test edge_x
        if diff_x_x < thr:
            print('T2.2 - edge_x: PASS (%d)' % diff_x_x)
        elif diff_y_x < thr:
            print('T2.2 - edge_x: PASS (%d)' % diff_y_x)
        else:
            print('T2.2 - edge_x: NOT PASS (%d)' % min(diff_x_x, diff_y_x))
        # test edge_y
        if diff_y_y < thr:
            print('T2.2 - edge_y: PASS (%d)' % diff_y_y)
        elif diff_x_y < thr:
            print('T2.2 - edge_y: PASS (%d)' % diff_x_y)
        else:
            print('T2.2 - edge_y: NOT PASS (%d)' % min(diff_x_y, diff_y_y))
        # test edge_mag
        if diff_mag < thr:
            print('T2.2 - edge_mag: PASS (%d)' % diff_mag)
        else:
            print('T2.2 - edge_mag: NOT PASS (%d)' % diff_mag)

    ## Efficiency testing: running time 
    end_time = time.time()
    running_time = end_time - start_time
    if running_time <= 60: 
        print('Efficiency Test: PASS (%.2fs)' % running_time)
    elif running_time <= 90:
        print('Efficiency Test: HALF PASS (%.2fs)' % running_time)
    else:
        print('Efficiency Test: NOT PASS (%.2fs)' % running_time)
    ## original code
    edge_45_img, edge_135_img = edge_diag(ref_denoise_img)
    imwrite('results/task2_edge22_diag1.png', edge_45_img)
    imwrite('results/task2_edge22_diag2.png', edge_135_img)
    ################################################################

    print('Please check folder ' + '\'results\'' 
            + ' for the correctness of two diagonal edge images: ' 
            + 'task2_edge_diag1.png, ' + 'task2_edge_diag2.png\n')





