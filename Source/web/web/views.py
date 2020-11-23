import pyodbc as pyodbc
from django.shortcuts import render
import pandas as pd

from web.contrains.base_url import base_url_model, conn
from web.model.ThongKeChung import ThongKeChung
from web.model.ThongKeDauTu import ThongKeDauTu
from web.view.indext import getYearFromTo, getThongDauTu
from web.view.phantich import DuDoanDauTuVND, DuDoanDauTuUSD, DuDoanDauTu_SX, DuDoanDauTu_DT_UT, DuDoanDauTu_DV, \
    DuDoanDauTu_PTHT, DuDoanDauTu_DT, DuDoanDauTu_KHAC
from web.view.thongke import thongketylechiRD, thongKeTyLeLoaiHinhDauTu, thongKeVonDauTuVND, thongKeVonDauTuSX, \
    thongKeVonDauTuPTHT, thongKeVonDauTuDV, thongKeVonDauTuKHAC, thongKeVonDauTuDT_UT
import pickle
from django.http import HttpResponseRedirect
import pandas as pd

from fbprophet import Prophet

import pystan

import matplotlib.pyplot as plt
import base64
import io
import urllib
import json

# url(r'^createPost', CreatePost.as_view())

# from testapp.models import User
# from django.shortcuts import render
from django.http import HttpResponse


# def index(request):
#     template = 'index.html'
#     return render(request, template)
#
#
# def create_user(request):
#     if request.method == "POST":
#         fname = request.POST['fname']
#         lname = request.POST['lname']


def index(request):
    # thong ke chung
    thongkeChung = pd.read_sql_query('EXEC [dbo].[SP_DASHBOARD_THONGKECHUNG]', conn)
    thongKeChungResult = [
        (ThongKeChung(row.SO_DU_AN_DT, row.DOANH_NGHIEP_HOAT_DONG, row.SO_DA_RD, row.LAO_DONG_CHAT_LUONG_CAO)) for
        index, row in thongkeChung.iterrows()]
    response = [vars(ob) for ob in thongKeChungResult]

    # thong ke vong dau tu
    from_to = getYearFromTo()

    val1 = request.POST.get("fname");
    val2 = request.POST.get("lname")

    if val1 is None or val1 == "":
        val1 = "2003"
    if val2 is None or val2 == "":
        val2 = "2020"

    val3 = str(val1)
    val4 = str(val2)

    print(val3)
    print(val4)

    return render(request, 'indext.html', {"thongkechung": response[0],
                                           "thongkeDauTu": getThongDauTu(val3, val4)[0],
                                           "year_from_to": from_to})


def report(request):
    return render(request, 'report.html')


def thongke(request):
    # thong ke chung
    thongkeChung = pd.read_sql_query('EXEC [dbo].[SP_DASHBOARD_THONGKECHUNG]', conn)
    thongKeChungResult = [
        (ThongKeChung(row.SO_DU_AN_DT, row.DOANH_NGHIEP_HOAT_DONG, row.SO_DA_RD, row.LAO_DONG_CHAT_LUONG_CAO)) for
        index, row in thongkeChung.iterrows()]
    response = [vars(ob) for ob in thongKeChungResult]

    # Cai nay dung roi
    val1 = request.GET.get("a")
    val2 = request.GET.get("b")

    if val1 is None:
        val1 = "2010"
    if val2 is None:
        val2 = "2020"

    try:

        a = thongKeTyLeLoaiHinhDauTu()

        return render(request, 'thongke.html', {"thongkechung": response[0],
                                                "tylechiRd": thongketylechiRD(),
                                                "tyleloaihinhdautu": a})

    except Exception as e:
        print("Hieu tesst nef")
        print(e)
        pass
    # Khi mà viết một trang muốn sử dụng nhiều request thì nên dùng class-based view
    # Trong đố sẽ như sau
    return render(request, 'thongke.html')


def phantich(request):
    # m = pickle.load(open(base_url_model + '/VonDauTuVND.pickle', 'rb'))
    # future = m.make_future_dataframe(periods=12, freq='M')  # so ngay can du bao
    # future.tail()
    # forecast = m.predict(future)
    # forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
    # fig1 = m.plot(forecast, xlabel='Năm', ylabel='Vốn đầu tư')
    # ax = fig1.gca()
    # ax.set_title("Biểu đồ thể nguồn vốn đầu tư và dự đoán đầu tư", size=28)
    # # fig1.show()
    #
    # buf = io.BytesIO()
    # fig1.savefig(buf, format='png')
    # buf.seek(0)
    # string = base64.b64encode(buf.read())
    # uri = 'data:image/png;base64,' + urllib.parse.quote(string)
    #

    # duDoanDauTuUSD_uri = DuDoanDauTuUSD()
    # DuDoanDauTu_SX_uri = DuDoanDauTu_SX()
    # duDoanDauTu_DT_UT_uri = DuDoanDauTu_DT_UT()

    # buf2 = io.BytesIO()
    # fig2 = m.plot_components(forecast)
    # fig2.savefig(buf2, format='png')
    # buf2.seek(0)
    # string2 = base64.b64encode(buf2.read())
    # uri2 = 'data:image/png;base64,' + urllib.parse.quote(string2)
    #
    # labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
    # sizes = [15, 30, 45, 10]
    # explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
    #
    # fig1, ax1 = plt.subplots()
    # ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
    #         shadow=True, startangle=90)
    # ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    #
    # tyleloaihinhdautu = thongKeTyLeLoaiHinhDauTu(conn)

    #
    # # test

    # test

    query = 'Exec SP_THONGKE_TY_LE_DAU_TU'

    data = pd.read_sql_query(query, conn)

    lable = [desc.strip() for desc in data['HINH_THUC_DAU_TU']]
    value = [desc for desc in data['SO_LUONG']]

    args = {
        # 'image_dau_tu_VND': DuDoanDauTuVND(),
        # # Cần làm
        # 'thong_ke_dau_tu_VND': thongKeVonDauTuVND(),
        # 'image_dau_tu_USD': DuDoanDauTuUSD(),
        # 'image_dau_tu_SX': DuDoanDauTu_SX(),
        # 'image_dau_tu_DT_UT': DuDoanDauTu_DT_UT(),
        # 'image_dau_tu_DV': DuDoanDauTu_DV(),
        # 'image_dau_tu_PTHT': DuDoanDauTu_PTHT(),

        # 'image_dau_tu_DT': DuDoanDauTu_DT(),
        # 'image_dau_tu_VDT': DuDoanDauTu_VDT(),
        # 'image_dau_tu_KHAC': DuDoanDauTu_SX_uri,

        "lable": lable,
        "value": value}
    return render(request, 'phantich.html', args)


