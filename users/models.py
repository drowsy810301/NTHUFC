#-*- encoding=UTF-8 -*-
from django.db import models
from django.conf import settings

# Create your models here.
'''
class UserProfile(models.Model):
    user = models.OneToOneField(User)

    #activation_key = models.CharField(max_length=40, blank=True)
    # default active time is 15 minutes
    #active_time = models.DateTimeField(default=lambda: datetime.now() + timedelta(minutes=15))

    current_student = models.BooleanField(default=True)

    def __unicode__(self):
        return self.user.username
'''

class Account(models.Model):
    username = models.CharField(max_length=20, default='')
    FB_ID = models.CharField(max_length=40, primary_key=True)

    #year_in_school choice
    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'
    FIRST_YEAR_OF_MASTER = 'FM'
    SECON_YEAR_OF_MASTER = 'SM'
    YEAR_IN_SCHOOL_CHOICES = (
        (FRESHMAN, '大一'),
        (SOPHOMORE, '大二'),
        (JUNIOR, '大三'),
        (SENIOR, '大四'),
        (FIRST_YEAR_OF_MASTER, '碩一'),
        (SECON_YEAR_OF_MASTER, '碩二')
    )
    #major choice
    ANTH = 'ANTH'
    ASTR = 'ASTR'
    BME = 'BME'
    BMES = 'BMES'
    CHE = 'CHE'
    CHEM = 'CHEM'
    CL = 'CL'
    COM = 'COM'
    CS = 'CS'
    DMS = 'DMS'
    ECON = 'ECON'
    EE = 'EE'
    EECS = 'EECS'
    EMBA = 'EMBA'
    ENE = 'ENE'
    ESS = 'ESS'
    EST = 'EST'
    FL = 'FL'
    GOM = 'GOM'
    GTPS = 'GTPS'
    HIS = 'HIS'
    HSS = 'HSS'
    IACS = 'IACS'
    IEEM = 'IEEM'
    IEM = 'IEM'
    ILS = 'ILS'
    IMBA = 'IMBA'
    IPE = 'IPE'
    IPHD = 'IPHD'
    IPNS = 'IPNS'
    IPT = 'IPT'
    ISA = 'ISA'
    ISS = 'ISS'
    LING = 'LING'
    LS = 'LS'
    LSBS = 'LSBS'
    LSBT = 'LSBT'
    LSIN = 'LSIN'
    LSIP = 'LSIP'
    LSMC = 'LSMC'
    LSMM = 'LSMM'
    LSSN = 'LSSN'
    LST = 'LST'
    MATH = 'MATH'
    MBA = 'MBA'
    MS = 'MS'
    NEEP = 'NEEP'
    NEMS = 'NEMS'
    NES = 'NES'
    PHIL = 'PHIL'
    PHYS = 'PHYS'
    PME = 'PME'
    QF = 'QF'
    RDDM = 'RDDM'
    SCI = 'SCI'
    SLS = 'SLS'
    SNHC = 'SNHC'
    SOC = 'SOC'
    ST = 'ST'
    STAT = 'STAT'
    TL = 'TL'
    TM = 'TM'
    UPMT = 'UPMT'
    UPPP = 'UPPP'

    MAJOR_CHOICES = (
        (ANTH, 'ANTH 人類所'),
        (ASTR, 'ASTR 天文所'),
        (BME, 'BME 醫工所'),
        (BMES, 'BMES 醫環系'),
        (CHE, 'CHE 化工系'),
        (CHEM, 'CHEM 化學系'),
        (CL, 'CL 中文系'),
        (COM, 'COM 通訊所'),
        (CS, 'CS 資工系'),
        (DMS, 'DMS 醫科系'),
        (ECON, 'ECON 經濟系'),
        (EE, 'EE 電機系'),
        (EECS, 'EECS 電資院學士班'),
        (EMBA, 'EMBA EMBA專班'),
        (ENE, 'ENE 電子所'),
        (ESS, 'ESS 工科系'),
        (EST, 'EST 環境博士學程'),
        (FL, 'FL 外語系'),
        (GOM, 'GOM 全球營運管理碩士學程'),
        (GTPS, 'GTPS 台研教'),
        (HIS, 'HIS 歷史所'),
        (HSS, 'HSS 人社院學士班'),
        (IACS, 'IACS 亞際文化碩士學程'),
        (IEEM, 'IEEM 工工系'),
        (IEM, 'IEM 工工在職班'),
        (ILS, 'ILS 學科所'),
        (IMBA, 'IMBA IMBA碩士班'),
        (IPE, 'IPE 工學院學士班'),
        (IPHD, 'IPHD 跨院國際博士'),
        (IPNS, 'IPNS 原科院學士班'),
        (IPT, 'IPT 光電所'),
        (ISA, 'ISA 資應所 '),
        (ISS, 'ISS 服科所'),
        (LING, 'LING 語言所'),
        (LS, 'LS 生科系'),
        (LSBS, 'LSBS 生資所'),
        (LSBT, 'LSBT 生技所'),
        (LSIN, 'LSIN 神經科學博士學程'),
        (LSIP, 'LSIP 生科院學士班'),
        (LSMC, 'LSMC 分生所'),
        (LSMM, 'LSMM 分醫所'),
        (LSSN, 'LSSN 系神所'),
        (LST, 'LST 科法所'),
        (MATH, 'MATH 數學系'),
        (MBA, 'MBA MBA專班'),
        (MS, 'MS 材料系'),
        (NEEP, 'NEEP 核物系'),
        (NEMS, 'NEMS 奈微所'),
        (NES, 'NES 核工所'),
        (PHIL, 'PHIL 哲學所'),
        (PHYS, 'PHYS 物理系'),
        (PME, 'PME 動機系'),
        (QF, 'QF 計財系'),
        (RDDM, 'RDDM 半導體專班'),
        (SCI, 'SCI 理學院學士班'),
        (SLS, 'SLS 先進光源學位學程'),
        (SNHC, 'SNHC 社群人智國際學程'),
        (SOC, 'SOC 社會所'),
        (ST, 'ST 不分系招生'),
        (STAT, 'STAT 統計所'),
        (TL, 'TL 台文所'),
        (TM, 'TM 科管所'),
        (UPMT, 'UPMT 科管院學士班'),
        (UPPP, 'UPPP 光電博士學程'),
    )
    major = models.CharField(max_length=6, choices=MAJOR_CHOICES, default=None)
    year_in_school = models.CharField(max_length=2, choices=YEAR_IN_SCHOOL_CHOICES, default=None)
    remarks = models.TextField(default=None, blank=True, null=True)

    def __unicode__(self):
        return self.username

