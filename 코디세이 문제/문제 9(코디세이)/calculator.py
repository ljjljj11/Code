
# 시스템 종료와 명령줄 인자 처리를 위한 모듈
import sys

# PyQt5에서 필요한 위젯들을 불러옴
from PyQt5.QtWidgets import (
    QApplication,    # 애플리케이션 전체를 관리하는 클래스
    QWidget,         # 기본 창 위젯
    QVBoxLayout,     # 위젯들을 수직 방향으로 배치하는 레이아웃
    QGridLayout,     # 격자(표 형태)로 버튼을 배치하기 위한 레이아웃
    QPushButton,     # 클릭할 수 있는 버튼 위젯
    QLineEdit        # 텍스트를 표시할 수 있는 한 줄 입력창
)

from PyQt5.QtCore import Qt  # 텍스트 정렬 등을 위한 상수 포함

# 계산기 클래스 정의 (QWidget을 상속받아 하나의 창을 만듦)
class Calculator(QWidget):
    def __init__(self):
        super().__init__()  # 부모 클래스(QWidget) 초기화
        self.setWindowTitle('아이폰 스타일 계산기')  # 창 제목 설정
        self.setFixedSize(370, 550)               # 창 크기 고정
        self.init_ui()                            # UI 초기화 함수 호출

    # UI를 구성하는 함수 정의
    def init_ui(self):
        # 수직 레이아웃 생성 (디스플레이 + 버튼들을 위아래로 쌓기 위해)
        main_layout = QVBoxLayout()

        # 디스플레이(텍스트 입력창) 생성
        self.display = QLineEdit()               # 한 줄 입력 위젯 생성
        self.display.setReadOnly(True)           # 사용자 입력 불가능하게 설정 (버튼으로만 입력)
        self.display.setAlignment(Qt.AlignRight) # 텍스트를 오른쪽 정렬
        self.display.setFixedHeight(60)          # 디스플레이 높이 설정
        self.display.setStyleSheet('font-size: 30px; padding: 10px;')  # 글자 크기 및 여백 설정
        main_layout.addWidget(self.display)      # 디스플레이를 메인 레이아웃에 추가

        # 버튼들을 담을 그리드 레이아웃 생성 (행과 열 기준으로 정렬됨)
        grid = QGridLayout()
        main_layout.addLayout(grid)              # 메인 레이아웃에 그리드 추가

        # 버튼 배열 정의: (텍스트, 행, 열, [행병합], [열병합])
        buttons = [
            ('AC', 0, 0), ('±', 0, 1), ('%', 0, 2), ('÷', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('×', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('−', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('0', 4, 0, 1, 2), ('.', 4, 2), ('=', 4, 3)
        ]

        # 버튼을 생성하고 레이아웃에 추가하는 함수 정의
        def create_button(text, row, col, rowspan=1, colspan=1):
            button = QPushButton(text)                     # 버튼 생성
            button.setFixedHeight(80)                      # 버튼 높이 고정
            button.setStyleSheet('font-size: 20px; margin: 2px;')  # 버튼 스타일
            button.clicked.connect(lambda _, t=text: self.display_input(t))  # 클릭 시 텍스트 출력 연결
            grid.addWidget(button, row, col, rowspan, colspan)  # 버튼을 그리드에 배치

        # 위에서 정의한 버튼 배열을 바탕으로 버튼 생성 및 배치
        for btn in buttons:
            if len(btn) == 3:
                create_button(btn[0], btn[1], btn[2])  # 기본 버튼
            else:
                create_button(btn[0], btn[1], btn[2], btn[3], btn[4])  # 병합이 필요한 버튼 (예: 0)

        # 전체 레이아웃을 창에 적용
        self.setLayout(main_layout)

    # 버튼 클릭 시 실행되는 함수 (디스플레이에 텍스트 추가)
    def display_input(self, text):
        current = self.display.text()           # 현재 디스플레이 텍스트 가져오기
        self.display.setText(current + text)    # 버튼 텍스트를 이어 붙여 디스플레이에 표시


# 프로그램 실행 부분
if __name__ == '__main__':
    app = QApplication(sys.argv)  # PyQt 애플리케이션 객체 생성
    calc = Calculator()           # 계산기 창 인스턴스 생성
    calc.show()                   # 계산기 창 띄우기
    sys.exit(app.exec_())         # 프로그램 종료 시까지 이벤트 루프 실행
