# Text-to-Image Generator with Modal

## Cài đặt

### 1. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 2. Thiết lập Modal

1. Tạo tài khoản Model 
2. Cài đặt Modal CLI và đăng nhập:

```bash
python -m modal setup
```

Lệnh này sẽ mở trình duyệt để bạn đăng nhập vào tài khoản Modal.

### 3. Deploy ứng dụng

Deploy ứng dụng lên Modal:

```bash
modal deploy app.py
```

## Cách sử dụng

### Cách 1: Chạy trực tiếp từ app.py

```bash
modal run app.py
```

Lệnh này sẽ tạo ảnh và lưu thành `generated_image.png`.

### Cách 2: Sử dụng client script

#### Tạo hình ảnh với các tùy chọn:

```bash
python client.py "A futuristic city at night" --negative-prompt "blurry, low quality" --steps 30 --guidance 8.0 --output "my_city.png"
```

#### Tạo nhiều hình ảnh cùng lúc:

```bash
python client.py --multiple "A cat in space" "A dragon flying" "A magical forest"
```

### Cách 3: Sử dụng Modal CLI trực tiếp

```bash
modal run app.py::generate_image --prompt "Your prompt here"
```


### Xem trạng thái app:

```bash
modal app list
```

## Tùy chỉnh

### Thay đổi model:

Trong `app.py`, thay đổi:
```python
"runwayml/stable-diffusion-v1-5"
```

Thành model khác như:
- `"stabilityai/stable-diffusion-2-1"`
- `"runwayml/stable-diffusion-v1-4"`

### Thay đổi GPU:

Thay đổi:
```python
gpu=modal.gpu.A10G()
```

Thành:
- `gpu=modal.gpu.T4()`
- `gpu=modal.gpu.A100()` 
