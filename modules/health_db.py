import json
import csv
import pickle
import os
import ast


# 1. 건강정보 클래스
class HealthRecord:
    def __init__(self, id, name, birth_year, gender, height, weight):
        self.id = id
        self.name = name
        self.birth_year = birth_year
        self.gender = gender
        self.height = float(height)
        self.weight = float(weight)

        self.bmi = round(weight / ((height / 100) ** 2), 2)

        if self.bmi < 18.5:
            self.status = "저체중"
        elif self.bmi < 23:
            self.status = "정상"
        elif self.bmi < 25:
            self.status = "과체중"
        else:
            self.status = "비만"

    # 딕셔너리로 변환
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "height": self.height,
            "weight": self.weight,
            "bmi": self.bmi,
            "status": self.status
        }


# 2. 건강정보 관리 클래스
class HealthManager:
    def __init__(self):
        self.records = []
        self.number = 1

    # 식별번호 생성
    def create_id(self):
        id = f"P2026-{self.number:04d}"
        self.number += 1
        return id

    # 건강정보 추가
    def add_record(self, name, birth_year, gender, height, weight):
        record = HealthRecord(
            self.create_id(), name, birth_year,
            gender, height, weight
        )
        self.records.append(record)

    # 목록 출력
    def show_records(self):
        for record in self.records:
            print(record.to_dict())

    # 3. JSON 저장 및 읽기
    def save_json(self):
        data = [r.to_dict() for r in self.records]
        with open("data/health_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_json(self):
        try:
            with open("data/health_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            return []

    # 4. CSV 저장 및 읽기
    def save_csv(self):
        data = [r.to_dict() for r in self.records]
        with open("data/health_data.csv", "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    def load_csv(self):
        try:
            with open("data/health_data.csv", "r", encoding="utf-8-sig") as f:
                return list(csv.DictReader(f))
        except OSError:
            return []

    # 5. TXT 저장 및 읽기
    def save_txt(self):
        with open("data/health_data.txt", "w", encoding="utf-8") as f:
            for r in self.records:
                f.write(str(r.to_dict()) + "\n")

    def load_txt(self):
        try:
            with open("data/health_data.txt", "r", encoding="utf-8") as f:
                return [ast.literal_eval(line) for line in f]
        except (OSError, ValueError, SyntaxError):
            return []

    # 6. PICKLE 저장 및 읽기
    def save_pickle(self):
        data = [r.to_dict() for r in self.records]
        with open("data/health_data.pkl", "wb") as f:
            pickle.dump(data, f)

    def load_pickle(self):
        try:
            with open("data/health_data.pkl", "rb") as f:
                return pickle.load(f)
        except (OSError, pickle.UnpicklingError, EOFError):
            return []


# 7. 프로그램 실행
if __name__ == "__main__":

    os.makedirs("data", exist_ok=True)

    manager = HealthManager()

    # 테스트 데이터 입력
    manager.add_record("홍길동", 2000, "남", 175, 70)
    manager.add_record("김영희", 2001, "여", 162, 52)

    print("===== 건강정보 목록 =====")
    manager.show_records()

    # 4가지 파일 저장
    manager.save_json()
    manager.save_csv()
    manager.save_txt()
    manager.save_pickle()

    print("\n===== 파일 읽기 및 비교 =====")

    original = [r.to_dict() for r in manager.records]

    print("JSON:", manager.load_json() == original)
    print("CSV:", len(manager.load_csv()) == len(original))
    print("TXT:", manager.load_txt() == original)
    print("PICKLE:", manager.load_pickle() == original)

    print("\n모듈 1 실행 완료!")
