import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import warnings
from matplotlib import font_manager as fm
from streamlit_option_menu import option_menu
import os

# 한글 폰트 설정 (프로젝트 내부에서 폰트 로드)
def set_korean_font():
    font_path = "NotoSansKR-VariableFont_wght.ttf"  # 다운받은 폰트 파일 경로
    if os.path.exists(font_path):  # 파일이 존재하는지 확인
        fm.fontManager.addfont(font_path)  # 폰트 등록
        plt.rc('font', family='Noto Sans KR')  # 폰트 이름 설정
        plt.rc('axes', unicode_minus=False)  # 마이너스 기호 깨짐 방지
    else:
        raise FileNotFoundError(f"폰트 파일을 찾을 수 없습니다. '{font_path}'를 프로젝트 디렉토리에 업로드하세요.")

# 한국어 폰트 적용
set_korean_font()

# Streamlit 페이지 설정
st.set_page_config(page_title="혼인율 및 결혼 인식 변화 분석", layout="wide")

#####################################
#1. 결혼인식 대비 대한 혼인율 데이터

# 배경 색상을 변경하는 함수
def set_background_color():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #FEFFED; /* 연한 노랑색 */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Streamlit 앱 시작
set_background_color()


# 사이드바 설정
with st.sidebar:
    option = option_menu(
        "탐구하고자 하는 데이터",  # 메뉴 제목
        ["결혼 및 혼인 데이터", "자녀 계획 및 출산 데이터"],  # 메뉴 항목
        icons=["heart-fill", "person-fill-add"],  #각 항목 아이콘
        menu_icon="app-indicator",  # 사이드바 아이콘
        default_index=0,  # 기본 선택 항목
        styles={
            "container": {"padding": "5px", "background-color": "#f8f9fa"},
            "icon": {"color": "plum", "font-size": "20px"}, 
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#e8f5fa",
            },
            "nav-link-selected": {"background-color": "#08c7b4", "color": "white"},
        },
    )
    
     # 사이드바 하단에 이미지 추가
    st.image(
        "https://liberal.kangwon.ac.kr/_attach/knu/image/2021/11/UuLZqXtPWLSbaJvNcfRdeKlfre.png",  # 이미지 URL 또는 파일 경로
        caption="곰두리",  # 이미지 캡션
        use_container_width=True  # 사이드바 너비에 맞추어 이미지 크기 조정
    )   
    
    st.write(
    """
    <중급반_2조: 이현조>\n
    1. 박준석: 개발(자녀 계획 및 Streamlit)\n
    2. 양민영: 개발(결혼 및 혼인)\n
    3. 김현우: 자료 및 디자인 총괄
    """
    )


