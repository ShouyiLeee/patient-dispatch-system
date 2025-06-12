# Hướng dẫn sử dụng hệ thống điều phối bệnh nhân

## Cách chạy các script demo

Hệ thống cung cấp hai cách để chạy demo:

### 1. Demo đơn giản (không cần LangGraph)

```bash
python run_demo.py --mode simple
```

Demo này sẽ chạy `test_workflow_demo.py`, một phiên bản đơn giản không phụ thuộc vào thư viện LangGraph. 
Nó sẽ hiển thị hai trường hợp demo:
- Trường hợp thông thường: Bệnh nhân với các triệu chứng mức độ trung bình
- Trường hợp khẩn cấp: Bệnh nhân với các triệu chứng đe dọa tính mạng

### 2. Demo với LangGraph

```bash
python run_demo.py --mode langgraph
```

Demo này sẽ chạy `langgraph_demo.py`, sử dụng thư viện LangGraph để tạo một workflow có cấu trúc với các node và edge rõ ràng. Nó cũng sẽ hiển thị hai trường hợp demo tương tự như phiên bản đơn giản.

### 3. Tự động chọn chế độ demo

```bash
python run_demo.py
```

Chương trình sẽ tự động kiểm tra xem LangGraph đã được cài đặt chưa và chọn chế độ demo phù hợp.

## Giải thích về các thành phần

### 1. GeminiClient

`modules/gemini_client.py` là một client giả lập cho Gemini Flash 2.0, cung cấp các chức năng:
- `generate()`: Tạo ra phản hồi cho các prompt text
- `generate_image()`: Phân tích hình ảnh

### 2. Các module xử lý ban đầu

- `modules/triage_module/text_processing.py`: Trích xuất triệu chứng, mức độ ưu tiên từ mô tả
- `modules/triage_module/image_processing.py`: Phân tích ảnh y tế để tìm bất thường

### 3. Các agent điều phối

- `modules/patient_care_module/hospital_agent.py`: Tìm bệnh viện phù hợp dựa trên triệu chứng
- `modules/patient_care_module/dispatch_agent.py`: Tìm xe cứu thương gần nhất
- `modules/patient_care_module/qa_chatbot.py`: Trả lời các câu hỏi y tế
- `modules/flow_optimizer_module/flow_agent.py`: Tối ưu hóa kết quả từ các agent khác

### 4. Flow Tracking

`utils/flow_tracker.py` theo dõi và lưu lại toàn bộ quá trình xử lý thông qua các agent, giúp việc debug và phân tích hiệu quả hơn. Các log được lưu trong thư mục `flow_logs/` dưới dạng JSON.

## Các trường hợp đầu vào mẫu

Hệ thống đã được thiết kế để xử lý nhiều loại tình huống khác nhau:

### Trường hợp 1: Bệnh nhân với triệu chứng thông thường
- Mô tả: "Bệnh nhân nam, 45 tuổi, sốt cao 2 ngày, ho khan, khó thở nhẹ."
- Vị trí: 10.77, 106.67
- Chỉ số sinh tồn: Nhịp tim 98, Huyết áp 120/80, SpO2 97%

### Trường hợp 2: Bệnh nhân với triệu chứng nghiêm trọng
- Mô tả: "Bệnh nhân nam, 65 tuổi, đột ngột đau ngực dữ dội, lan ra cánh tay trái và hàm dưới, khó thở, vã mồ hôi từ 20 phút trước."
- Vị trí: 10.79, 106.70
- Chỉ số sinh tồn: Nhịp tim 110, Huyết áp 160/95, SpO2 91%

### Trường hợp 3: Bệnh nhân với triệu chứng sốc phản vệ
- Mô tả: "Bệnh nhân nữ, 25 tuổi, bất ngờ phát ban đỏ toàn thân, sưng mặt và môi, khó thở sau khi uống thuốc kháng sinh."
- Vị trí: 10.81, 106.72
- Chỉ số sinh tồn: Nhịp tim 135, Huyết áp 80/50, SpO2 88%

## Sử dụng API trong ứng dụng thực tế

Trong trường hợp thực tế, hệ thống có thể được tích hợp với:

1. **API Gemini Flash thực**: Thay thế client giả lập bằng client thực
2. **Hệ thống quản lý bệnh viện**: Để cập nhật thông tin giường bệnh và chuyên khoa
3. **Hệ thống GPS của xe cứu thương**: Để có vị trí thực tế và thời gian di chuyển chính xác
4. **Hệ thống y tế điện tử**: Để có thông tin bệnh án và tiền sử bệnh

## Giải thích về các kết quả

Kết quả cuối cùng bao gồm:

1. **Danh sách triệu chứng được trích xuất**: Từ mô tả và hình ảnh
2. **Mức độ ưu tiên**: Thang đo từ 1-5, với 5 là khẩn cấp nhất
3. **Chuyên khoa phù hợp**: Chuyên khoa y tế phù hợp với triệu chứng
4. **Bệnh viện được chọn**: Thông tin về bệnh viện phù hợp nhất 
5. **Xe cứu thương được chọn**: Thông tin về xe cứu thương gần nhất (nếu cần)
6. **Thời gian dự kiến**: Ước tính thời gian xe cứu thương đến nơi

Mọi quá trình xử lý đều được lưu lại trong các file log json trong thư mục `flow_logs/`.
