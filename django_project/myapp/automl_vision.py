#잘린 이미지가 매개 변수로 들어옴
def my_detect_text_mat(img):
    """Detects text in the file."""
    from google.cloud import vision

    client = vision.ImageAnnotatorClient()
    image = vision.types.Image(content=cv2.imencode('.jpg', img)[1].tobytes())

    #글자 추출
    response = client.text_detection(image=image)
    texts = response.text_annotations

    return texts #글자 추출 결과물


from google.cloud import automl
import cv2
import os


# autoML 프로젝트 ID, 모델 ID, 이미지 파일 경로를 매개변수로 받는 함수 predict
def automl_vision(file_path):
    """Predict."""
    # [START automl_vision_classification_predict]
    #print(file_path)
    # autoML JSon 키 설정
    #credential_path = r"키.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
    project_id = "수정"
    model_id = "수정"

    # 원본 이미지
    img = cv2.imread(file_path)
    # 원본 이미지 크기
    img_height = img.shape[0]
    img_width = img.shape[1]
    # RGB 색상으로 변환
    orig = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    prediction_client = automl.PredictionServiceClient()

    # Get the full path of the model.
    model_full_id = automl.AutoMlClient.model_path(
        project_id, "us-central1", model_id
    )

    # 파일 읽어들이기
    with open(file_path, "rb") as content_file:
        content = content_file.read()

    image = automl.Image(image_bytes=content)
    payload = automl.ExamplePayload(image=image)

    # params is additional domain-specific parameters.
    # score_threshold is used to filter the result
    # https://cloud.google.com/automl/docs/reference/rpc/google.cloud.automl.v1#predictrequest
    params = {"score_threshold": "0.8"}

    request = automl.PredictRequest(
        name=model_full_id,
        payload=payload,
        params=params
    )
    response = prediction_client.predict(request=request)

    tags = []
    for result in response.payload:
        # 태그로 잡힌 박스 몇 개인지
        bounding_box = result.image_object_detection.bounding_box

        # normalized vertices로 되어있는 좌표를 실사이즈로 변환 및 직사각형의 네 꼭짓점 좌표를 구함
        lu = bounding_box.normalized_vertices[0]  # left/up x, y 좌표
        rd = bounding_box.normalized_vertices[1]  # right/down x, y 좌표
        w = rd.x - lu.x
        h = rd.y - lu.y

        # cropping
        cropped_img = orig[int(lu.y * img_height):int((lu.y + h) * img_height),
                      int(lu.x * img_width):int((lu.x + w) * img_width)]

        texts = my_detect_text_mat(cropped_img)   #잘린 이미지들 속 글자 추출하기 위해 my_detect_text_mat() 호출
        tags.append(texts[0].description)


    return tags
