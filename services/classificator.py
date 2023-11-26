import cv2
import torch
import torch.nn as nn
import torchvision.transforms as transforms


class CustomClassifier(nn.Module):
    def __init__(self):
        super(CustomClassifier, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=64, kernel_size=3)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(2)
        self.dropout1 = nn.Dropout(0.15)

        self.conv2 = nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3)
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(2)

        self.conv3 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3)
        self.relu3 = nn.ReLU()

        self.fc1 = nn.Linear(100352, 128)
        self.relu4 = nn.ReLU()

        self.fc2 = nn.Linear(128, 256)
        self.relu5 = nn.ReLU()

        self.fc3 = nn.Linear(256, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.conv1(x)
        x = self.relu1(x)
        x = self.pool1(x)
        x = self.dropout1(x)
        x = self.conv2(x)
        x = self.relu2(x)
        x = self.pool2(x)
        x = self.conv3(x)
        x = self.relu3(x)
        x = x.view(x.size(0), -1)  # Flatten
        x = self.fc1(x)
        x = self.relu4(x)
        x = self.fc2(x)
        x = self.relu5(x)
        x = self.fc3(x)
        x = self.sigmoid(x)

        return x


class classificator:
    def __init__(self, messenger):
        self.messenger = messenger

        self.transform = transforms.Compose(
            [
                transforms.ToPILImage(),
                transforms.Resize((128, 128)),
                transforms.ToTensor(),
            ]
        )

        self.model = CustomClassifier()
        self.model.load_state_dict(
            torch.load("./models/classificator.pth", map_location=torch.device("cpu"))
        )

        self.model.eval()

    def getPrediction(self, frame):
        with torch.no_grad():
            output = self.model(frame)
            return torch.sigmoid(output).item()

    def run(self, frame):
        try:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = self.transform(frame).unsqueeze(0)

            prediction = self.getPrediction(frame)
            prediction = "wall" if prediction > 0.5 else "road"

            self.messenger.info(prediction)
        except Exception as e:
            self.messenger.error(e)