if option == "결혼 및 혼인 데이터":
    # 제목 입력 1번 주제
    st.title("결혼 및 혼인 데이터를 분석해보자" )
    st.write("""
    =================================================================================================
    """)



    # 혼인율 데이터 입력
    yearly_data_manual = { 
        "연도": [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
        "남성_평균혼인율": [14.5, 13.8, 13.8, 13.1, 12.0, 11.9, 10.6, 9.1, 8.5, 8.5],
        "여성_평균혼인율": [12.7, 12.1, 12.1, 11.6, 10.7, 10.4, 9.3, 8.3, 7.8, 7.8]
    }
    df_yearly_honin = pd.DataFrame(yearly_data_manual)

    # 결혼에 대한 인식 데이터 입력
    data_perception_retry = {
        "연도": [1998, 2002, 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020, 2022],
        "반드시 해야 한다": [33.6, 25.6, 25.7, 23.6, 21.7, 20.3, 14.9, 12.5, 11.1, 16.8, 15.3],
        "하는 것이 좋다": [39.9, 43.5, 42.0, 44.4, 43.0, 42.4, 41.9, 39.3, 37.0, 34.4, 34.8],
        "해도 좋고, 하지 않아도 좋다": [23.8, 27.2, 27.5, 27.7, 30.7, 33.6, 38.9, 42.9, 46.6, 41.4, 43.2],
        "하지 않는 것이 좋다": [1.1, 1.7, 1.8, 2.4, 2.8, 1.5, 1.6, 2.5, 2.5, 3.5, 2.9],
        "하지 말아야 한다": [0.2, 0.2, 0.4, 0.5, 0.5, 0.3, 0.4, 0.6, 0.5, 0.9, 0.7],
        "잘 모르겠다": [1.4, 1.8, 2.6, 1.4, 1.3, 1.9, 2.2, 2.2, 2.3, 3.0, 3.2]
    }
    df_perception = pd.DataFrame(data_perception_retry)

    # 공통 연도 필터링
    common_years = set(df_yearly_honin["연도"]) & set(df_perception["연도"])
    df_yearly_honin_filtered = df_yearly_honin[df_yearly_honin["연도"].isin(common_years)]
    df_perception_filtered = df_perception[df_perception["연도"].isin(common_years)]

    # Streamlit 데이터프레임 출력
    st.subheader("<혼인율 및 결혼 인식 변화 시각화>")
    st.dataframe(df_yearly_honin_filtered)

    st.dataframe(df_perception_filtered)

    # 시각화
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # 혼인율 막대그래프 (공통 연도만, 크기 조정)
    bar_width = 0.35
    ax1.bar(df_yearly_honin_filtered["연도"] - bar_width / 2,
        df_yearly_honin_filtered["남성_평균혼인율"],
        width=bar_width, label="남성 평균 혼인율", color="blue", alpha=0.7)
    ax1.bar(df_yearly_honin_filtered["연도"] + bar_width / 2,
            df_yearly_honin_filtered["여성_평균혼인율"],
            width=bar_width, label="여성 평균 혼인율", color="orange", alpha=0.7)

    # 결혼 인식 선그래프 (공통 연도만, 범위 조정)
    for column in df_perception_filtered.columns[1:]:
            ax1.plot(df_perception_filtered["연도"], df_perception_filtered[column],
            marker='o', label=column, linewidth=2)

    # 스타일 설정
    ax1.set_ylabel("혼인율 및 응답율 (%)", fontsize=14)
    ax1.set_xlabel("연도", fontsize=14)
    ax1.set_ylim(0, 50) # 동일한 y축 범위 설정
    ax1.legend(fontsize=12, loc="upper center", bbox_to_anchor=(0.5, 1.1), ncol=4)
    ax1.grid(alpha=0.5)
    ax1.tick_params(axis='y', labelsize=12)
    ax1.tick_params(axis='x', labelsize=12)
    plt.xticks(df_yearly_honin_filtered["연도"], fontsize=12)

    # 타이틀
    plt.title("혼인율(막대) 및 결혼 인식(선) 변화 (공통 연도)", fontsize=18)

    # Streamlit에 그래프 출력
    st.pyplot(fig)

    # 인사이트 도출
    st.subheader("시각화 기반 인사이트 요약")
    st.write("""
    **1. 혼인율**
    - 남성, 여성 모두 감소 추세 -> 2018년 이후 급격히 하락
    - 2022년 남성 평균 혼인율: 8.5%, 2022년 여성의 평균 혼인율: 7.8%

    **2. 결혼 인식 변화**
    - "반드시 해야 한다" 지속적 감소
    - "해도 좋고, 하지 않아도 좋다" 꾸준히 증가(2022년 가장 높은 응답률)\n
    **--> 결혼에 대한 인식이 다양화 -> 필수적인 선택에서 개인의 가치관에 따른 선택으로 변화**\n 
        

    **--> 결혼에 대한 인식에 비해 실제 혼인율은 그에 못 미침**\n
    **--> 결혼에 대한 인식도 중요 but, 실제 혼인으로 이어지는 과정에서의 경제적, 사회적 요인이 큰 걸림돌이 되고 있음**\n

    """)

    st.write("""

    """)
    st.write("""
    =================================================================================================
    """)

    ##############################

    ##2. 지역별 주거비에 대한 인식

    # 수동 데이터 입력 (이미지에서 추출한 데이터)
    data_manual = {
    "지역": ["전국", "서울", "인천・경기", "광역시, 세종시, 수도권 외 특례시", "그 외 지역"],
    "전혀 그렇지 않다": [23.2, 12.0, 24.7, 20.1, 29.5],
    "그렇지 않다": [25.0, 18.0, 23.3, 23.7, 31.0],
    "그저 그렇다": [19.4, 21.9, 21.0, 22.2, 15.4],
    "그렇다": [25.9, 36.6, 24.4, 27.8, 20.3],
    "매우 그렇다": [6.6, 11.6, 6.5, 6.2, 3.8]
    }

    # 데이터프레임 생성
    df_manual = pd.DataFrame(data_manual)

    # 데이터 전치 (stacked bar chart를 위한 형식 변환)
    df_plot = df_manual.set_index("지역").T

    # Streamlit 앱 UI 설정
    st.subheader("<지역별 주거비 부담 응답 분포 (2022년)>")

    st.dataframe(df_manual)
    
    # 그래프 시각화
    fig, ax = plt.subplots(figsize=(14, 8))
    df_plot.plot(kind="bar", stacked=True, ax=ax, alpha=0.85, cmap="tab10")

    # 그래프 스타일 설정
    ax.set_title("지역별 주거비 부담 응답 분포 (2022년)", fontsize=16)
    ax.set_xlabel("응답 항목", fontsize=14)
    ax.set_ylabel("비율 (%)", fontsize=14)
    ax.tick_params(axis="x", rotation=45, labelsize=12)
    ax.tick_params(axis="y", labelsize=12)
    ax.grid(axis="y", alpha=0.5)

    # 범례 설정
    ax.legend(title="지역", bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=12)

    # Streamlit에 그래프 출력
    st.pyplot(fig)

    # 인사이트 도출
    st.subheader("시각화 기반 인사이트 요약")
    st.write("""
    **1. 지역별 주거비 부담 인식**
    - '그렇다' 항목의 비율이 최다

    **2. 지역 차이**
    - 서울 및 인천・경기 지역 상대적으로 높은 비율\n
    --> 서울과 수도권 지역의 주거비가 상대적으로 더 비쌈

    **3. 결론**
    - 지역에 따라 주거비 부담의 인식이 상이\n
    **-> '그렇다' 비율이 높은 지역에서 정부의 주거비 부담 경감 정책이 필수적**
    """)

    st.write("""
    =================================================================================================
    """)
    ##############################

    ##3. 지역별 주거비에 대한 인식

    # Streamlit 앱 제목
    st.subheader("<2022년 지역별 평균 혼인율 데이터>")
    plt.rcParams['font.family'] = 'Malgun Gothic' # Windows 환경에서 실행 시
    plt.rcParams['axes.unicode_minus'] = False

    # 파일 업로드 위젯
    uploaded_file = st.file_uploader("혼인율 데이터를 업로드하세요 (엑셀 파일만 지원)", type=["xlsx"])

    if uploaded_file is not None:
        try:
            # 데이터 읽기
            data = pd.read_excel(uploaded_file)
        
            # 열 이름 간소화
            data.columns = ['지역', '연령별', '남성_혼인율', '여성_혼인율']
        
            # 결측치 제거 및 숫자형 변환
            data = data.dropna(subset=['남성_혼인율', '여성_혼인율'])
            data['남성_혼인율'] = pd.to_numeric(data['남성_혼인율'], errors='coerce')
            data['여성_혼인율'] = pd.to_numeric(data['여성_혼인율'], errors='coerce')
        
            # 시도별 평균 혼인율 계산
            region_avg = data.groupby('지역')[['남성_혼인율', '여성_혼인율']].mean().reset_index()
        
            # 전처리된 데이터 표시
            st.subheader("전처리된 데이터")
            st.dataframe(region_avg)

            # 시각화
            st.subheader("지역별 평균 혼인율 시각화")
            fig, ax = plt.subplots(figsize=(10, 8))
            x = range(len(region_avg['지역']))
        
            # 색상 설정
            husband_color = '#4c72b0'
            wife_color = '#dd8452'

            # 막대 그래프 생성
            ax.bar(x, region_avg['남성_혼인율'], width=0.4, label='남성 평균 혼인율', color=husband_color, alpha=0.8)
            ax.bar([i + 0.4 for i in x], region_avg['여성_혼인율'], width=0.4, label='여성 평균 혼인율', color=wife_color, alpha=0.8)

            # 막대 위 값 표시
            for i, val in enumerate(region_avg['남성_혼인율']):
                ax.text(i, val + 0.1, f"{val:.1f}", ha='center', fontsize=10, color='black')
            for i, val in enumerate(region_avg['여성_혼인율']):
                ax.text(i + 0.4, val + 0.1, f"{val:.1f}", ha='center', fontsize=10, color='black')

            # 그래프 스타일 설정
            ax.set_title("2022년 지역별 평균 혼인율", fontsize=18, fontweight="bold")
            ax.set_xlabel("지역", fontsize=14)
            ax.set_ylabel("평균 혼인율 (천 명당)", fontsize=14)
            ax.set_xticks([i + 0.2 for i in x])
            ax.set_xticklabels(region_avg['지역'], rotation=45, fontsize=12)
            ax.legend(fontsize=12)
            ax.grid(axis="y", linestyle='--', alpha=0.5)

            # 그래프를 Streamlit에 표시
            st.pyplot(fig)

            st.subheader("시각화 기반 인사이트 요약")
            st.write("""
            **1. 남성 평균 혼인율**
            - 최저: 광주, 대구, 서울, 세종 (0.1%)
            - 최고: 전라남도 (0.4%)\n
            **-> 대부분 지역에서 0.2 이하. 남성 평균 혼인율은 전반적으로 낮음을 확인**
        
        
            **2.여성 평균 혼인율**
            - 최저: 서울 (0.2%)
            - 최고: 강원도, 전라남도 (1.1%, 매우 높음)\n
            **-> 다른 지역(광역시 포함) 대비 도 지역에서 더 높은 경향이 나타남**
            
            """)

        except Exception as e:
                st.error(f"파일을 처리하는 중 오류가 발생했습니다: {e}")


    else:
            st.warning("혼인율 데이터를 업로드해주세요.")

    st.write("""
    =================================================================================================
    """)
    ################################
    #4. '남녀가 결혼하지 않아도 같이 살 수 있다'

    # 제목 설정
    st.subheader("<'남녀가 결혼하지 않아도 같이 살 수 있다'의 인식변화>")

    # 수동 데이터 입력
    data_by_age_full = {
            "15~19세": {
            "전적으로 동의": [7.8, 7.5, 11.0, 10.2, 13.3, 18.3, 26.9, 27.3],
            "약간 동의": [45.6, 43.1, 46.1, 44.2, 43.9, 51.2, 49.2, 48.6],
            "약간 반대": [29.7, 33.5, 29.8, 32.8, 30.8, 22.4, 17.4, 18.6],
            "전적으로 반대": [16.8, 16.0, 13.2, 12.7, 12.0, 8.1, 6.5, 5.6]
            },
            "20~29세": {
            "전적으로 동의": [9.4, 8.9, 12.9, 13.0, 15.7, 22.1, 28.2, 30.2],
            "약간 동의": [51.7, 50.4, 48.3, 48.5, 49.4, 52.3, 50.4, 50.8],
            "약간 반대": [26.0, 27.5, 26.8, 25.6, 23.1, 18.3, 15.7, 13.8],
            "전적으로 반대": [12.9, 13.1, 12.1, 13.0, 11.8, 7.3, 5.7, 5.1]
            },
            "30~39세": {
            "전적으로 동의": [7.2, 8.0, 11.3, 12.8, 13.6, 19.2, 24.2, 29.9],
            "약간 동의": [47.0, 45.5, 50.4, 50.0, 48.8, 54.0, 50.0, 50.5],
            "약간 반대": [28.1, 31.0, 25.1, 23.7, 24.8, 18.6, 17.3, 14.6],
            "전적으로 반대": [17.8, 15.5, 13.2, 13.5, 12.7, 8.2, 8.5, 5.0]
            }
    }

    # 연도 정의
    years = ["2008", "2010", "2012", "2014", "2016", "2018", "2020", "2022"]

    # 응답 항목별 색상 지정
    response_colors = {
            "전적으로 동의": "blue",
            "약간 동의": "green",
            "약간 반대": "orange",
            "전적으로 반대": "red"
    }

    # 모든 연령대 데이터를 DataFrame으로 변환
    df_list = []
    for age_group, responses in data_by_age_full.items():
            df = pd.DataFrame(responses, index=years)
            df.index.name = "연도"
            df.reset_index(inplace=True)
            df.insert(0, "연령대", age_group)
            df_list.append(df)

    # 데이터프레임 결합
    final_df = pd.concat(df_list)

    # Streamlit에 데이터프레임 표시
    st.subheader("모든 연령대 데이터")
    st.dataframe(final_df)

    # 시각화
    st.subheader("연령대별 태도 변화 시각화")

    fig, ax = plt.subplots(figsize=(14, 8))

    for response, color in response_colors.items():
            for age_group, responses in data_by_age_full.items():
                ax.plot(
                    years,
                responses[response],
                marker="o",
                label=f"{age_group} - {response}",
                color=color,
                    alpha=0.5
            )

    # 그래프 스타일 설정
    ax.set_title("연령대별 '남녀가 결혼하지 않아도 같이 살 수 있다' 태도 추세 (2008~2022년)", fontsize=16)
    ax.set_xlabel("연도", fontsize=14)
    ax.set_ylabel("비율 (%)", fontsize=14)
    ax.set_xticks(range(len(years)))
    ax.set_xticklabels(years, rotation=45, fontsize=12)
    ax.legend(fontsize=12, bbox_to_anchor=(1.05, 1), loc="upper left")
    ax.grid(alpha=0.5)

    # Streamlit에 그래프 출력
    st.pyplot(fig)

    st.subheader("시각화 기반 인사이트 요약")
    st.write("""
    **1. "적극적으로 동의"**
    - 모든 연령대에서 증가\n
    --> 20 ~ 29세, 30 ~ 39세에서 약 15%포인트 증가로 가장 큰 상승

    **2. "약간 동의"**
    - 모든 연령대에서 감소\n
    --> 15~19세에서 약 20%포인트 감소로 가장 큰 하락

    **3. "약간 반대"**   
    - 모든 연령대에서 감소\n
    --> 15 ~ 19세, 30 ~ 39세에서 약 15%포인트 감소

    **4. "적극적으로 반대"**
    - 모든 연령대에서 감소\n
    --> 30~39세에서 약 10%포인트 감소로 가장 큰 하락함

    **--> 결혼 없이도 동거를 받아들이는 태도가 전 연령대에서 확산되고 있으며, 특히 젊은 층(20~29세)에서 이러한 변화가 두드러짐**
    """)
    
elif option == '자녀 계획 및 출산 데이터':
    # 경고 메시지 무시
    warnings.filterwarnings('ignore')

    # 한글 폰트 설정 
    plt.rcParams['font.family'] = 'Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] = False 


    # Streamlit 앱 제목
    st.title("자녀 계획 데이터를 분석해보자")

    # 엑셀 파일 업로드
    uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요 (예: 최종.xlsx)", type=["xlsx"])

    if uploaded_file:
        # 엑셀 파일 불러오기
        df = pd.read_excel(uploaded_file, sheet_name='자녀 필요성 인식')

        # 1. 헤더 재정의
        df.columns = ['항목', '2018', '2020', '2022']
        df = df[2:]  # 실제 데이터만 남김
        df = df.reset_index(drop=True)

        # 2. 출처, 주석, 합계 제외
        df = df[~df['항목'].isin(['출처:', '주석:', '합계'])]

        # 3. 결측치 처리
        for col in ['2018', '2020', '2022']:
            df[col] = pd.to_numeric(df[col], errors='coerce')  # 숫자형 변환
            df[col].fillna(df[col].mean(), inplace=True)  # 결측치 처리

        # 4. 데이터 구조 변환
        df_long = pd.melt(df, id_vars=['항목'], var_name='연도', value_name='값')

        # 5. 데이터 타입 변환
        df_long['연도'] = df_long['연도'].astype(int)
        df_long['값'] = pd.to_numeric(df_long['값'])

        # 6. 데이터 시각화
        st.subheader("<연도별 자녀 필요성 인식 시각화>")
        st.dataframe(df)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=df_long, x='연도', y='값', hue='항목', palette='Set2', ax=ax)

        # 그래프 꾸미기
        ax.set_title('연도별 자녀 필요성 인식', fontsize=16)
        ax.set_xlabel('연도', fontsize=12)
        ax.set_ylabel('비율 (%)', fontsize=12)
        ax.legend(title='Category')
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

        # 7. 인사이트 도출
        st.subheader("시각화 기반 인사이트 요약")
        st.write("""
        **1. 연도별 동의 및 반대 비율 변화**
        - 2018년: 동의 69.6%, 반대 30.4%
        - 2020년: 동의 68.0%, 반대 32.0%
        - 2022년: 동의 65.3%, 반대 34.7%
        
        - **동의 비율 감소**:
        - 매년 지속적 감소(약 4.3%p)
        
        - **반대 비율 증가**:
        - 매년 지속적 증가(약 4.3%p)

        **--> 동의와 반대 비율의 변화는 일정한 추세(약 4.3%p)를 보이고, 이는 사회적/경제적 요인의 영향을 받고 있음을 의미**\n
        **--> 그러나 전반적인 자녀 필요성에 대한 인식은 약 70%p로 상당히 높은 통계를 보여줌**\n
        """)

    else:
        st.warning("엑셀 파일을 업로드해주세요.")

    st.write("========================================================================================\n")

    #-------------------------------------------------------------------------------------------------------------------------------------------------

    if uploaded_file:
        # 데이터 로드
        df = pd.read_excel(uploaded_file, sheet_name='대학 졸업자 취업률')
        
        st.subheader("<대학 졸업자 취업률 데이터>")
        st.dataframe(df)
        
        
        # 전처리 단계
        # 1. 불필요한 행 제거
        processed_df = df.iloc[2:].reset_index(drop=True)

        # 2. 컬럼 이름 설정
        processed_df.columns = processed_df.iloc[0]
        processed_df = processed_df[1:].reset_index(drop=True)
        processed_df.columns = ['Category'] + [f'Year_{int(col)}' if pd.notna(col) else f'Unnamed_{i}'
                                            for i, col in enumerate(processed_df.columns[1:])]

        # 3. 결측값 제거
        processed_df = processed_df.dropna(subset=['Category'], how='all')

        # 4. 숫자형 데이터로 변환
        year_columns = [col for col in processed_df.columns if col.startswith('Year_')]
        processed_df[year_columns] = processed_df[year_columns].apply(pd.to_numeric, errors='coerce')

        # 5. 성별 데이터를 분리
        overall_employment = processed_df[processed_df['Category'] == '취업률']
        male_employment = processed_df[(processed_df['Category'] == '성별') & (processed_df['Unnamed_0'] == '남자')]

        # 추가로 제공받은 여성 취업률 데이터
        female_values = [64.5, 65.7, 65.1, 65.2, 66.1, 66.4, 64.8, 66.0, 65.2, 63.1, 66.1, 68.2, 68.5]

        # 연도 데이터 추출
        years = [int(col.split('_')[1]) for col in year_columns]

        # 전체 취업률과 남성 취업률 데이터 추출
        overall_values = overall_employment.iloc[0, 1:].values.astype(float)
        male_values = male_employment.iloc[0, 2:].values.astype(float)

        # 데이터 길이 일치화
        min_length = min(len(years), len(overall_values), len(male_values), len(female_values))
        years = years[:min_length]
        overall_values = overall_values[:min_length]
        male_values = male_values[:min_length]
        female_values = female_values[:min_length]

        # 시각화
        st.subheader("취업률 추이 (2011-2023)")
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.plot(years, overall_values, label='전체 취업률', marker='o', linestyle='-')
        ax.plot(years, male_values, label='남성 취업률', marker='o', linestyle='-')
        ax.plot(years, female_values, label='여성 취업률', marker='o', linestyle='-')

        # 특정 연도(2014, 2018, 2022)에만 수치를 표시
        highlight_years = [2014, 2018, 2022]
        for x, y in zip(years, overall_values):
            if x in highlight_years:
                ax.text(x, y, f"{y:.1f}", fontsize=10, ha='center', va='bottom')
        for x, y in zip(years, male_values):
            if x in highlight_years:
                ax.text(x, y, f"{y:.1f}", fontsize=10, ha='center', va='bottom')
        for x, y in zip(years, female_values):
            if x in highlight_years:
                ax.text(x, y, f"{y:.1f}", fontsize=10, ha='center', va='bottom')

        # 그래프 제목과 축 설정
        ax.set_title('취업률 추이 (2011-2023)', fontsize=16)
        ax.set_xlabel('연도', fontsize=14)
        ax.set_ylabel('취업률 (%)', fontsize=14)
        ax.legend(fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.7)
        st.pyplot(fig)

        # 인사이트 요약
        st.subheader("시각화 기반 인사이트 요약")
        st.write("""
        **1. 2020년 팬데믹(코로나19) 영향**:
        - 전체 취업률, 특히 여성 취업률에 큰 영향 -> 빠르게 회복 중
        
        **2. 남성 취업률과 여성 취업률**:
        - 남성 취업률이 여성 취업률보다 지속적으로 높으나, 격차는 점진적으로 줄어드는 추세.
        
        **3. 2023년 최고 취업률**:
        - 남성(72.4%)과 여성(68.5%) 모두 분석 기간 중 최고치 기록.
        
        **4. 남녀 간 격차 감소**:
        - 2011년: 6% -> 2023년: 3.9%
        
        **--> 전반적으로 감소 후 2020년 팬데믹의 영향으로 최저점을 찍고 이후 전부 상승 추세**
        """)
    else:
        st.warning("엑셀 파일을 업로드해주세요.")
    st.write("========================================================================================\n")
        
        
    #-------------------------------------------------------------------------------------------------------------------------------------------------

    # Streamlit 앱 제목
    st.subheader("<업종별 육아 지원 제도 분석>")

    # 데이터 생성
    data = {
        "업종별(1)": ["합계", "제조업", None, None, None, None, None, None, None, "건설업", "서비스업", None, None, None],
        "업종별(2)": ["소계", "소계", "음식료·섬유", "화학", "의료·정밀", "금속", "전자·통신", "기계장비", "기타", "소계", "소계", "출판·영상", "전문·과학", "기타"],
        "육아휴직": ["4,284", "2,984", "338", "430", "322", "304", "375", "1,112", "105", "164", "1,136", "517", "332", "287"],
        "수유시간보장": ["3,125", "2,252", "253", "344", "240", "237", "281", "820", "78", "108", "765", "345", "233", "186"],
        "수유실": ["731", "515", "68", "88", "61", "32", "79", "173", "13", "28", "189", "90", "43", "56"],
        "보육료지원(이용비지원)": ["1,137", "830", "98", "124", "87", "83", "106", "301", "31", "43", "264", "123", "59", "82"],
    }

    # 데이터프레임 생성
    childcare_support_df = pd.DataFrame(data)

    # 원본 데이터 표시
    st.dataframe(childcare_support_df)

    # 데이터 전처리
    childcare_support_df["업종별(1)"] = childcare_support_df["업종별(1)"].fillna(method="ffill")

    numeric_columns = childcare_support_df.columns[2:]
    for col in numeric_columns:
        childcare_support_df[col] = childcare_support_df[col].str.replace(",", "").astype(float)

    # 필요한 데이터만 필터링
    columns_to_keep = [
        "업종별(1)", "업종별(2)",
        "육아휴직", "수유시간보장", "수유실", "보육료지원(이용비지원)"
    ]
    filtered_data = childcare_support_df[columns_to_keep]

    # 카테고리별 데이터 준비 함수
    def prepare_data(data, category):
        return data[data["업종별(1)"] == category].set_index("업종별(2)").drop("업종별(1)", axis=1)

    manufacturing_data = prepare_data(filtered_data, "제조업")
    construction_data = prepare_data(filtered_data, "건설업")
    service_data = prepare_data(filtered_data, "서비스업")
    summary_data = prepare_data(filtered_data, "합계")

    # 시각화
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    colors = ["plum", "lightpink", "darkblue", "yellow"]

    # 제조업
    manufacturing_data.plot(kind="bar", stacked=False, ax=axes[0, 0], color=colors)
    axes[0, 0].set_title("제조업", fontsize=14)
    axes[0, 0].set_ylabel("운영기관 수 (개)", fontsize=12)
    axes[0, 0].tick_params(axis="x", rotation=0)
    axes[0, 0].legend(title="제조업 지원 제도", fontsize=10)

    # 건설업
    construction_data.loc["소계"].plot(kind="bar", stacked=False, ax=axes[0, 1], color=colors, legend=False)
    axes[0, 1].set_title("건설업", fontsize=14)
    axes[0, 1].set_ylabel("운영기관 수 (개)", fontsize=12)
    axes[0, 1].tick_params(axis="x", rotation=0)

    # 서비스업
    service_data.plot(kind="bar", stacked=False, ax=axes[1, 0], color=colors)
    axes[1, 0].set_title("서비스업", fontsize=14)
    axes[1, 0].set_ylabel("운영기관 수 (개)", fontsize=12)
    axes[1, 0].tick_params(axis="x", rotation=0)
    axes[1, 0].legend(title="서비스업 지원 제도", fontsize=10)

    # 합계
    summary_data.loc["소계"].plot(kind="bar", stacked=False, ax=axes[1, 1], color=colors, legend=False)
    axes[1, 1].set_title("합계", fontsize=14)
    axes[1, 1].set_ylabel("운영기관 수 (개)", fontsize=12)
    axes[1, 1].tick_params(axis="x", rotation=0)

    # 레이아웃 및 출력
    plt.tight_layout()
    st.pyplot(fig)

    # 인사이트
    st.subheader("시각화 기반 인사이트 요약")
    st.write("""
    **1. 육아휴직 운영이 가장 활발**:
    - 모든 업종 중 육아휴직 운영기관 수 최다

    **2. 수유실 및 보육료지원 운영 미흡**:
    - 전반적으로 운영기관 수 미흡

    **3. 서비스업의 선도적 운영**:
    - 출판·영상 업종이 육아지원제도 운영에서 두드러진 비중 차지
    - 기타 서비스업은 상대적으로 운영기관 수가 적어 정책적 지원 필요

    **4. 건설업의 제도 참여 부족**:
    - 전반적으로 운영기관 수가 낮음, 제도 확대 시급

    **5. 업종별 맞춤형 접근 필요**:
    - 제조업의 수유실 운영 부족, 건설업의 전반적인 제도 미흡 등 각 업종별로 특화된 정책 설계가 필요
    """)

    st.write("========================================================================================\n")

    #-------------------------------------------------------------------------------------------------------------------------------------------------

    # 데이터 생성
    regions = [
        "전국", "서울특별시", "부산광역시", "대구광역시", "인천광역시", "광주광역시", "대전광역시", "울산광역시",
        "세종특별자치시", "경기도", "강원특별자치도", "충청북도", "충청남도", "전라북도", "전라남도",
        "경상북도", "경상남도", "제주특별자치도"
    ]
    birth_rates = [
        0.721, 0.552, 0.664, 0.702, 0.694, 0.706, 0.787, 0.814, 0.971, 0.766, 0.893,
        0.886, 0.842, 0.780, 0.972, 0.860, 0.799, 0.827
    ]

    # DataFrame 생성
    df = pd.DataFrame({
        "지역": regions,
        "출산율": birth_rates
    })

    st.subheader("<2023년 지역별 합계출산율>")

    # Streamlit 앱에서 원본 데이터 표시
    st.dataframe(df)  # 데이터프레임 표시

    # 시각화
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(regions, birth_rates, marker='o', color="skyblue", linewidth=2)
    ax.set_title("2023년 지역별 합계출산율", fontsize=16)
    ax.set_xlabel("지역", fontsize=14)
    ax.set_ylabel("합계출산율", fontsize=14)
    ax.set_xticks(range(len(regions)))
    ax.set_xticklabels(regions, rotation=45, fontsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    # 데이터 레이블 추가
    for i, rate in enumerate(birth_rates):
        ax.text(i, rate + 0.02, f"{rate:.3f}", ha='center', fontsize=10)

    st.pyplot(fig)

    # 인사이트 출력
    st.subheader("시각화 기반 인사이트 요약")
    st.write("""
    **1. 전체 출산율의 심각한 저조**
    - **전국 평균 출산율**: 0.721S
    - 합계출산율이 1을 넘는 지역이 단 하나 X
    
    - **전 세계 최저 수준**:
    - OECD 국가 평균 출산율과 비교했을 때, 한국의 출산율은 절반에도 미치지 못함. (OECD 국가 평균 출산율: 1.6)
    - 특히, 세계적인 저출산 국가 중에서도 가장 낮은 출산율 기록

    **2. 지역별 출산율의 차이**
    - **전라남도 (0.972)와 세종특별자치시 (0.971)**: 출산율이 가장 높지만, 여전히 1명에 못 미침
    - **서울특별시 (0.552)**: 출산율이 가장 낮고, 서울에서의 출산과 육아가 극도로 어려운 환경임을 시사

    **3. 합계출산율 1 이하의 의미**
    - **세대 교체 불가능**:
    - 인구 유지에 필요한 최소 기준: 2.1명
    --> 인구의 자연 감소로, 인구의 고령화와 사회적 부담 증가 초래
    - **인구 감소의 가속화**:
    - "모든 지역"이 출산율 1을 넘지 못한다는 것: 지역 간 인구 이동 X, 전국적으로 출산율이 감소 O
    - **경제 및 사회적 영향**:
    - 생산 가능 인구의 급격한 감소로 경제 성장 잠재력이 크게 약화
    - 병역 자원 감소, 연금 시스템 부담 가중, 노인 복지 문제 등이 장기적 사회적 부담 증가
    
    **--> 세대 교체 불가, 인구 감소, 지역 소멸, 경제 및 사회적 영향 등 부정적인 전망의 예측이 지배적**    
    """)

    st.write("========================================================================================\n")

    #-------------------------------------------------------------------------------------------------------------------------------------------------

    # 데이터 생성
    data = {
        "Category": [
            "전체", "남자", "여자", "전문관리", "사무", "서비스판매", "농어업", "기능노무",
            "만족", "보통", "불만족", "100만원 미만", "100~200만원 미만", "200~300만원 미만",
            "300~400만원 미만", "400~500만원 미만", "500~600만원 미만", "600만원 이상"
        ],
        "매우 여유있음": [1.4, 1.6, 0.9, 3.9, 1.7, 0.9, 1.0, 0.9, 3.0, 0.3, 0.3, 0.1, 0.3, 0.5, 0.8, 1.6, 1.3, 4.8],
        "약간 여유있음": [12.2, 13.4, 9.2, 23.0, 17.1, 10.1, 11.6, 9.5, 22.1, 6.3, 2.1, 2.3, 4.9, 8.4, 9.2, 13.7, 15.2, 29.4],
        "여유적정함": [31.2, 31.9, 29.4, 32.7, 35.5, 31.3, 39.9, 30.5, 39.6, 30.0, 11.5, 19.2, 27.5, 29.7, 34.8, 33.6, 39.3, 36.2],
        "약간 부족함": [39.6, 39.0, 41.1, 32.0, 35.8, 41.7, 38.2, 44.4, 29.6, 47.7, 43.9, 42.0, 46.2, 44.8, 42.9, 41.2, 37.8, 24.7],
        "매우 부족함": [15.5, 14.0, 19.4, 8.5, 10.0, 16.0, 9.2, 14.6, 5.7, 15.7, 42.2, 36.4, 21.2, 16.5, 12.3, 9.9, 6.5, 4.9]
    }
    df = pd.DataFrame(data)

    # Streamlit 앱에서 원본 데이터 표시
    st.subheader("<2023년 성별, 소득별, 직업별 주관적 소득 수준>")
    st.dataframe(df)  # 데이터프레임 표시

    # 서브플롯 생성
    fig, axes = plt.subplots(2, 2, figsize=(18, 16))
    fig.suptitle("주관적 소득 수준", fontsize=20)

    # 성별 - 막대 그래프
    gender_data = df[df["Category"].isin(["남자", "여자"])]
    gender_data.set_index("Category").plot(kind="bar", ax=axes[0, 0], colormap="viridis")
    axes[0, 0].set_title("성별", fontsize=16)
    axes[0, 0].tick_params(axis="x", rotation=0)
    axes[0, 0].set_ylabel("비율 (%)", fontsize=12)
    axes[0, 0].legend(title="항목", fontsize=10)

    # 직업 - 히트맵
    job_data = df[df["Category"].isin(["전문관리", "사무", "서비스판매", "농어업", "기능노무"])].set_index("Category")
    sns.heatmap(job_data, annot=True, cmap="coolwarm", fmt=".1f", ax=axes[1, 0], cbar=False)
    axes[1, 0].set_title("직업별 데이터", fontsize=16)
    axes[1, 0].set_ylabel("직업")

    # 가구소득 - 막대 그래프
    income_data = df[df["Category"].str.contains("만원")]
    income_data.set_index("Category").plot(kind="bar", stacked=True, ax=axes[0, 1], colormap="viridis")
    axes[0, 1].set_title("가구소득", fontsize=16)
    axes[0, 1].set_ylabel("비율 (%)", fontsize=12)
    axes[0, 1].legend(title="항목", fontsize=10)

    # 주관적 만족도 - 파이 차트
    satisfaction_data = df[df["Category"].isin(["만족", "보통", "불만족"])]
    totals = satisfaction_data.iloc[:, 1:].sum(axis=1)
    labels = satisfaction_data["Category"]
    colors = ["#4CAF50", "#FFC107", "#F44336"]  # 만족: 녹색, 보통: 노랑, 불만족: 빨강
    axes[1, 1].pie(
        totals,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors,
        textprops={"fontsize": 12}
    )
    axes[1, 1].set_title("주관적 만족도", fontsize=16)

    # 레이아웃 및 Streamlit에 표시
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    st.pyplot(fig)

    # 전체 파이 차트
    total_data = df[df["Category"] == "전체"].iloc[:, 1:].T
    total_data.columns = ["전체"]

    fig, ax = plt.subplots(figsize=(8, 8))
    total_data.plot.pie(
        y="전체",
        autopct="%1.1f%%",
        startangle=90,
        legend=False,
        colors=sns.color_palette("pastel"),
        ax=ax
    )
    ax.set_title("전체", fontsize=16)
    ax.set_ylabel("")  # y축 레이블 제거
    st.pyplot(fig)

    # 인사이트 요약
    st.subheader("시각화 기반 인사이트 요약")
    st.write("""
    **1. 성별에 따른 주관적 소득 수준**
    - 남성과 여성 간 차이:
    - "매우 여유 있음" 및 "약간 여유 있음": 남성이 상대적으로 높은 비율
    - "매우 부족함" 및 "약간 부족함": 여성이 상대적으로 높은 비율\n
    **--> 성별에 따른 임금 차별 및 경제적 불평등이 존재함 시사**

    **2. 직업별 주관적 소득 수준**
    - 전문관리직:
    - 상대적으로 안정된 소득 구조
    - 기능노무직:
    - 경제적 안정성이 낮은 경향
    - 농어업:
    - "여유 적정함"에 가장 높은 비율 안정적 --> 상위 수준 도달을 제한적

    **3. 가구소득 분포**
    - 낮은 소득 -> 부족함 비율 증가
    - 500만 원 이상의 고소득층-> 여유 있음 비율이 뚜렷하게 높음

    **4. 주관적 만족도**
    - 전체적인 만족도 분포:
    - "보통" 만족도가 가장 큰 비중 -> 경제적 안정성을 기반으로 한 현실적인 만족도 반영
    - "만족" 비율 > "불만족" 비율 but 경제적으로 어려움을 느끼는 층 상당수 존재\n
    \n
    **--> 전체적으로 여유가 적당하거나 여유가 있다고 답한 비율이 약 40%. 여유가 없고 부족하다고 답한 비율이 약 60%. 사회가 경제적으로 불안정함을 시사**   
    """)
