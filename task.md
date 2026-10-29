# Kế hoạch & Tiến độ Khắc phục Nhận xét Đồ án MIMO 2x2

## Mục tiêu
Khắc phục toàn diện 8 điểm số liệu/lý thuyết (Mục A), 2 vấn đề tính trung thực và đề bài (Mục B), 7 lỗi nhỏ về hình thức và đường dẫn (Mục C) theo phản hồi đánh giá đồ án.

---

## Danh sách công việc và Tiến độ

### Phần A: Hiệu chỉnh Số liệu & Lý thuyết
- [x] **A.1:** Tính toán lại chính xác mức SNR cần tại $\text{BER} = 10^{-3}$:
  - SISO: $23.97\text{ dB} \approx 24.0\text{ dB}$
  - SIMO 1x2 SC: $12.58\text{ dB} \approx 12.6\text{ dB}$ (sửa lỗi $13.5\text{ dB}$ trên slide 14)
  - SIMO 1x2 MRC: $11.09\text{ dB} \approx 11.1\text{ dB}$
  - MISO 2x1 Alamouti: $14.10\text{ dB} \approx 14.1\text{ dB}$
  - MIMO 2x2 STBC: $7.05\text{ dB}$
  - Độ lợi tiết kiệm công suất: $16.92\text{ dB} \approx 16.9\text{ dB}$ (tiết kiệm $\approx 49.2$ lần công suất phát).
- [x] **A.2:** Sửa chuẩn xác các giá trị $\sigma, \lambda$ và số điều kiện của ma trận kênh $\mathbf{H} = [0.7\ 0.3; 0.4\ 0.6]$:
  - $\lambda_1 \approx 1.01098, \lambda_2 \approx 0.08902$
  - $\sigma_1 \approx 1.00547, \sigma_2 \approx 0.29837$
  - $\kappa(\mathbf{H}) = \sigma_1 / \sigma_2 \approx 3.37$.
- [x] **A.3:** Hiệu chỉnh ngưỡng chuyển đổi Water-filling:
  - $\Delta = 1/\lambda_2 - 1/\lambda_1 = 11.233 - 0.989 = 10.244$ (tuyến tính)
  - $\text{SNR}_{th} = 10 \log_{10}(10.244) \approx 10.10\text{ dB}$ (khớp với $10.1\text{ dB}$ trên Hình 4.2).
- [x] **A.4:** Làm rõ bản chất khuếch đại nhiễu và triệt can nhiễu của tiền mã hóa SVD:
  - Lọc không gian $\mathbf{U}^H$ giữ trắng tạp âm ($\mathbf{R}_{\tilde{n}} = \sigma_n^2 \mathbf{I}$).
  - Khôi phục $\hat{x}_i = \tilde{y}_i / \sigma_i$ làm khuếch đại nhiễu kênh con 2 lên $1/\sigma_2^2 \approx 11.23$ lần (+10.5 dB).
  - Ưu thế của SVD là triệt tiêu hoàn toàn can nhiễu đa luồng (Inter-Stream Interference), kết hợp Water-filling để tắt kênh yếu ở SNR thấp.
- [x] **A.5:** Chuẩn hóa bậc phân tập của kỹ thuật ghép kênh không gian SDM:
  - SDM với bộ tách sóng tuyến tính ZF/MMSE đạt $d = N_r - N_t + 1 = 1$ ở tốc độ bit cố định.
  - Điểm $d = 0$ là điểm cực biên khi hệ thống truyền ở tốc độ ghép kênh tối đa $r = 2$.
- [x] **A.6:** Cập nhật đường đánh đổi DMT (Zheng–Tse 2003):
  - Đường gấp khúc tuyến tính từng đoạn nối 3 điểm $(0, 4) \to (1, 1) \to (2, 0)$:
    $d^*(r) = 4 - 3r$ ($0 \le r \le 1$), $d^*(r) = 2 - r$ ($1 \le r \le 2$).
- [x] **A.7:** Chuẩn hóa Bảng 3.1 và phân tích độ khớp lý thuyết - mô phỏng:
  - Ghi rõ nguồn từng cột (mô phỏng $5 \times 10^5$ bit hay công thức giải tích).
  - Đổi "khớp tuyệt đối" thành "khớp tốt", phân tích phương sai thống kê ở SNR cao ($\ge 20\text{ dB}$).
  - Làm rõ mức giảm lỗi tại $10\text{ dB}$: lý thuyết giải tích là $205.3$ lần, mẫu mô phỏng là $218.0$ lần.
