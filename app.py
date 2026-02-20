import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Khảo sát Bầu cử Elder 2026", page_icon="🗳️", layout="centered")

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
    div.stButton > button:first-child { border-left: 10px solid #ff4d4d; } 
    div.stButton > button:nth-child(2) { border-left: 10px solid #3399ff; } 
    div.stButton > button:nth-child(3) { border-left: 10px solid #ffcc00; } 
    div.stButton > button:nth-child(4) { border-left: 10px solid #33cc33; } 
    
    .question-text {
        font-size: 26px !important;
        line-height: 1.4;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE ---
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
    st.session_state.scores = {"A": 0, "B": 0, "C": 0, "D": 0}
    st.session_state.history = []
    # Track scores per section
    st.session_state.sect_scores = {"Kinh tế": 0, "An ninh": 0, "Môi trường": 0}

# --- DATABASE: ALL 30 QUESTIONS ---
questions = [
    # KINH TẾ (1-10)
    {"cat": "Kinh tế", "q": "Chính phủ có nên trợ cấp tiền hằng tháng (UBI) nếu máy móc thay thế việc làm của con người?", "opts": {"A": "Có, để đảm bảo cuộc sống cơ bản", "B": "Không, nên giảm thuế tạo việc làm", "C": "Chỉ trợ cấp cho công dân lâu năm", "D": "Có, và đánh thuế các công ty robot"}},
    {"cat": "Kinh tế", "q": "Ba mẹ nghĩ sao về việc bỏ ưu đãi thuế cho người sở hữu nhiều nhà đất (Negative Gearing)?", "opts": {"A": "Đồng ý, để dùng tiền xây bệnh viện", "B": "Không đồng ý, khuyến khích đầu tư", "C": "Chỉ áp dụng với công ty địa ốc lớn", "D": "Rất đồng ý, hạ giá nhà cho người nghèo"}},
    {"cat": "Kinh tế", "q": "Cách tốt nhất để giảm giá hóa đơn điện và thực phẩm cho gia đình là gì?", "opts": {"A": "Chính phủ trực tiếp hỗ trợ tiền điện", "B": "Cắt giảm chi tiêu chính phủ để giảm lạm phát", "C": "Ưu tiên giữ hàng hóa sản xuất tại Úc", "D": "Kiểm soát giá trần tại các siêu thị lớn"}},
    {"cat": "Kinh tế", "q": "Chính phủ có nên trực tiếp xây nhà xã hội và cho thuê với giá rẻ không?", "opts": {"A": "Có, chính phủ nên quản lý nhà ở", "B": "Không, để thị trường tự do cạnh tranh", "C": "Có, nhưng chỉ dành cho người gốc Úc", "D": "Có, và phải xây thật nhiều cho mọi người"}},
    {"cat": "Kinh tế", "q": "Khi các ngân hàng lớn có lợi nhuận quá cao, họ nên làm gì?", "opts": {"A": "Đóng thêm thuế đầu tư hạ tầng", "B": "Được giữ lại để tái đầu tư kinh tế", "C": "Phải giảm lãi suất cho vay cho dân", "D": "Chia sẻ lợi nhuận cho quỹ cộng đồng"}},
    {"cat": "Kinh tế", "q": "Làm sao giúp người trẻ mua được căn nhà đầu tiên?", "opts": {"A": "Chính phủ hỗ trợ tiền đặt cọc nhà", "B": "Cắt giảm thuế trước bạ và thủ tục", "C": "Ngừng cho người nước ngoài mua đất", "D": "Đóng băng giá nhà và giới hạn sở hữu"}},
    {"cat": "Kinh tế", "q": "Học nghề (TAFE) và Đại học có nên được hoàn toàn miễn phí?", "opts": {"A": "Nên miễn phí cho các ngành ưu tiên", "B": "Mọi người nên đóng một phần học phí", "C": "Chỉ miễn phí cho công dân Úc chính gốc", "D": "Tất cả giáo dục phải miễn phí"}},
    {"cat": "Kinh tế", "q": "Tiền hưu bổng (Super) nên được sử dụng như thế nào?", "opts": {"A": "Chính phủ đóng thêm cho người thu nhập thấp", "B": "Cho phép rút sớm để mua nhà", "C": "Giữ nguyên bảo đảm tuổi già", "D": "Tăng đóng góp bắt buộc từ các tập đoàn"}},
    {"cat": "Kinh tế", "q": "Có nên áp đặt giới hạn tăng tiền thuê nhà (Rent caps)?", "opts": {"A": "Có, để bảo vệ người đi thuê nhà", "B": "Không, làm chủ nhà không muốn sửa nhà", "C": "Chỉ áp dụng cho các căn hộ lớn", "D": "Dừng việc tăng tiền thuê ngay lập tức"}},
    {"cat": "Kinh tế", "q": "Chính phủ nên làm gì với các khoản nợ quốc gia?", "opts": {"A": "Vay thêm nếu cần đầu tư y tế/giáo dục", "B": "Phải trả nợ nhanh dù phải cắt chi tiêu", "C": "Chỉ vay cho các dự án quốc phòng", "D": "Ưu tiên an sinh xã hội, không lo nợ"}},

    # AN NINH & TRUYỀN THỐNG (11-20)
    {"cat": "An ninh", "q": "Làm sao để khu phố Elder an toàn hơn trước các vụ trộm cắp?", "opts": {"A": "Đầu tư vào giáo dục thanh thiếu niên", "B": "Tăng thêm cảnh sát tuần tra", "C": "Áp dụng hình phạt tù nghiêm khắc hơn", "D": "Cải thiện đời sống người nghèo"}},
    {"cat": "An ninh", "q": "Chính phủ nên ưu tiên đối tượng nhập cư nào?", "opts": {"A": "Người có kỹ năng y tế và công nghệ", "B": "Người lao động tay nghề cao theo nhu cầu", "C": "Nên giảm bớt người nhập cư giữ bản sắc", "D": "Chào đón tất cả ai có thiện chí đóng góp"}},
    {"cat": "An ninh", "q": "Quan điểm của ba mẹ về những người tị nạn đến Úc bằng thuyền?", "opts": {"A": "Xét duyệt dựa trên lòng nhân đạo", "B": "Cần kiểm tra an ninh thật nghiêm ngặt", "C": "Kiên quyết yêu cầu tàu quay trở lại", "D": "Chào đón và hỗ trợ nơi ở ngay"}},
    {"cat": "An ninh", "q": "Trẻ em ở trường nên tập trung học điều gì nhất?", "opts": {"A": "Sự bao dung và tôn trọng đa văn hóa", "B": "Kỹ năng tài chính và khoa học", "C": "Lòng tự hào về lịch sử và truyền thống", "D": "Ý thức bảo vệ môi trường và bình đẳng"}},
    {"cat": "An ninh", "q": "Chính phủ có nên quyền kiểm tra tin nhắn mạng để bắt tội phạm?", "opts": {"A": "Không, quyền riêng tư là quan trọng nhất", "B": "Có, nếu giúp bảo vệ cộng đồng", "C": "Có, trật tự và an ninh là trên hết", "D": "Không, chính phủ không nên can thiệp"}},
    {"cat": "An ninh", "q": "Có nên dành cho người Bản địa một tiếng nói riêng (The Voice)?", "opts": {"A": "Có, tôn trọng chủ nhân đầu tiên của đất nước", "B": "Không, mọi người nên được đối xử giống nhau", "C": "Không, tập trung vào việc thực tế", "D": "Rất cần thiết để họ có quyền tự quyết"}},
    {"cat": "An ninh", "q": "Nên xử lý các vấn đề về chất gây nghiện như thế nào?", "opts": {"A": "Coi là vấn đề y tế và hỗ trợ cai nghiện", "B": "Giữ lệnh cấm nhưng không phạt quá nặng", "C": "Phải phạt tù thật nặng để răn đe", "D": "Hợp pháp hóa và quản lý như thuốc lá"}},
    {"cat": "An ninh", "q": "Chính phủ có nên bảo vệ các giá trị gia đình truyền thống?", "opts": {"A": "Không, đừng can thiệp lựa chọn cá nhân", "B": "Nên hỗ trợ tất cả các loại hình gia đình", "C": "Có, gia đình truyền thống là nền tảng", "D": "Tôn trọng sự đa dạng, không chỉ truyền thống"}},
    {"cat": "An ninh", "q": "Có nên lắp đặt thêm nhiều camera giám sát (CCTV) công cộng?", "opts": {"A": "Không, làm người dân không thoải mái", "B": "Có, giúp cảnh sát phá án nhanh hơn", "C": "Có, cần thiết để giữ kỷ cương", "D": "Không, camera không giải quyết gốc rễ"}},
    {"cat": "An ninh", "q": "Lịch sử nước Úc nên được giảng dạy theo hướng nào?", "opts": {"A": "Nhìn nhận khách quan cả những mặt tối", "B": "Tập trung vào những thành tựu vĩ đại", "C": "Giảng dạy lòng yêu nước và sự hy sinh", "D": "Ưu tiên lịch sử của người Bản địa"}},

    # MÔI TRƯỜNG & CÔNG NGHỆ (21-30)
    {"cat": "Môi trường", "q": "Nguồn năng lượng nào là tốt nhất cho Nam Úc?", "opts": {"A": "Năng lượng gió và mặt trời", "B": "Kết hợp các nguồn điện rẻ nhất", "C": "Sử dụng than đá bảo đảm ổn định", "D": "Chuyển sang 100% năng lượng tái tạo ngay"}},
    {"cat": "Môi trường", "q": "Chính phủ có nên hỗ trợ tiền mua xe điện (EV)?", "opts": {"A": "Có, để bảo vệ bầu không khí sạch", "B": "Không, để thị trường tự quyết định", "C": "Không, nên dùng tiền giảm giá xăng dầu", "D": "Có, và cấm xe xăng trong tương lai"}},
    {"cat": "Môi trường", "q": "Ba mẹ có ủng hộ xây nhà máy điện hạt nhân tại Úc?", "opts": {"A": "Không, vì lo ngại an toàn và chất thải", "B": "Có thể xem xét nếu giúp giảm tiền điện", "C": "Ủng hộ mạnh mẽ để Úc tự chủ năng lượng", "D": "Tuyệt đối không, chỉ dùng năng lượng xanh"}},
    {"cat": "Môi trường", "q": "Có nên cấm nhựa xài một lần (ống hút, túi nilon)?", "opts": {"A": "Có, rất cần thiết cho môi trường", "B": "Nên làm từ từ để doanh nghiệp quen", "C": "Không nên cấm vì bất tiện", "D": "Cấm ngay và phạt nặng công ty sản xuất"}},
    {"cat": "Môi trường", "q": "Nông dân có quyền tự do chặt cây trên đất của họ không?", "opts": {"A": "Không, cần bảo vệ rừng chống biến đổi khí hậu", "B": "Có, họ có quyền quản lý tài sản cá nhân", "C": "Được phép, nếu cam kết trồng lại cây", "D": "Không, phải được kiểm soát nghiêm ngặt"}},
    {"cat": "Môi trường", "q": "Ba mẹ nghĩ sao về việc xây các trạm pin khổng lồ trữ điện?", "opts": {"A": "Là bước đi hiện đại và đúng đắn", "B": "Chỉ làm nếu giúp giảm giá điện", "C": "Không hiệu quả bằng điện truyền thống", "D": "Rất ủng hộ, đây là chìa khóa bỏ than đá"}},
    {"cat": "Môi trường", "q": "Nguồn nước sông Murray nên được ưu tiên cho ai?", "opts": {"A": "Ưu tiên bảo vệ hệ sinh thái dòng sông", "B": "Ưu tiên cho nông dân sản xuất thực phẩm", "C": "Giữ tối đa cho người Nam Úc", "D": "Trả lại nước cho thiên nhiên"}},
    {"cat": "Môi trường", "q": "Có nên đánh thuế carbon đối với nhà máy gây ô nhiễm?", "opts": {"A": "Có, để buộc họ chuyển sang điện sạch", "B": "Không, vì làm tăng giá hàng hóa", "C": "Chỉ đánh thuế các công ty đa quốc gia", "D": "Rất đồng ý, dùng tiền đó trồng rừng"}},
    {"cat": "Môi trường", "q": "Có nên mở rộng khai thác khoáng sản (Lithium) làm pin?", "opts": {"A": "Có, để Úc dẫn đầu công nghệ xanh", "B": "Có, tạo nhiều việc làm lương cao", "C": "Chỉ làm ở xa khu dân cư", "D": "Chỉ khai thác nếu không hại thiên nhiên"}},
    {"cat": "Môi trường", "q": "Nếu có thiên tai, ai nên chịu chi phí khắc phục?", "opts": {"A": "Chính phủ phải hỗ trợ ngay", "B": "Mỗi cá nhân nên tự mua bảo hiểm", "C": "Cộng đồng quyên góp giúp nhau", "D": "Các công ty ô nhiễm lớn phải đóng góp"}}
]

def process_answer(choice, category):
    st.session_state.scores[choice] += 1
    st.session_state.sect_scores[category] += 1
    st.session_state.history.append((choice, category))
    st.session_state.current_q += 1

def go_back():
    if st.session_state.current_q > 0:
        last_choice, last_cat = st.session_state.history.pop()
        st.session_state.scores[last_choice] -= 1
        st.session_state.sect_scores[last_cat] -= 1
        st.session_state.current_q -= 1

# --- MAIN UI ---
st.title("🗳️ Khảo sát Bầu cử Elder 2026")

if st.session_state.current_q < len(questions):
    q_data = questions[st.session_state.current_q]
    st.progress(st.session_state.current_q / len(questions))
    st.write(f"Chủ đề: **{q_data['cat']}** | Câu {st.session_state.current_q + 1}/30")
    st.markdown(f'<p class="question-text">{q_data["q"]}</p>', unsafe_allow_html=True)

    for key, val in q_data['opts'].items():
        if st.button(val, key=f"btn_{st.session_state.current_q}_{key}"):
            process_answer(key, q_data['cat'])
            st.rerun()

    st.divider()
    if st.button("← QUAY LẠI (BACK)", disabled=(st.session_state.current_q == 0)):
        go_back()
        st.rerun()

else:
    st.balloons()
    winner = max(st.session_state.scores, key=st.session_state.scores.get)
    top_sect = max(st.session_state.sect_scores, key=st.session_state.sect_scores.get)
    
    res_map = {
        "A": "NADIA CLANCY (Lao Động)", 
        "B": "SHAWN VAN GROESEN (Tự Do)", 
        "C": "MATTHEW MANGELSDORF (One Nation)", 
        "D": "STEF ROZITIS (Đảng Xanh)"
    }
    
    st.markdown("---")
    st.header("🏁 Kết quả khảo sát của Ba Mẹ")

    # Use Columns to make the text and chart visible together
    col_text, col_chart = st.columns([1, 1])

    with col_text:
        st.subheader("💡 Gợi ý cho Ba Mẹ")
        # st.metric makes the result big and bold
        st.metric(label="Ứng cử viên phù hợp", value=res_map[winner])
        st.write(f"Chủ đề ba mẹ quan tâm nhất: **{top_sect}**")
        
        st.info(f"Dựa trên 30 câu trả lời, quan điểm của ba mẹ gần gũi nhất với cương lĩnh của {res_map[winner]}.")

    with col_chart:
        st.subheader("📊 Biểu đồ phân tích")
        # Prepare data for a cleaner bar chart
        chart_data = {
            "Đảng": ["Lao Động", "Tự Do", "One Nation", "Đảng Xanh"],
            "Điểm": [st.session_state.scores["A"], st.session_state.scores["B"], 
                     st.session_state.scores["C"], st.session_state.scores["D"]]
        }
        st.bar_chart(data=chart_data, x="Đảng", y="Điểm", color="Đảng")

    st.markdown("---")

