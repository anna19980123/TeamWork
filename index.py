import file_manager
import sys
import model
import time

def start():
    while True:
        content = "----------------------\n歡迎來到成績管理系統\n1.管理員登入\n2.學生登入\n3.教授登入\n4.退出\n----------------------\n請選擇1-4\n"
        operator = input(content)
        if operator == "1":
            username = input("請輸入帳號:\n")
            password = input("請輸入密碼:\n")
            data = file_manager.read_json("manager.json", {})
            if username in data:
                if password == data[username]:
                    while True:
                        print("---------------")
                        op = input("1.新增學生\n2.新增教授\n3.新增課程\n4.退出\n")

                        if op == "1":
                            student_data = file_manager.read_json(
                                "student.json", {})
                            student_dataC = student_data.get("all_students")
                            student_size = student_data.get("nums")
                            std_num = "std" + str(int(student_size) + 1)
                            username = input("請輸入帳號:")
                            password = input("請輸入密碼:")
                            enter_year = input("請輸入入學年份(2020):")
                            gender = input("請輸入性別(male/female):")
                            birth = input("請輸入生日(1970/12/25):")

                            s = model.Student(
                                std_num, username, password, enter_year, gender, birth)
                            student_dataC.append(s.__dict__)
                            student_data['all_students'] = student_dataC
                            student_data['nums'] = student_size + 1
                            file_manager.write_json(
                                'student.json', student_data)
                            print("添加成功")
                            op = input("繼續請輸入1,退出請輸入2\n")
                            if op == "2":
                                break
                        elif op == "2":
                            professor_data = file_manager.read_json(
                                "professor.json", {})

                            professor_dataC = professor_data.get(
                                "all_professor")
                            
                            professor_size = professor_data.get("nums")
                            pid = "pid" + str(int(professor_size) + 1)
                            username = input("請輸入帳號:")
                            password = input("請輸入密碼:")
                            gender = input("請輸入性別(male/female):")
                            birth = input("請輸入生日(1970/12/25):")
                            p = model.Professor(
                                pid, username, password, gender, birth)
                            professor_dataC.append(p.__dict__)
                            professor_data = {
                                "all_professor": professor_dataC,
                                "nums": professor_size + 1
                            }
                            file_manager.write_json(
                                "professor.json", professor_data)
                            print("新增成功\n")
                        elif op == "3":
                            classData = file_manager.read_json(
                                "classname.json", {})
                            num = input("請輸入課程代號:")
                            classname = input("請輸入課程名稱:")
                            points = input("請輸入學分數:")
                            professor = input("請輸入授課教授:")
                            tp = input("請輸入必選修:")
                            c = model.Class(
                                num, classname, points, professor, tp)
                            classData["all_classname"].append(c.__dict__)
                            file_manager.write_json(
                                "classname.json", classData)
                            print("新增成功\n")
                        elif op=="4":
                            break
                        else:
                            print("輸入錯誤")
                            break
                    
                    

                else:
                    print('管理員帳號密碼錯誤,一秒後跳轉\n')
                    time.sleep(1)
                    start()
                    break
        elif operator == "2":
            username = input("請輸入帳號:\n")
            password = input("請輸入密碼:\n")
            data = file_manager.read_json("student.json", {})
            
            for ii in data['all_students']:
                if ii['username'] == username and password == ii['password']:
                    user = ii
                else:
                    print('學生不存在,一秒後跳轉\n')
                    time.sleep(1)
                    start()
            while True:
                print(f"歡迎回來,學生{ii['username']}")
                op = input("-----------\n1.選課\n2.學生資訊\n3.退出\n")
                if op == "1":
                    classData = file_manager.read_json('classname.json', {})
                    classData = classData['all_classname']
                    for i in classData:
                        print(
                            f"課程號碼: {i['num']}, 課程名稱: {i['classname']}, 學分數: {i['points']}, 教授: {i['professor']},類型:{i['tp']}")
                    op = input("請輸入課程號碼:\n")
                    for i in classData:
                        if i['num'] == op:
                            chooseClass = i
                            print(chooseClass['classname'])
                    c = model.Class(chooseClass['num'],chooseClass['classname'],chooseClass['points'],chooseClass['professor'],chooseClass['tp'])
                    for i,j in enumerate(data['all_students']):
                        if j['username'] == user['username']:
                            data['all_students'][i]['classname'].append(c.__dict__)
                    file_manager.write_json('student.json',data)
                    print("新增成功")
                elif op=="2":
                    testclass= []
                    for k in user['classname']:
                        testclass.append(k['classname'])
                    print(f"姓名:{user['username']},入學年:{user['enter_year']},性別:{user['gender']},生日:{user['birth']},修課:{testclass}")
                else:
                    break
        elif operator == "3":
            username = input("請輸入帳號:\n")
            password = input("請輸入密碼:\n")
            data = file_manager.read_json("professor.json", {})
            for ii in data['all_professor']:
                if ii['username'] == username and password == ii['password']:
                    user = ii
                else:
                    print('教授不存在,一秒後跳轉\n')
                    time.sleep(1)
                    start()
            while True:
                print(f"歡迎回來,教授{user['username']}")
                op = input("-----------\n1.查看修課學生\n2.退出\n")
                if op == "1":
                    std = []
                    checkdata = file_manager.read_json("student.json", {})
                    for i in checkdata['all_students']:
                        for j in i['classname']:
                            if j['professor'] == user['username']:
                                std.append(i['username'])
                    for i in range(len(std)):
                        print(f'學生:{std[i]}')
                    
                elif op == "2":
                    break
        elif operator == "4":
            sys.exit(0)
        else:
            print("輸入錯誤!")


if __name__ == "__main__":
    start()
