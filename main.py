import pygame
import sys
from pathlib import Path

#파일을 실행하기 위해서 깃허브에 같이 공유된 모든 사진을 다운받아야 합니다
# 화면 단계: 검사 → 전환 애니메이션 → 결과
PHASE_QUIZ = "quiz"
PHASE_TRANSITION = "transition"
PHASE_RESULT = "result"

TRANSITION_DURATION_MS = 2800
TRANSITION_ROTATIONS = 3

# ==========================
# MBTI 질문 데이터 (그대로 사용)
# ==========================
MBTI_QUESTIONS = {
    "EI": {
        "pos": [
            "주기적으로 새로운 친구를 사귄다.", "대화를 시작하는 것이 불편하지 않다.",
            "말하기를 좋아한다.", "경험을 통해 이해한다.",
            "사람들과 어울리는 것을 선호한다.", "활기차고 외향적이라는 말을 듣는다.",
            "방금 만난 사람과 쉽게 친해진다.", "떠들썩한 장소에 마음이 끌린다."
        ],
        "neg": [
            "모르는 사람과의 관계가 부담스럽다.", "혼자 하는 활동을 더 좋아한다.",
            "남이 먼저 다가오기를 기다린다.", "전화 거는 일을 피하려고 한다.",
            "혼자 일하는 직업을 원한다.", "옷 잘 입는 것이 최고의 플러팅이라 생각한다.",
            "개강파티에서 금방 집에 가고 싶다.", "이해한 다음에 행동한다."
        ],
        "labels": ("E", "I")
    },
    "SN": {
       "pos": [ "창작물의 다양한 해석에 대해 토론하는 것에는 큰 관심이 없다.",
               "내가 소설가로 일하는 모습은 상상할 수 없다.",
                "미래의 세상이 어떤 모습일지에 대해 이론적으로 논의하는 것에는 크게 관심이 없다.",
                "추상적인 철학적 질문에 대해 깊게 생각하는 것은 시간 낭비라고 생각한다.",
                "대부분의 밸런스 게임은 듣자마자 말이 안 된다고 생각한다.",
                "샤워할 때 별 생각 안 한다.",
                "숲보다 나무를 보려는 경향이 강하다.",
                "현실주의적이라는 말을 종종 듣는다."],
        "neg": ["단순하고 직관적인 아이디어보다는 복잡하고 참신한 이이디어에 흥미를 느낀다.",
                "새롭고 검증되지 않은 방법을 실험하는 것을 좋아한다.",
                "탐구할 만한 지식 분야와 새로운 경험을 적극적으로 추구한다.",
                "일이 잘못될까봐 자주 걱정하는 편이다.",
                "윤리적 딜레마에 대해 토론하는 것을 좋아한다.",
                "글쓰기 등 창의성을 표현하는 다양한 형태의 활동에 관심이 있다.",
                "생소한 아이디어와 관점을 탐구하는 것을 좋아한다.",
                "구체적인 단계를 따르기보다는 창의적인 해결책을 생각해 내야 하는 작업을 선호한다."],
        "labels": ("S", "N")
    },
    "TF": {
        "pos": ["압박감이 심한 환경에서도 평정심을 유지하는 편이다.",
                "행동 계획을 결정할 때 사람들의 감정보다는 사실을 우선한다.",
                "감정적 측면을 다소 무시하더라도 의사 결정의 효율성을 중시한다.",
                "의견 차이가 존재하는 경우에는 다른 사람의 감정을 지켜주기보다는 나의 주장을 입증하는 것을 우선시한다.",
                "감정적인 논쟁에 쉽게 동요하지 않는다.",
                "불안함을 느끼는 경우는 드물다.",
                "마음보다 머리로 결정을 내린다.",
                "나는 팀플의 성공적인 결과를 위해, 공감과 배려보다 사실에 우선하여 행동하는 편이다."],
        "neg": ["숫자나 데이터보다는 사람들의 이야기와 감정이 마음에 더 와닿는다.",
                "100% 솔직한 사람이 되기보다는 세심한 사람이 되는 것을 우선시한다.",
                "감정이 매우 빠르게 변할 때가 있다.",
                "사실과 감정이 충돌할 때는 감정에 따라 행동하는 편이다.",
                "감정을 통제하기보다는 감정에 휘둘리곤 한다.",
                "결정을 내릴 때는 가장 논리적이고 효율적인 결정보다는 관련자들의 감정에 집중한다.",
                "상대방이 나를 높게 평가하면 나중에 상대방이 실망하게 될까 걱정하곤 한다.",
                "결정을 내릴 때 논리적인 추론보다는 감정적인 직관에 더 의지하는 경향이 있다."],
        "labels": ("T", "F")
    },
    "JP": {
        "pos": ["생활공간과 업무공간이 깨끗하게 정돈되어 있다.",
                "효과적으로 작업을 계획하고 우선순위를 정하며, 마감 기한보다 훨씬 일찍 작업을 완료할 때가 많다.",
                "일정이나 목록 등 일을 체계화할 수 있는 도구를 사용하는 것을 좋아한다.",
                "휴식을 취하기 전에 먼저 해야 할 일을 마치는 것을 선호한다.",
                "매일 할 일을 계획하는 것이 좋다.",
                "계획에 차질이 생기는 경우에는 최대한 신속하게 원래 계획대로 진행하는 것을 최우선으로 한다.",
                "단계를 건너뛰지 않고 체계적으로 일을 완수한다.",
                "분명한 목적과 방향을 선호한다."],
        "neg": [ "계획없이 하루를 보낼 때가 많다.",
                "해야 할 일을 마지막까지 미룰 때가 많다.",
                 "업무나 학업 일정을 일관성 있게 유지하는 것이 어렵다.",
                 "계획에 따라 일관성 있게 업무를 진행하기보다는 즉흥적인 에너지로 업무를 몰아서 처리하는 편이다.",
                 "어떤 결정이 옳다고 생각하면 추가적인 근거 없이 행동으로 옮기는 경우가 많다.",
                 "마감 기한을 지키기가 힘들다.",
                 "최대한 많은 정보를 인식할 때까지 결정을 보류한다.",
                 "자율적이고 체계는 없지만 재량에 따라 일정을 변경할 수 있다."],
        "labels": ("J", "P")
    }
}