- [x] **A.8:** Làm rõ phương thức điều chế:
  - QPSK sử dụng cho phần khôi phục số học từng bước (Chương 2).
  - BPSK sử dụng cho mô phỏng Monte Carlo BER (Chương 3) để đối chiếu với mô hình giải tích khép kín.

---

### Phần B: Tính Trung thực và Ngữ cảnh Đề bài
- [x] **B.1:** Minh bạch hóa kết quả mô phỏng trên terminal và tính toán số học:
  - Giải thích rõ cơ chế sai số số học máy tính trên cả hai môi trường: MATLAB đạt $\approx 2.22 \times 10^{-16}$, Python đạt $\approx 1.11 \times 10^{-16}$ (đều ở ngưỡng $\varepsilon_{\text{mach}}$).
  - Đổi tiêu đề chú thích Hình 2.3, 2.4 và Slide 11 thành: *"Kết quả mô phỏng số khôi phục tín hiệu thực thi trên môi trường tính toán"*.
  - Đồng bộ số liệu sai số giữa script, bảng số liệu và terminal visualized output.
- [x] **B.2:** Khớp nối ngữ cảnh đề tài và tài liệu hướng dẫn:
  - Nêu rõ đề tài nghiên cứu chuyên sâu MIMO 2x2 phát triển từ đề cương hướng dẫn đồ án (`Ref/Project_Instructions.pdf`, gồm P1 về kênh Rayleigh và P2 về bộ cân bằng ZF/MMSE).
  - Cập nhật chú thích trong `README.md` và Chương 1 báo cáo.

---

### Phần C: Lỗi Kỹ thuật, Hình thức & Tự động hóa
- [x] **C.1:** Bổ sung mục 4.6 (Khảo sát dung lượng ergodic trên kênh Rayleigh ngẫu nhiên) vào thân bài báo cáo Markdown; gắn đầy đủ caption cho 7 bảng biểu và đồng bộ với Danh mục Bảng biểu.
- [x] **C.2:** Khắc phục lỗi lặp từ: xóa cụm "giải tích giải tích" trong tóm tắt và đổi "độ dốc dốc đứng" thành "độ dốc lớn, suy giảm nhanh" trong `README.md`.
- [x] **C.3:** Đồng bộ phiên bản MATLAB: sửa `MATLAB R2026` thành `MATLAB R2025b` trong toàn bộ slide thuyết trình.
- [x] **C.4:** Sửa độ lợi dung lượng tại $20\text{ dB}$ trên slide 17 thành $+4.65\text{ bps/Hz}$.
- [x] **C.5:** Chuyển đổi toàn bộ đường dẫn hard-coded trong `render_terminal_captures.py`, `mimo_full_simulation.py` và `generate_slides.py` sang đường dẫn tương đối độc lập nền tảng, có font fallback.
- [x] **C.6:** Bổ sung các lệnh `assert` kiểm tra nghiêm ngặt trong `verify_all_simulations.py` (sai số khôi phục $< 10^{-12}$, tính đơn điệu BER và Capacity, $C_{WF} \ge C_{EPA}$).
- [x] **C.7:** Bổ sung đầy đủ hệ thống trích dẫn học thuật `[1]` đến `[10]` trong toàn bộ nội dung báo cáo.

---

### Kiểm tra & Xuất bản Sản phẩm
- [x] `verify_all_simulations.py`: Chạy thành công 100%, tất cả các lệnh assert đều vượt qua.
- [x] `render_terminal_captures.py`: Xuất thành công các ảnh terminal mới trong `figures/`.
- [x] `generate_slides.py`: Xuất thành công file `Slide_ThuyetTrinh_MIMO_2026.pptx`.
- [x] LibreOffice & pdftoppm: Re-generate thành công `Slide_ThuyetTrinh_MIMO_2026.pdf` và 21 ảnh PNG slide preview.
- [x] Google Chrome headless: Re-generate thành công `report/BaoCao_DoAn_MIMO_2026.pdf` (43 trang học thuật hoàn chỉnh).
- [x] Git working tree: Đã rà soát diff sạch sẽ, chuẩn bị sẵn sàng cho commit.
