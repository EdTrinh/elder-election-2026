import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Elder 2026 Election Survey", page_icon="🗳️", layout="centered")

# --- CUSTOM CSS FOR SENIORS ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 4.5em;
        font-size: 20px !important;
        font-weight: 500;
        margin-bottom: 12px;
        border-radius: 12px;
        border: 1px solid #dcdde1;
        transition: all 0.3s;
    }
    /* Specific Colors for Parties */
    div.stButton > button:first-child { border-left: 10px solid #ff4d4d; } /* A - Labor */
    div.stButton > button:nth-child(2) { border-left: 10px solid #3399ff; } /* B - Liberal */
    div.stButton > button:nth-child(3) { border-left: 10px solid #ffcc00; } /* C - One Nation */
    div.stButton > button:nth-child(4) { border-left: 10px solid #33cc33; } /* D - Greens */
    
    .question-text {
        font-size: 26px !important;
        line-height: 1.4;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 25px;
    }
    .stProgress > div > div > div > div {
        background-color: #3498db;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE ---
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
    st.session_state.scores = {"A": 0, "B": 0, "C": 0, "D": 0}
    st.session_state.history = []

# --- DATABASE: ALL 30 QUESTIONS ---
questions = [
    # SECTION 1: ECONOMY (1-10)
    {"q": "Nếu máy móc thay thế con người, chính phủ có nên trợ cấp tiền hằng tháng cho dân không?", 
     "opts": {"A": "A: Có, để đảm bảo cuộc sống", "B": "B: Không, nên giảm thuế tạo việc làm", "C": "C: Chỉ trợ cấp dân bản địa", "D": "D: Có, và đánh thuế robot"}},
    {"q": "Ba mẹ nghĩ sao về việc đánh thêm thuế đối với người có rất nhiều nhà đất?", 
     "opts": {"A": "A: Đồng ý, để xây bệnh viện", "B": "B: Không đồng ý, để họ giữ tiền", "C": "C: Chỉ đánh thuế người nước ngoài", "D": "D: Rất đồng ý, xây nhà cho người nghèo"}},
    {"q": "Cách tốt nhất để giảm giá tiền điện và thực phẩm cho gia đình mình là gì?", 
     "opts": {"A": "A: Chính phủ giảm giá trực tiếp hóa đơn", "B": "B: Chính phủ chi tiêu ít đi", "C": "C: Giữ lại hàng hóa Úc dùng trong nước", "D": "D: Cấm các siêu thị tăng giá quá cao"}},
    {"q": "Chính phủ có nên tự xây nhà và cho thuê với giá thật rẻ không?", 
     "opts": {"A": "A: Có, chính phủ nên làm chủ nhà", "B": "B: Không, để tư nhân tự xây", "C": "C: C: Chỉ dành cho người gốc Úc", "D": "D: Có, xây thật nhiều nhà xã hội"}},
    {"q": "Khi các ngân hàng lớn có lợi nhuận khổng lồ, họ nên làm gì?", 
     "opts": {"A": "A: Đóng thuế nhiều hơn sửa đường xá", "B": "B: Để họ đầu tư kinh tế mạnh hơn", "C": "C: Giảm lãi suất vay cho dân", "D": "D: Chia sẻ lợi nhuận cho cộng đồng"}},
    {"q": "Làm sao giúp người trẻ mua được căn nhà đầu tiên của mình?", 
     "opts": {"A": "A: Chính phủ hỗ trợ tiền đặt cọc", "B": "B: Xóa bỏ thuế phí mua nhà", "C": "C: Ngừng cho người ngoại quốc mua đất", "D": "D: Đóng băng giá nhà & giới hạn sở hữu"}},
    {"q": "Ba mẹ nghĩ học nghề (TAFE) và Đại học có nên được miễn phí không?", 
     "opts": {"A": "A: Nên miễn phí học nghề", "B": "B: Mọi người đóng một phần học phí", "C": "C: Chỉ miễn phí cho các nghề thiết yếu", "D": "D: Tất cả giáo dục phải miễn phí"}},
    {"q": "Hệ thống tiền hưu bổng (Super) nên được thay đổi thế nào?", 
     "opts": {"A": "A: Chính phủ nộp thêm cho người lương thấp", "B": "B: Cho rút tiền hưu sớm mua nhà", "C": "C: Giữ nguyên bảo vệ tiền dưỡng già", "D": "D: Tăng hưu bổng bằng thuế tập đoàn"}},
    {"q": "Có nên giới hạn để chủ nhà không được tăng tiền thuê quá cao?", 
     "opts": {"A": "A: Có, bảo vệ người thuê", "B": "B: Không, để chủ nhà muốn đầu tư", "C": "C: Chỉ giới hạn công ty địa ốc lớn", "D": "D: Dừng việc tăng tiền thuê ngay lập tức"}},
    {"q": "Chính phủ nên quản lý các khoản nợ công như thế nào?", 
     "opts": {"A": "A: Vay thêm nếu lo cho tương lai", "B": "B: Trả nợ nhanh dù phải bớt chi tiêu", "C": "C: Chỉ vay quân đội/nhà máy lớn", "D": "D: Ưu tiên giúp dân trước, không lo nợ"}},

    # SECTION 2: SECURITY & TRADITION (11-20)
    {"q": "Làm sao để khu phố Elder trở nên an toàn hơn?", 
     "opts": {"A": "A: Đầu tư giáo dục thanh thiếu niên", "B": "B: Thuê thêm cảnh sát và thiết bị", "C": "C: Hình phạt thật nghiêm khắc", "D": "D: Giải quyết tận gốc nghèo đói"}},
    {"q": "Úc nên ưu tiên ai khi xét duyệt định cư?", 
     "opts": {"A": "A: Người giỏi công nghệ", "B": "B: Người đã có sẵn tay nghề", "C": "C: Giảm người nhập cư giữ văn hóa", "D": "D: Chào đón tất cả ai muốn đóng góp"}},
    {"q": "Xử lý thế nào với người đi tàu lậu vào Úc?", 
     "opts": {"A": "A: Đối xử nhân đạo", "B": "B: Kiểm tra an ninh thật kỹ", "C": "C: Buộc các tàu đó quay trở lại", "D": "D: Chào đón và hỗ trợ hòa nhập"}},
    {"q": "Điều quan trọng nhất trẻ em cần học ở trường là gì?", 
     "opts": {"A": "A: Lòng nhân ái và đa văn hóa", "B": "B: Khoa học và kinh tế", "C": "C: Lòng tự hào dân tộc và lịch sử Úc", "D": "D: Bảo vệ môi trường và công bằng"}},
    {"q": "Chính phủ có được xem tin nhắn mạng để bắt tội phạm không?", 
     "opts": {"A": "A: Không, quyền riêng tư trên hết", "B": "B: Có, nếu bắt được người xấu", "C": "C: Có, trật tự xã hội là hàng đầu", "D": "D: Không, chính phủ không được theo dõi"}},
    {"q": "Có nên có nhóm tư vấn riêng cho người Bản địa không?", 
     "opts": {"A": "A: Có, sửa chữa sai lầm quá khứ", "B": "B: Không, mọi người đối xử giống nhau", "C": "C: Không, nhìn về tương lai", "D": "D: Rất cần thiết để họ tự quyết"}},
    {"q": "Nên xử lý các chất gây nghiện (như cần sa) thế nào?", 
     "opts": {"A": "A: Coi là vấn đề sức khỏe/cai nghiện", "B": "B: Vẫn bất hợp pháp nhưng phạt nhẹ", "C": "C: Phải phạt tù thật nghiêm khắc", "D": "D: Hợp pháp hóa và quản lý"}},
    {"q": "Chính phủ có nên bảo vệ giá trị gia đình truyền thống?", 
     "opts": {"A": "A: Không, đừng xen vào đời tư", "B": "B: Hỗ trợ chung tôn trọng mọi lựa chọn", "C": "C: Gia đình truyền thống là nền tảng", "D": "D: Tôn trọng sự đa dạng mọi gia đình"}},
    {"q": "Có nên lắp thêm nhiều camera an ninh công cộng không?", 
     "opts": {"A": "A: Không, làm mất sự tự do", "B": "B: Có, giúp bắt trộm nhanh hơn", "C": "C: Có, cần giám sát giữ kỷ luật", "D": "D: Không, camera không làm an toàn hơn"}},
    {"q": "Lịch sử nước Úc nên được dạy như thế nào?", 
     "opts": {"A": "A: Nói rõ cả chuyện tốt và xấu", "B": "B: Tập trung vào thành tựu vĩ đại", "C": "C: Tự hào về nguồn gốc dựng nước", "D": "D: Tập trung sửa lỗi với người Bản địa"}},

    # SECTION 3: ENVIRONMENT & TECH (21-30)
    {"q": "Nguồn điện của Nam Úc nên lấy từ đâu là tốt nhất?", 
     "opts": {"A": "A: Năng lượng sạch mặt trời/gió", "B": "B: Kết hợp nguồn điện giá rẻ nhất", "C": "C: Than đá đảm bảo ổn định", "D": "D: 100% tái tạo và đóng mỏ than"}},
    {"q": "Chính phủ có hỗ trợ tiền mua xe điện không?", 
     "opts": {"A": "A: Có, khuyến khích công nghệ sạch", "B": "B: Không, để thị trường tự quyết", "C": "C: Không, hãy giảm giá xăng", "D": "D: Có, bỏ hẳn xe xăng tương lai"}},
    {"q": "Ba mẹ có ủng hộ xây nhà máy điện hạt nhân?", 
     "opts": {"A": "A: Không, quá nguy hiểm", "B": "B: Nghiên cứu kỹ nếu giá rẻ", "C": "C: Có, giúp nước Úc mạnh mẽ", "D": "D: Tuyệt đối không, dùng điện mặt trời"}},
    {"q": "Có nên cấm nhựa xài một lần không?", 
     "opts": {"A": "A: Cấm ngay để bảo vệ môi trường", "B": "B: Cấm từ từ để doanh nghiệp quen", "C": "C: Không nên cấm vì bất tiện", "D": "D: Cấm ngay và phạt nặng công ty"}},
    {"q": "Nông dân được chặt cây trên đất của họ không?", 
     "opts": {"A": "A: Không, giữ rừng bảo vệ trái đất", "B": "B: Có, vì đó là đất làm kinh tế", "C": "C: Được, nếu họ trồng lại cây nơi khác", "D": "D: Không, bảo vệ bằng luật nghiêm ngặt"}},
    {"q": "Chính phủ xây các trạm pin khổng lồ trữ điện?", 
     "opts": {"A": "A: Có, bước đi hiện đại tương lai", "B": "B: Chỉ làm nếu giúp tiết kiệm tiền", "C": "C: Không, xây nhà máy điện cũ tốt hơn", "D": "D: Rất nên, đây là cách bỏ than đá"}},
    {"q": "Nước sông Murray ưu tiên cho ai trước?", 
     "opts": {"A": "A: Ưu tiên môi trường và tôm cá", "B": "B: Ưu tiên nông dân thực phẩm", "C": "C: Giữ tối đa cho người Nam Úc", "D": "D: Trả lại nước cho dòng sông"}},
    {"q": "Ba mẹ đồng ý đánh thuế nhà máy ô nhiễm không?", 
     "opts": {"A": "A: Đồng ý, để họ sản xuất sạch hơn", "B": "B: Không, giá đồ siêu thị sẽ tăng", "C": "C: Chỉ đánh thuế công ty nước ngoài", "D": "D: Rất đồng ý, tiền đó cứu môi trường"}},
    {"q": "Có nên mở thêm mỏ khoáng sản làm pin điện thoại?", 
     "opts": {"A": "A: Có, Úc dẫn đầu công nghệ", "B": "B: Có, tạo nhiều việc làm lương cao", "C": "C: Chỉ làm ở xa khu dân cư", "D": "D: Chỉ làm nếu không hại thiên nhiên"}},
    {"q": "Nếu có thiên tai, ai nên trả tiền sửa chữa?", 
     "opts": {"A": "A: Chính phủ hỗ trợ ngay", "B": "B: Mỗi gia đình tự mua bảo hiểm", "C": "C: Cộng đồng và hàng xóm giúp nhau", "D": "D: Các công ty ô nhiễm phải trả tiền"}}
]

# --- APP LOGIC ---
def process_answer(choice):
    st.session_state.scores[choice] += 1
    st.session_state.history.append(choice)
    st.session_state.current_q += 1

def go_back():
    if st.session_state.current_q > 0:
        last_choice = st.session_state.history.pop()
        st.session_state.scores[last_choice] -= 1
        st.session_state.current_q -= 1

# --- MAIN UI ---
st.title("🗳️ Khảo sát Bầu cử Elder 2026")
st.write("Dành cho Ba Mẹ: Hãy chọn ý kiến ba mẹ đồng ý nhất.")

if st.session_state.current_q < len(questions):
    # Progress Bar
    progress = (st.session_state.current_q) / len(questions)
    st.progress(progress)
    st.write(f"Câu hỏi {st.session_state.current_q + 1} / 30")

    # Question Display
    q_data = questions[st.session_state.current_q]
    st.markdown(f'<p class="question-text">{q_data["q"]}</p>', unsafe_allow_html=True)

    # Option Buttons
    col1, col2 = st.columns(2)
    options = list(q_data['opts'].items())
    
    # We display buttons in a grid for iPad readability
    for key, val in options:
        if st.button(val, key=f"q{st.session_state.current_q}_{key}"):
            process_answer(key)
            st.rerun()

    # Back Button
    st.divider()
    if st.button("← QUAY LẠI (BACK)", disabled=(st.session_state.current_q == 0)):
        go_back()
        st.rerun()

else:
    # --- FINAL RESULTS ---
    st.balloons()
    winner = max(st.session_state.scores, key=st.session_state.scores.get)
    results_map = {
        "A": "NADIA CLANCY (Đảng Lao Động - Labor)",
        "B": "SHAWN VAN GROESEN (Đảng Tự Do - Liberal)",
        "C": "MATTHEW MANGELSDORF (Một Quốc Gia - One Nation)",
        "D": "STEF ROZITIS (Đảng Xanh - Greens)"
    }
    
    st.header("✨ Kết quả gợi ý cho Ba Mẹ")
    st.success(f"### Ứng cử viên phù hợp nhất: {results_map[winner]}")
    
    st.write("---")
    st.subheader("📊 Biểu đồ chi tiết quan điểm của Ba Mẹ:")
    
    # Chart Data
    chart_data = {
        "Đảng": ["Lao Động", "Tự Do", "One Nation", "Đảng Xanh"],
        "Số câu chọn": [
            st.session_state.scores["A"], 
            st.session_state.scores["B"], 
            st.session_state.scores["C"], 
            st.session_state.scores["D"]
        ]
    }
    st.bar_chart(data=chart_data, x="Đảng", y="Số câu chọn")
    
    st.info("💡 Lưu ý: Đây là gợi ý dựa trên các câu trả lời. Ba mẹ có thể tùy chọn người mình tin tưởng nhất khi đi bầu.")

    if st.button("Làm lại khảo sát từ đầu"):
        st.session_state.current_q = 0
        st.session_state.scores = {"A": 0, "B": 0, "C": 0, "D": 0}
        st.session_state.history = []
        st.rerun()