# ==========================
# 점수 계산 함수 (기존 로직 유지)
# ==========================
def calc_score(pos_ans, neg_ans):
    pos_sum, neg_sum = sum(pos_ans), sum(neg_ans)
    raw_min = (len(pos_ans) * 1) - (len(neg_ans) * 5)
    raw_max = (len(pos_ans) * 5) - (len(neg_ans) * 1)
    norm = ((pos_sum - neg_sum) - raw_min) / (raw_max - raw_min) * 100
    return pos_sum, neg_sum, norm


def dimension_all_threes(pos_ans, neg_ans):
    """한 지표(긍정+부정 문항)의 응답이 모두 3(보통)인지 확인."""
    combined = pos_ans + neg_ans
    if not combined:
        return False
    return all(v == 3 for v in combined)

# ==========================
# Pygame 설정 및 UI
# ==========================
BASE_DIR = Path(__file__).resolve().parent
BACKGROUND_FILE = "background.png"

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("MBTI 검사")

# 커스텀 폰트: main.py와 같은 폴더에 Ghanachocolate.otf 를 넣어 두세요.
# SysFont("가나초콜릿체") 는 Windows에 설치된 글꼴만 찾아서 .otf 파일은 못 씁니다.
FONT_FILE = BASE_DIR / "Ghanachocolate.otf"

def load_font(size):
    if FONT_FILE.exists():
        return pygame.font.Font(str(FONT_FILE), size)
    print("Ghanachocolate.otf 를 찾을 수 없어 맑은 고딕을 사용합니다.")
    return pygame.font.SysFont("malgungothic", size)

FONT_MAIN = load_font(24)
FONT_SMALL = load_font(18)
FONT_TITLE = load_font(32)
TEXT_COLOR = (255, 255, 255)

# 이미지 로드 (main.py가 있는 폴더 기준 — 실행 위치와 무관)
try:
    background_img = pygame.image.load(str(BASE_DIR / BACKGROUND_FILE)).convert()
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
except Exception as e:
    background_img = None
    print("background.png 를 불러올 수 없습니다:", e)

try:
    helper_img = pygame.image.load(str(BASE_DIR / "helper.png")).convert_alpha()
    helper_img = pygame.transform.scale(helper_img, (250, 350))
except Exception as e:
    helper_img = None
    print("helper.png 를 불러올 수 없습니다:", e)

try:
    helper_sneeze_img = pygame.image.load(str(BASE_DIR / "helper_sneeze.png")).convert_alpha()
except Exception as e:
    helper_sneeze_img = None
    print("helper_sneeze.png 를 불러올 수 없습니다:", e)

