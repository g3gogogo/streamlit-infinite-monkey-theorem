import random
import streamlit as st

st.title("무한 원숭이 정리")

st.write("""
*무한 원숭이 정리* 란?

'원숭이가 무한한 시간 동안 타자기의 자판을 
무작위로 누를 수 있다면,\n
어느 시점에는 
셰익스피어 전집을 입력할 수 있다'는 사고 실험과
이 실험에서 유래한 정리에다.

증명은 패스하지만 결론은 가능하다는 것이다.\n
자 그럼 원숭이가 되어보자.
""")

monkey = st.checkbox("원숭이가 되는 것에 동의하시나요?")

if monkey:
  st.subheader("우끼끽~")

  # 1. 세션 상태 초기화
  if "monkey_typing" not in st.session_state:
    st.session_state.monkey_typing = ""
  if "count" not in st.session_state:
    st.session_state.count = 0
  if "is_completed" not in st.session_state:
    st.session_state.is_completed = False


  # 2. 전체 문장을 보여주는 팝업 다이얼로그 정의 (스타일 적용)
  @st.dialog("📜 원숭이가 타이핑한 전체 기록", width="large")
  def show_full_text_modal(full_text, target):
    st.write(
        f"총 입력된 글자 수: **{len(full_text)}자** (시도 횟수:"
        f" {st.session_state.count}회)"
    )
    st.write("---")

    if full_text:
      if target and target in full_text:
        # 목표 문장은 검정색 굵은 글씨, 나머지 글자는 옅은 회색으로 처리
        highlighted_text = full_text.replace(
            target,
            f"<strong style='color: #000000; font-weight: 900;'>{target}</strong>",
        )
        st.markdown(
            f"<div style='word-break: break-all; white-space: pre-wrap; max-height: 400px; overflow-y: auto; padding: 15px; border: 1px solid #ddd; border-radius: 5px; background-color: #ffffff; color: #b0b0b0; line-height: 1.6; font-size: 15px;'>{highlighted_text}</div>",
            unsafe_allow_html=True,
        )
        st.caption(
            "진하고 선명한 검은색 글씨가 목표로 하신 문장입니다! 🍌 (나머지는 옅은"
            " 회색)"
        )
      else:
        # 목표 문장이 없거나 입력 안 한 경우 일반 출력 (모두 회색톤으로 보이게)
        st.markdown(
            f"<div style='word-break: break-all; white-space: pre-wrap; max-height: 400px; overflow-y: auto; padding: 15px; border: 1px solid #ddd; border-radius: 5px; background-color: #ffffff; color: #444444; line-height: 1.6; font-size: 15px;'>{full_text}</div>",
            unsafe_allow_html=True,
        )
    else:
      st.info("아직 입력된 글자가 없습니다.")

    if st.button("닫기"):
      st.rerun()


  # 3. 목표 문장 입력받기
  target_text = st.text_input(
      "완성하고 싶은 단어 / 문장을 입력하세요 (영어 소문자, .,!?'\" 공백만 허용)"
  )

  multiply = st.slider("클릭 한 번에 입력하는 글자수", 1, 100, 33)
  typing_letters = "abcdefghijklmnopqrstuvwxyz,?!'\" "

  # 4. 완성 여부에 따른 화면 분기
  if st.session_state.is_completed:
    st.success(
        f"🎉 축하합니다, 원숭이 씨! {st.session_state.count}번만에 완성했군요."
        " 상으로 여기, 바나나입니다. 🍌"
    )
  else:
    if st.button(f"{multiply} 글자 입력"):
      st.session_state.count += 1

      new_text = "".join(
          random.choice(typing_letters) for _ in range(multiply)
      )

      st.session_state.monkey_typing += new_text

      if target_text:
        overlap_len = len(target_text) - 1
        recent_chunk = (
            st.session_state.monkey_typing[-overlap_len:]
            if overlap_len > 0
            else ""
        ) + new_text

        if target_text in recent_chunk:
          st.session_state.is_completed = True
          st.rerun()

  # 5. 현재까지 누적된 글자 출력 (최근 500자 - 여러 줄 출력)
  st.write("---")
  full_len = len(st.session_state.monkey_typing)

  if st.session_state.monkey_typing:
    display_text = (
        ("..." + st.session_state.monkey_typing[-500:])
        if full_len > 500
        else st.session_state.monkey_typing
    )
    st.write(f"**현재 타자 기록 (총 {full_len}자 중 최근 500자):**")
    # st.code 대신 st.write를 사용하여 줄바꿈이 자연스러운 여러 줄 텍스트 블록으로 표시
    st.write(display_text)
  else:
    st.write("**현재 타자 기록:**\n(아직 입력된 글자가 없습니다)")

  # 전체 문장 확인 버튼
  if st.button("🔍 전체 문장 확인"):
    show_full_text_modal(st.session_state.monkey_typing, target_text)

  st.write(f"현재까지 버튼을 누른 횟수: {st.session_state.count}번")
  st.write("---")

  # 6. 초기화 버튼
  if st.button("초기화"):
    st.session_state.monkey_typing = ""
    st.session_state.count = 0
    st.session_state.is_completed = False
    st.rerun()