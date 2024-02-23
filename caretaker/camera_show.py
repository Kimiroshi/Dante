import cv2
from caretaker.face_cutter import find_face


def take_photo(win_name, savepath, show):
    if '/' in savepath:
        direct, name = savepath.split('/')
        direct += '/'
    else:
        direct, name = '', savepath
    img_name = direct + name
    img_name.lstrip()
    cam = cv2.VideoCapture(0)
    if show:
        cv2.namedWindow(win_name)

    while True:
        ret, frame = cam.read()
        if not ret:
            print('failed to grab frame')
            break

        if show:
            cv2.imshow(win_name, frame)
        k = cv2.waitKey(1)
        if k % 256 == 27:
            break
        if show:
            if k == 32:
                cv2.imwrite(img_name, frame)
                find_face(img_name, output=img_name)
                break
        else:
            cv2.imwrite(img_name, frame)
            find_face(img_name, output=img_name)
            break

    cam.release()
    cv2.destroyAllWindows()