# MBTI 결과별 이미지 매핑 (있는 것만 사용해도 됨)
RESULT_IMAGES = {
    mbti: f"{mbti}.png"
    for mbti in (
        "INTJ", "INTP", "ENTJ", "ENTP",
        "INFJ", "INFP", "ENFJ", "ENFP",
        "ISTJ", "ISFJ", "ESTJ", "ESFJ",
        "ISTP", "ISFP", "ESTP", "ESFP",
    )
}

def load_result_image(mbti):
    filename = RESULT_IMAGES.get(mbti)
    if not filename:
        return None
    try:
        img = pygame.image.load(str(BASE_DIR / filename)).convert_alpha()
        # 결과 그림은 화면 중앙 정도에 맞춰 적당히 스케일
        max_w, max_h = SCREEN_WIDTH - 80, SCREEN_HEIGHT - 100
        w, h = img.get_size()
        scale = min(max_w / w, max_h / h, 1)
        img = pygame.transform.scale(img, (int(w * scale), int(h * scale)))
        return img
    except Exception as e:
        print(f"{filename} 이미지를 불러올 수 없습니다:", e)
        return None

# Likert 버튼 정의 (5~1)
LIKERT_OPTIONS = [
    ("매우 그렇다 (5)", 5),
    ("그렇다 (4)", 4),
    ("보통 (3)", 3),
    ("아니다 (2)", 2),
    ("전혀 아니다 (1)", 1),
]

def draw_text(surface, text, font, color, x, y):
    """한 줄 텍스트 그리기 (좌측 정렬)"""
    rendered = font.render(text, True, color)
    surface.blit(rendered, (x, y))

def draw_background(surface):
    if background_img:
        surface.blit(background_img, (0, 0))
    else:
        surface.fill((20, 20, 40))


def draw_sneeze_transition(surface, img, progress):
    """helper_sneeze를 회전·확대. progress 1.0이면 화면을 가득 채운 상태."""
    draw_background(surface)
    if img is None:
        return True

    ow, oh = img.get_size()
    fill_scale = max(SCREEN_WIDTH / ow, SCREEN_HEIGHT / oh) * 1.2
    start_scale = min(250 / ow, 350 / oh)
    eased = progress * progress
    scale = start_scale + (fill_scale - start_scale) * eased
    angle = progress * 360 * TRANSITION_ROTATIONS

    w = max(1, int(ow * scale))
    h = max(1, int(oh * scale))
    scaled = pygame.transform.smoothscale(img, (w, h))
    rotated = pygame.transform.rotate(scaled, angle)
    rect = rotated.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    surface.blit(rotated, rect)
    return progress >= 1.0


def draw_multiline_text(surface, text, font, color, x, y, max_width):
    """긴 질문을 여러 줄로 나눠서 출력"""
    words = list(text)
    lines = []
    current = ""
    for ch in words:
        test = current + ch
        if font.size(test)[0] > max_width and current != "":
            lines.append(current)
            current = ch
        else:
            current = test
    if current:
        lines.append(current)

    for line in lines:
        rendered = font.render(line, True, color)
        surface.blit(rendered, (x, y))
        y += font.get_linesize()
    return y

