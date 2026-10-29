import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

NAVY = RGBColor(0, 43, 73)
TEAL = RGBColor(0, 168, 150)
DARK_BLUE = RGBColor(13, 59, 102)
CYAN = RGBColor(2, 128, 144)
BG_LIGHT = RGBColor(248, 249, 250)
WHITE = RGBColor(255, 255, 255)
TEXT_DARK = RGBColor(30, 41, 59)
TEXT_MUTED = RGBColor(100, 116, 139)
ACCENT_CORAL = RGBColor(230, 57, 70)
CARD_BORDER = RGBColor(226, 232, 240)
CARD_BG = RGBColor(255, 255, 255)
ROW_ALT = RGBColor(241, 245, 249)

SLIDE_WIDTH = 13.333
SLIDE_HEIGHT = 7.5

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(SLIDE_WIDTH)
    prs.slide_height = Inches(SLIDE_HEIGHT)
    blank_layout = prs.slide_layouts[6]

    figures_dir = "/home/tuong/Desktop/HK1-26-27/ETC10309_TruyenThongKhongDay/DoAn_2026/figures"

    def set_slide_background(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(SLIDE_WIDTH), Inches(SLIDE_HEIGHT))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, title, category, slide_num):
        set_slide_background(slide, BG_LIGHT)

        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.4), Inches(3.6), Inches(0.3))
        pill.fill.solid()
        pill.fill.fore_color.rgb = TEAL
        pill.line.fill.background()
        tf_pill = pill.text_frame
        tf_pill.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_pill = tf_pill.paragraphs[0]
        p_pill.text = category.upper()
        p_pill.font.name = "Arial"
        p_pill.font.size = Pt(9.5)
        p_pill.font.bold = True
        p_pill.font.color.rgb = WHITE
        p_pill.alignment = PP_ALIGN.CENTER

        tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.733), Inches(0.55))
        tf = tx_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(20)
        p.font.bold = True
        p.font.color.rgb = NAVY

        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.3), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = CARD_BORDER
        line.line.fill.background()

        f_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.3))
        tf_f = f_box.text_frame
        p_f = tf_f.paragraphs[0]
        p_f.text = f"Trường ĐH Khoa học Tự nhiên - ĐHQG TP.HCM | Khoa ĐTVT  •  Đồ án MIMO 2x2 (ETC10309)  •  Trang {slide_num} / 21"
        p_f.font.name = "Arial"
        p_f.font.size = Pt(9)
        p_f.font.color.rgb = TEXT_MUTED

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1)
        return shape

    def add_card_header(slide, left, top, width, height, title, color=NAVY):
        add_card(slide, left, top, width, height)
        hb = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(0.42))
        hb.fill.solid()
        hb.fill.fore_color.rgb = color
        hb.line.fill.background()
        tf = hb.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = f"  {title.upper()}"
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.LEFT

    def add_stat_tile(slide, left, top, width, height, label, value, subtext, color=TEAL):
        add_card(slide, left, top, width, height)
        tb = slide.shapes.add_textbox(Inches(left), Inches(top + 0.08), Inches(width), Inches(height - 0.16))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = label.upper()
        p1.font.name = "Arial"
        p1.font.size = Pt(9)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_MUTED
        p1.alignment = PP_ALIGN.CENTER

        p2 = tf.add_paragraph()
        p2.text = value
        p2.font.name = "Arial"
        p2.font.size = Pt(22)
        p2.font.bold = True
        p2.font.color.rgb = color
        p2.alignment = PP_ALIGN.CENTER

        p3 = tf.add_paragraph()
        p3.text = subtext
        p3.font.name = "Arial"
        p3.font.size = Pt(9.5)
        p3.font.color.rgb = TEXT_DARK
        p3.alignment = PP_ALIGN.CENTER

    def add_bullet_points(tf, items, font_size=11, space_after=6, text_color=TEXT_DARK):
        for idx, item in enumerate(items):
            p = tf.add_paragraph() if (idx > 0 or len(tf.paragraphs[0].text) > 0) else tf.paragraphs[0]
            p.text = f"•  {item}"
            p.font.name = "Arial"
            p.font.size = Pt(font_size)
            p.font.color.rgb = text_color
            p.space_after = Pt(space_after)

    def add_table_data(slide, left, top, width, height, headers, rows, col_widths=None):
        rows_count = len(rows) + 1
        cols_count = len(headers)
        table_shape = slide.shapes.add_table(rows_count, cols_count, Inches(left), Inches(top), Inches(width), Inches(height))
        table = table_shape.table
        if col_widths:
            for idx, w in enumerate(col_widths):
                table.columns[idx].width = Inches(w)
        for c_idx, header in enumerate(headers):
            cell = table.cell(0, c_idx)
            cell.text = header
            cell.fill.solid()
            cell.fill.fore_color.rgb = NAVY
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.font.name = "Arial"
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = WHITE
            p.alignment = PP_ALIGN.CENTER
        for r_idx, row in enumerate(rows):
            bg = ROW_ALT if r_idx % 2 == 0 else WHITE
            for c_idx, val in enumerate(row):
                cell = table.cell(r_idx + 1, c_idx)
                cell.text = str(val)
                cell.fill.solid()
                cell.fill.fore_color.rgb = bg
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                p = cell.text_frame.paragraphs[0]
                p.font.name = "Arial"
                p.font.size = Pt(9.5)
                p.font.color.rgb = TEXT_DARK
                p.alignment = PP_ALIGN.CENTER
        return table_shape

    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1, NAVY)

    top_bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(SLIDE_WIDTH), Inches(0.12))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = TEAL
    top_bar.line.fill.background()

    tb1_top = slide1.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.733), Inches(0.9))
    tf1_top = tb1_top.text_frame
    p1_1 = tf1_top.paragraphs[0]
    p1_1.text = "ĐẠI HỌC QUỐC GIA TP. HỒ CHÍ MINH  •  TRƯỜNG ĐẠI HỌC KHOA HỌC TỰ NHIÊN"
    p1_1.font.name = "Arial"
    p1_1.font.size = Pt(11)
    p1_1.font.bold = True
    p1_1.font.color.rgb = TEAL

    p1_2 = tf1_top.add_paragraph()
    p1_2.text = "KHOA ĐIỆN TỬ – VIỄN THÔNG  |  BỘ MÔN VIỄN THÔNG VÀ MẠNG"
    p1_2.font.name = "Arial"
    p1_2.font.size = Pt(10)
    p1_2.font.color.rgb = WHITE

    pill1 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.8), Inches(0.36))
    pill1.fill.solid()
    pill1.fill.fore_color.rgb = DARK_BLUE
    pill1.line.color.rgb = TEAL
    pill1.line.width = Pt(1)
    tf1_pill = pill1.text_frame
    tf1_pill.vertical_anchor = MSO_ANCHOR.MIDDLE
    p1_pill = tf1_pill.paragraphs[0]
    p1_pill.text = "BÁO CÁO ĐỒ ÁN MÔN HỌC: TRUYỀN THÔNG KHÔNG DÂY (ETC10309)"
    p1_pill.font.name = "Arial"
    p1_pill.font.size = Pt(10.5)
    p1_pill.font.bold = True
    p1_pill.font.color.rgb = TEAL
    p1_pill.alignment = PP_ALIGN.CENTER

    tb1_main = slide1.shapes.add_textbox(Inches(0.8), Inches(2.2), Inches(11.733), Inches(1.8))
    tf1_main = tb1_main.text_frame
    tf1_main.word_wrap = True
    p1_m1 = tf1_main.paragraphs[0]
    p1_m1.text = "THIẾT KẾ VÀ MÔ PHỎNG HỆ THỐNG MIMO 2x2"
    p1_m1.font.name = "Arial"
    p1_m1.font.size = Pt(32)
    p1_m1.font.bold = True
    p1_m1.font.color.rgb = WHITE
    p1_m1.space_after = Pt(8)

    p1_m2 = tf1_main.add_paragraph()
    p1_m2.text = "Nghiên cứu Kỹ thuật Phân tập Không - Thời gian STBC Alamouti và Ghép kênh Không gian SDM"
    p1_m2.font.name = "Arial"
    p1_m2.font.size = Pt(17)
    p1_m2.font.color.rgb = TEAL

    c1_1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(4.3), Inches(5.7), Inches(2.0))
    c1_1.fill.solid()
    c1_1.fill.fore_color.rgb = DARK_BLUE
    c1_1.line.color.rgb = TEAL
    c1_1.line.width = Pt(1)
    tf1_c1 = c1_1.text_frame
    tf1_c1.word_wrap = True
    p1_c1_h = tf1_c1.paragraphs[0]
    p1_c1_h.text = "GIẢNG VIÊN HƯỚNG DẪN"
    p1_c1_h.font.name = "Arial"
    p1_c1_h.font.size = Pt(11)
    p1_c1_h.font.bold = True
    p1_c1_h.font.color.rgb = TEAL
    p1_c1_h.space_after = Pt(8)

    p1_c1_t1 = tf1_c1.add_paragraph()
    p1_c1_t1.text = "•  TS. Đặng Lê Khoa"
    p1_c1_t1.font.name = "Arial"
    p1_c1_t1.font.size = Pt(13)
    p1_c1_t1.font.bold = True
    p1_c1_t1.font.color.rgb = WHITE
    p1_c1_t1.space_after = Pt(4)

    p1_c1_t2 = tf1_c1.add_paragraph()
    p1_c1_t2.text = "•  CN. Nguyễn Dũng"
    p1_c1_t2.font.name = "Arial"
    p1_c1_t2.font.size = Pt(13)
    p1_c1_t2.font.bold = True
    p1_c1_t2.font.color.rgb = WHITE

    c1_2 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(4.3), Inches(5.733), Inches(2.0))
    c1_2.fill.solid()
    c1_2.fill.fore_color.rgb = DARK_BLUE
    c1_2.line.color.rgb = TEAL
    c1_2.line.width = Pt(1)
    tf1_c2 = c1_2.text_frame
    tf1_c2.word_wrap = True
    p1_c2_h = tf1_c2.paragraphs[0]
    p1_c2_h.text = "SINH VIÊN THỰC HIỆN"
    p1_c2_h.font.name = "Arial"
    p1_c2_h.font.size = Pt(11)
    p1_c2_h.font.bold = True
    p1_c2_h.font.color.rgb = TEAL
    p1_c2_h.space_after = Pt(8)

    p1_c2_t1 = tf1_c2.add_paragraph()
    p1_c2_t1.text = "•  Họ và tên: Lê Ngọc Tường"
    p1_c2_t1.font.name = "Arial"
    p1_c2_t1.font.size = Pt(13)
    p1_c2_t1.font.bold = True
    p1_c2_t1.font.color.rgb = WHITE
    p1_c2_t1.space_after = Pt(4)

    p1_c2_t2 = tf1_c2.add_paragraph()
    p1_c2_t2.text = "•  MSSV: 22207044  —  Lớp: 22DTV_CLC1"
    p1_c2_t2.font.name = "Arial"
    p1_c2_t2.font.size = Pt(12)
    p1_c2_t2.font.color.rgb = WHITE

    tb1_bot = slide1.shapes.add_textbox(Inches(0.8), Inches(6.8), Inches(11.733), Inches(0.4))
    tf1_bot = tb1_bot.text_frame
    p1_b = tf1_bot.paragraphs[0]
    p1_b.text = "Thành phố Hồ Chí Minh, Tháng 10 Năm 2026"
    p1_b.font.name = "Arial"
    p1_b.font.size = Pt(10)
    p1_b.font.color.rgb = TEXT_MUTED
    p1_b.alignment = PP_ALIGN.CENTER

    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "Mục tiêu Nghiên cứu và Yêu cầu Kỹ thuật Đề tài P6", "Tổng quan đề tài", 2)

    add_card_header(slide2, 0.8, 1.5, 5.7, 3.8, "Mục tiêu cốt lõi của đề tài", NAVY)
    tb2_left = slide2.shapes.add_textbox(Inches(0.9), Inches(2.0), Inches(5.5), Inches(3.2))
    tf2_left = tb2_left.text_frame
    tf2_left.word_wrap = True
    items2_left = [
        "Khảo sát giải tích số học trên ma trận kênh thực nghiệm cố định H = [0.7 0.3; 0.4 0.6] truyền 2 ký hiệu QPSK s0 = 1+j, s1 = 1-j.",
        "Phân tích chuyên sâu 2 kỹ thuật nền tảng: STBC Alamouti (tối đa hóa độ tin cậy) và SDM Ghép kênh không gian (tối đa hóa tốc độ).",
        "Khảo sát toàn diện hiệu năng thống kê: Đánh giá BER qua 2x10^5 bit Monte Carlo và Dung lượng Shannon-Telatar trên kênh Rayleigh.",
        "Xác thực tính đúng đắn: Đối chiếu chặt chẽ giữa công thức giải tích lý thuyết và mô phỏng thực nghiệm trên MATLAB & Python."
    ]
    add_bullet_points(tf2_left, items2_left, 11, 7)

    add_card_header(slide2, 6.833, 1.5, 5.7, 3.8, "Ràng buộc kỹ thuật & Phương pháp luận", DARK_BLUE)
    tb2_right = slide2.shapes.add_textbox(Inches(6.933), Inches(2.0), Inches(5.5), Inches(3.2))
    tf2_right = tb2_right.text_frame
    tf2_right.word_wrap = True
    items2_right = [
        "Mô hình hệ thống: 2 anten phát (Tx1, Tx2) và 2 anten thu (Rx1, Rx2).",
        "Môi trường vô tuyến: Kênh fading phẳng Rayleigh biến đổi chậm (quasi-static) cộng nhiễu tạp âm trắng Gauss (AWGN).",
        "Độ chính xác thuật toán: Chứng minh giải tích triệt can nhiễu, sai số khôi phục đạt mức epsilon máy tính (< 1e-15).",
        "Kiểm chứng độc lập: Xây dựng đồng thời hai bộ mã nguồn kiểm chứng chéo trên MATLAB R2026 và Python 3.12 (NumPy/SciPy)."
    ]
    add_bullet_points(tf2_right, items2_right, 11, 7)

    add_stat_tile(slide2, 0.8, 5.5, 3.7, 1.3, "Bậc phân tập tối đa", "d = 4", "MIMO 2x2 STBC tiết kiệm 16.5 dB công suất", TEAL)
    add_stat_tile(slide2, 4.816, 5.5, 3.7, 1.3, "Ghép kênh song song", "r = 2 luồng", "Nhân đôi hiệu suất phổ bps/Hz không tốn băng thông", CYAN)
    add_stat_tile(slide2, 8.833, 5.5, 3.7, 1.3, "Ngưỡng Water-filling", "10.15 dB", "Chuyển mượt từ Beamforming sang Ghép kênh", NAVY)

    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "Kiến trúc Tổng quan Mô hình Hệ thống MIMO 2x2", "Kiến trúc hệ thống", 3)

    b3 = add_card(slide3, 0.8, 1.5, 11.733, 0.8, WHITE, TEAL)
    tb3_top = slide3.shapes.add_textbox(Inches(0.9), Inches(1.55), Inches(11.533), Inches(0.7))
    tf3_top = tb3_top.text_frame
    p3_t = tf3_top.paragraphs[0]
    p3_t.text = "Mô hình toán học tổng quát:   y = H x + n   với   H ∈ C^(2x2),  x ∈ C^(2x1),  y ∈ C^(2x1),  n ~ CN(0, σ_n^2 I_2)"
    p3_t.font.name = "Arial"
    p3_t.font.size = Pt(13)
    p3_t.font.bold = True
    p3_t.font.color.rgb = NAVY
    p3_t.alignment = PP_ALIGN.CENTER

    add_card_header(slide3, 0.8, 2.5, 3.7, 4.3, "1. Khối phát (Transmitter)", NAVY)
    tb3_c1 = slide3.shapes.add_textbox(Inches(0.9), Inches(3.0), Inches(3.5), Inches(3.6))
    tf3_c1 = tb3_c1.text_frame
    tf3_c1.word_wrap = True
    items3_c1 = [
        "Bộ điều chế số: Ánh xạ luồng bit nhị phân thành các ký hiệu phức (QPSK / 4-QAM).",
        "Bộ xử lý không - thời gian: Phân chia luồng song song (SDM Demux) hoặc Mã hóa ma trận liên khe (STBC Encoder).",
        "Ràng buộc công suất tổng cộng: E[||x||^2] = P_t (chia đều P_t/2 mỗi anten).",
        "Mảng anten phát: Tx1 và Tx2 bức xạ độc lập vào không gian vô tuyến."
    ]
    add_bullet_points(tf3_c1, items3_c1, 10.5, 6)

    add_card_header(slide3, 4.816, 2.5, 3.7, 4.3, "2. Kênh truyền không gian", DARK_BLUE)
    tb3_c2 = slide3.shapes.add_textbox(Inches(4.916), Inches(3.0), Inches(3.5), Inches(3.6))
    tf3_c2 = tb3_c2.text_frame
    tf3_c2.word_wrap = True
    items3_c2 = [
        "Ma trận kênh H: Chứa 4 hệ số suy hao phức h_ij từ anten phát j đến anten thu i.",
        "Kênh cố định thực nghiệm: H = [0.7 0.3; 0.4 0.6] dùng kiểm chứng giải tích từng bước.",
        "Kênh ngẫu nhiên: Fading Rayleigh biến đổi chậm mô phỏng đa đường không có tầm nhìn thẳng (NLOS).",
        "Tạp âm AWGN: Nhiễu nhiệt tại các nhánh thu độc lập thống kê."
    ]
    add_bullet_points(tf3_c2, items3_c2, 10.5, 6)

    add_card_header(slide3, 8.833, 2.5, 3.7, 4.3, "3. Khối thu (Receiver)", TEAL)
    tb3_c3 = slide3.shapes.add_textbox(Inches(8.933), Inches(3.0), Inches(3.5), Inches(3.6))
    tf3_c3 = tb3_c3.text_frame
    tf3_c3.word_wrap = True
    items3_c3 = [
        "Mảng anten thu: Rx1 và Rx2 đón nhận tín hiệu chồng lấn y1, y2.",
        "Bộ ước lượng kênh (CSI): Cung cấp ma trận H chính xác cho bộ giải mã.",
        "Bộ tách tín hiệu: Bộ kết hợp trực giao (STBC Combiner) hoặc Bộ cân bằng (ZF, MMSE, SVD).",
        "Giải điều chế và Quyết định: Khôi phục chuỗi bit nhị phân ban đầu."
    ]
    add_bullet_points(tf3_c3, items3_c3, 10.5, 6)

    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "Khảo sát Đặc tính Đại số Ma trận Kênh Thực nghiệm H", "Kênh truyền thực nghiệm", 4)

    add_card_header(slide4, 0.8, 1.5, 5.7, 5.3, "Các thông số đại số ma trận H", NAVY)
    tb4_left = slide4.shapes.add_textbox(Inches(0.9), Inches(2.0), Inches(5.5), Inches(4.6))
    tf4_left = tb4_left.text_frame
    tf4_left.word_wrap = True
    items4_left = [
        "Ma trận kênh khảo sát: H = [0.7 0.3; 0.4 0.6]",
        "Định thức (Determinant): det(H) = (0.7)(0.6) - (0.3)(0.4) = 0.42 - 0.12 = 0.30 ≠ 0",
        "Hạng ma trận (Rank): Rank(H) = 2 (Full-rank, ma trận khả nghịch hoàn toàn).",
        "Chuẩn Frobenius bình phương: ||H||_F^2 = 0.7^2 + 0.3^2 + 0.4^2 + 0.6^2 = 1.10",
        "Phân rã giá trị kỳ dị (SVD): σ_1 ≈ 1.00596,  σ_2 ≈ 0.29671",
        "Trị riêng của H^H H: λ_1 = σ_1^2 = 1.01196,  λ_2 = σ_2^2 = 0.08804 (Tổng λ_1 + λ_2 = 1.10)",
        "Số điều kiện (Condition Number): κ(H) = σ_1 / σ_2 = 3.3904 (10.60 dB)"
    ]
    add_bullet_points(tf4_left, items4_left, 11, 8)

    add_card_header(slide4, 6.833, 1.5, 5.7, 5.3, "Ý nghĩa vật lý & Tác động kỹ thuật", DARK_BLUE)
    tb4_right = slide4.shapes.add_textbox(Inches(6.933), Inches(2.0), Inches(5.5), Inches(4.6))
    tf4_right = tb4_right.text_frame
    tf4_right.word_wrap = True
    items4_right = [
        "Đánh giá tính ổn định số học: Số điều kiện κ(H) = 3.39 ở mức vừa phải, chứng minh ma trận kênh truyền không bị suy biến nghiêm trọng (well-conditioned).",
        "Bất đối xứng năng lượng kênh: Kênh con thứ nhất (λ_1 = 1.012) có độ lợi năng lượng gấp 11.5 lần kênh con thứ hai (λ_2 = 0.088).",
        "Khả năng thích ứng STBC: Khai thác trọn vẹn tổng năng lượng cả 4 đường truyền với ||H||_F^2 = 1.10, đảm bảo phân tập tối đa.",
        "Dự báo tách sóng SDM: Do σ_2 khá nhỏ, phép nghịch đảo ma trận trong giải thuật Zero-Forcing sẽ gây ra hiện tượng khuếch đại nhiễu trên luồng thứ hai.",
        "Tiền đề cho Water-filling: Sự chênh lệch độ sâu 1/σ_2^2 - 1/σ_1^2 là cơ sở hình thành ngưỡng chuyển tiếp chế độ Beamforming sang SDM."
    ]
    add_bullet_points(tf4_right, items4_right, 11, 7)

    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "Kỹ thuật STBC Alamouti 2x2: Nguyên lý và Cấu trúc Mã hóa", "Phân tích STBC", 5)

    b5_top = add_card(slide5, 0.8, 1.5, 11.733, 1.1, WHITE, TEAL)
    tb5_top = slide5.shapes.add_textbox(Inches(0.9), Inches(1.55), Inches(11.533), Inches(1.0))
    tf5_top = tb5_top.text_frame
    tf5_top.word_wrap = True
    p5_t1 = tf5_top.paragraphs[0]
    p5_t1.text = "NGUYÊN LÝ PHÁT MÃ HÓA KHÔNG GIAN – THỜI GIAN ALAMOUTI (1998)"
    p5_t1.font.name = "Arial"
    p5_t1.font.size = Pt(11)
    p5_t1.font.bold = True
    p5_t1.font.color.rgb = TEAL
    p5_t2 = tf5_top.add_paragraph()
    p5_t2.text = "• Phát 2 ký hiệu phức s0, s1 qua 2 anten phát trên 2 khe thời gian liên tiếp. Tốc độ mã hóa đạt R = 1 ký hiệu / khe (Full rate).\n• Khối phát hoàn toàn không cần biết trước thông tin kênh truyền (CSIT-free), chỉ cần CSIR tại khối thu."
    p5_t2.font.name = "Arial"
    p5_t2.font.size = Pt(10.5)
    p5_t2.font.color.rgb = TEXT_DARK

    add_card_header(slide5, 0.8, 2.8, 5.7, 4.0, "Cấu trúc ma trận mã hóa S", NAVY)
    tb5_left = slide5.shapes.add_textbox(Inches(0.9), Inches(3.3), Inches(5.5), Inches(3.3))
    tf5_left = tb5_left.text_frame
    tf5_left.word_wrap = True
    items5_left = [
        "Ma trận phát Alamouti: S = [ s0  -s1* ;  s1   s0* ]",
        "Khe thời gian t (Cột 1): Anten Tx1 phát s0, Anten Tx2 phát s1.",
        "Khe thời gian t+Ts (Cột 2): Anten Tx1 phát -s1*, Anten Tx2 phát s0*.",
        "Ràng buộc năng lượng: Mỗi anten phát công suất trung bình P_t/2 để tổng công suất phát bằng P_t như hệ thống SISO.",
        "Không suy giảm tốc độ: Truyền trọn vẹn 2 ký hiệu trong 2 khe thời gian, tốc độ tương đương hệ thống anten đơn."
    ]
    add_bullet_points(tf5_left, items5_left, 11, 7)

    add_card_header(slide5, 6.833, 2.8, 5.7, 4.0, "Tính trực giao tuyệt đối & Độ lợi", DARK_BLUE)
    tb5_right = slide5.shapes.add_textbox(Inches(6.933), Inches(3.3), Inches(5.5), Inches(3.3))
    tf5_right = tb5_right.text_frame
    tf5_right.word_wrap = True
    items5_right = [
        "Trực giao giữa hai cột của ma trận phát S:\n  <col1, col2> = s0(-s1*)* + s1(s0*)* = -s0 s1 + s1 s0 = 0",
        "Quan hệ Gram trực giao:\n  S S^H = (|s0|^2 + |s1|^2) I_2",
        "Bậc phân tập cực đại: Đạt bậc d = Nt * Nr = 2 * 2 = 4 khi kết hợp 2 anten thu.",
        "Giải mã vô hướng đơn giản: Bộ thu chỉ cần thực hiện các phép nhân tuyến tính ma trận để tách độc lập từng ký hiệu, triệt tiêu hoàn toàn can nhiễu đa anten mà không cần đảo ma trận."
    ]
    add_bullet_points(tf5_right, items5_right, 11, 7)

    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "Tính toán Lý thuyết Số học Chi tiết Tín hiệu Nhận r0, r1, r2, r3", "Phân tích STBC", 6)

    b6_top = add_card(slide6, 0.8, 1.45, 11.733, 0.7, WHITE, TEAL)
    tb6_top = slide6.shapes.add_textbox(Inches(0.9), Inches(1.5), Inches(11.533), Inches(0.6))
    tf6_top = tb6_top.text_frame
    p6_t = tf6_top.paragraphs[0]
    p6_t.text = "Đầu vào kiểm chứng:  s0 = 1 + 1j,  s1 = 1 - 1j   ⇒   s0* = 1 - 1j,  s1* = 1 + 1j   (Kênh H = [0.7 0.3; 0.4 0.6])"
    p6_t.font.name = "Arial"
    p6_t.font.size = Pt(12)
    p6_t.font.bold = True
    p6_t.font.color.rgb = NAVY
    p6_t.alignment = PP_ALIGN.CENTER

    add_card_header(slide6, 0.8, 2.3, 5.7, 2.1, "Anten Rx1 — Khe thời gian 1 (r0)", NAVY)
    tb6_c1 = slide6.shapes.add_textbox(Inches(0.9), Inches(2.75), Inches(5.5), Inches(1.5))
    tf6_c1 = tb6_c1.text_frame
    tf6_c1.word_wrap = True
    items6_c1 = [
        "Công thức: r0 = h11 s0 + h12 s1 + n0",
        "Thay số: r0 = 0.7(1 + 1j) + 0.3(1 - 1j) = 0.7 + 0.7j + 0.3 - 0.3j",
        "Kết quả lý thuyết: r0 = 1.0 + 0.4j"
    ]
    add_bullet_points(tf6_c1, items6_c1, 10.5, 4)

    add_card_header(slide6, 6.833, 2.3, 5.7, 2.1, "Anten Rx1 — Khe thời gian 2 (r1)", DARK_BLUE)
    tb6_c2 = slide6.shapes.add_textbox(Inches(6.933), Inches(2.75), Inches(5.5), Inches(1.5))
    tf6_c2 = tb6_c2.text_frame
    tf6_c2.word_wrap = True
    items6_c2 = [
        "Công thức: r1 = -h11 s1* + h12 s0* + n1",
        "Thay số: r1 = -0.7(1 + 1j) + 0.3(1 - 1j) = -0.7 - 0.7j + 0.3 - 0.3j",
        "Kết quả lý thuyết: r1 = -0.4 - 1.0j   (Lấy liên hợp: r1* = -0.4 + 1.0j)"
    ]
    add_bullet_points(tf6_c2, items6_c2, 10.5, 4)

    add_card_header(slide6, 0.8, 4.6, 5.7, 2.1, "Anten Rx2 — Khe thời gian 1 (r2)", DARK_BLUE)
    tb6_c3 = slide6.shapes.add_textbox(Inches(0.9), Inches(5.05), Inches(5.5), Inches(1.5))
    tf6_c3 = tb6_c3.text_frame
    tf6_c3.word_wrap = True
    items6_c3 = [
        "Công thức: r2 = h21 s0 + h22 s1 + n2",
        "Thay số: r2 = 0.4(1 + 1j) + 0.6(1 - 1j) = 0.4 + 0.4j + 0.6 - 0.6j",
        "Kết quả lý thuyết: r2 = 1.0 - 0.2j"
    ]
    add_bullet_points(tf6_c3, items6_c3, 10.5, 4)

    add_card_header(slide6, 6.833, 4.6, 5.7, 2.1, "Anten Rx2 — Khe thời gian 2 (r3)", TEAL)
    tb6_c4 = slide6.shapes.add_textbox(Inches(6.933), Inches(5.05), Inches(5.5), Inches(1.5))
    tf6_c4 = tb6_c4.text_frame
    tf6_c4.word_wrap = True
    items6_c4 = [
        "Công thức: r3 = -h21 s1* + h22 s0* + n3",
        "Thay số: r3 = -0.4(1 + 1j) + 0.6(1 - 1j) = -0.4 - 0.4j + 0.6 - 0.6j",
        "Kết quả lý thuyết: r3 = 0.2 - 1.0j   (Lấy liên hợp: r3* = 0.2 + 1.0j)"
    ]
    add_bullet_points(tf6_c4, items6_c4, 10.5, 4)

    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "Bộ Tách Tín hiệu STBC Alamouti & Kiểm chứng Khôi phục Tín hiệu", "Phân tích STBC", 7)

    add_card_header(slide7, 0.8, 1.5, 5.5, 5.3, "Chứng minh toán học khôi phục ký hiệu", NAVY)
    tb7_left = slide7.shapes.add_textbox(Inches(0.9), Inches(2.0), Inches(5.3), Inches(4.6))
    tf7_left = tb7_left.text_frame
    tf7_left.word_wrap = True
    items7_left = [
        "Vector quan sát mở rộng: r_eff = [r0, r1*, r2, r3*]^T",
        "Ma trận kênh hiệu dụng H_eff (kích thước 4x2):\n  H_eff = [0.7 0.3; 0.3 -0.7; 0.4 0.6; 0.6 -0.4]",
        "Kiểm tra tính trực giao hoàn hảo:\n  H_eff^H H_eff = [1.10  0 ;  0  1.10] = ||H||_F^2 I_2",
        "Tín hiệu ngõ ra bộ kết hợp z_tilde = H_eff^H r_eff:\n  z0 = 0.7(1.0+0.4j) + 0.3(-0.4+1.0j) + 0.4(1.0-0.2j) + 0.6(0.2+1.0j) = 1.10 + 1.10j\n  z1 = 0.3(1.0+0.4j) - 0.7(-0.4+1.0j) + 0.6(1.0-0.2j) - 0.4(0.2+1.0j) = 1.10 - 1.10j",
        "Khôi phục bằng chuẩn hóa ||H||_F^2 = 1.10:\n  s0_hat = z0 / 1.10 = 1.0 + 1.0j = s0\n  s1_hat = z1 / 1.10 = 1.0 - 1.0j = s1",
        "Sai số số học thực tế máy tính:\n  |s0_hat - s0| = 1.11e-16,   |s1_hat - s1| = 1.11e-16 (Tuyệt đối)"
    ]
    add_bullet_points(tf7_left, items7_left, 10, 6)

    add_card_header(slide7, 6.6, 1.5, 5.933, 5.3, "Hình ảnh mô phỏng chòm sao tín hiệu", DARK_BLUE)
    fig1_path = os.path.join(figures_dir, "fig1_stbc_signal_recovery.png")
    if os.path.exists(fig1_path):
        slide7.shapes.add_picture(fig1_path, Inches(6.75), Inches(2.2), width=Inches(5.633))
    tb7_cap = slide7.shapes.add_textbox(Inches(6.75), Inches(5.9), Inches(5.633), Inches(0.7))
    tf7_cap = tb7_cap.text_frame
    tf7_cap.word_wrap = True
    p7_c = tf7_cap.paragraphs[0]
    p7_c.text = "Hình 2.1: Quá trình khôi phục ký hiệu và chòm sao tín hiệu STBC Alamouti (Sai số máy tính = 1.11 x 10^-16)."
    p7_c.font.name = "Arial"
    p7_c.font.size = Pt(9.5)
    p7_c.font.color.rgb = TEXT_MUTED
    p7_c.alignment = PP_ALIGN.CENTER

    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "Kỹ thuật Ghép kênh Không gian SDM: Nguyên lý và Tách sóng", "Phân tích SDM", 8)

    b8_top = add_card(slide8, 0.8, 1.5, 11.733, 1.0, WHITE, TEAL)
    tb8_top = slide8.shapes.add_textbox(Inches(0.9), Inches(1.55), Inches(11.533), Inches(0.9))
    tf8_top = tb8_top.text_frame
    tf8_top.word_wrap = True
    p8_t1 = tf8_top.paragraphs[0]
    p8_t1.text = "NGUYÊN LÝ GHÉP KÊNH PHÂN CHIA THEO KHÔNG GIAN (SPATIAL DIVISION MULTIPLEXING)"
    p8_t1.font.name = "Arial"
    p8_t1.font.size = Pt(11)
    p8_t1.font.bold = True
    p8_t1.font.color.rgb = TEAL
    p8_t2 = tf8_top.add_paragraph()
    p8_t2.text = "• Phát đồng thời 2 luồng dữ liệu độc lập x = [s0, s1]^T trên cùng dải tần số. Nâng tốc độ truyền lên gấp 2 lần mà không cần mở rộng băng thông.\n• Tín hiệu nhận tại 2 anten thu (chưa nhiễu): y = H x = [0.7 0.3; 0.4 0.6] [1+1j; 1-1j]^T = [1.0 + 0.4j; 1.0 - 0.2j]^T."
    p8_t2.font.name = "Arial"
    p8_t2.font.size = Pt(10)
    p8_t2.font.color.rgb = TEXT_DARK

    add_card_header(slide8, 0.8, 2.7, 3.7, 4.1, "1. Zero-Forcing (ZF)", NAVY)
    tb8_c1 = slide8.shapes.add_textbox(Inches(0.9), Inches(3.2), Inches(3.5), Inches(3.4))
    tf8_c1 = tb8_c1.text_frame
    tf8_c1.word_wrap = True
    items8_c1 = [
        "Ma trận cân bằng: W_zf = H^-1 = (H^H H)^-1 H^H",
        "Triệt tiêu can nhiễu: W_zf H = I_2, tách biệt hoàn toàn 2 luồng tín hiệu phát.",
        "Ưu điểm: Thuật toán đơn giản, không cần biết trước tỷ số tín hiệu trên nhiễu (SNR).",
        "Nhược điểm: Gây khuếch đại tạp âm lớn ở các kênh con có giá trị kỳ dị bé."
    ]
    add_bullet_points(tf8_c1, items8_c1, 10.5, 6)

    add_card_header(slide8, 4.816, 2.7, 3.7, 4.1, "2. Cân bằng MMSE", DARK_BLUE)
    tb8_c2 = slide8.shapes.add_textbox(Inches(4.916), Inches(3.2), Inches(3.5), Inches(3.4))
    tf8_c2 = tb8_c2.text_frame
    tf8_c2.word_wrap = True
    items8_c2 = [
        "Ma trận cân bằng: W_mmse = (H^H H + σ_n^2 I)^-1 H^H",
        "Tối ưu hóa Wiener: Giảm thiểu sai số toàn phương trung bình E[||x_hat - x||^2].",
        "Cân bằng thông minh: Chấp nhận một lượng can nhiễu dư nhỏ để kìm hãm sự bùng nổ của tạp âm ở SNR thấp.",
        "Tiệm cận: Khi SNR cao (σ_n^2 → 0), MMSE hội tụ hoàn toàn về bộ tách sóng ZF."
    ]
    add_bullet_points(tf8_c2, items8_c2, 10.5, 6)

    add_card_header(slide8, 8.833, 2.7, 3.7, 4.1, "3. Tiền mã hóa SVD", TEAL)
    tb8_c3 = slide8.shapes.add_textbox(Inches(8.933), Inches(3.2), Inches(3.5), Inches(3.4))
    tf8_c3 = tb8_c3.text_frame
    tf8_c3.word_wrap = True
    items8_c3 = [
        "Phân rã kênh: H = U Σ V^H",
        "Phát tiền mã hóa: x_tx = V x",
        "Thu lọc không gian: y_tilde = U^H y = Σ x + n_tilde",
        "Kênh trực giao song song: Chuyển đổi thành 2 kênh con độc lập tuyệt đối.",
        "Ưu thế vượt trội: Hoàn toàn không gây khuếch đại tạp âm, song đòi hỏi cả CSIT và CSIR."
    ]
    add_bullet_points(tf8_c3, items8_c3, 10.5, 6)

    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "Tách sóng SDM Zero-Forcing: Khôi phục Tín hiệu & Khuếch đại Nhiễu", "Phân tích SDM", 9)

    add_card_header(slide9, 0.8, 1.5, 5.7, 5.3, "Giải thuật tách sóng ZF & Khôi phục", NAVY)
    tb9_left = slide9.shapes.add_textbox(Inches(0.9), Inches(2.0), Inches(5.5), Inches(4.6))
    tf9_left = tb9_left.text_frame
    tf9_left.word_wrap = True
    items9_left = [
        "Vì det(H) = 0.30 ≠ 0, ma trận nghịch đảo giải tích là:\n  W_zf = H^-1 = (1 / 0.30) [0.6 -0.3 ; -0.4 0.7] = [2.0 -1.0 ; -1.3333 2.3333]",
        "Tín hiệu ước lượng sau tách sóng x_hat = W_zf y:\n  x_hat = [2.0 -1.0 ; -1.3333 2.3333] [1.0 + 0.4j ; 1.0 - 0.2j]^T",
        "Tính toán chi tiết từng luồng dữ liệu:\n  x0_hat = 2.0(1.0 + 0.4j) - 1.0(1.0 - 0.2j) = 1.0 + 1.0j = s0\n  x1_hat = -1.3333(1.0 + 0.4j) + 2.3333(1.0 - 0.2j) = 1.0 - 1.0j = s1",
        "Sai số khôi phục số học máy tính:\n  ||x_hat - x||_2 = 1.05e-15 (Khôi phục chính xác tuyệt đối không nhiễu)."
    ]
    add_bullet_points(tf9_left, items9_left, 10.5, 7)

    add_card_header(slide9, 6.833, 1.5, 5.7, 5.3, "Bản chất hiện tượng khuếch đại nhiễu", DARK_BLUE)
    tb9_right = slide9.shapes.add_textbox(Inches(6.933), Inches(2.0), Inches(5.5), Inches(4.6))
    tf9_right = tb9_right.text_frame
    tf9_right.word_wrap = True
    items9_right = [
        "Khi có tạp âm AWGN n:\n  x_hat = W_zf (H x + n) = x + W_zf n = x + n_tilde",
        "Ma trận hiệp phương sai tạp âm sau tách sóng:\n  R_n_tilde = σ_n^2 (H^H H)^-1 = σ_n^2 [5.000  -5.000 ; -5.000  7.222]",
        "Hệ số khuếch đại công suất tạp âm trên từng luồng:\n  • Luồng 1 (Tx1): Nhiễu bị khuếch đại 5.0 lần (+6.99 dB).\n  • Luồng 2 (Tx2): Nhiễu bị khuếch đại 7.222 lần (+8.59 dB).",
        "Hệ quả kỹ thuật nghiêm trọng:\n  ZF triệt can nhiễu giữa các luồng thành công nhưng làm suy giảm mạnh SNR hiệu dụng ở máy thu, dẫn đến hiệu năng BER kém hơn nhiều so với STBC ở dải SNR thấp/trung bình."
    ]
    add_bullet_points(tf9_right, items9_right, 10.5, 7)

    slide10 = prs.slides.add_slide(blank_layout)
    add_header(slide10, "Kỹ thuật Tiền mã hóa SVD & Hai Kênh con Không gian Song song", "Phân tích SDM", 10)

    add_card_header(slide10, 0.8, 1.5, 5.5, 5.3, "Cơ chế phân rã kênh trực giao SVD", NAVY)
    tb10_left = slide10.shapes.add_textbox(Inches(0.9), Inches(2.0), Inches(5.3), Inches(4.6))
    tf10_left = tb10_left.text_frame
    tf10_left.word_wrap = True
    items10_left = [
        "Phân rã giá trị kỳ dị: H = U Σ V^H\n  U, V là các ma trận unita (U^H U = I, V^H V = I)\n  Σ = diag(σ_1, σ_2) = diag(1.00596, 0.29671)",
        "Khối phát nhân ma trận tiền mã hóa: x_tx = V x",
        "Khối thu nhân ma trận lọc không gian: y_tilde = U^H y\n  y_tilde = U^H (H V x + n) = Σ x + U^H n = Σ x + n_tilde",
        "Hai kênh con trực giao song song hoàn toàn độc lập:\n  y_tilde_1 = 1.00596 x1 + n_tilde_1\n  y_tilde_2 = 0.29671 x2 + n_tilde_2",
        "Bảo toàn phân bố tạp âm:\n  Do U là ma trận unita nên R_n_tilde = σ_n^2 U^H U = σ_n^2 I_2.\n  => Hoàn toàn không bị khuếch đại tạp âm!",
        "Sai số khôi phục mô phỏng: 9.42e-16"
    ]
    add_bullet_points(tf10_left, items10_left, 10, 6)

    add_card_header(slide10, 6.6, 1.5, 5.933, 5.3, "Hình ảnh mô phỏng tách sóng SDM", DARK_BLUE)
    fig2_path = os.path.join(figures_dir, "fig2_sdm_signal_recovery.png")
    if os.path.exists(fig2_path):
        slide10.shapes.add_picture(fig2_path, Inches(6.75), Inches(2.3), width=Inches(5.633))
    tb10_cap = slide10.shapes.add_textbox(Inches(6.75), Inches(5.9), Inches(5.633), Inches(0.7))
    tf10_cap = tb10_cap.text_frame
    tf10_cap.word_wrap = True
    p10_c = tf10_cap.paragraphs[0]
    p10_c.text = "Hình 2.2: Tách sóng và khôi phục tín hiệu hệ thống MIMO 2x2 SDM (ZF, MMSE, SVD parallel channels)."
    p10_c.font.name = "Arial"
    p10_c.font.size = Pt(9.5)
    p10_c.font.color.rgb = TEXT_MUTED
    p10_c.alignment = PP_ALIGN.CENTER

    slide11 = prs.slides.add_slide(blank_layout)
    add_header(slide11, "Ảnh chụp Kết quả Chạy Mô phỏng Thực tế trên Terminal MATLAB", "Kiểm chứng thực tế", 11)

    add_card_header(slide11, 0.8, 1.5, 5.7, 5.3, "Mô phỏng STBC Alamouti (Terminal)", NAVY)
    term_stbc_path = os.path.join(figures_dir, "term_capture_stbc_matlab.png")
    if os.path.exists(term_stbc_path):
        slide11.shapes.add_picture(term_stbc_path, Inches(1.3), Inches(2.1), height=Inches(3.8))
    tb11_cap1 = slide11.shapes.add_textbox(Inches(0.9), Inches(6.05), Inches(5.5), Inches(0.65))
    tf11_cap1 = tb11_cap1.text_frame
    tf11_cap1.word_wrap = True
    p11_c1 = tf11_cap1.paragraphs[0]
    p11_c1.text = "Xác thực mô phỏng STBC: Tính toán 4 giá trị r0..r3, H_eff trực giao, khôi phục x0, x1 với sai số 1.11e-16."
    p11_c1.font.name = "Arial"
    p11_c1.font.size = Pt(9.5)
    p11_c1.font.color.rgb = TEXT_MUTED
    p11_c1.alignment = PP_ALIGN.CENTER

    add_card_header(slide11, 6.833, 1.5, 5.7, 5.3, "Mô phỏng SDM 2x2 (Terminal)", DARK_BLUE)
    term_sdm_path = os.path.join(figures_dir, "term_capture_sdm_matlab.png")
    if os.path.exists(term_sdm_path):
        slide11.shapes.add_picture(term_sdm_path, Inches(8.3), Inches(2.05), height=Inches(3.9))
    tb11_cap2 = slide11.shapes.add_textbox(Inches(6.933), Inches(6.05), Inches(5.5), Inches(0.65))
    tf11_cap2 = tb11_cap2.text_frame
    tf11_cap2.word_wrap = True
    p11_c2 = tf11_cap2.paragraphs[0]
    p11_c2.text = "Xác thực mô phỏng SDM: Nghịch đảo ZF, hệ số khuếch đại nhiễu 5.0x và 7.2x, kiểm chứng MMSE và SVD."
    p11_c2.font.name = "Arial"
    p11_c2.font.size = Pt(9.5)
    p11_c2.font.color.rgb = TEXT_MUTED
    p11_c2.alignment = PP_ALIGN.CENTER

    slide12 = prs.slides.add_slide(blank_layout)
    add_header(slide12, "Cơ sở Lý thuyết về Bậc Phân tập và Công thức Giải tích BER", "Hiệu năng phân tập", 12)

    add_card_header(slide12, 0.8, 1.5, 5.7, 3.5, "Khái niệm bậc phân tập (Diversity Order)", NAVY)
    tb12_left = slide12.shapes.add_textbox(Inches(0.9), Inches(2.0), Inches(5.5), Inches(2.9))
    tf12_left = tb12_left.text_frame
    tf12_left.word_wrap = True
    items12_left = [
        "Định nghĩa toán học: d = - lim_{SNR → ∞} [ log(P_b) / log(SNR) ]",
        "Ý nghĩa hình học: Bậc phân tập d quyết định độ dốc tiệm cận của đường cong BER trên thang đo log-log ở dải SNR cao.",
        "Quy luật suy hao: Xác suất lỗi tiệm cận theo tỷ lệ P_b ~ (1 / (c SNR))^d.",
        "Giá trị kỹ thuật: Hệ số d càng lớn, xác suất tất cả các kênh rơi vào fading sâu đồng thời càng triệt tiêu nhanh chóng."
    ]
    add_bullet_points(tf12_left, items12_left, 11, 6)

    add_card_header(slide12, 6.833, 1.5, 5.7, 3.5, "Bậc phân tập của các cấu hình anten", DARK_BLUE)
    tb12_right = slide12.shapes.add_textbox(Inches(6.933), Inches(2.0), Inches(5.5), Inches(2.9))
    tf12_right = tb12_right.text_frame
    tf12_right.word_wrap = True
    items12_right = [
        "SISO (1x1): d = 1  (Độ dốc cơ sở: cần 10 dB cho mỗi thập kỷ giảm BER).",
        "SIMO 1x2 SC (Selection Combining): d = N_r = 2  (Độ dốc gấp 2 lần).",
        "SIMO 1x2 MRC (Maximal Ratio Combining): d = N_r = 2  (Độ lợi mảng +3 dB).",
        "MISO 2x1 Alamouti STBC: d = N_t = 2  (Dịch 3 dB so với MRC do chia công suất).",
        "MIMO 2x2 Alamouti STBC: d = N_t N_r = 4  (Bậc phân tập tối đa, độ dốc gấp 4 lần)."
    ]
    add_bullet_points(tf12_right, items12_right, 11, 5)

    add_card_header(slide12, 0.8, 5.15, 11.733, 1.7, "Công thức giải tích khép kín (Closed-form Analytical Formulas)", TEAL)
    tb12_bot = slide12.shapes.add_textbox(Inches(0.9), Inches(5.6), Inches(11.533), Inches(1.15))
    tf12_bot = tb12_bot.text_frame
    tf12_bot.word_wrap = True
    items12_bot = [
        "SISO: P_b = 0.5 * (1 - μ)   với   μ = √( γ̄ / (1 + γ̄) )",
        "SIMO 1x2 MRC: P_b = ((1 - μ)/2)^2 * (2 + μ)   với   μ = √( γ̄ / (1 + γ̄) )",
        "MISO 2x1 Alamouti: P_b = ((1 - μ')/2)^2 * (2 + μ')   với   μ' = √( (γ̄/2) / (1 + γ̄/2) )",
        "MIMO 2x2 Alamouti: P_b = q^4 * (1 + 4p + 10p^2 + 20p^3)   với   p = (1+μ')/2,  q = (1-μ')/2"
    ]
    add_bullet_points(tf12_bot, items12_bot, 10.5, 3)

    slide13 = prs.slides.add_slide(blank_layout)
    add_header(slide13, "Đồ thị So sánh Hiệu năng BER: Lý thuyết vs Mô phỏng Thực tế", "Hiệu năng phân tập", 13)

    add_card_header(slide13, 0.8, 1.5, 6.2, 5.3, "Đồ thị khảo sát hiệu năng BER", NAVY)
    fig3_path = os.path.join(figures_dir, "fig3_ber_diversity_comparison.png")
    if os.path.exists(fig3_path):
        slide13.shapes.add_picture(fig3_path, Inches(0.95), Inches(2.05), width=Inches(5.9))
    tb13_cap = slide13.shapes.add_textbox(Inches(0.95), Inches(6.05), Inches(5.9), Inches(0.6))
    tf13_cap = tb13_cap.text_frame
    tf13_cap.word_wrap = True
    p13_c = tf13_cap.paragraphs[0]
    p13_c.text = "Hình 3.1: So sánh hiệu năng BER giữa SISO, SIMO SC/MRC, MISO 2x1 và MIMO 2x2 Alamouti."
    p13_c.font.name = "Arial"
    p13_c.font.size = Pt(9.5)
    p13_c.font.color.rgb = TEXT_MUTED
    p13_c.alignment = PP_ALIGN.CENTER

    add_card_header(slide13, 7.3, 1.5, 5.233, 5.3, "Phân tích đặc tuyến hiệu năng", DARK_BLUE)
    tb13_right = slide13.shapes.add_textbox(Inches(7.4), Inches(2.0), Inches(5.0), Inches(4.6))
    tf13_right = tb13_right.text_frame
    tf13_right.word_wrap = True
    items13_right = [
        "Kiểm chứng mô phỏng Monte Carlo:\nCác điểm mô phỏng 2x10^5 bit (markers) trùng khớp tuyệt đối với các đường cong lý thuyết giải tích liên tục trên toàn dải SNR từ 0 đến 25 dB.",
        "Khác biệt độ dốc (Slope):\nĐường cong MIMO 2x2 STBC có độ dốc d = 4 dốc đứng nhất, lao nhanh xuống vùng lỗi thấp khi SNR tăng.",
        "So sánh tại mốc SNR = 10 dB:\n• SISO: BER = 2.31 x 10^-2 (Lỗi cao)\n• SIMO SC: BER = 2.99 x 10^-3\n• MISO 2x1: BER = 5.53 x 10^-3\n• SIMO MRC: BER = 1.60 x 10^-3\n• MIMO 2x2 STBC: BER = 1.06 x 10^-4\n  => MIMO 2x2 giảm lỗi hơn 218 lần so với SISO!",
        "Vùng SNR > 15 dB:\nHiệu năng MIMO 2x2 STBC đạt dưới 10^-5, không ghi nhận bất kỳ bit lỗi nào trong tập dữ liệu mô phỏng."
    ]
    add_bullet_points(tf13_right, items13_right, 10, 6)

    slide14 = prs.slides.add_slide(blank_layout)
    add_header(slide14, "Phân tích Độ lợi Phân tập và Tiết kiệm Công suất Phát", "Hiệu năng phân tập", 14)

    add_card_header(slide14, 0.8, 1.5, 6.2, 5.3, "Đối chiếu SNR yêu cầu tại BER = 10^-3", NAVY)
    headers14 = ["Cấu hình anten", "Bậc d", "SNR cần (dB)", "Độ lợi SNR (dB)"]
    rows14 = [
        ["SISO (1x1)", "1", "23.9 dB", "0.0 dB (Chuẩn)"],
        ["MISO 2x1 (Alamouti)", "2", "14.0 dB", "+9.9 dB"],
        ["SIMO 1x2 (SC)", "2", "13.5 dB", "+10.4 dB"],
        ["SIMO 1x2 (MRC)", "2", "11.0 dB", "+12.9 dB"],
        ["MIMO 2x2 (Alamouti STBC)", "4", "7.4 dB", "+16.5 dB (Vượt trội)"]
    ]
    add_table_data(slide14, 0.95, 2.1, 5.9, 2.5, headers14, rows14, [2.2, 0.8, 1.4, 1.5])

    tb14_sub = slide14.shapes.add_textbox(Inches(0.95), Inches(4.8), Inches(5.9), Inches(1.8))
    tf14_sub = tb14_sub.text_frame
    tf14_sub.word_wrap = True
    items14_sub = [
        "Độ lợi công suất vượt bậc: MIMO 2x2 STBC chỉ cần 7.4 dB để đạt BER = 10^-3, tiết kiệm tới 16.5 dB so với SISO (23.9 dB).",
        "Ý nghĩa thực tiễn: Giảm công suất phát của máy phát đi xấp xỉ 45 lần mà vẫn duy trì chất lượng đường truyền tương đương."
    ]
    add_bullet_points(tf14_sub, items14_sub, 10.5, 6)

    add_card_header(slide14, 7.3, 1.5, 5.233, 5.3, "Bản chất các thành phần độ lợi", DARK_BLUE)
    tb14_right = slide14.shapes.add_textbox(Inches(7.4), Inches(2.0), Inches(5.0), Inches(4.6))
    tf14_right = tb14_right.text_frame
    tf14_right.word_wrap = True
    items14_right = [
        "Độ lợi phân tập (Diversity Gain):\nTăng bậc phân tập từ d=1 lên d=4 làm thay đổi căn bản độ dốc của đường cong BER, giúp loại bỏ hầu như hoàn toàn nguy cơ fading sâu đa đường.",
        "Độ lợi mảng (Array Gain):\nNhờ có 2 anten thu (N_r = 2), công suất tín hiệu thu thập tăng gấp 2 lần (+3 dB độ lợi mảng), giải thích vì sao SIMO MRC tốt hơn MISO Alamouti đúng 3 dB dù cùng bậc phân tập d=2.",
        "Tác động thương mại viễn thông:\nTiết kiệm 16.5 dB công suất đồng nghĩa với việc gia tăng thời lượng sử dụng pin của thiết bị di động, kéo dài tầm phủ sóng của trạm gốc, và giảm phát thải can nhiễu vào môi trường vô tuyến."
    ]
    add_bullet_points(tf14_right, items14_right, 10.5, 7)

    slide15 = prs.slides.add_slide(blank_layout)
    add_header(slide15, "Dung lượng Kênh truyền Shannon-Telatar của Hệ thống MIMO SDM", "Dung lượng kênh truyền", 15)

    b15_top = add_card(slide15, 0.8, 1.5, 11.733, 1.0, WHITE, TEAL)
    tb15_top = slide15.shapes.add_textbox(Inches(0.9), Inches(1.55), Inches(11.533), Inches(0.9))
    tf15_top = tb15_top.text_frame
    tf15_top.word_wrap = True
    p15_t1 = tf15_top.paragraphs[0]
    p15_t1.text = "CÔNG THỨC SHANNON-TELATAR CHO KÊNH TRUYỀN MIMO"
    p15_t1.font.name = "Arial"
    p15_t1.font.size = Pt(11)
    p15_t1.font.bold = True
    p15_t1.font.color.rgb = TEAL
    p15_t2 = tf15_top.add_paragraph()
    p15_t2.text = "C = log2 det( I_Nr + (1/σ_n^2) H R_x H^H ) = ∑_{i=1}^r log2( 1 + (p_i σ_i^2) / σ_n^2 )   với   r = min(N_t, N_r) = 2"
    p15_t2.font.name = "Arial"
    p15_t2.font.size = Pt(12)
    p15_t2.font.bold = True
    p15_t2.font.color.rgb = NAVY

    add_card_header(slide15, 0.8, 2.7, 5.7, 4.1, "Kênh SISO — Tăng trưởng logarit", NAVY)
    tb15_left = slide15.shapes.add_textbox(Inches(0.9), Inches(3.2), Inches(5.5), Inches(3.4))
    tf15_left = tb15_left.text_frame
    tf15_left.word_wrap = True
    items15_left = [
        "Công thức dung lượng: C_SISO = log2(1 + SNR) bps/Hz.",
        "Tăng trưởng tiệm cận: Ở dải SNR cao, dung lượng tăng theo hàm logarit:\n  C_SISO ≈ log2(SNR)",
        "Độ dốc công suất: Cứ tăng gấp đôi công suất phát (+3 dB) thì dung lượng chỉ tăng thêm đúng 1 bps/Hz.",
        "Nút thắt thắt cổ chai: Không thể đáp ứng nhu cầu dữ liệu tốc độ cực cao trong các mạng thế hệ mới nếu chỉ dựa vào tăng công suất đơn anten."
    ]
    add_bullet_points(tf15_left, items15_left, 11, 7)

    add_card_header(slide15, 6.833, 2.7, 5.7, 4.1, "Kênh MIMO 2x2 SDM — Tăng trưởng tuyến tính", DARK_BLUE)
    tb15_right = slide15.shapes.add_textbox(Inches(6.933), Inches(3.2), Inches(5.5), Inches(3.4))
    tf15_right = tb15_right.text_frame
    tf15_right.word_wrap = True
    items15_right = [
        "Công thức dung lượng (EPA):\n  C_MIMO = log2(1 + (SNR/2) σ_1^2) + log2(1 + (SNR/2) σ_2^2)",
        "Độ dốc nhân đôi ở SNR cao:\n  C_MIMO ≈ 2 * log2(SNR) + C_offset\n  => Mỗi +3 dB công suất mang lại 2 bps/Hz (Gấp đôi SISO!).",
        "Hiệu quả phổ tối đa: Khai thác không gian như một chiều tài nguyên mới, nhân đôi thông lượng dữ liệu mà hoàn toàn không tốn thêm băng thông tần số."
    ]
    add_bullet_points(tf15_right, items15_right, 11, 7)

    slide16 = prs.slides.add_slide(blank_layout)
    add_header(slide16, "Tối ưu hóa Phân bổ Công suất bằng Thuật toán Water-filling", "Tối ưu công suất", 16)

    add_card_header(slide16, 0.8, 1.5, 5.5, 5.3, "Nguyên lý thuật toán Water-filling", NAVY)
    tb16_left = slide16.shapes.add_textbox(Inches(0.9), Inches(2.0), Inches(5.3), Inches(4.6))
    tf16_left = tb16_left.text_frame
    tf16_left.word_wrap = True
    items16_left = [
        "Bài toán tối ưu hóa lồi:\n  max ∑_{i=1}^2 log2( 1 + p_i σ_i^2 / N0 )  thỏa  p1 + p2 = P_t",
        "Lời giải Kuhn-Tucker (KKT):\n  p_i = max( 0,  μ - N0 / σ_i^2 )   (Mức ngập nước μ)",
        "Mức chênh lệch đáy bồn trên kênh H = [0.7 0.3; 0.4 0.6]:\n  Δ = 1/σ_2^2 - 1/σ_1^2 = 11.358 - 0.988 = 10.370\n  => Tương ứng với ngưỡng SNR_th ≈ 10.15 dB",
        "Hai chế độ hoạt động rõ rệt:\n  • SNR ≤ 10.15 dB: Nước chưa ngập đáy 2 => p1 = P_t, p2 = 0.\n    Hệ thống tự động chuyển sang chế độ Eigen-Beamforming (dồn 100% công suất vào kênh con mạnh nhất).\n  • SNR > 10.15 dB: Nước tràn sang đáy 2 => Cả 2 kênh con đều có công suất. Chuyển sang Ghép kênh đa luồng.",
        "Tiệm cận: Khi SNR → ∞, tỷ lệ p1/p2 → 1, Water-filling hội tụ hoàn toàn về phân bổ đều (EPA)."
    ]
    add_bullet_points(tf16_left, items16_left, 10, 6)

    add_card_header(slide16, 6.6, 1.5, 5.933, 5.3, "Minh họa phân bổ công suất Water-filling", DARK_BLUE)
    fig5_path = os.path.join(figures_dir, "fig5_waterfilling_allocation.png")
    if os.path.exists(fig5_path):
        slide16.shapes.add_picture(fig5_path, Inches(6.75), Inches(2.3), width=Inches(5.633))
    tb16_cap = slide16.shapes.add_textbox(Inches(6.75), Inches(5.9), Inches(5.633), Inches(0.7))
    tf16_cap = tb16_cap.text_frame
    tf16_cap.word_wrap = True
    p16_c = tf16_cap.paragraphs[0]
    p16_c.text = "Hình 4.2: Minh họa phân bổ công suất tối ưu Water-filling trên kênh MIMO 2x2 (Ngưỡng chuyển tiếp chế độ 10.15 dB)."
    p16_c.font.name = "Arial"
    p16_c.font.size = Pt(9.5)
    p16_c.font.color.rgb = TEXT_MUTED
    p16_c.alignment = PP_ALIGN.CENTER

    slide17 = prs.slides.add_slide(blank_layout)
    add_header(slide17, "Đồ thị So sánh Dung lượng Kênh truyền: SISO vs MIMO 2x2 SDM", "Dung lượng kênh truyền", 17)

    add_card_header(slide17, 0.8, 1.5, 6.2, 5.3, "Đồ thị khảo sát dung lượng Shannon", NAVY)
    fig4_path = os.path.join(figures_dir, "fig4_capacity_sdm_comparison.png")
    if os.path.exists(fig4_path):
        slide17.shapes.add_picture(fig4_path, Inches(0.95), Inches(2.05), width=Inches(5.9))
    tb17_cap = slide17.shapes.add_textbox(Inches(0.95), Inches(6.05), Inches(5.9), Inches(0.6))
    tf17_cap = tb17_cap.text_frame
    tf17_cap.word_wrap = True
    p17_c = tf17_cap.paragraphs[0]
    p17_c.text = "Hình 4.1: So sánh dung lượng kênh truyền Shannon giữa SISO và MIMO 2x2 SDM (EPA và Water-filling)."
    p17_c.font.name = "Arial"
    p17_c.font.size = Pt(9.5)
    p17_c.font.color.rgb = TEXT_MUTED
    p17_c.alignment = PP_ALIGN.CENTER

    add_card_header(slide17, 7.3, 1.5, 5.233, 5.3, "Bảng số liệu đối chiếu dung lượng (bps/Hz)", DARK_BLUE)
    headers17 = ["SNR", "SISO", "MIMO EPA", "MIMO WF", "Ergodic WF"]
    rows17 = [
        ["-10 dB", "0.14", "0.08", "0.14", "0.42"],
        ["0 dB", "1.00", "0.65", "1.01", "2.08"],
        ["10 dB", "3.46", "3.13", "3.47", "5.71"],
        ["20 dB", "6.66", "8.13", "8.15", "11.31"],
        ["30 dB", "9.97", "14.49", "14.49", "17.74"]
    ]
    add_table_data(slide17, 7.45, 2.1, 4.9, 2.4, headers17, rows17, [1.0, 0.9, 1.0, 1.0, 1.0])

    tb17_sub = slide17.shapes.add_textbox(Inches(7.45), Inches(4.7), Inches(4.9), Inches(1.9))
    tf17_sub = tb17_sub.text_frame
    tf17_sub.word_wrap = True
    items17_sub = [
        "Vùng SNR thấp (< 10 dB): EPA bị suy thoái do lãng phí công suất vào kênh con yếu (σ_2=0.297). Water-filling khắc phục triệt để bằng cách dồn lực cho kênh con mạnh.",
        "Vùng SNR cao (> 20 dB): MIMO 2x2 bứt phá vượt trội so với SISO (+4.52 bps/Hz tại 20 dB và +7.77 bps/Hz tại 30 dB trên kênh ergodic)."
    ]
    add_bullet_points(tf17_sub, items17_sub, 10, 5)

    slide18 = prs.slides.add_slide(blank_layout)
    add_header(slide18, "Sự Đánh đổi giữa Độ lợi Phân tập và Tốc độ Ghép kênh (DMT)", "Đánh đổi hệ thống", 18)

    add_card_header(slide18, 0.8, 1.5, 5.7, 3.5, "Lý thuyết đánh đổi căn bản Zheng - Tse (2003)", NAVY)
    tb18_left = slide18.shapes.add_textbox(Inches(0.9), Inches(2.0), Inches(5.5), Inches(2.9))
    tf18_left = tb18_left.text_frame
    tf18_left.word_wrap = True
    items18_left = [
        "Hệ thức đánh đổi DMT cho hệ thống MIMO 2x2:\n  d(r) = (N_t - r)(N_r - r) = (2 - r)^2   với  0 ≤ r ≤ 2",
        "Bản chất vật lý: Cùng một số lượng anten trong không gian, hệ thống không thể đồng thời tối đa hóa cả độ tin cậy và tốc độ truyền dữ liệu.",
        "Cực biên 1 (r = 0): Đạt bậc phân tập tối đa d_max = 4  ⇒  Kỹ thuật STBC Alamouti (Tối đa tin cậy, chống fading sâu).",
        "Cực biên 2 (d = 0): Đạt tốc độ ghép kênh tối đa r_max = 2  ⇒  Kỹ thuật SDM (Tối đa thông lượng, nhân đôi tốc độ)."
    ]
    add_bullet_points(tf18_left, items18_left, 10.5, 6)

    add_card_header(slide18, 6.833, 1.5, 5.7, 3.5, "Bảng so sánh tổng hợp STBC vs SDM", DARK_BLUE)
    headers18 = ["Tiêu chí", "STBC Alamouti", "Ghép kênh SDM"]
    rows18 = [
        ["Mục tiêu cốt lõi", "Tối đa độ tin cậy (chống lỗi)", "Tối đa tốc độ (thông lượng)"],
        ["Tốc độ mã hóa R", "R = 1 ký hiệu/khe (như SISO)", "R = 2 ký hiệu/khe (nhân đôi)"],
        ["Bậc phân tập d", "d = 4 (Cực đại)", "d = 0 (với tách sóng ZF)"],
        ["Phức tạp máy thu", "Rất thấp (kết hợp tuyến tính)", "Trung bình / cao (đảo ma trận)"],
        ["Yêu cầu CSI", "Chỉ cần CSIR tại bộ thu", "Cần CSIR (ZF/MMSE), CSIT (SVD)"]
    ]
    add_table_data(slide18, 6.95, 2.05, 5.5, 2.7, headers18, rows18, [1.5, 2.0, 2.0])

    add_card_header(slide18, 0.8, 5.15, 11.733, 1.7, "Chiến lược thích nghi liên kết trong 5G / 6G (Adaptive Link Adaptation)", TEAL)
    tb18_bot = slide18.shapes.add_textbox(Inches(0.9), Inches(5.6), Inches(11.533), Inches(1.15))
    tf18_bot = tb18_bot.text_frame
    tf18_bot.word_wrap = True
    items18_bot = [
        "Vùng biên tế bào (Cell Edge) / SNR thấp: Chuyển sang chế độ STBC Alamouti để tận dụng độ lợi phân tập d=4 và độ lợi mảng, đảm bảo cuộc gọi và dữ liệu không bị ngắt quãng.",
        "Vùng tâm tế bào (Cell Center) / SNR cao: Chuyển sang chế độ SDM để mở rộng thông lượng phục vụ truyền dữ liệu băng rộng tốc độ Gigabit."
    ]
    add_bullet_points(tf18_bot, items18_bot, 10.5, 4)

    slide19 = prs.slides.add_slide(blank_layout)
    add_header(slide19, "Bảng Tổng hợp Đối chiếu Kết quả Lý thuyết vs Mô phỏng Thực tế", "Tổng hợp kết quả", 19)

    add_card_header(slide19, 0.8, 1.5, 6.7, 5.3, "Bảng đối chiếu toàn diện các chỉ số kỹ thuật", NAVY)
    headers19 = ["Hạng mục khảo sát", "Lý thuyết giải tích", "Thực tế mô phỏng", "Đánh giá"]
    rows19 = [
        ["Sai số khôi phục STBC", "0.0 (Tuyệt đối)", "1.11 x 10^-16", "Khôi phục hoàn hảo"],
        ["Sai số khôi phục SDM ZF", "0.0 (Tuyệt đối)", "1.05 x 10^-15", "Khôi phục hoàn hảo"],
        ["Khuếch đại nhiễu ZF", "5.0x và 7.22x", "5.000x và 7.222x", "Trùng khớp 100%"],
        ["Bậc phân tập MIMO 2x2", "d = 4", "d = 4 (khớp độ dốc)", "Độ dốc gấp 4 lần SISO"],
        ["Độ lợi SNR tại BER 10^-3", "+16.5 dB", "+16.5 dB", "Tiết kiệm 45x công suất"],
        ["Ngưỡng chuyển đổi WF", "10.15 dB", "10.15 dB", "Chuyển tiếp chính xác"],
        ["Độ dốc dung lượng SDM", "2 bps/Hz / 3dB", "2.0 bps/Hz / 3dB", "Nhân đôi hiệu suất phổ"]
    ]
    add_table_data(slide19, 0.95, 2.05, 6.4, 4.5, headers19, rows19, [2.1, 1.4, 1.4, 1.5])

    add_card_header(slide19, 7.8, 1.5, 4.733, 5.3, "Ảnh chụp tổng hợp Terminal", DARK_BLUE)
    term_sum_path = os.path.join(figures_dir, "term_capture_simulation_summary.png")
    if os.path.exists(term_sum_path):
        slide19.shapes.add_picture(term_sum_path, Inches(8.3), Inches(2.1), width=Inches(3.8))
    tb19_cap = slide19.shapes.add_textbox(Inches(7.9), Inches(6.05), Inches(4.5), Inches(0.65))
    tf19_cap = tb19_cap.text_frame
    tf19_cap.word_wrap = True
    p19_c = tf19_cap.paragraphs[0]
    p19_c.text = "Hình 4.3: Bảng tổng hợp đối chiếu kết quả mô phỏng toàn diện xuất ra từ terminal Python."
    p19_c.font.name = "Arial"
    p19_c.font.size = Pt(9.5)
    p19_c.font.color.rgb = TEXT_MUTED
    p19_c.alignment = PP_ALIGN.CENTER

    slide20 = prs.slides.add_slide(blank_layout)
    add_header(slide20, "Kết luận Khoa học & Đánh giá Mức độ Hoàn thành Mục tiêu", "Kết luận đồ án", 20)

    add_card_header(slide20, 0.8, 1.5, 3.7, 5.3, "1. Lý thuyết & Giải tích", NAVY)
    tb20_c1 = slide20.shapes.add_textbox(Inches(0.9), Inches(2.0), Inches(3.5), Inches(4.6))
    tf20_c1 = tb20_c1.text_frame
    tf20_c1.word_wrap = True
    items20_c1 = [
        "Hoàn thành 100% dẫn xuất toán học chi tiết cho cả hai sơ đồ STBC Alamouti và SDM 2x2.",
        "Khảo sát toàn diện ma trận kênh cố định H = [0.7 0.3; 0.4 0.6]: Tính chính xác các giá trị r0..r3.",
        "Chứng minh toán học tính trực giao của ma trận kênh hiệu dụng H_eff và khôi phục hoàn hảo tín hiệu gốc.",
        "Làm rõ hiện tượng khuếch đại nhiễu của tách sóng tuyến tính ZF và cơ chế phân rã kênh trực giao SVD."
    ]
    add_bullet_points(tf20_c1, items20_c1, 10.5, 7)

    add_card_header(slide20, 4.816, 1.5, 3.7, 5.3, "2. Mô phỏng & Thực nghiệm", DARK_BLUE)
    tb20_c2 = slide20.shapes.add_textbox(Inches(4.916), Inches(2.0), Inches(3.5), Inches(4.6))
    tf20_c2 = tb20_c2.text_frame
    tf20_c2.word_wrap = True
    items20_c2 = [
        "Xây dựng thành công bộ mô phỏng Monte Carlo 2x10^5 bit trên cả hai nền tảng MATLAB và Python.",
        "Kiểm chứng tính đúng đắn: Các đường cong mô phỏng BER và dung lượng Shannon trùng khớp hoàn hảo với các mô hình giải tích khép kín.",
        "Xác thực độ lợi phân tập d=4 và độ lợi SNR +16.5 dB tại BER=10^-3 của hệ thống MIMO 2x2 Alamouti.",
        "Khẳng định ngưỡng Water-filling 10.15 dB phân định rõ 2 chế độ Beamforming và Ghép kênh."
    ]
    add_bullet_points(tf20_c2, items20_c2, 10.5, 7)

    add_card_header(slide20, 8.833, 1.5, 3.7, 5.3, "3. Giá trị & Hướng phát triển", TEAL)
    tb20_c3 = slide20.shapes.add_textbox(Inches(8.933), Inches(2.0), Inches(3.5), Inches(4.6))
    tf20_c3 = tb20_c3.text_frame
    tf20_c3.word_wrap = True
    items20_c3 = [
        "Làm sáng tỏ nguyên lý đánh đổi DMT (Zheng - Tse), cung cấp luận cứ khoa học cho thuật toán thích nghi đường truyền.",
        "Đặt nền tảng vững chắc để mở rộng nghiên cứu sang các cấu hình đa anten quy mô lớn trong 5G-Advanced và 6G:",
        "• Massive MIMO và XL-MIMO với hàng trăm phần tử anten.",
        "• Băng tần sóng milimet (mmWave / THz) kết hợp Hybrid Beamforming.",
        "• Mạng phân tán Cell-Free MIMO tích hợp bề mặt phản xạ thông minh RIS."
    ]
    add_bullet_points(tf20_c3, items20_c3, 10.5, 6)

    slide21 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide21, NAVY)

    top_bar21 = slide21.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(SLIDE_WIDTH), Inches(0.12))
    top_bar21.fill.solid()
    top_bar21.fill.fore_color.rgb = TEAL
    top_bar21.line.fill.background()

    tb21_top = slide21.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.733), Inches(0.8))
    tf21_top = tb21_top.text_frame
    p21_t = tf21_top.paragraphs[0]
    p21_t.text = "TRƯỜNG ĐẠI HỌC KHOA HỌC TỰ NHIÊN - ĐHQG TP.HCM  •  KHOA ĐIỆN TỬ - VIỄN THÔNG"
    p21_t.font.name = "Arial"
    p21_t.font.size = Pt(12)
    p21_t.font.bold = True
    p21_t.font.color.rgb = TEAL
    p21_t.alignment = PP_ALIGN.CENTER

    tb21_main = slide21.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.733), Inches(1.5))
    tf21_main = tb21_main.text_frame
    tf21_main.word_wrap = True
    p21_m1 = tf21_main.paragraphs[0]
    p21_m1.text = "XIN CHÂN THÀNH CẢM ƠN QUÝ THẦY\nVÀ CÁC BẠN ĐÃ LẮNG NGHE!"
    p21_m1.font.name = "Arial"
    p21_m1.font.size = Pt(30)
    p21_m1.font.bold = True
    p21_m1.font.color.rgb = WHITE
    p21_m1.alignment = PP_ALIGN.CENTER

    c21 = slide21.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(2.8), Inches(3.6), Inches(7.733), Inches(2.2))
    c21.fill.solid()
    c21.fill.fore_color.rgb = DARK_BLUE
    c21.line.color.rgb = TEAL
    c21.line.width = Pt(1)
    tf21_c = c21.text_frame
    tf21_c.word_wrap = True
    p21_c_h = tf21_c.paragraphs[0]
    p21_c_h.text = "ĐỒ ÁN MÔN HỌC: TRUYỀN THÔNG KHÔNG DÂY (ETC10309)"
    p21_c_h.font.name = "Arial"
    p21_c_h.font.size = Pt(12)
    p21_c_h.font.bold = True
    p21_c_h.font.color.rgb = TEAL
    p21_c_h.alignment = PP_ALIGN.CENTER
    p21_c_h.space_after = Pt(8)

    p21_c_t1 = tf21_c.add_paragraph()
    p21_c_t1.text = "Đề tài: Thiết kế và Mô phỏng Hệ thống MIMO 2x2 sử dụng STBC và SDM"
    p21_c_t1.font.name = "Arial"
    p21_c_t1.font.size = Pt(13)
    p21_c_t1.font.bold = True
    p21_c_t1.font.color.rgb = WHITE
    p21_c_t1.alignment = PP_ALIGN.CENTER
    p21_c_t1.space_after = Pt(6)

    p21_c_t2 = tf21_c.add_paragraph()
    p21_c_t2.text = "GVHD: TS. Đặng Lê Khoa  —  CN. Nguyễn Dũng"
    p21_c_t2.font.name = "Arial"
    p21_c_t2.font.size = Pt(11.5)
    p21_c_t2.font.color.rgb = WHITE
    p21_c_t2.alignment = PP_ALIGN.CENTER
    p21_c_t2.space_after = Pt(4)

    p21_c_t3 = tf21_c.add_paragraph()
    p21_c_t3.text = "SVTH: Lê Ngọc Tường  —  MSSV: 22207044  —  Lớp: 22DTV_CLC1"
    p21_c_t3.font.name = "Arial"
    p21_c_t3.font.size = Pt(11.5)
    p21_c_t3.font.color.rgb = WHITE
    p21_c_t3.alignment = PP_ALIGN.CENTER

    pill21 = slide21.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.6), Inches(6.1), Inches(4.133), Inches(0.55))
    pill21.fill.solid()
    pill21.fill.fore_color.rgb = TEAL
    pill21.line.fill.background()
    tf21_p = pill21.text_frame
    tf21_p.vertical_anchor = MSO_ANCHOR.MIDDLE
    p21_p = tf21_p.paragraphs[0]
    p21_p.text = "CHƯƠNG TRÌNH HỎI & ĐÁP (Q&A)"
    p21_p.font.name = "Arial"
    p21_p.font.size = Pt(13)
    p21_p.font.bold = True
    p21_p.font.color.rgb = WHITE
    p21_p.alignment = PP_ALIGN.CENTER

    output_pptx = "/home/tuong/Desktop/HK1-26-27/ETC10309_TruyenThongKhongDay/DoAn_2026/slides/Slide_ThuyetTrinh_MIMO_2026.pptx"
    prs.save(output_pptx)
    print(f"SAVED_PPTX: {output_pptx} with {len(prs.slides)} slides")

if __name__ == "__main__":
    create_deck()
