import torchvision.transforms as transforms
from classificatorCNN import CustomClassifier

config = {
    "translate": True,
    "camera": {
        "device": 1,
        "width": 256,
        "height": 256,
    },
    "detector": {
        "model": ".\\models\\detector.pt",
        "labels": [
            "tree",
            "car",
            "person",
            "pole",
            "fence",
            "utility_pole",
            "bollard",
            "bicycle",
            "motorcycle",
            "flower_bed",
            "dog",
            "bus_stop",
            "traffic_cone",
            "truck",
            "bench",
            "bus",
            "kickboard",
            "streetlamp",
            "telephone_booth",
            "trash",
            "fire_plug",
            "plant",
            "sign_board",
            "fire_hydrant",
            "corner",
            "opened_door",
            "mailbox",
            "unknown",
            "banner",
        ],
        "printLabels": [
            "person",
            "bollard",
            "bicycle",
            "motorcycle",
            "traffic_cone",
            "kickboard",
        ],
    },
    "classificator": {
        "model": ".\\models\\classificator.pth",
        "class": ["road", "wall"],
        "transform": transforms.Compose(
            [
                transforms.ToPILImage(),
                transforms.Resize((128, 128)),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),
            ]
        ),
        "cnn": CustomClassifier(),
    },
}