# class ThongKe(View):
#     def get(self, request, *args, **kwargs):
#         # Trong ddaay trar ve template
#         pass
#     def post(self, request, *ergs, **kwargs):
#         # Nhaajn ket qua tu request den cung trang
#         pass


def testData(request):
    thongkeChung = pd.read_sql_query('EXEC[dbo].[SP_DASHBOARD_THONGKECHUNG]', conn)
    thongKeChungResult = [
        (ThongKeChung(row.SO_DU_AN_DT, row.DOANH_NGHIEP_HOAT_DONG, row.SO_DA_RD, row.LAO_DONG_CHAT_LUONG_CAO)) for
        index, row in thongkeChung.iterrows()]
    response = [vars(ob) for ob in thongKeChungResult]
    return render(request, "testdata.html", {'thongkechung': response[0]})


# new 19/11/2020

def vonVND(request):
    return render(request, "phantich_von_dt_vnd.html", {'thongke': thongKeVonDauTuVND(),
                                                        'phantich': DuDoanDauTuVND()})


# 5 cai

def vonSX(request):
    return render(request, "phantich_von_dt_SX.html", {'thongke': thongKeVonDauTuSX(),
                                                       'phantich': DuDoanDauTu_SX()})


def vonPTHT(request):
    return render(request, "phantich_von_dt_PTHT.html", {'thongke': thongKeVonDauTuPTHT(),
                                                         'phantich': DuDoanDauTu_PTHT()})


def vonDV(request):
    return render(request, "phantich_von_dt_DV.html", {'thongke': thongKeVonDauTuDV(),
                                                       'phantich': DuDoanDauTu_DV()})


def vonKhac(request):
    return render(request, "phantich_von_dt_Khac.html", {'thongke': thongKeVonDauTuKHAC(),
                                                         'phantich': DuDoanDauTu_KHAC()})


def vonDT_UT(request):
    return render(request, "phantich_von_dt_DT_UT.html", {'thongke': thongKeVonDauTuDT_UT(),
                                                          'phantich': DuDoanDauTu_DT_UT()})


# thong_ke_
def thongKe_kinh_phi(request):
    return render(request, "thongke_kinh_phi.html", {"thongke": thongketylechiRD()})


def thongke_tile_ld_clc_tham_gia_rd(request):
    return render(request, "thongke_lao_dong_clc_tham_gia_rd.html", {"thongke": thongketylechiRD()})


def thongke_doanh_nghiep_hoat_dong(request):
    query = ' SELECT TEN_DU_AN_TIENG_VIET, TEN_DU_AN_VIET_TAT,MUC_TIEU_HOAT_DONG,VON_DAU_TU_VND FROM dbo.GIAY_CNDT';
    data = pd.read_sql_query(query, conn)

    dataResult = [
        (DoanhNghiepHoatDong(row.TEN_DU_AN_TIENG_VIET, row.TEN_DU_AN_VIET_TAT, row.MUC_TIEU_HOAT_DONG,
                             row.VON_DAU_TU_VND)) for
        index, row in data.iterrows()]
    response = [vars(ob) for ob in dataResult]

    return render(request, "thong_ke_doanh_nghiep_hoat_dong.html", {"thongke": response})


class DoanhNghiepHoatDong:
    def __init__(self, TEN_DU_AN_TIENG_VIET, TEN_DU_AN_VIET_TAT, MUC_TIEU_HOAT_DONG, VON_DAU_TU_VND):
        self.TEN_DU_AN_TIENG_VIET = TEN_DU_AN_TIENG_VIET
        self.TEN_DU_AN_VIET_TAT = TEN_DU_AN_VIET_TAT
        self.MUC_TIEU_HOAT_DONG = MUC_TIEU_HOAT_DONG
        self.VON_DAU_TU_VND = VON_DAU_TU_VND



def thong_ke_du_an_dau_tu(request):
    query = ' SELECT TEN_DU_AN_TIENG_VIET, TEN_DU_AN_VIET_TAT,MUC_TIEU_HOAT_DONG,VON_DAU_TU_VND FROM dbo.GIAY_CNDT';
    data = pd.read_sql_query(query, conn)

    dataResult = [
        (DoanhNghiepHoatDong(row.TEN_DU_AN_TIENG_VIET, row.TEN_DU_AN_VIET_TAT, row.MUC_TIEU_HOAT_DONG,
                             row.VON_DAU_TU_VND)) for
        index, row in data.iterrows()]
    response = [vars(ob) for ob in dataResult]

    return render(request, "thong_ke_du_an_dau_tu.html", {"thongke": response})


def thong_ke_doanh_nghiep_hoat_dong():
    return None