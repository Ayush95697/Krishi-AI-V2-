from PIL import Image
import torch
from torchvision import transforms, models
import torch.nn as nn

class_names = ['Apple___Apple_scab',
 'Apple___Black_rot',
 'Apple___Cedar_apple_rust',
 'Apple___healthy',
 'Banana_Cordana',
 'Banana_Healthy',
 'Banana_Pestalotiopsis',
 'Banana_Sigatoka',
 'Blackgarm_Anthracnose',
 'Blackgarm_Healthy',
 'Blackgarm_Leaf Crinckle',
 'Blackgarm_Powdery Mildew',
 'Blackgarm_Yellow Mosaic',
 'Maize_Cercospora_leaf_spot Gray_leaf_spot',
 'Maize_Common_rust_',
 'Maize_Healthy',
 'Maize_aphid',
 'Maize_curvularia_leaf_spot',
 'Maize_fall_armyworm',
 'Maize_maydis_leaf_blight',
 'Maize_sorghum_downy_mildew',
 'Maize_turcicum_leaf_blight',
 'Mango_Anthracnose',
 'Mango_Bacterial Canker',
 'Mango_Cutting Weevil',
 'Mango_Die Back',
 'Mango_Gall Midge',
 'Mango_Healthy',
 'Mango_Powdery Mildew',
 'Mango_Sooty Mould',
 'Pepper__bell___Bacterial_spot',
 'Pepper__bell___healthy',
 'Potato___Early_blight',
 'Potato___Late_blight',
 'Potato___healthy',
 'Rice_Bacterial_leaf_blight',
 'Rice_Brown_spot',
 'Rice_False_smut',
 'Rice_Healthy',
 'Rice_Leaf_folder',
 'Rice_Rice_skipper',
 'Rice_White_stem_borer',
 'Rice_Yellow_stem_borer',
 'Rice_leaf_sheath_blight',
 'Tomato_Bacterial_spot',
 'Tomato_Early_blight',
 'Tomato_Late_blight',
 'Tomato_Leaf_Mold',
 'Tomato_Septoria_leaf_spot',
 'Tomato_Target_Spot',
 'Tomato_Tomato_mosaic_virus',
 'Tomato_Two_spotted_Spider_mites',
 'Tomato_Yellow_Leaf_Curl_Virus',
 'Tomato_healthy']

trained_model =None

class PlantDiseaseEfficientNet(nn.Module):
    def __init__(self, num_classes, dropout_rate=0.26063647813636287):
        super().__init__()

        self.model = models.efficientnet_b0(weights="DEFAULT")

        # Freeze entire pretrained backbone
        for param in self.model.features.parameters():
            param.requires_grad = False

        # Unfreeze only the last feature block
        for param in self.model.features[-1].parameters():
            param.requires_grad = True

        # Replace classifier
        in_features = self.model.classifier[1].in_features

        self.model.classifier = nn.Sequential(
            nn.Dropout(dropout_rate),
            nn.Linear(in_features, 256),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        return self.model(x)
        

def disease_Detection(image_path):
    image = Image.open(image_path).convert("RGB")
    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    image = transform(image)
    image_tensor = image.unsqueeze(0)

    global trained_model

    if trained_model is None:
        trained_model = PlantDiseaseEfficientNet()
        trained_model.load_state_dict(torch.load('saved_image_DetectionModel.pth'))
        trained_model.eval()

    with torch.no_grad():
        outputs = trained_model(image_tensor)
        _,predicted_class = torch.max(outputs,1)

    return class_names[predicted_class.item()]

