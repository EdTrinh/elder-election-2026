import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Elder 2026 Election Survey", page_icon="🗳️", layout="centered")

# --- CUSTOM CSS FOR READABILITY ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 4.5em;
        font-size: 18px !important;
        font-weight: 500;
        margin-bottom: 12px;
        border-radius: 12px;
        transition: all 0.2s;
    }
    .question-text {
        font-size: 24px !important;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 25px;
        line-height: 1.4;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE ---
if 'lang' not in st.session_state:
    st.session_state.lang = None
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
    st.session_state.scores = {"A": 0, "B": 0, "C": 0, "D": 0}
    st.session_state.sect_scores = {"Economy": 0, "Security": 0, "Environment": 0}
    st.session_state.history = []

# --- TRANSLATIONS FOR UI ---
UI = {
    "en": {
        "title": "Elder 2026 Election Survey",
        "back": "← BACK",
        "reset": "Start Over",
        "result_header": "🏁 Your Results",
        "match": "Best Candidate Match:",
        "top_topic": "You cared most about:",
        "chart_title": "Party Alignment Breakdown",
        "parties": ["Labor", "Liberal", "One Nation", "Greens"]
    },
    "vi": {
        "title": "Khảo sát Bầu cử Elder 2026",
        "back": "← QUAY LẠI",
        "reset": "Làm lại từ đầu",
        "result_header": "🏁 Kết quả dành cho Ba Mẹ",
        "match": "Ứng cử viên phù hợp nhất:",
        "top_topic": "Chủ đề ba mẹ quan tâm nhất:",
        "chart_title": "Biểu đồ phân tích chi tiết",
        "parties": ["Lao Động", "Tự Do", "One Nation", "Đảng Xanh"]
    }
}

# --- THE 30 QUESTIONS DATABASE ---
questions = [
    # ECONOMY (1-10)
    {"cat": "Economy", 
     "q_en": "Should the govt provide a monthly allowance (UBI) if machines replace human jobs?", 
     "q_vi": "Chính phủ có nên trợ cấp tiền hằng tháng (UBI) nếu máy móc thay thế việc làm của con người?",
     "opts_en": {"A": "Yes, for basic living", "B": "No, cut taxes for jobs", "C": "Only for long-term citizens", "D": "Yes, tax robot companies"},
     "opts_vi": {"A": "Có, để đảm bảo cuộc sống", "B": "Không, giảm thuế tạo việc làm", "C": "Chỉ cho công dân lâu năm", "D": "Có, đánh thuế công ty robot"}},
    {"cat": "Economy", 
     "q_en": "Should tax perks (Negative Gearing) be removed for those with many properties?", 
     "q_vi": "Có nên bỏ ưu đãi thuế (Negative Gearing) cho người sở hữu nhiều nhà đất không?",
     "opts_en": {"A": "Agree, fund hospitals", "B": "Disagree, encourages investment", "C": "Only for big corporations", "D": "Strongly agree, lower house prices"},
     "opts_vi": {"A": "Đồng ý, dùng tiền xây bệnh viện", "B": "Không, khuyến khích đầu tư", "C": "Chỉ cho các công ty lớn", "D": "Rất đồng ý, hạ giá nhà"}},
    {"cat": "Economy", 
     "q_en": "Best way to lower electricity and grocery bills?", 
     "q_vi": "Cách tốt nhất để giảm giá hóa đơn điện và thực phẩm là gì?",
     "opts_en": {"A": "Direct govt bill rebates", "B": "Cut govt spending to lower inflation", "C": "Keep Aussie goods for local use", "D": "Price caps on big supermarkets"},
     "opts_vi": {"A": "Hỗ trợ tiền điện trực tiếp", "B": "Cắt chi tiêu giảm lạm phát", "C": "Ưu tiên giữ hàng nội địa", "D": "Áp giá trần cho siêu thị"}},
    {"cat": "Economy", 
     "q_en": "Should the govt build social housing and rent it out cheaply?", 
     "q_vi": "Chính phủ có nên trực tiếp xây nhà xã hội và cho thuê giá rẻ không?",
     "opts_en": {"A": "Yes, govt should manage it", "B": "No, let the market compete", "C": "Only for Australian-born citizens", "D": "Yes, build for everyone"},
     "opts_vi": {"A": "Có, chính phủ nên quản lý", "B": "Không, để thị trường tự do", "C": "Chỉ cho người gốc Úc", "D": "Có, xây thật nhiều cho dân"}},
    {"cat": "Economy", 
     "q_en": "When big banks make massive profits, what should happen?", 
     "q_vi": "Khi các ngân hàng lớn có lợi nhuận quá cao, họ nên làm gì?",
     "opts_en": {"A": "Pay more tax for infrastructure", "B": "Reinvest into the economy", "C": "Lower loan interest rates", "D": "Share with community funds"},
     "opts_vi": {"A": "Đóng thêm thuế hạ tầng", "B": "Để họ tái đầu tư kinh tế", "C": "Phải giảm lãi suất cho vay", "D": "Chia lợi nhuận cho quỹ dân"}},
    {"cat": "Economy", 
     "q_en": "How to help young people buy their first home?", 
     "q_vi": "Làm sao giúp người trẻ mua được căn nhà đầu tiên?",
     "opts_en": {"A": "Govt help with deposit", "B": "Cut stamp duty and red tape", "C": "Ban foreign land ownership", "D": "Freeze house prices"},
     "opts_vi": {"A": "Hỗ trợ tiền đặt cọc nhà", "B": "Cắt thuế trước bạ và thủ tục", "C": "Cấm người nước ngoài mua đất", "D": "Đóng băng giá nhà đất"}},
    {"cat": "Economy", 
     "q_en": "Should TAFE and University be completely free?", 
     "q_vi": "Học nghề (TAFE) và Đại học có nên được hoàn toàn miễn phí?",
     "opts_en": {"A": "Free for priority jobs only", "B": "Everyone should pay a portion", "C": "Free for Aussie-born citizens", "D": "Free for everyone"},
     "opts_vi": {"A": "Miễn phí ngành ưu tiên", "B": "Mọi người nên tự đóng góp", "C": "Chỉ miễn phí cho dân gốc Úc", "D": "Tất cả phải miễn phí"}},
    {"cat": "Economy", 
     "q_en": "How should Superannuation be used?", 
     "q_vi": "Tiền hưu bổng (Super) nên được sử dụng như thế nào?",
     "opts_en": {"A": "Govt top up for low earners", "B": "Allow withdrawal for first home", "C": "Keep it for retirement only", "D": "Increase corporate contributions"},
     "opts_vi": {"A": "Hỗ trợ thêm cho người nghèo", "B": "Cho rút mua nhà đầu tiên", "C": "Giữ nguyên cho tuổi già", "D": "Tăng mức đóng từ tập đoàn"}},
    {"cat": "Economy", 
     "q_en": "Should there be limits on rent increases (Rent caps)?", 
     "q_vi": "Có nên áp đặt giới hạn tăng tiền thuê nhà (Rent caps)?",
     "opts_en": {"A": "Yes, to protect tenants", "B": "No, stops maintenance", "C": "Only for large apartments", "D": "Freeze all rents now"},
     "opts_vi": {"A": "Có, để bảo vệ người thuê", "B": "Không, chủ nhà sẽ bỏ bê nhà", "C": "Chỉ cho căn hộ chung cư lớn", "D": "Dừng tăng tiền thuê ngay"}},
    {"cat": "Economy", 
     "q_en": "How should the govt manage national debt?", 
     "q_vi": "Chính phủ nên làm gì với các khoản nợ quốc gia?",
     "opts_en": {"A": "Borrow for health/education", "B": "Pay back fast via cuts", "C": "Borrow for defense only", "D": "Welfare is more important"},
     "opts_vi": {"A": "Vay đầu tư y tế/giáo dục", "B": "Phải trả nợ nhanh chóng", "C": "Chỉ vay cho quốc phòng", "D": "Quan trọng là an sinh xã hội"}},

    # SECURITY & TRADITION (11-20)
    {"cat": "Security", 
     "q_en": "How to make the Elder area safer from crime?", 
     "q_vi": "Làm sao để khu phố Elder an toàn hơn trước tội phạm?",
     "opts_en": {"A": "Invest in youth programs", "B": "Increase police patrols", "C": "Harsher prison sentences", "D": "Fix poverty first"},
     "opts_vi": {"A": "Đầu tư giáo dục thanh niên", "B": "Tăng thêm cảnh sát tuần tra", "C": "Phạt tù thật nghiêm khắc", "D": "Giải quyết tận gốc nghèo đói"}},
    {"cat": "Security", 
     "q_en": "Who should be the immigration priority?", 
     "q_vi": "Chính phủ nên ưu tiên đối tượng nhập cư nào?",
     "opts_en": {"A": "Health and tech workers", "B": "High-skilled business needs", "C": "Reduce intake for identity", "D": "Welcome all who contribute"},
     "opts_vi": {"A": "Người có kỹ năng y tế/công nghệ", "B": "Lao động theo nhu cầu kinh tế", "C": "Giảm nhập cư giữ bản sắc", "D": "Chào đón tất cả mọi người"}},
    {"cat": "Security", 
     "q_en": "View on refugees arriving by boat?", 
     "q_vi": "Quan điểm về người tị nạn đến Úc bằng thuyền?",
     "opts_en": {"A": "Humanitarian processing", "B": "Strict security checks", "C": "Turn the boats back", "D": "Welcome and house them"},
     "opts_vi": {"A": "Xét duyệt theo lòng nhân đạo", "B": "Kiểm tra an ninh nghiêm ngặt", "C": "Kiên quyết đẩy tàu trở lại", "D": "Chào đón và giúp đỡ ngay"}},
    {"cat": "Security", 
     "q_en": "What should schools focus on most?", 
     "q_vi": "Trẻ em ở trường nên tập trung học điều gì nhất?",
     "opts_en": {"A": "Tolerance and diversity", "B": "Finance and science", "C": "Australian history/pride", "D": "Climate and equality"},
     "opts_vi": {"A": "Sự bao dung và đa văn hóa", "B": "Kỹ năng tài chính và khoa học", "C": "Lòng tự hào và truyền thống", "D": "Môi trường và bình đẳng"}},
    {"cat": "Security", 
     "q_en": "Should govt check private messages for crimes?", 
     "q_vi": "Chính phủ có nên kiểm tra tin nhắn mạng để bắt tội phạm?",
     "opts_en": {"A": "No, privacy is key", "B": "Yes, if it protects community", "C": "Yes, security is priority", "D": "No, govt shouldn't interfere"},
     "opts_vi": {"A": "Không, quyền riêng tư là nhất", "B": "Có, để bảo vệ cộng đồng", "C": "Có, an ninh là trên hết", "D": "Không, đừng can thiệp dân"}},
    {"cat": "Security", 
     "q_en": "A separate Indigenous Voice to Parliament?", 
     "q_vi": "Có nên dành cho người Bản địa tiếng nói riêng (The Voice)?",
     "opts_en": {"A": "Yes, respect first owners", "B": "No, treat everyone equal", "C": "No, focus on practical results", "D": "Essential for self-rule"},
     "opts_vi": {"A": "Có, tôn trọng chủ nhân đất", "B": "Không, mọi người như nhau", "C": "Không, hãy làm việc thực tế", "D": "Rất cần để họ tự quyết"}},
    {"cat": "Security", 
     "q_en": "How to handle drug/cannabis issues?", 
     "q_vi": "Nên xử lý các vấn đề chất gây nghiện như thế nào?",
     "opts_en": {"A": "Treat as health/rehab", "B": "Illegal but no harsh fines", "C": "Heavy jail as deterrent", "D": "Legalise and regulate"},
     "opts_vi": {"A": "Coi là vấn đề y tế/cai nghiện", "B": "Cấm nhưng không phạt nặng", "C": "Phạt tù thật nặng để răn đe", "D": "Hợp pháp hóa và quản lý"}},
    {"cat": "Security", 
     "q_en": "Should govt protect traditional family values?", 
     "q_vi": "Chính phủ có nên bảo vệ giá trị gia đình truyền thống?",
     "opts_en": {"A": "No, personal choice", "B": "Support all family types", "C": "Yes, it's the foundation", "D": "Respect diversity only"},
     "opts_vi": {"A": "Không, lựa chọn cá nhân", "B": "Hỗ trợ mọi loại gia đình", "C": "Có, gia đình là nền tảng", "D": "Tôn trọng sự đa dạng"}},
    {"cat": "Security", 
     "q_en": "More public CCTV cameras?", 
     "q_vi": "Có nên lắp thêm nhiều camera giám sát công cộng?",
     "opts_en": {"A": "No, uncomfortable", "B": "Yes, helps solve crimes", "C": "Yes, maintains discipline", "D": "No, doesn't fix root causes"},
     "opts_vi": {"A": "Không, cảm thấy bất an", "B": "Có, giúp cảnh sát phá án", "C": "Có, cần để giữ kỷ cương", "D": "Không, không giải quyết gốc"}},
    {"cat": "Security", 
     "q_en": "How should Australian history be taught?", 
     "q_vi": "Lịch sử nước Úc nên được giảng dạy thế nào?",
     "opts_en": {"A": "Include dark parts/truth", "B": "Focus on achievements", "C": "Teach patriotism", "D": "Prioritise First Nations"},
     "opts_vi": {"A": "Nhìn nhận cả những mặt tối", "B": "Tập trung vào thành tựu", "C": "Dạy về lòng yêu nước", "D": "Ưu tiên lịch sử Bản địa"}},

    # ENVIRONMENT (21-30)
    {"cat": "Environment", 
     "q_en": "Best energy source for SA?", 
     "q_vi": "Nguồn năng lượng tốt nhất cho Nam Úc?",
     "opts_en": {"A": "Wind and solar", "B": "Cheapest mix", "C": "Coal for stability", "D": "100% renewables now"},
     "opts_vi": {"A": "Gió và mặt trời", "B": "Kết hợp nguồn rẻ nhất", "C": "Than đá cho ổn định", "D": "100% tái tạo ngay lập tức"}},
    {"cat": "Environment", 
     "q_en": "Tax money to help people buy EVs?", 
     "q_vi": "Dùng tiền thuế hỗ trợ dân mua xe điện (EV)?",
     "opts_en": {"A": "Yes, for clean air", "B": "No, market decide", "C": "No, lower petrol price", "D": "Yes, ban petrol later"},
     "opts_vi": {"A": "Có, để sạch không khí", "B": "Không, để thị trường tự do", "C": "Không, nên giảm giá xăng", "D": "Có, và cấm xe xăng sau này"}},
    {"cat": "Environment", 
     "q_en": "Nuclear power plants in Australia?", 
     "q_vi": "Có ủng hộ xây điện hạt nhân tại Úc không?",
     "opts_en": {"A": "No, safety concerns", "B": "Maybe if it lowers bills", "C": "Strong support", "D": "Never, only green energy"},
     "opts_vi": {"A": "Không, lo ngại an toàn", "B": "Có thể nếu giúp giảm giá", "C": "Ủng hộ mạnh mẽ", "D": "Tuyệt đối không, chỉ xanh"}},
    {"cat": "Environment", 
     "q_en": "Ban single-use plastics?", 
     "q_vi": "Có nên cấm nhựa xài một lần?",
     "opts_en": {"A": "Yes, essential", "B": "Slowly for business", "C": "No, inconvenient", "D": "Ban and fine now"},
     "opts_vi": {"A": "Có, rất cần thiết", "B": "Làm từ từ cho công ty quen", "C": "Không, vì bất tiện", "D": "Cấm ngay và phạt nặng"}},
    {"cat": "Environment", 
     "q_en": "Can farmers clear trees on their land?", 
     "q_vi": "Nông dân có quyền tự chặt cây trên đất họ không?",
     "opts_en": {"A": "No, protect climate", "B": "Yes, private property", "C": "Yes, if they replant", "D": "Strict govt control"},
     "opts_vi": {"A": "Không, bảo vệ khí hậu", "B": "Có, quyền sở hữu cá nhân", "C": "Được, nếu trồng lại cây", "D": "Chính phủ kiểm soát kỹ"}},
    {"cat": "Environment", 
     "q_en": "Giant batteries for energy storage?", 
     "q_vi": "Xây trạm pin khổng lồ trữ điện?",
     "opts_en": {"A": "Modern and correct", "B": "Only if saves money", "C": "Inefficient vs coal", "D": "Key to quitting coal"},
     "opts_vi": {"A": "Hiện đại và đúng đắn", "B": "Nếu thực sự giảm giá điện", "C": "Không tốt bằng truyền thống", "D": "Chìa khóa để bỏ than đá"}},
    {"cat": "Environment", 
     "q_en": "Murray River water priority?", 
     "q_vi": "Nguồn nước sông Murray ưu tiên cho ai?",
     "opts_en": {"A": "Ecosystem/River health", "B": "Farmers for food", "C": "Keep for South Aussies", "D": "Return to nature"},
     "opts_vi": {"A": "Hệ sinh thái dòng sông", "B": "Nông dân sản xuất thực phẩm", "C": "Giữ cho người Nam Úc", "D": "Trả lại cho thiên nhiên"}},
    {"cat": "Environment", 
     "q_en": "Tax factories for pollution (Carbon Tax)?", 
     "q_vi": "Đánh thuế carbon các nhà máy ô nhiễm?",
     "opts_en": {"A": "Yes, force clean tech", "B": "No, raises prices", "C": "Only multinations", "D": "Yes, use for forests"},
     "opts_vi": {"A": "Có, ép họ dùng điện sạch", "B": "Không, sẽ làm tăng giá", "C": "Chỉ các công ty đa quốc gia", "D": "Đồng ý, dùng tiền trồng rừng"}},
    {"cat": "Environment", 
     "q_en": "Expand mining (Lithium) for batteries?", 
     "q_vi": "Mở rộng khai thác Lithium làm pin?",
     "opts_en": {"A": "Yes, lead green tech", "B": "Yes, high-pay jobs", "C": "Only far from homes", "D": "Only if zero harm"},
     "opts_vi": {"A": "Có, dẫn đầu công nghệ xanh", "B": "Có, tạo việc làm lương cao", "C": "Chỉ làm ở xa dân cư", "D": "Chỉ làm nếu không hại gì"}},
    {"cat": "Environment", 
     "q_en": "Who pays for natural disaster damage?", 
     "q_vi": "Ai nên chịu chi phí khắc phục thiên tai?",
     "opts_en": {"A": "Govt budget support", "B": "Personal insurance", "C": "Community donations", "D": "Big polluters must pay"},
     "opts_vi": {"A": "Chính phủ chi ngân sách", "B": "Cá nhân tự mua bảo hiểm", "C": "Cộng đồng quyên góp", "D": "Công ty ô nhiễm phải trả"}}
]

# --- APP LOGIC ---
def reset_app():
    st.session_state.current_q = 0
    st.session_state.lang = None
    st.session_state.scores = {"A": 0, "B": 0, "C": 0, "D": 0}
    st.session_state.sect_scores = {"Economy": 0, "Security": 0, "Environment": 0}
    st.session_state.history = []

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

# --- UI RENDERING ---
if st.session_state.lang is None:
    st.title("Election 2026 / Bầu cử 2026")
    st.subheader("Select Language / Chọn Ngôn Ngữ")
    col1, col2 = st.columns(2)
    if col1.button("ENGLISH"):
        st.session_state.lang = "en"
        st.rerun()
    if col2.button("TIẾNG VIỆT"):
        st.session_state.lang = "vi"
        st.rerun()

elif st.session_state.current_q < len(questions):
    L = st.session_state.lang
    q_data = questions[st.session_state.current_q]
    
    st.title(UI[L]["title"])
    st.progress(st.session_state.current_q / len(questions))
    st.write(f"**{st.session_state.current_q + 1} / 30**")
    
    st.markdown(f'<p class="question-text">{q_data[f"q_{L}"]}</p>', unsafe_allow_html=True)
    
    for key, val in q_data[f"opts_{L}"].items():
        if st.button(val, key=f"btn_{st.session_state.current_q}_{key}"):
            process_answer(key, q_data["cat"])
            st.rerun()
    
    st.divider()
    if st.button(UI[L]["back"], disabled=(st.session_state.current_q == 0)):
        go_back()
        st.rerun()

else:
    L = st.session_state.lang
    st.balloons()
    winner = max(st.session_state.scores, key=st.session_state.scores.get)
    top_sect = max(st.session_state.sect_scores, key=st.session_state.sect_scores.get)
    
    res_map = {
        "A": "Labor (Nadia Clancy)", 
        "B": "Liberal (Shawn van Groesen)", 
        "C": "One Nation (Matthew Mangelsdorf)", 
        "D": "Greens (Stef Rozitis)"
    }
    
    st.header(UI[L]["result_header"])
    st.metric(label=UI[L]["match"], value=res_map[winner])
    st.info(f"{UI[L]['top_topic']} **{top_sect}**")

    st.subheader(UI[L]["chart_title"])
    chart_data = {
        "Party": UI[L]["parties"],
        "Points": [st.session_state.scores[k] for k in ["A", "B", "C", "D"]]
    }
    st.bar_chart(data=chart_data, x="Party", y="Points", color="Party")

    if st.button(UI[L]["reset"]):
        reset_app()
        st.rerun()