def main():
    clock = pygame.time.Clock()
    running = True

    # 검사 상태
    keys_order = list(MBTI_QUESTIONS.keys())  # ["EI", "SN", "TF", "JP"]
    key_index = 0
    question_index = 0      # 0~7
    is_pos = True           # True이면 pos 리스트, False이면 neg 리스트

    # 각 지표별 응답 저장
    answers_pos = {k: [] for k in keys_order}
    answers_neg = {k: [] for k in keys_order}

    # 결과 및 화면 단계
    phase = PHASE_QUIZ
    final_mbti = ""
    result_image = None
    transition_start_ms = 0
    restart_notice_until_ms = 0

    def reset_quiz():
        nonlocal key_index, question_index, is_pos, restart_notice_until_ms
        key_index = 0
        question_index = 0
        is_pos = True
        for k in keys_order:
            answers_pos[k].clear()
            answers_neg[k].clear()
        restart_notice_until_ms = pygame.time.get_ticks() + 2500

    # 버튼 위치 계산
    button_width = 130
    button_height = 40
    gap = 8
    # 오른쪽 영역에 버튼 배치
    start_x = 320
    start_y = 350
    buttons = []
    for i, (label, value) in enumerate(LIKERT_OPTIONS):
        rect = pygame.Rect(start_x + (button_width + gap) * i, start_y, button_width, button_height)
        buttons.append((rect, label, value))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if phase == PHASE_QUIZ and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                # Likert 버튼 클릭 체크
                for rect, label, value in buttons:
                    if rect.collidepoint(mx, my):
                        current_key = keys_order[key_index]
                        if is_pos:
                            answers_pos[current_key].append(value)
                        else:
                            answers_neg[current_key].append(value)

                        # 다음 질문으로 이동
                        current_data = MBTI_QUESTIONS[current_key]
                        total_questions = len(current_data["pos"])
                        if question_index < total_questions - 1:
                            question_index += 1
                        else:
                            # pos/neg 전환 또는 다음 지표로
                            if is_pos:
                                is_pos = False
                                question_index = 0
                            else:
                                # 이 지표 끝 — 모두 3이면 처음부터
                                if dimension_all_threes(
                                    answers_pos[current_key],
                                    answers_neg[current_key],
                                ):
                                    reset_quiz()
                                    break

                                is_pos = True
                                question_index = 0
                                if key_index < len(keys_order) - 1:
                                    key_index += 1
                                else:
                                    # 모든 지표 끝
                                    # 점수 계산
                                    final = ""
                                    for k in keys_order:
                                        data = MBTI_QUESTIONS[k]
                                        p_label, n_label = data["labels"]
                                        p_sum, n_sum, _ = calc_score(
                                            answers_pos[k], answers_neg[k]
                                        )
                                        res_letter = p_label if p_sum >= n_sum else n_label
                                        final += res_letter
                                    final_mbti = final
                                    result_image = load_result_image(final_mbti)
                                    phase = PHASE_TRANSITION
                                    transition_start_ms = pygame.time.get_ticks()
                        break

        # ==========================
        # 화면 그리기
        # ==========================
        if phase == PHASE_QUIZ:
            draw_background(screen)

            if helper_img:
                screen.blit(helper_img, (50, 150))
            # 상단 안내 텍스트
            draw_text(screen, "심층 MBTI 검사", FONT_TITLE, TEXT_COLOR, 330, 30)

            current_key = keys_order[key_index]
            data = MBTI_QUESTIONS[current_key]
            p_label, n_label = data["labels"]

            # 질문 텍스트
            q_list = data["pos"] if is_pos else data["neg"]
            question = q_list[question_index]
            y_after = draw_multiline_text(screen, "Q: " + question, FONT_MAIN, TEXT_COLOR, 330, 140, 600)

            # Likert 안내
            draw_text(screen, "응답을 선택하세요 (1~5)", FONT_SMALL, TEXT_COLOR, 330, y_after + 20)

            if pygame.time.get_ticks() < restart_notice_until_ms:
                draw_text(
                    screen,
                    "한 지표에서 모두 '보통(3)'을 선택해 처음부터 다시 시작합니다.",
                    FONT_MAIN,
                    TEXT_COLOR,
                    80,
                    SCREEN_HEIGHT - 70,
                )

            # 버튼 그리기
            for rect, label, value in buttons:
                pygame.draw.rect(screen, (50, 50, 70), rect)
                pygame.draw.rect(screen, TEXT_COLOR, rect, 2)
                text_surf = FONT_SMALL.render(label, True, TEXT_COLOR)
                text_rect = text_surf.get_rect(center=rect.center)
                screen.blit(text_surf, text_rect)

        elif phase == PHASE_TRANSITION:
            elapsed = pygame.time.get_ticks() - transition_start_ms
            progress = min(1.0, elapsed / TRANSITION_DURATION_MS)
            if draw_sneeze_transition(screen, helper_sneeze_img, progress):
                phase = PHASE_RESULT

        else:
            draw_background(screen)
            if result_image:
                img_rect = result_image.get_rect()
                img_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                screen.blit(result_image, img_rect)
            else:
                draw_text(
                    screen,
                    f"결과 이미지를 찾을 수 없습니다. ({final_mbti}.png — RESULT_IMAGES 확인)",
                    FONT_SMALL,
                    TEXT_COLOR,
                    80,
                    SCREEN_HEIGHT // 2 - 20,
                )

            draw_text(screen, "창을 닫아 종료할 수 있습니다.", FONT_SMALL, TEXT_COLOR, 330, SCREEN_HEIGHT - 40)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

# 종료 처리
pygame.quit()
sys.exit()