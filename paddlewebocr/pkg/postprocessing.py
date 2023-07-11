import re
import json
import string


class IdCardFront:
    """
    模拟阿里云身份证OCR返回结果，待改进。
    """

    def __init__(self, result):
        self.result = [
            i.replace(" ", "").translate(str.maketrans("", "", string.punctuation))
            for i in result
        ]
        self.out = {"Data": {"FrontResult": {}}}
        self.res = self.out["Data"]["FrontResult"]
        self.res["Name"] = ""
        self.res["IDNumber"] = ""
        self.res["Address"] = ""
        self.res["Gender"] = ""
        self.res["Nationality"] = ""

    def birth_no(self):
        """
        身份证号码
        """
        for i in range(len(self.result)):
            txt = self.result[i]

            # 身份证号码
            if "X" in txt or "x" in txt:
                res = re.findall("\d*[X|x]", txt)
            else:
                res = re.findall("\d{16,18}", txt)

            if len(res) > 0:
                if len(res[0]) == 18:
                    self.res["IDNumber"] = res[0].replace("号码", "")
                    self.res["Gender"] = "男" if int(res[0][16]) % 2 else "女"
                break

    def full_name(self):
        """
        身份证姓名
        """
        for i in range(len(self.result)):
            txt = self.result[i]
            if ("姓名" or "名" in txt) and len(txt) > 2:
                res = re.findall("名[\u4e00-\u9fa5]{1,4}", txt)
                if len(res) > 0:
                    self.res["Name"] = res[0].split("名")[-1]
                    self.result[i] = "temp"  # 避免身份证姓名对地址造成干扰
                    break

    def sex(self):
        """
        性别女民族汉
        """
        for i in range(len(self.result)):
            txt = self.result[i]
            if "男" in txt:
                self.res["Gender"] = "男"

            elif "女" in txt:
                self.res["Gender"] = "女"

    def national(self):
        # 性别女民族汉
        for i in range(len(self.result)):
            txt = self.result[i]
            res = re.findall(".*民族[\u4e00-\u9fa5]+", txt)

            if len(res) > 0:
                self.res["Nationality"] = res[0].split("族")[-1]
                break

    def address(self):
        """
        身份证地址
        """
        addString = []
        for i in range(len(self.result)):
            txt = self.result[i]
            txt = txt.replace("号码", "")
            if "公民" in txt:
                txt = "temp"
            # 身份证地址

            if (
                    "住址" in txt
                    or "址" in txt
                    or "省" in txt
                    or "市" in txt
                    or "县" in txt
                    or "街" in txt
                    or "乡" in txt
                    or "村" in txt
                    or "镇" in txt
                    or "区" in txt
                    or "城" in txt
                    or "组" in txt
                    or "号" in txt
            ):

                if "住址" in txt or "省" in txt or "址" in txt:
                    addString.insert(0, txt.split("址")[-1])
                else:
                    addString.append(txt)

                self.result[i] = "temp"

        if len(addString) > 0:
            self.res["Address"] = "".join(addString)
        else:
            self.res["Address"] = ""

    def predict_name(self):
        """
        如果PaddleOCR返回的不是姓名xx连着的，则需要去猜测这个姓名，此处需要改进
        """
        for i in range(len(self.result)):
            txt = self.result[i]
            if self.res["Name"] == "":
                if len(txt) > 1 and len(txt) < 5:
                    if (
                            "性别" not in txt
                            and "姓名" not in txt
                            and "民族" not in txt
                            and "住址" not in txt
                            and "出生" not in txt
                            and "号码" not in txt
                            and "身份" not in txt
                    ):
                        result = re.findall("[\u4e00-\u9fa5]{2,4}", txt)
                        if len(result) > 0:
                            self.res["Name"] = result[0]
                            break

    def run(self):
        self.full_name()
        self.national()
        self.birth_no()
        self.address()
        self.predict_name()
        return json.dumps(self.out)


class IdCardBack:
    """
    模拟阿里云身份证OCR返回结果，待改进。
    """

    def __init__(self, result):
        self.result = [
            i.replace(" ", "").translate(str.maketrans("", "", string.punctuation))
            for i in result
        ]
        self.out = {"Data": {"BackResult": {}}}
        self.res = self.out["Data"]["BackResult"]
        self.res["Authority"] = ""
        self.res["ValidDate"] = ""

    def authority(self):
        """
        身份证签发机关
        """
        for i in range(len(self.result)):
            txt = self.result[i]
            if "公安局" in txt:
                self.res["Authority"] = txt.split("机关")[-1]
                self.result[i] = "temp"
                break

    def valid_date(self):
        """
        身份证有效期
        :return:
        """
        # 用正则表达式匹配有效期 如：2015082120250821
        for i in range(len(self.result)):
            txt = self.result[i].split("限")[-1]
            print(txt)
            res = re.findall("\d{16}", txt)
            if len(res) > 0:
                self.res["ValidDate"] = res[0]

    def run(self):
        self.authority()
        self.valid_date()
        return json.dumps(self.out)


