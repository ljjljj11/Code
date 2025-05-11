import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()  # UI 초기화
        self.reset()   # 계산기 초기화

    def initUI(self):
        """계산기의 UI를 설정합니다."""
        self.setWindowTitle('iPhone Calculator')  # 창 제목 설정
        self.setGeometry(100, 100, 300, 400)  # 창 크기 설정

        # 메인 레이아웃
        main_layout = QVBoxLayout()

        # 디스플레이 (결과를 보여주는 화면)
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)  # 텍스트를 오른쪽 정렬
        self.display.setReadOnly(True)  # 사용자가 직접 입력하지 못하도록 설정
        self.display.setStyleSheet("font-size: 24px; padding: 10px;")  # 스타일 설정
        main_layout.addWidget(self.display)

        # 버튼 레이아웃
        buttons_layout = QGridLayout()
        buttons = [
            ('AC', 0, 0), ('+/-', 0, 1), ('%', 0, 2), ('÷', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('×', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('0', 4, 0, 1, 2), ('.', 4, 2), ('=', 4, 3),
        ]

        # 버튼 생성 및 레이아웃에 추가
        for text, row, col, *span in buttons:
            button = QPushButton(text)  # 버튼 생성
            button.setStyleSheet("font-size: 18px; padding: 15px;")  # 버튼 스타일 설정
            button.clicked.connect(self.on_button_click)  # 버튼 클릭 시 이벤트 연결
            if span:
                buttons_layout.addWidget(button, row, col, *span)  # 버튼이 여러 칸 차지할 경우
            else:
                buttons_layout.addWidget(button, row, col)  # 일반 버튼

        main_layout.addLayout(buttons_layout)
        self.setLayout(main_layout)

    def reset(self):
        """계산기를 초기 상태로 리셋합니다."""
        self.current_expression = ''  # 현재 수식 초기화
        self.last_operator = None  # 마지막 연산자 초기화
        self.last_operand = None  # 마지막 피연산자 초기화
        self.display.setText('0')  # 디스플레이를 0으로 설정

    def add_to_expression(self, value):
        """숫자나 연산자를 수식에 추가합니다."""
        if self.current_expression == '0' and value.isdigit():
            self.current_expression = value  # 0일 경우 숫자를 대체
        else:
            self.current_expression += value  # 수식에 값 추가
        self.display.setText(self.current_expression)  # 디스플레이 업데이트

    def add_decimal(self):
        """소수점을 수식에 추가합니다."""
        if '.' not in self.current_expression.split()[-1]:  # 현재 숫자에 소수점이 없을 경우
            self.current_expression += '.'
            self.display.setText(self.current_expression)

    def negative_positive(self):
        """현재 숫자의 부호를 변경합니다."""
        if self.current_expression:
            if self.current_expression.startswith('-'):  # 음수일 경우
                self.current_expression = self.current_expression[1:]  # 부호 제거
            else:
                self.current_expression = '-' + self.current_expression  # 음수로 변경
            self.display.setText(self.current_expression)

    def percent(self):
        """현재 숫자를 백분율로 변환합니다."""
        try:
            value = float(self.current_expression) / 100  # 백분율 계산
            self.current_expression = str(value)
            self.display.setText(self.current_expression)
        except ValueError:
            self.display.setText('Error')  # 잘못된 입력 처리

    def equal(self):
        """수식을 평가하고 결과를 출력합니다."""
        try:
            if self.last_operator and self.last_operand is not None:
                # 연속 계산 처리
                self.current_expression += f' {self.last_operator} {self.last_operand}'
            else:
                # 마지막 연산자와 피연산자 저장
                parts = self.current_expression.split()
                if len(parts) >= 3:
                    self.last_operator = parts[-2]
                    self.last_operand = parts[-1]

            # 수식 평가
            expression = self.current_expression.replace('÷', '/').replace('×', '*')
            result = eval(expression)  # 수식 계산

            # 결과 범위 확인
            if abs(result) > 1e308:
                raise OverflowError('Number out of range')

            self.current_expression = str(result)
            self.display.setText(self.current_expression)
        except ZeroDivisionError:
            self.display.setText('Cannot divide by zero')  # 0으로 나누기 처리
            self.current_expression = ''
        except OverflowError:
            self.display.setText('Number out of range')  # 범위 초과 처리
            self.current_expression = ''
        except Exception:
            self.display.setText('Error')  # 기타 오류 처리
            self.current_expression = ''

    def on_button_click(self):
        """버튼 클릭 이벤트를 처리합니다."""
        sender = self.sender()  # 클릭된 버튼 가져오기
        text = sender.text()  # 버튼의 텍스트 가져오기

        if text == 'AC':
            self.reset()  # 초기화
        elif text == '+/-':
            self.negative_positive()  # 부호 변경
        elif text == '%':
            self.percent()  # 백분율 계산
        elif text == '=':
            self.equal()  # 결과 계산
        elif text in '0123456789':
            self.add_to_expression(text)  # 숫자 추가
        elif text == '.':
            self.add_decimal()  # 소수점 추가
        else:
            # 연산자 처리
            if self.current_expression and self.current_expression[-1] not in '+-×÷':
                self.add_to_expression(f' {text} ')


if __name__ == '__main__':
    # PyQt5 애플리케이션 실행
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec_())