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
    # KINH TẾ (ECONOMY)
    {"q": "Chính phủ có nên trợ cấp tiền hằng tháng (UBI) nếu máy móc thay thế việc làm của con người?", 
     "opts": {"A": "Có, để đảm bảo cuộc sống cơ bản", "B": "Không, nên giảm thuế để doanh nghiệp tự tạo việc làm", "C": "Chỉ trợ cấp cho công dân lâu năm", "D": "Có, và phải đánh thuế các công ty sử dụng robot"}},
    {"q": "Ba mẹ nghĩ sao về việc bỏ ưu đãi thuế cho người sở hữu rất nhiều nhà đất (Negative Gearing)?", 
     "opts": {"A": "Đồng ý, để dùng tiền đó xây bệnh viện", "B": "Không đồng ý, để khuyến khích người dân đầu tư", "C": "Chỉ áp dụng với các công ty địa ốc lớn", "D": "Rất đồng ý, để hạ giá nhà cho người nghèo"}},
    {"q": "Cách tốt nhất để giảm giá hóa đơn điện và thực phẩm cho gia đình là gì?", 
     "opts": {"A": "Chính phủ trực tiếp hỗ trợ tiền điện", "B": "Cắt giảm chi tiêu chính phủ để giảm lạm phát", "C": "Ưu tiên giữ hàng hóa sản xuất tại Úc để dùng trong nước", "D": "Kiểm soát giá trần tại các siêu thị lớn như Coles/Woolies"}},
    {"q": "Chính phủ có nên trực tiếp xây nhà xã hội và cho thuê với giá rẻ không?", 
     "opts": {"A": "Có, chính phủ nên quản lý việc nhà ở", "B": "Không, nên để thị trường tự do cạnh tranh", "C": "Có, nhưng chỉ dành cho người gốc Úc", "D": "Có, và phải xây thật nhiều để ai cũng có chỗ ở"}},
    {"q": "Khi các ngân hàng lớn có lợi nhuận quá cao, họ nên làm gì?", 
     "opts": {"A": "Đóng thêm thuế để đầu tư vào hạ tầng", "B": "Được giữ lại để tái đầu tư vào kinh tế", "C": "Phải giảm lãi suất cho vay cho người dân", "D": "Chia sẻ lợi nhuận cho các quỹ cộng đồng"}},
    {"q": "Làm sao giúp người trẻ mua được căn nhà đầu tiên?", 
     "opts": {"A": "Chính phủ hỗ trợ tiền đặt cọc nhà", "B": "Cắt giảm thuế trước bạ và thủ tục", "C": "Ngừng cho người nước ngoài mua đất tại Úc", "D": "Đóng băng giá nhà và giới hạn số nhà một người được sở hữu"}},
    {"q": "Học nghề (TAFE) và Đại học có nên được hoàn toàn miễn phí?", 
     "opts": {"A": "Nên miễn phí cho các ngành nghề ưu tiên", "B": "Mọi người nên đóng góp một phần học phí", "C": "Chỉ miễn phí cho công dân Úc chính gốc", "D": "Tất cả giáo dục phải miễn phí cho mọi người"}},
    {"q": "Tiền hưu bổng (Super) nên được sử dụng như thế nào?", 
     "opts": {"A": "Chính phủ đóng thêm cho người thu nhập thấp", "B": "Cho phép rút sớm để mua nhà đầu tiên", "C": "Giữ nguyên để bảo đảm cuộc sống tuổi già", "D": "Tăng mức đóng góp bắt buộc từ các tập đoàn"}},
    {"q": "Có nên áp đặt giới hạn tăng tiền thuê nhà (Rent caps)?", 
     "opts": {"A": "Có, để bảo vệ người đi thuê nhà", "B": "Không, sẽ làm chủ nhà không muốn sửa chữa nhà", "C": "Chỉ áp dụng cho các căn hộ chung cư lớn", "D": "Dừng việc tăng tiền thuê ngay lập tức"}},
    {"q": "Chính phủ nên làm gì với các khoản nợ quốc gia?", 
     "opts": {"A": "Vay thêm nếu cần đầu tư cho giáo dục/y tế", "B": "Phải trả nợ nhanh chóng dù phải cắt giảm chi tiêu", "C": "Chỉ vay cho các dự án quốc phòng", "D": "Ưu tiên an sinh xã hội, không nên quá lo lắng về nợ"}},

    # AN NINH & TRUYỀN THỐNG (SECURITY & TRADITION)
    {"q": "Làm sao để khu phố Elder an toàn hơn trước các vụ trộm cắp?", 
     "opts": {"A": "Đầu tư vào các câu lạc bộ thanh thiếu niên", "B": "Tăng thêm cảnh sát tuần tra", "C": "Áp dụng hình phạt tù nghiêm khắc hơn", "D": "Cải thiện đời sống người nghèo để bớt tội phạm"}},
    {"q": "Chính phủ nên ưu tiên đối tượng nhập cư nào?", 
     "opts": {"A": "Những người có kỹ năng về y tế và công nghệ", "B": "Những người lao động tay nghề cao theo nhu cầu doanh nghiệp", "C": "Nên giảm bớt người nhập cư để giữ gìn bản sắc", "D": "Chào đón tất cả những ai có thiện chí đóng góp"}},
    {"q": "Quan điểm của ba mẹ về những người tị nạn đến Úc bằng thuyền?", 
     "opts": {"A": "Nên xét duyệt định cư dựa trên lòng nhân đạo", "B": "Cần kiểm tra an ninh thật nghiêm ngặt", "C": "Kiên quyết yêu cầu tàu quay trở lại", "D": "Chào đón và cung cấp nơi ở ngay lập tức"}},
    {"q": "Trẻ em ở trường nên tập trung học điều gì nhất?", 
     "opts": {"A": "Sự bao dung và tôn trọng các nền văn hóa", "B": "Các kỹ năng thực tế về tài chính và khoa học", "C": "Lòng tự hào về lịch sử và truyền thống nước Úc", "D": "Ý thức bảo vệ môi trường và bình đẳng giới"}},
    {"q": "Chính phủ có nên có quyền kiểm tra tin nhắn mạng để bắt tội phạm?", 
     "opts": {"A": "Không, quyền riêng tư là quan trọng nhất", "B": "Có, nếu việc đó giúp bảo vệ cộng đồng", "C": "Có, trật tự và an ninh là trên hết", "D": "Không, chính phủ không nên can thiệp vào đời sống dân"}},
    {"q": "Có nên dành cho người Bản địa một tiếng nói riêng trong quốc hội (The Voice)?", 
     "opts": {"A": "Có, để tôn trọng những người chủ đầu tiên của đất nước", "B": "Không, mọi người dân Úc nên được đối xử công bằng như nhau", "C": "Không, nên tập trung vào việc thực tế thay vì hình thức", "D": "Rất cần thiết để họ có quyền tự quyết định tương lai"}},
    {"q": "Nên xử lý các vấn đề về chất gây nghiện như thế nào?", 
     "opts": {"A": "Coi là vấn đề y tế và cần hỗ trợ cai nghiện", "B": "Giữ nguyên lệnh cấm nhưng không nên phạt quá nặng", "C": "Phải phạt tù thật nặng để răn đe", "D": "Hợp pháp hóa và quản lý chặt chẽ như thuốc lá/rượu"}},
    {"q": "Chính phủ có nên bảo vệ các giá trị gia đình truyền thống?", 
     "opts": {"A": "Không, chính phủ không nên can thiệp vào lựa chọn cá nhân", "B": "Nên hỗ trợ tất cả các loại hình gia đình", "C": "Có, gia đình truyền thống là nền tảng xã hội", "D": "Nên tôn trọng sự đa dạng, không chỉ gia đình truyền thống"}},
    {"q": "Có nên lắp đặt thêm nhiều camera giám sát (CCTV) ở nơi công cộng?", 
     "opts": {"A": "Không, làm người dân cảm thấy không thoải mái", "B": "Có, giúp cảnh sát phá án nhanh hơn", "C": "Có, cần thiết để giữ gìn kỷ cương", "D": "Không, camera không giải quyết được gốc rễ tội phạm"}},
    {"q": "Lịch sử nước Úc nên được giảng dạy theo hướng nào?", 
     "opts": {"A": "Nhìn nhận khách quan cả những mặt tối trong quá khứ", "B": "Tập trung vào những thành tựu xây dựng đất nước", "C": "Giảng dạy về lòng yêu nước và sự hy sinh", "D": "Ưu tiên giảng dạy về lịch sử của người Bản địa"}},

    # MÔI TRƯỜNG & CÔNG NGHỆ (ENVIRONMENT & TECH)
    {"q": "Nguồn năng lượng nào là tốt nhất cho Nam Úc?", 
     "opts": {"A": "Năng lượng gió và mặt trời", "B": "Kết hợp các nguồn điện có chi phí thấp nhất", "C": "Sử dụng than đá để bảo đảm nguồn điện ổn định", "D": "Chuyển sang 100% năng lượng tái tạo ngay lập tức"}},
    {"q": "Chính phủ có nên dùng tiền thuế để hỗ trợ người dân mua xe điện?", 
     "opts": {"A": "Có, để bảo vệ bầu không khí sạch", "B": "Không, nên để thị trường tự quyết định", "C": "Không, nên dùng tiền đó để giảm giá xăng dầu", "D": "Có, và nên cấm hoàn toàn xe xăng trong tương lai"}},
    {"q": "Ba mẹ có ủng hộ việc xây dựng nhà máy điện hạt nhân tại Úc?", 
     "opts": {"A": "Không, vì lo ngại về an toàn và chất thải", "B": "Có thể xem xét nếu giúp giảm tiền điện", "C": "Ủng hộ mạnh mẽ để Úc có nguồn năng lượng tự chủ", "D": "Tuyệt đối không, chỉ nên dùng năng lượng xanh"}},
    {"q": "Có nên cấm sử dụng nhựa xài một lần (như ống hút, túi nilon)?", 
     "opts": {"A": "Có, đây là việc cần thiết cho môi trường", "B": "Nên thực hiện từ từ để không gây khó khăn cho doanh nghiệp", "C": "Không nên cấm vì gây bất tiện cho đời sống", "D": "Cấm ngay lập tức và phạt nặng các công ty sản xuất"}},
    {"q": "Nông dân có quyền tự do chặt cây trên đất của họ không?", 
     "opts": {"A": "Không, cần bảo vệ cây xanh để chống biến đổi khí hậu", "B": "Có, họ có quyền quản lý tài sản cá nhân", "C": "Được phép, nếu họ cam kết trồng lại cây ở nơi khác", "D": "Không, mọi việc chặt cây phải được kiểm soát nghiêm ngặt"}},
    {"q": "Ba mẹ nghĩ sao về việc xây dựng các trạm pin khổng lồ trữ điện?", 
     "opts": {"A": "Là bước đi hiện đại và đúng đắn", "B": "Chỉ làm nếu việc đó thực sự giúp giảm giá điện", "C": "Không hiệu quả bằng việc xây nhà máy điện truyền thống", "D": "Rất ủng hộ, đây là chìa khóa để bỏ than đá"}},
    {"q": "Nguồn nước sông Murray nên được ưu tiên cho ai?", 
     "opts": {"A": "Ưu tiên bảo vệ hệ sinh thái dòng sông", "B": "Ưu tiên cho nông dân sản xuất thực phẩm", "C": "Giữ nước tối đa cho nhu cầu của người Nam Úc", "D": "Trả lại nước cho thiên nhiên để hồi sinh dòng sông"}},
    {"q": "Có nên đánh thuế carbon đối với các nhà máy gây ô nhiễm?", 
     "opts": {"A": "Có, để buộc họ phải chuyển sang sản xuất sạch", "B": "Không, vì sẽ làm tăng giá hàng hóa", "C": "Chỉ đánh thuế các công ty đa quốc gia", "D": "Rất đồng ý, tiền thuế đó nên dùng để trồng rừng"}},
    {"q": "Có nên mở rộng khai thác khoáng sản (như Lithium) để làm pin?", 
     "opts": {"A": "Có, để Úc dẫn đầu về công nghệ xanh", "B": "Có, vì tạo ra nhiều việc làm lương cao", "C": "Chỉ làm ở những nơi xa khu dân cư", "D": "Chỉ khai thác nếu không gây hại đến thiên nhiên"}},
    {"q": "Nếu có thiên tai (như cháy rừng), ai nên chịu chi phí khắc phục?", 
     "opts": {"A": "Chính phủ phải trích ngân sách hỗ trợ ngay", "B": "Mỗi cá nhân nên tự mua bảo hiểm cho tài sản của mình", "C": "Cộng đồng nên quyên góp hỗ trợ lẫn nhau", "D": "Các công ty gây ô nhiễm lớn phải đóng góp kinh phí"}}
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
