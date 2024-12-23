import torch
import torch.nn as nn
from torchvision import models
import torchvision.transforms as transforms
from PIL import Image
import pickle


# BaseModel 정의
class BaseModel(nn.Module):
    def __init__(self, num_classes=50):  # 학습 시 클래스 수와 동일
        super(BaseModel, self).__init__()
        self.backbone = models.convnext_large(pretrained=False)  # 사전 학습 불필요
        self.classifier = nn.Linear(1000, num_classes)

    def forward(self, x):
        x = self.backbone(x)
        x = self.classifier(x)
        return x


# 전처리 함수
def preprocess_image(image_path, img_size=224):
    preprocess = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    image = Image.open(image_path).convert("RGB")
    return preprocess(image).unsqueeze(0)


# 모델 로드 함수
def load_model(weight_path, num_classes):
    model = BaseModel(num_classes=num_classes)
    model.load_state_dict(torch.load(weight_path, map_location=torch.device('cpu')))
    model.eval()
    return model


# 화가 예측 함수
def predict_artist(model, image_path, class_names):
    input_tensor = preprocess_image(image_path)
    with torch.no_grad():
        output = model(input_tensor)
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        predicted_index = probabilities.argmax().item()
        confidence = probabilities[predicted_index].item()
        predicted_artist = class_names[predicted_index]
    return predicted_artist, confidence


def running_AI(image): ## image 값 : <FileStorage: '123.jpg' ('image/jpeg')>
    weight_path = './AI/best_model_fold5.pt'  # 저장된 가중치 경로

    # 수동으로 클래스 이름 리스트 작성
    class_names = [
        "Albrecht Dürer",
        "Alfred Sisley",
        "Amedeo Modigliani",
        "Andrei Rublev",
        "Andy Warhol",
        "Camille Pissarro",
        "Caravaggio",
        "Claude Monet",
        "Diego Rivera",
        "Diego Velazquez",
        "Edgar Degas",
        "Edouard Manet",
        "Edvard Munch",
        "El Greco",
        "Eugene Delacroix",
        "Francisco Goya",
        "Frida Kahlo",
        "Georges Seurat",
        "Giotto di Bondone",
        "Gustav Klimt",
        "Gustave Courbet",
        "Henri Matisse",
        "Henri Rousseau",
        "Henri de Toulouse-Lautrec",
        "Hieronymus Bosch",
        "Jackson Pollock",
        "Jan van Eyck",
        "Joan Miró",
        "Kazimir Malevich",
        "Leonardo da Vinci",
        "Marc Chagall",
        "Michelangelo",
        "Mikhail Vrubel",
        "Pablo Picasso",
        "Paul Cézanne",
        "Paul Gauguin",
        "Paul Klee",
        "Peter Paul Rubens",
        "Pierre-Auguste Renoir",
        "Piet Mondrian",
        "Pieter Bruegel",
        "Raphael",
        "Rembrandt",
        "René Magritte",
        "Salvador Dalí",
        "Sandro Botticelli",
        "Titian",
        "Vasily Kandinsky",
        "Vincent van Gogh",
        "William Turner"
    ]

    num_classes = len(class_names)

    preprocess = transforms.Compose([
        transforms.Resize((224, 224)),  # 모델 입력 크기에 맞게 변환
        transforms.ToTensor(),  # Tensor로 변환
        transforms.Normalize(  # 정규화
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

    # FileStorage 객체에서 이미지 열기
    image = Image.open(image)

    # 전처리 적용
    input_tensor = preprocess(image).unsqueeze(0)  # 배치 차원 추가

    # 모델 로드
    model = load_model(weight_path, num_classes)
    model.eval()  # 평가 모드 설정

    # 예측
    with torch.no_grad():
        outputs = model(input_tensor)
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
        confidence, predicted_idx = torch.max(probabilities, dim=0)
        predicted_artist = class_names[predicted_idx]

    print(f"Predicted Artist: {predicted_artist}")
    print(f"Confidence: {confidence.item() * 100:.2f}%")
    data = [predicted_artist,f"{confidence.item() * 100:.2f}%"]
    return data