class BusinessLicense:
    """
    营业执照OCR返回结果
    """

    def __init__(self, result):
        self.result = [
            i.replace(" ", "").translate(str.maketrans("", "", string.punctuation))
            for i in result
        ]
        self.raw = result
        self.out = {"Data": {"BusinessLicenseResult": {}}}
        self.res = self.out["Data"]["BusinessLicenseResult"]
        self.res["CreditCode"] = ""
        self.res["FundDate"] = ""
        self.res["BusinessTerm"] = ""
        self.res["BusinessName"] = ""
        self.res["BusinessType"] = ""
        self.res["RegisteredCapital"] = ""
        self.res["Address"] = ""
        self.res["Name"] = ""
        self.res["BusinessScope"] = ""

    def test(self):
        for i in range(len(self.result)):
            txt = self.result[i]
            print(txt)

    def credit_code(self):  # 统一社会信用代码
        for i in range(len(self.result)):
            txt = self.result[i]
            # 可以同时匹配新旧统一社会信用代码的regex /^([0-9A-HJ-NPQRTUWXY]{2}\d{6}[0-9A-HJ-NPQRTUWXY]{10}|[1-9]\d{14})$/
            res = re.findall("^([0-9A-HJ-NPQRTUWXY]{2}\d{6}[0-9A-HJ-NPQRTUWXY]{10}|[1-9]\d{14})$", txt)
            if len(res) > 0:
                self.res["CreditCode"] = res[0]
                self.result[i] = "temp"
                break

    def fund_date(self):  # 营业执照成立日期
        for i in range(len(self.result)):
            txt = self.result[i]
            if (
                    "年" in txt
                    and "月" in txt
                    and "日" in txt
                    and "至" not in txt
            ):
                self.res["FundDate"] = txt.split("期")[-1]
                self.result[i] = "temp"
                break

    def business_term(self):  # 营业执照营业期限
        for i in range(len(self.result)):
            txt = self.result[i]
            if (
                    "年" in txt
                    and "月" in txt
                    and "日" in txt
                    and "至" in txt
            ):
                self.res["BusinessTerm"] = txt.split("限")[-1]
                self.result[i] = "temp"
                break

    def business_name(self):
        """
        企业名称
        """
        for i in range(len(self.result)):
            txt = self.result[i]
            if ("名称" in txt or "称" in txt or "公司" in txt) and len(txt) > 2:
                self.res["BusinessName"] = txt.split("称")[-1]
                self.result[i] = "temp"  # 避免公司名称对地址造成干扰
                break

    def business_type(self):
        """
        企业类型名称
        """
        for i in range(len(self.result)):
            txt = self.result[i]
            if ("类型" in txt or "型" in txt or "公司" in txt) and len(txt) > 2:
                self.res["BusinessType"] = txt.split("型")[-1]
                self.result[i] = "temp"  # 避免公司名称对地址造成干扰
                break

    def registered_capital(self):
        for i in range(len(self.result)):
            txt = self.result[i]
            if ("资本" in txt or "本" in txt or "万" in txt) and len(txt) > 6:
                self.res["RegisteredCapital"] = self.raw[i].split("本")[-1]
                self.result[i] = "temp"

    def address(self):
        """
        住所
        """
        addString = []
        for i in range(len(self.result)):
            txt = self.result[i]
            if (
                    len(re.findall(
                        "(\w+省|\w+自治区)?(\w+市|\w+自治州|\w+地区)?(\w+区|\w+县|\w+市|\w+镇|\w+乡|\w+街道)?(\w+路|\w+街|\w+巷|\w+村)?(\d+号|(\w+号)(\d+单元)?(\d+室)?)",
                        txt)) > 0
            ):

                if "住所" in txt or "省" in txt or "所" in txt:
                    addString.insert(0, txt.split("所")[-1])
                elif "编" not in txt:
                    addString.append(txt)

                self.result[i] = "temp"

        if len(addString) > 0:
            self.res["Address"] = "".join(addString)
        else:
            self.res["Address"] = ""

    def full_name(self):
        """
        法人/负责人姓名
        """
        for i in range(len(self.result)):
            txt = self.result[i]
            if (
                    "表人" in txt or "法定" in txt or "负责" in txt or "代表" in txt or "责人" in txt or "人" in txt) and len(
                    txt) > 2:
                res = re.findall("人[\u4e00-\u9fa5]{1,8}", txt)
                if len(res) > 0:
                    self.res["Name"] = res[0].split("人")[-1]
                    self.result[i] = "temp"  # 避免姓名对地址造成干扰
                    break
                else:
                    txt = self.result[i + 1]
                    if len(txt) > 1:
                        self.res["Name"] = txt
                        self.result[i + 1] = "temp"
                        break

    def business_scope(self):
        """
        经营范围
        """
        addString = []
        for i in range(len(self.result)):
            if i < 10 or i > len(self.result) - 5:
                continue
            txt = self.result[i]
            if len(re.findall("[\u3000-\u301E\uFE10-\uFE19\uFE30-\uFE44\uFE50-\uFE6B\uFF01-\uFF5E\u3007\u3010-\u3011\u3014-\u3015\uFF08-\uFF09]", txt)) > 0:
                addString.append(txt)
                self.result[i] = "temp"
        if len(addString) > 0:
            self.res["BusinessScope"] = "".join(addString)
        else:
            self.res["BusinessScope"] = ""

    def run(self):
        self.credit_code()
        self.fund_date()
        self.business_term()
        self.business_name()
        self.business_type()
        self.registered_capital()
        self.address()
        self.full_name()
        self.business_scope()
        self.test()
        return json.dumps(self.out)
