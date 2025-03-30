import requests
import base64
import time
import random

headers = {
    "Content-Type": "application/json",
    "Authorization": "Api-key "
}

def yandex_art_request(prompt):
    payload = {
        "modelUri": "art:///yandex-art/latest",
        "generationOptions": {
            "seed": random.randint(-100000, 100000),
            "aspectRatio": {
                "widthRatio": "1",
                "heightRatio": "1"
            }
        },
        "messages": [
            {
                "weight": 1,
                "text": prompt
            }
        ]
    }
    
    create_request = requests.post(
        'https://llm.api.cloud.yandex.net/foundationModels/v1/imageGenerationAsync', 
        headers=headers, 
        json=payload
    )
    
    operation_id = create_request.json()['id']
    
    while True:
        done_request = requests.get(
            f'https://llm.api.cloud.yandex.net:443/operations/{operation_id}', 
            headers=headers
        )
        done_data = done_request.json()
        
        if done_data.get('done', False):

            image_data = done_data['response']['image']
            with open(f"response/images/{operation_id}.jpeg", "wb") as file:
                file.write(base64.b64decode(image_data))
            
            print(f"{operation_id}.jpeg")
            return f"response/images/{operation_id}.jpeg"
        
        time.sleep(5)

def check_operation_status(operation_id):
    try:
       
        done_request = requests.get(
            f'https://llm.api.cloud.yandex.net:443/operations/{operation_id}', 
            headers=headers
        )
        done_request.raise_for_status()  
        
        done_data = done_request.json()
        
        if done_data.get('done', False):
            image_data = done_data['response']['image']
            image_path = f"response/images/{operation_id}.jpeg"
            
            with open(image_path, "wb") as file:
                file.write(base64.b64decode(image_data))
            
            print(f"{operation_id}.jpeg сохранено в {image_path}")
            return image_path
        
        print(f"Операция {operation_id} ещё не завершена.")
        return None
    
    except requests.RequestException as e:
        print(f"Ошибка при запросе статуса операции: {e}")
        return None
