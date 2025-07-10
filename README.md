# Text-to-Image Generator với Modal

Dự án này sử dụng Modal để tạo ra các hình ảnh từ văn bản bằng mô hình Stable Diffusion. Modal cung cấp GPU cloud computing mạnh mẽ để chạy các tác vụ AI một cách hiệu quả.

## Yêu cầu hệ thống

- Python 3.10 hoặc cao hơn
- Tài khoản Modal (miễn phí để bắt đầu)
- Kết nối internet ổn định

## Cài đặt

### 1. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 2. Thiết lập Modal

Đầu tiên, bạn cần tạo tài khoản Modal:

1. Truy cập [modal.com](https://modal.com) và đăng ký tài khoản
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

Lệnh này sẽ:
- Tải lên code của bạn lên Modal
- Tạo container với tất cả dependencies
- Thiết lập GPU environment
- Tạo volume để cache model

## Cách sử dụng

### Phương pháp 1: Chạy trực tiếp từ app.py

```bash
modal run app.py
```

Lệnh này sẽ tạo một hình ảnh test với prompt mặc định và lưu thành `generated_image.png`.

### Phương pháp 2: Sử dụng client script (Khuyến nghị)

#### Tạo một hình ảnh đơn:

```bash
python client.py "A beautiful sunset over mountains, digital art"
```

#### Tạo hình ảnh với tùy chọn nâng cao:

```bash
python client.py "A futuristic city at night" --negative-prompt "blurry, low quality" --steps 30 --guidance 8.0 --output "my_city.png"
```

#### Tạo nhiều hình ảnh cùng lúc:

```bash
python client.py --multiple "A cat in space" "A dragon flying" "A magical forest"
```

### Phương pháp 3: Sử dụng Modal CLI trực tiếp

```bash
modal run app.py::generate_image --prompt "Your prompt here"
```

## Tùy chọn Parameters

- `prompt`: Mô tả những gì bạn muốn tạo ra (bắt buộc)
- `negative_prompt`: Mô tả những gì bạn muốn tránh (tùy chọn)
- `num_inference_steps`: Số bước tạo (mặc định: 20, càng cao càng chi tiết nhưng chậm hơn)
- `guidance_scale`: Mức độ tuân theo prompt (mặc định: 7.5, từ 1-20)

## Ví dụ Prompts

### Prompts cơ bản:
- "A cute cat wearing a hat"
- "A beautiful landscape with mountains and lakes"
- "A futuristic robot in a cyberpunk city"

### Prompts nâng cao:
- "A portrait of a wise old wizard, highly detailed, digital art, trending on artstation"
- "A magical forest with glowing mushrooms, fantasy art, ethereal lighting"
- "A steampunk airship flying through clouds, Victorian era, brass and copper details"

### Negative prompts hữu ích:
- "blurry, low quality, distorted"
- "ugly, deformed, extra limbs"
- "text, watermark, signature"

## Cấu trúc dự án

```
txt2img-modal/
├── app.py              # Ứng dụng Modal chính
├── client.py           # Script client để sử dụng dễ dàng
├── requirements.txt    # Dependencies
└── README.md          # Hướng dẫn này
```

## Troubleshooting

### Lỗi phổ biến và cách khắc phục:

1. **"App not found"**: Đảm bảo bạn đã deploy app bằng `modal deploy app.py`

2. **"Authentication error"**: Chạy `modal token set` để cập nhật token

3. **"Out of memory"**: Giảm `num_inference_steps` hoặc sử dụng GPU nhỏ hơn

4. **"Model loading error"**: Đợi model được tải xuống lần đầu, có thể mất vài phút

### Kiểm tra logs:

```bash
modal logs text-to-image
```

### Xem trạng thái app:

```bash
modal app list
```

## Chi phí

Modal cung cấp:
- $30 miễn phí hàng tháng cho người dùng mới
- GPU A10G: khoảng $1.10/giờ
- Một hình ảnh thường mất 10-30 giây tạo ra

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

Trong `@app.function()`, thay đổi:
```python
gpu=modal.gpu.A10G()
```

Thành:
- `gpu=modal.gpu.T4()` (rẻ hơn)
- `gpu=modal.gpu.A100()` (mạnh hơn)

### Thêm features:

- Image-to-image generation
- ControlNet support
- Batch processing
- Web interface với FastAPI

## Hỗ trợ

- [Modal Documentation](https://modal.com/docs)
- [Stable Diffusion Guide](https://huggingface.co/docs/diffusers)
- [GitHub Issues](https://github.com/modal-labs/modal-client/issues)

## Lưu ý bảo mật

- Không chia sẻ Modal token
- Kiểm tra usage để tránh chi phí bất ngờ
- Sử dụng negative prompts để tránh nội dung không phù hợp

---

**Chúc bạn tạo ra những hình ảnh tuyệt vời! 🎨**