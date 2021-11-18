import base64
from removebg import RemoveBg
import requests, logging

# 라이브러리 설치해서 사용 -> 속도향상
API_ENDPOINT = "https://api.remove.bg/v1.0/removebg"


class NewRemoveBg(RemoveBg):  # 메소드 오버라이드
    def __init__(self, api_key, error_log_file):
        self.__api_key = api_key
        logging.basicConfig(filename=error_log_file)

    def remove_background_from_img_file(
        self, img_file_path, size="regular", bg_color=None
    ):
        # Open image file to send information post request and send the post request
        img_file = open(img_file_path, "rb")
        response = requests.post(
            API_ENDPOINT,
            files={"image_file": img_file},
            data={"size": size, "bg_color": bg_color},
            headers={"X-Api-Key": self.__api_key},
        )
        response.raise_for_status()
        self.__output_file__(response, img_file.name + "_removebg.png")  # 출력 파일 이름 변경

        img_file.close()
    
    def remove_background_from_base64_img(
        self, base64_img, size="regular", new_file_name="no-bg.png", bg_color=None
    ):
        response = requests.post(
            API_ENDPOINT,
            data={
                'image_file_b64': base64_img,
                'size': size,
                'bg_color': bg_color
            },
            headers={'X-Api-Key': self.__api_key}
        )
        response.raise_for_status()
        self.__output_file__(response, new_file_name)

rmbg = NewRemoveBg("eihrhcx6ZmqHYx69CZna8mHa", "error.log")
with open('testimagege.jpg', 'rb') as f:
    encode_str = base64.b64encode(f.read())
#rmbg.remove_background_from_img_file("testimage.png")
rmbg.remove_background_from_base64_img(encode_str)